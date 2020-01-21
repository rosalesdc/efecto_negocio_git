# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class en_so_lines_values(models.Model):
#     _name = 'en_so_lines_values.en_so_lines_values'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100