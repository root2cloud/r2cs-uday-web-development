{
    'name': 'Real Estate Management',
    'version': '1.0',
    'category': 'Website',
    'summary': 'Module for managing real estate properties and website integration',
    'description': 'Manage real estate properties with interactive map, listings, and contact forms.',
    'depends': ['base', 'web', 'website', 'mail'],
    'data': [
        # Security
        'security/ir.model.access.csv',

        # Views
        'views/property_views.xml',
        'views/property_category_views.xml',
        'views/menu.xml',

        # Qweb Templates
        'views/qweb_templates/website_templates.xml',
        # 'views/qweb_templates/test_button_template.xml',
        # 'views/qweb_templates/test_button_component.xml'

    ],
    'assets': {
        'web.assets_frontend': [
            'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
            'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js',
            # 'real_estate_management/static/src/js/property_map.js',
        ],
    },
    'installable': True,
    'application': True,
}
