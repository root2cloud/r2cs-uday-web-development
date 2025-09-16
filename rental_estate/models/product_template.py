from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    bedrooms = fields.Integer(string="Bedrooms")
    bathrooms = fields.Integer(string="Bathrooms")
    square_feet = fields.Float(string="Square Footage")
    rental_price = fields.Float(string="Rental Price")
    availability_status = fields.Selection([
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('maintenance', 'Under Maintenance'),
    ], string="Availability Status", default='available')
    landlord_id = fields.Many2one('res.partner', string="Landlord")
    # amenities = fields.Many2many('rental.amenity', string="Amenities")
    lease_duration = fields.Char(string="Lease Duration")
    deposit_amount = fields.Float(string="Security Deposit")
    property_type = fields.Selection([
        ('buy', 'Buy'),
        ('rent', 'Rent'),
        ('sell', 'Sell'),
    ], string="Property Type", required=True, default='rent')
    location = fields.Char(string="Location")
    zip_code = fields.Char(string="Zip Code")
    status = fields.Selection([
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('sold', 'Sold'),
        ('maintenance', 'Under Maintenance'),
    ], string="Status", default='available')
    room_image_ids = fields.One2many('property.room.image', 'product_tmpl_id', string="Room Images")
