from odoo import models, fields, api


class Property(models.Model):
    _name = 'property.property'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Real Estate Property'

    # Core Info
    name = fields.Char(string='Property Name', required=True)
    alias_name = fields.Char(string='Alternate Display Name')
    short_description = fields.Char(string='Short Description')
    detailed_description = fields.Html('Detailed Description')
    price = fields.Float('Estimated Price')
    marketing_video_url = fields.Char(string='Marketing Video URL')
    property_website_url = fields.Char(string='Property Website URL')
    image = fields.Image(string='Property Image')


    # Location - Hardcoded to Vishakapatnam in process logic, so keep minimal address details
    street = fields.Char(string='Street Address')
    locality = fields.Char(string='Locality/Neighborhood')
    city = fields.Char(string='City', default='Vishakapatnam')
    zip_code = fields.Char(string='Postal Code')
    latitude = fields.Float(string="Latitude", digits=(16, 4))
    longitude = fields.Float(string="Longitude", digits=(16, 4))

    # Contact
    contact_name = fields.Char(string='Contact Person')
    contact_phone = fields.Char(string='Phone Number')
    contact_email = fields.Char(string='Email Address')
    contact_website = fields.Char(string='Contact Website')

    # Amenities & Nearby Locations
    amenities = fields.Text(string='Amenities and Features')
    nearby_landmarks = fields.Text(string='Nearby Landmarks')

    # Media
    image_ids = fields.Many2many('ir.attachment', string='Property Images')

    # SEO & Publishing
    seo_title = fields.Char(string='SEO Title')
    seo_description = fields.Text(string='SEO Description')
    is_published = fields.Boolean(string='Published on Website', default=False)

    # Analytics
    views_count = fields.Integer(string='Page Views', default=0)

    # Computed
    image_count = fields.Integer(string='Number of Images', compute='_compute_image_count')
    category_id = fields.Many2one('property.category', string='Category')

    @api.depends('image_ids')
    def _compute_image_count(self):
        for record in self:
            record.image_count = len(record.image_ids)
