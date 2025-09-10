from odoo import http
from odoo.http import request


class RealEstateController(http.Controller):

    @http.route(['/properties'], type='http', auth="public", website=True)
    def property_list(self):
        properties = request.env['property'].search([('status', '=', 'available')])
        return request.render('real_estate_website.real_estate_property_list', {'properties': properties})

    @http.route(['/property/<int:property_id>'], type='http', auth="public", website=True)
    def property_detail(self, property_id):
        property = request.env['property'].browse(property_id)
        if not property.exists():
            return request.redirect('/properties')
        return request.render('real_estate_website.property_detail', {'property': property})

    @http.route(['/properties/search'], type='http', auth="public", website=True)
    def property_search(self, location=None):
        domain = [('status', '=', 'available')]
        if location:
            domain.append('|')
            domain.append('|')
            domain.append(('city', 'ilike', location))
            domain.append(('zip', 'ilike', location))
            domain.append(('street', 'ilike', location))
        properties = request.env['property'].search(domain)
        return request.render('real_estate_website.real_estate_property_list', {'properties': properties})
