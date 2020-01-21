# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError


class SOLinesValues(models.Model):
    _inherit = 'sale.order.line'

    x_precio_base = fields.Float(
        string='Precio Base')
    x_porcentaje_utilidad = fields.Float(
        string='% Utilidad deseada')
    x_precio_unidad = fields.Float(string='Calcular Utilidad (Precio deseado)')

    # establecer en 0 el porcentaje de la utilidad y se obtiene el precio base del producto seleccionado
    @api.onchange('product_id')
    def get_default_price(self):
        print('cambiado product id', self.product_id)
        self.write({'x_precio_base': self.product_id.list_price})
        self.write({'x_porcentaje_utilidad': 0})

    # si se cambia el porcentaje de utilidad se cambia el precio unitario
    @api.onchange('x_porcentaje_utilidad')
    def get_price(self):
        print('cambiado porcentaje utilidad')
        if self.x_porcentaje_utilidad < 0:
            raise ValidationError('Valor de utilidad no debe ser menor a 0')
        self.write({'price_unit': self.x_precio_base +
                    (self.x_precio_base*(self.x_porcentaje_utilidad/100))})

    # si se cambia el precio, se cambia el porcentaje de utilidad
    @api.onchange('x_precio_unidad')
    def get_precio_unitario(self):
        print('cambiado precio deseado')
        if self.x_precio_base != 0:
            self.x_porcentaje_utilidad = (
                self.x_precio_unidad * 100 / self.x_precio_base)-100

    # def create(self, vals):
    #     res_id = super(SOLinesValues, self).create(vals)
    #     for record in res_id:
    #         utilidad = record.x_porcentaje_utilidad
    #         record.x_precio_base = record.product_id.list_price
    #     return res_id


class SOValues(models.Model):
    _inherit = 'sale.order'

    def write(self, vals):
        res_id = super(SOValues, self).write(vals)
        for line in self.order_line:
            utilidad = line.x_porcentaje_utilidad
            line.x_precio_unidad = 0
            line.x_porcentaje_utilidad = utilidad
        return res_id
