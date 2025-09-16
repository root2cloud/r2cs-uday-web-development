from odoo import http
from odoo.http import request
import base64


class RealEstateWebsite(http.Controller):

    @http.route(['/properties', '/properties/<string:ptype>'], type='http', auth='public', website=True)
    def list_properties(self, ptype=None, zip_code=None, property_type=None, **kwargs):
        valid_types = ['buy', 'rent']

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
        valid_types = ['buy', 'rent', 'sell']

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

    @http.route('/property/sell', type='http', auth='public', website=True)
    def sell_property_form(self, **kwargs):
        return request.render('rental_estate.sell_property_form', {})

    @http.route('/property/sell/submit', type='http', auth='public', methods=['POST'], website=True)
    def sell_property_submit(self, **post):
        required_fields = ['name', 'location', 'zip_code']
        for field in required_fields:
            if not post.get(field):
                return request.render('rental_estate.sell_property_form', {
                    'error': f"Missing required field: {field}",
                    **post,
                })

        # Read main image if uploaded
        main_image_file = request.httprequest.files.get('image_1920')
        main_image_data = False
        if main_image_file:
            main_image_data = base64.b64encode(main_image_file.read())

        vals = {
            'name': post.get('name'),
            'property_type': 'sell',  # Default property type for sell form
            'location': post.get('location'),
            'zip_code': post.get('zip_code'),
            'bedrooms': post.get('bedrooms'),
            'bathrooms': post.get('bathrooms'),
            'square_feet': post.get('square_feet'),
            'rental_price': post.get('rental_price'),
            'availability_status': 'available',
            'status': 'available',
            'is_published': True,
        }
        if main_image_data:
            vals['image_1920'] = main_image_data

        product_obj = request.env['product.template'].sudo().create(vals)

        # Handle multiple room images uploads
        room_images_files = request.httprequest.files.getlist('room_images')
        for image_file in room_images_files:
            if image_file:
                image_data = base64.b64encode(image_file.read())
                request.env['property.room.image'].sudo().create({
                    'product_tmpl_id': product_obj.id,
                    'name': f"Room image for {product_obj.name}",
                    'image': image_data,
                })

        return request.render('rental_estate.sell_thank_you')
