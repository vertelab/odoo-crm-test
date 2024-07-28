from odoo import models, fields, api, _
from datetime import date
import logging
from odoo.exceptions import ValidationError
import re

from allabolag import Company, iter_liquidated_companies
from allabolag.list import iter_list
from copy import deepcopy
from datetime import datetime

_logger = logging.getLogger(__name__)

class CrmLead(models.Model):
    _name = 'crm.lead'
    _inherit = ['crm.lead',"res.builtwith.mixin"]

    company_registry = fields.Char(string='Company Registry', size=64, trim=True, )
    vat = fields.Char(string='VAT', size=64, trim=True, )
 
    def enrich_allabolag(self):
        for crm in self:
            _logger.warning('%s' % crm._fields['summary_revenue'])
            if not crm.company_registry:
                crm.company_registry=self.env['res.partner'].name2orgno(crm.partner_name)

            record=crm.env['res.partner'].partner_enrich_allabolag(crm.company_registry)
            crm.write(record)
            
    def enrich_crm(self):
        for crm in self:
            crm.enrich_allabolag()
            


