{
    "name": "Rental Estate",
    "version": "1.0",
    "category": "Real Estate",
    "summary": "Rental estate listings",
    "depends": ["product", "website"],
    "data": [
        'security/ir.model.access.csv',
        "views/product_template_views.xml",
        'views/qweb_templates/property_listing_templates.xml',

    ],
    "installable": True,
    "application": True,
}
