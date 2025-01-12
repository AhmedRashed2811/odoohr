from odoo import http
from odoo.http import request
import base64

class CandidateCVDownload(http.Controller):
    @http.route('/candidate/cv/download/<int:candidate_id>', type='http', auth='user')
    def download_candidate_cv(self, candidate_id):
        # Retrieve the candidate record
        candidate = request.env['hr.customized.candidates'].browse(candidate_id)
        if not candidate:
            return request.not_found()

        # Ensure the CV field has data
        if not candidate.cv:
            return request.make_response(
                "No CV found for this candidate.",
                headers=[('Content-Type', 'text/plain')]
            )

        # Decode the binary data and prepare the response
        cv_data = base64.b64decode(candidate.cv)
        file_name = f"{candidate.partner_name or 'Candidate'}_CV.pdf"

        return request.make_response(
            cv_data,
            headers=[
                ('Content-Type', 'application/pdf'),
                ('Content-Disposition', f'attachment; filename={file_name}')
            ]
        )
