from odoo import models, fields, api, _
import logging
from datetime import date
import requests
import json
import time
from requests.exceptions import HTTPError

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
    street = fields.Char(string='Street')
    street2 = fields.Char(string='Street 2')
    city = fields.Char(string='City', required=True, default='Visakhapatnam')
    zip_code = fields.Char(string='ZIP')

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

    # AI-generated fields
    ai_property_description = fields.Html(readonly=True)
    ai_investment_benefits = fields.Text(readonly=True)
    ai_lifestyle_benefits = fields.Text(readonly=True)
    ai_nearby_facilities = fields.Text(readonly=True)
    ai_unique_selling_points = fields.Text(readonly=True)
    ai_content_generated = fields.Boolean(default=False)
    ai_generation_date = fields.Datetime()
    last_viewed = fields.Datetime(string='Last Viewed')  # Ensure this field is defined
    image_ids = fields.One2many('ir.attachment', 'res_id', domain=[('res_model', '=', 'property.property')],
                                string="AI Generated Images")

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
                    print(f"Geocoded {rec.name}: {coords}")
                else:
                    rec.latitude = rec.longitude = False
                    rec.date_localization = False
                    _logger.warning(f"Geocode failed {rec.name}: {params}")
            except Exception as e:
                rec.latitude = rec.longitude = False
                rec.date_localization = False
                _logger.error(f"Geocode error {rec.name}: {e}")

    def generate_ai_content(self):
        api_key = self.env['ir.config_parameter'].sudo().get_param('openai.api_key')
        if not api_key:
            _logger.error("OpenAI API key is not configured in system parameters.")
            return

        _logger.info(f"Generating AI content for property: {self.name}")
        location = f"{self.street}, {self.street2 or ''}, {self.city}"
        prompt = (
            f"Generate marketing content for a real estate property named '{self.name}', "
            f"located at {location}, priced at ₹{self.price:,}, type {self.category_id.name or 'N/A'}. "
            "Return the response as a JSON object with the following keys: "
            "'description' (a detailed HTML description of the property), "
            "'investment_benefits' (text listing investment benefits), "
            "'lifestyle_benefits' (text listing lifestyle benefits), "
            "'nearby_facilities' (text listing nearby facilities), "
            "'unique_selling_points' (text listing unique selling points)."
        )
        headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
        payload = {
            'model': 'gpt-4o-mini',
            'messages': [
                {'role': 'system', 'content': 'You are a real estate marketing expert.'},
                {'role': 'user', 'content': prompt}
            ],
            'max_tokens': 800,
            'temperature': 0.7
        }

        try:
            res = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers=headers,
                json=payload,
                timeout=30
            )
            res.raise_for_status()
            response_data = res.json()
            _logger.info(f"OpenAI API response for property {self.name}: {response_data}")
            response_text = response_data['choices'][0]['message']['content']
            print(response_text)
            if response_text.startswith("```json"):
                response_text = response_text.replace("```json", "").replace("```", "").strip()
            try:
                js = json.loads(response_text)
            except Exception as e:
                print("Wrong", e)
                js = {
                    'description': response_text,
                }
            self.write({
                'ai_property_description': js.get('description', ''),
                'ai_investment_benefits': js.get('investment_benefits', ''),
                'ai_lifestyle_benefits': js.get('lifestyle_benefits', ''),
                'ai_nearby_facilities': js.get('nearby_facilities', ''),
                'ai_unique_selling_points': js.get('unique_selling_points', ''),
                'ai_content_generated': True,
                'ai_generation_date': fields.Datetime.now(),
            })
            _logger.info(f"AI content written for property {self.name}: {js}")

        except Exception as e:
            _logger.error(f"AI generation failed for property {self.name}: {e}")
            return
