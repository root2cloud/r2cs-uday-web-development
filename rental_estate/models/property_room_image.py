from odoo import models, fields


class PropertyRoomImage(models.Model):
    _name = "property.room.image"
    _description = "Property Room Image"

    product_tmpl_id = fields.Many2one('product.template', string="Property", required=True, ondelete='cascade')
    name = fields.Char(string="Room Name")
    image = fields.Binary(string="Room Image")
