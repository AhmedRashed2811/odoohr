{
    'name':'Customized HR Module',
    'author' : 'Customized HR Module for Odootec by Ahmed Rashed',
    'category': 'Human Resources',
    'version': '18.0.0.1.0',
    'depends': ['base', 'hr_recruitment', 'mail'],
    'data':[
        'data/job_title_des.csv',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/employees_view.xml',
        'views/departments_view.xml',
        'views/jobs_view.xml',
        'views/recruitment_view.xml',
    ],

    'assets': {
    'web.assets_backend': [
        '/cutomized_hr_module/static/src/css/recruitment.css',
    ],
},
    'application': 'True'
}