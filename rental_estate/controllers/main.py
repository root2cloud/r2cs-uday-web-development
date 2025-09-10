from odoo import http
from odoo.http import request


class RealEstateWebsite(http.Controller):

    @http.route(['/properties', '/properties/<string:ptype>'], type='http', auth='public', website=True)
    def list_properties(self, ptype=None, **kwargs):
        valid_types = ['buy', 'rent', 'sale']

        # If ptype is given but not in valid list, raise 404 error
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
