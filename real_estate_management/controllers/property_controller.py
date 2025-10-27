from odoo import http, fields
from odoo.http import request
import json
from odoo.tools.json import scriptsafe as json_scriptsafe
import base64
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class RealEstateController(http.Controller):

    @http.route('/', type='http', auth='public', website=True)
    def property_map(self, **kwargs):

        # Fetch published properties from database
        Property = request.env['property.property'].sudo()
        # Get the selected city from URL parameters (if any)
        selected_city = kwargs.get('city', '')
        all_properties = Property.search([('is_published', '=', True)])
        city_list = sorted(list(set([p.city for p in all_properties if p.city])))
        # Build the search domain with city filter if selected
        search_domain = [
            ('is_published', '=', True),
            ('latitude', '!=', False),
            ('longitude', '!=', False)
        ]
        # Add city filter if a city is selected
        if selected_city:
            search_domain.append(('city', '=', selected_city))

        # Fetch properties based on the search domain
        properties = Property.search(search_domain)

        # Define a reusable color palette
        palette = ["#059669", "#dc2626", "#7c3aed", "#ea580c", "#2563eb", "#d97706", "#0891b2", "#9333ea"]
        category_colors = {}
        idx = 0

        # Build comprehensive data
        property_data = []
        for prop in properties:
            if prop.latitude and prop.longitude:
                cat = prop.category_id.name if prop.category_id else 'Property'
                if cat not in category_colors:
                    category_colors[cat] = palette[idx % len(palette)]
                    idx += 1

                image_url = None
                if prop.image:
                    # Create base64 data URL for the image
                    image_url = f"data:image/png;base64,{prop.image.decode('utf-8')}"
                elif prop.image_ids:
                    # Use first image from gallery if main image not available
                    first_image = prop.image_ids[0]
                    if first_image.datas:
                        image_url = f"data:image/png;base64,{first_image.datas.decode('utf-8')}"

                full_address = ", ".join(filter(None, [prop.street, prop.city, prop.zip_code]))

                # Build property data
                property_data.append({
                    'id': prop.id,
                    'name': prop.name or '',
                    'latitude': float(prop.latitude),
                    'longitude': float(prop.longitude),
                    'street': prop.street or '',
                    'city': prop.city or '',
                    'zip_code': prop.zip_code or '',
                    'price': float(prop.price) if prop.price else 0,
                    'contact_phone': prop.contact_phone or '',
                    'contact_email': prop.contact_email or '',
                    'contact_name': prop.contact_name or '',
                    'short_description': prop.short_description or '',
                    'image_url': image_url,
                    'property_type': cat,
                    'nearby_landmarks': prop.nearby_landmarks or '',
                    'views': prop.views or 0,
                    'seo_title': prop.seo_title or '',
                    'marker_color': category_colors[cat],
                    'full_address': full_address,
                })

        return request.render('real_estate_management.property_map_template', {
            'property_count': len(property_data),
            'properties_json': json_scriptsafe.dumps(property_data) if property_data else '[]',
            'category_colors': json_scriptsafe.dumps(category_colors),
            'city_list': city_list,
            'selected_city': selected_city,

        })

    @http.route('/property/<int:property_id>', type='http', auth='public', website=True)
    def property_detail(self, property_id, **kwargs):
        """Individual property detail page"""
        prop = request.env['property.property'].sudo().browse(property_id)
        if not prop.exists() or not prop.is_published:
            return request.not_found()
        if not prop.ai_content_generated:
            try:
                prop.generate_ai_content()
            except Exception as e:
                _logger.error(f"Failed to generate AI content for property {prop.id}: {e}")
        try:
            prop.write({'views': prop.views + 1})
        except Exception as e:
            _logger.error(f"Failed to update views for property {prop.id}: {e}")
        return request.render('real_estate_management.property_detail_page', {
            'property': prop,

        })
