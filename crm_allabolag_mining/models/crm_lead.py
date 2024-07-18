# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
import logging
from allabolag import Company, iter_liquidated_companies
from allabolag.list import iter_list

_logger = logging.getLogger(__name__)



class CRMLeadMining(models.Model):
    _inherit = 'crm.lead'

    lead_mining_request_id = fields.Many2one('crm.iap.lead.mining.request', string='Lead Mining Request', index=True)
