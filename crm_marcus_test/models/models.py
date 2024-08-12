# -*- coding: utf-8 -*-

from odoo import models, fields, api


class scaffold_test(models.TransientModel):
    _inherit = 'base.module.update'
    _description = 'scaffold_test.scaffold_test'

    test = fields.Boolean("Test")

