from ast import literal_eval
from odoo import http
from odoo.http import request
import os
import fasttext
import tempfile
import base64
import pandas as pd
import re
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from docx import Document
import fitz  # PyMuPDF

# Helper functions
def extract_text(file_path):
    text = ""
    if True:  # Using only the original text extraction logic
        doc = fitz.open(file_path)
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            text += page.get_text("text")
    elif file_path.lower().endswith('.docx'):
        document = Document(file_path)
        for paragraph in document.paragraphs:
            text += paragraph.text + '\n'
    return text

def preprocess_text(text):
    lemmatizer = WordNetLemmatizer()
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text, flags=re.UNICODE)
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word.isalpha()]
    return " ".join(tokens)

def predict_top_5_job_titles(cv_file_path, model, job_titles_mapping):
    # Extract and preprocess text from the CV
    cv_text = extract_text(cv_file_path)
    cv_text = re.sub(r'\s+', ' ', cv_text.strip())  # Remove newlines and extra spaces
  

    # Get the top 5 predictions (most similar job titles)
    predictions = model.predict(cv_text, k=1000)  # k=5 to get top 5 predictions


    # Get job titles and probabilities
    top_5_predictions = []
    for label, prob in zip(predictions[0], predictions[1]):
        # Remove the '__label__' prefix to get the job title key
        job_title_key = label.replace("__label__", "")
        # Get the full job title from the mapping, replacing underscores with spaces
        full_job_title = job_titles_mapping.get(job_title_key, job_title_key).replace("_", " ")
        probability = prob * 100  # Convert to percentage
        top_5_predictions.append((full_job_title, probability))

    return top_5_predictions

class Evaluation(http.Controller):
    @http.route('/candidates/evaluate/<string:candidates_ids>', type='http', auth='user')
    def download_employees_excel_report(self, candidates_ids):
        candidates_ids = request.env['hr.candidate'].browse(literal_eval(candidates_ids))

        # Get the path to the CSV file in the static folder of your module
        module_path = os.path.dirname(os.path.abspath(__file__))  # Path to the current file
        job_csv_path = os.path.join(module_path, '..', 'data', 'job_title_des.csv')  # Adjust relative path
        
        try:
            job_data = pd.read_csv(job_csv_path, encoding='utf-8')
        except UnicodeDecodeError:
            job_data = pd.read_csv(job_csv_path, encoding='latin1')

        # Create job titles mapping
        job_titles_mapping = {
            re.sub(r'[^a-zA-Z0-9\s]', '', title).lower().replace(" ", "_"): title
            for title in job_data['Job Title']
        }


        job_titles = job_data['Job Title'].tolist()



        # Load the pre-trained FastText model
        model_path = os.path.join(module_path, '..', 'data', 'cvmatchingmodel.ftz')
        fasttext_model = fasttext.load_model(model_path)

        for candidate in candidates_ids:
            if candidate.cv:
                # Save the binary CV file to a temporary file
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    tmp_file.write(base64.b64decode(candidate.cv))  # Decode base64 binary data
                    tmp_file_path = tmp_file.name

                # Predict top 5 job titles
                top_5_predictions = predict_top_5_job_titles(tmp_file_path, fasttext_model, job_titles_mapping)
                

                if candidate.job_required_id.name not in job_titles:
                    candidate.cv_score = 0
                    candidate.cv_rank = "Invalid Job"



                    return request.redirect('/odoo/recruitment-candidates?&view_type=list')

                job_index = job_titles.index(candidate.job_required_id.name)

                for prediction in top_5_predictions:
                    if prediction[0] == job_titles[job_index]:
                        if prediction[1] >= 80:
                            candidate.cv_rank = "High"
                        elif prediction[1] >= 40:
                            candidate.cv_rank = "Medium"
                        else:
                            candidate.cv_rank = "Low"
                        
                        candidate.cv_score = prediction[1]



        return request.redirect('/odoo/recruitment-candidates?&view_type=list')