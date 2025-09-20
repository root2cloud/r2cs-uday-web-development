from odoo import http
from odoo.http import request
import json
from odoo.tools.json import scriptsafe as json_scriptsafe


class RealEstateController(http.Controller):

    @http.route('/property-map', type='http', auth='public', website=True)
    def property_map(self, **kwargs):
        # Fetch published properties from database
        Property = request.env['property.property'].sudo()
        properties = Property.search([
            ('is_published', '=', True),
            ('latitude', '!=', False),
            ('longitude', '!=', False)
        ])

        # Build data for JavaScript
        property_data = []
        for prop in properties:
            if prop.latitude and prop.longitude:
                property_data.append({
                    'id': prop.id,
                    'name': prop.name or '',
                    'latitude': float(prop.latitude),
                    'longitude': float(prop.longitude),
                    'street': prop.street or '',
                    'price': float(prop.price) if prop.price else 0,
                    'contact_phone': prop.contact_phone or '',
                    'contact_email': prop.contact_email or '',
                })

        return request.render('real_estate_management.property_map_template', {
            'property_count': len(property_data),
            'properties_json': json_scriptsafe.dumps(property_data) if property_data else '[]',
        })
