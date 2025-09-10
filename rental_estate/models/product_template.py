from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    property_type = fields.Selection([
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('condo', 'Condominium'),
        ('townhouse', 'Townhouse'),
    ], string="Property Type")

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
