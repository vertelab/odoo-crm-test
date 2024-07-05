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

class ResPartnerMixin(models.AbstractModel):
    _name = "res.partner.allabolag.mixin"

    summary_revenue = fields.Float(string='Revenue')
    summary_profit_ebit = fields.Float(string='Profit EBIT')
    summary_purpose = fields.Text(string='Business and purpose')
    kpi_no_employees = fields.Integer(string='Number of employees')
    
    summary_net_sales_change = fields.Float(string='Net Sallary Changes')
    summary_profit_margin = fields.Float(string='Profit Margin')
    summary_solvency = fields.Float(string='Solvency')
    summary_cash_flow = fields.Float(string='Cash Flow')
    
    def name2orgno(self):
        
        i = 1
        for item in iter_list(
            f"what/{self.name}",
            # ~ lambda x: _parse_liquidated_company_item(x)["Konkurs inledd"] < until,
            ):
            print(item.keys())
            i += 1
            if i > 1:
                break 
        _logger.warning(f'{item=}')
        return item['orgnr']
        
    def enrich_allabolag(self):
        if not self.company_type == "company":
            raise UserError(_('This functio has to be on company.'))

        _logger.warning('%s' % self._fields['summary_revenue'])
        if not self.company_registry:
            self.company_registry=self.name2orgno()

        partner = Company(self.company_registry)
        # ~ _logger.warning(f'{partner.data=}')
        
        allabolag = {
        # ~ "Översikt - Besöksadress" :
        # ~ "Översikt - Ort" :
        # ~ "Översikt - Län" :
        "Översikt - Omsättning" : "summary_revenue",
        "Översikt - Årets resultat" : "summary_profit_ebit",
        "Aktivitet och status - Verksamhet & ändamål" : "summary_purpose",
        "Nycketal - Antal anställda" : "kpi_no_employees",
        "Nycketal - Nettoomsättningförändring" : "summary_net_sales_change" ,
        "Nycketal - Vinstmarginal" : "summary_profit_margin" ,
        "Nycketal - Soliditet" : "summary_solvency" ,
        "Nycketal - Kassalikviditet" : "summary_cash_flow" ,
        }

        # ~ _logger.warning(f"{self.fields_get()=}")
        #for key in self.fields_get():
        #        fields_dict[key] = self[key]
        f = self.fields_get()
        record = {allabolag[k]:partner.data[k] for k in allabolag.keys() }
        for k in record.keys():
            if f[k]['type'] == 'integer':
                if type(record[k]) == list:
                    record[k]=int(record[k][0][1])
                else:
                    record[k]=int(record[k])
                    
            if f[k]['type'] in ['float', 'monetary']:
                if type(record[k]) == list:
                    record[k]=record[k][0][1]
                else:
                    record[k]=record[k]
            if f[k]['type'] in ['char', 'text', 'html']:
                if type(record[k]) == list:
                    record[k]= ', '.join(record[k]) 
                else:
                    record[k]=record[k]
                    
                    
        # ~ _logger.warning(f'{record=}')

        self.write(record)
    
    
        # ~ self.env['res.partner'].write({'summary_revenue': 1000000663, 'summary_profit_ebit': 999999999, 'summary_purpose': 'Bolaget har till föremål för sin verksamhet att bedriva finansieringsrörelse och därmed sammanhängande verksamhet huvudsakligen genom att lämna och förmedla kredit avseende fastigheter och bostads- rätter, att lämna kredit till samfällighetsföreningar, att lämna kredit till stat, landsting, kommuner, kommunalförbund eller andra kommunala samfälligheter, samt - mot borgen av sådan samfällighet - till andra juridiska personer, att genom lämnande av betalningsgaranti underlätta kreditgivning av det slag bolaget får bedriva, samt att för annans räkning förvalta sådana lån jämte säkerheter som avses i denna paragraf samt ombesörja inteckningsåtgärder, Med "fastighet" avses i denna bolagsordning också tomträtt och byggnad på mark upplåten med nyttjanderätt samt ägarlägenheter. Med "bostadsrätt" avses även andel i bostadsförening eller aktie i bostadsaktiebolag, där en utan begränsning i tiden upplåten nyttjanderätt till en lägenhet är oskiljaktigt förenad med andelen eller aktien. Med "kredit" avses också byggnadskreditiv. Ord och uttryck som används i denna bolagsordning för att beteckna visst slag av egendom eller rättigheter innefattar egendom eller rättighet i samtliga länder där bolaget bedriver verksamhet, om kreditsäkerhetsegenskaperna för egendomen eller säkerheten i fråga väsentligen motsvarar vad som avses med den svenska benämningen. Med stat, kommun, landsting och samfällighetsföreningar avses förutom sådana organ i Sverige, motsvarande organ i samtliga länder där Stadshypotek bedriver verksamhet. För anskaffande av medel för sin rörelse får bolaget bl.a. 1. ge ut säkerställda obligationer 2. ge ut andra obligationer och certifikat och ta upp reverslån, 3. ge ut förlagsbevis eller andra förskrivningar som medför rätt till betalning efter bolagets övriga förbindelser, samt 4. utnyttja kredit i räkning.', 'kpi_no_employees': 49, 'summary_net_sales_change': 34, 'summary_profit_margin': 1, 'summary_solvency': 1, 'summary_cash_flow': 1})
