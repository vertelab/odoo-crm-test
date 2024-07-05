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
    _inherit = ['crm.lead',"res.partner.allabolag.mixin"]

    company_registry = fields.Char(string='Company Registry', size=64, trim=True, )

 
    def enrich_allabolag(self):

        _logger.warning('%s' % self._fields['summary_revenue'])
        if not self.company_registry:
            self.company_registry=self.env['res.partner'].name2orgno(self.partner_name)

        record=self.env['res.partner'].partner_enrich_allabolag(self.company_registry)
        self.write(record)

