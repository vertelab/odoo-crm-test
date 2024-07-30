from odoo import models, fields, api, _
from datetime import date
import logging
from odoo.exceptions import ValidationError
import re
from odoo.addons.partner_builtwith.tools.builtwith import name2url



_logger = logging.getLogger(__name__)

class CrmLead(models.Model):
    _name = 'crm.lead'
    _inherit = ['crm.lead',"res.builtwith.mixin"]
    
    def name2website(self, name):
        for crm in self:
            try:
                crm.website = name2url(name)
                _logger.warning(f"{crm.website=}")

            except Exception as e:
                _logger.warning(f"Google: An unexpected error occurred: {e}")
                crm.message_post(body=_(f'Google name2website: unexpected error {e} {crm.name}\nMaybe you can add website manually?'), message_type='notification')
    
    def crm_enrich(self):
        _logger.warning(f'{self.__class__.__name__=}  {type(self._name).__mro__=}')

        for crm in self:
            _logger.warning(f'crm_builtwith {crm.name=}')
            if not crm.website:
                crm.name2website(crm.partner_name or crm.name)
            crm.bw_enrich()
        super(CrmLead,self).crm_enrich()
        


