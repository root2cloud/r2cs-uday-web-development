from odoo import models, fields

class Property(models.Model):
    _name = 'property'
    _description = 'Real Estate Property'

    name = fields.Char('Title', required=True)
    price = fields.Float('Price')
    description = fields.Text('Description')
    street = fields.Char('Street Address')
    city = fields.Char('City')
    state_id = fields.Many2one('res.country.state', string='State')
    country_id = fields.Many2one('res.country', string='Country')
    zip = fields.Char('ZIP/Postal Code')
    bedrooms = fields.Integer('Bedrooms')
    bathrooms = fields.Integer('Bathrooms')
    area = fields.Float('Area (sq ft)')
    image = fields.Binary('Image')
    status = fields.Selection([
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('pending', 'Pending'),
    ], default='available')
