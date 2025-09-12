from odoo import http
from odoo.http import request


class RealEstateWebsite(http.Controller):

    @http.route(['/properties', '/properties/<string:ptype>'], type='http', auth='public', website=True)
    def list_properties(self, ptype=None, zip_code=None, property_type=None, **kwargs):
        valid_types = ['buy', 'rent', 'sale']

        # Validate property type from URL or query param
        if ptype and ptype not in valid_types:
            return request.not_found()

        # Determine filter property_type priority:
        # ptype from URL (for specific pages) overrides property_type query param (for all properties)
        filter_type = ptype or (property_type if property_type in valid_types else None)

        domain = [('is_published', '=', True)]
        if filter_type:
            domain.append(('property_type', '=', filter_type))

        if zip_code:
            domain.append(('zip_code', '=', zip_code))

        properties = request.env['product.template'].sudo().search(domain)

        return request.render('rental_estate.property_listing_page', {
            'properties': properties,
            'property_type': filter_type or 'all',
            'zip_code': zip_code or '',
            'valid_types': valid_types,
        })

    @http.route(['/property/<string:ptype>/<int:property_id>'], type='http', auth='public', website=True)
    def property_detail(self, ptype, property_id, **kwargs):
        valid_types = ['buy', 'rent', 'sale']

        if ptype not in valid_types:
            return request.not_found()

        property_record = request.env['product.template'].sudo().search([
            ('id', '=', property_id),
            ('property_type', '=', ptype),
            ('is_published', '=', True),
        ], limit=1)

        if not property_record:
            return request.not_found()

        room_images = property_record.room_image_ids

        return request.render('rental_estate.property_detail_page', {
            'property': property_record,
            'room_images': room_images,
        })
