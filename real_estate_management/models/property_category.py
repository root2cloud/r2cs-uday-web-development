from odoo import models, fields


class PropertyCategory(models.Model):
    _name = 'property.category'
    _description = 'Property Category'

    name = fields.Char('Category Name', required=True)
    description = fields.Text('Description')
    parent_left = fields.Integer('Left Parent', index=True)
    parent_right = fields.Integer('Right Parent', index=True)
    image = fields.Binary('Image')
    seo_title = fields.Char('SEO Title')
    seo_description = fields.Text('SEO Description')

    property_ids = fields.One2many('property.property', 'category_id', string='Properties')
