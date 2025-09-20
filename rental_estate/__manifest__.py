{
    "name": "Rental Estate",
    "version": "1.0",
    "category": "Real Estate",
    'license': 'LGPL-3',
    "summary": "Rental estate listings",
    "depends": ["product", "website"],
    "data": [
        'security/ir.model.access.csv',
        "views/product_template_views.xml",
        'views/qweb_templates/property_listing_templates.xml',
        'views/qweb_templates/property_detail_templates.xml',
        'views/qweb_templates/sell_property_form_template.xml',
        'views/qweb_templates/sell_thank_you_template.xml'

    ],
    "installable": True,
    "application": True,
}
