{
    'name': 'Real Estate',
    'version': '1.0',
    'category': 'Website',
    'summary': 'Manage real estate properties and website',
    'description': 'Custom real estate module with property listings and search on website',
    'author': 'Udaykiran',
    'depends': ['website'],
    'data': [
        'security/ir.model.access.csv',
        'views/property_views.xml',
        'views/website_property_templates.xml',
        'views/website_templates.xml',
    ],
    'installable': True,
    'application': True,
}
