from odoo import http
from odoo.http import request


class RealEstateWebsite(http.Controller):

    @http.route(['/properties', '/properties/<string:ptype>'], type='http', auth='public', website=True)
    def list_properties(self, ptype=None, **kwargs):
        valid_types = ['buy', 'rent', 'sale']

        if ptype and ptype not in valid_types:
            return request.not_found()

        domain = [('is_published', '=', True)]
        if ptype:
            domain.append(('property_type', '=', ptype))

        properties = request.env['product.template'].sudo().search(domain)

        return request.render('rental_estate.property_listing_page', {
            'properties': properties,
            'property_type': ptype or 'all',
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
