{
    'name': 'Ahmed Custom Module',
    'author' : "Ahmed Rashed",
    'website':"https://portfolio-eight-green-95.vercel.app/",
    'summary': "This is My First Odoo Custom Module",
    'version': '1.0',
    # 'depends': ['base','report_xlsx'],
      'depends': ['base'],
    'license': 'LGPL-3',
    'data' :[
    'security/ir.model.access.csv',
        'views/menu.xml',
        'views/employees.xml',
        'views/applicants.xml',
        'views/department.xml',
        'views/jobs.xml',
'reports/employee_report_template.xml'
    ],

    'installable': True,
}
