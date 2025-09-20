from odoo import models, fields, api, _
import logging
from datetime import date

_logger = logging.getLogger(__name__)


class Property(models.Model):
    _name = 'property.property'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Real Estate Property'

    # Core fields
    name = fields.Char(string='Property Name', required=True)
    alias_name = fields.Char(string='Alternate Display Name')
    short_description = fields.Char(string='Short Description')
    detailed_description = fields.Html(string='Detailed Description')
    price = fields.Float(string='Estimated Price')
    marketing_video_url = fields.Char(string='Marketing Video')
    property_website_url = fields.Char(string='Property Website')
    image = fields.Image(string='Property Image')

    # Address fields
    street = fields.Char(string='Street', required=True)
    street2 = fields.Char(string='Street 2')
    city = fields.Char(string='City', required=True, default='Visakhapatnam')
    zip_code = fields.Char(string='ZIP', required=True)

    state_id = fields.Many2one('res.country.state', string='State', readonly=True,
                               default=lambda self: self.env['res.country.state']
                               .search([('name', '=', 'Andhra Pradesh')], limit=1).id)
    country_id = fields.Many2one('res.country', string='Country', readonly=True,
                                 default=lambda self: self.env.company.country_id.id, store=True)

    # Computed, stored geolocation fields
    latitude = fields.Float(string='Latitude', digits=(16, 5),
                            compute='_compute_geolocation', store=True)
    longitude = fields.Float(string='Longitude', digits=(16, 5),
                             compute='_compute_geolocation', store=True)
    date_localization = fields.Date(string='Geolocation Date',
                                    compute='_compute_geolocation', store=True)

    # Other Info
    contact_name = fields.Char(string='Contact Person')
    contact_phone = fields.Char(string='Phone')
    contact_email = fields.Char(string='Email')
    contact_website = fields.Char(string='Website')
    amenities = fields.Text(string='Amenities')
    nearby_landmarks = fields.Text(string='Nearby Landmarks')
    image_ids = fields.Many2many('ir.attachment', string='Property Images')
    image_count = fields.Integer(string='Number of Images', compute='_compute_image_count')
    seo_title = fields.Char(string='SEO Title')
    seo_description = fields.Text(string='SEO Description')
    is_published = fields.Boolean(string='Published', default=False)
    views = fields.Integer(string='Views', default=0)
    category_id = fields.Many2one('property.category', string='Category')

    @api.depends('image_ids')
    def _compute_image_count(self):
        for rec in self:
            rec.image_count = len(rec.image_ids)

    @api.depends('street', 'street2', 'city', 'zip_code', 'state_id', 'country_id')
    def _compute_geolocation(self):
        geo = self.env['base.geocoder']
        for rec in self:
            street = ' '.join(filter(None, [rec.street, rec.street2]))
            params = {
                'street': street,
                'zip': rec.zip_code or '',
                'city': rec.city or '',
                'state': rec.state_id.name or '',
                'country': rec.country_id.name or '',
            }
            if not (params['street'] or params['zip']):
                rec.latitude = rec.longitude = False
                rec.date_localization = False
                continue
            try:
                query = geo.geo_query_address(**params)
                coords = geo.geo_find(query, force_country=params['country'])
                if coords and len(coords) == 2:
                    rec.latitude, rec.longitude = coords
                    rec.date_localization = fields.Date.context_today(rec)
                    _logger.info(f"Geocoded {rec.name}: {coords}")
                else:
                    rec.latitude = rec.longitude = False
                    rec.date_localization = False
                    _logger.warning(f"Geocode failed {rec.name}: {params}")
            except Exception as e:
                rec.latitude = rec.longitude = False
                rec.date_localization = False
                _logger.error(f"Geocode error {rec.name}: {e}")
