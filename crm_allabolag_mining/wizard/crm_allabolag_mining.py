# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError

class CrmAllabolagMining(models.Model):
    _name = 'crm.allabolag.mining'
    _description = 'CRM Allabolag Mining'

    state = fields.Selection(selection=[('draft','Draft'),('done','Done')])
    lan = fields.Selection(selection=[
            ('xl/10','Blekinge',),
            ('xl/20','Dalarna'),
            ('xl/9','Gotland'),
            ('Gävleborg','xl/21'),
            ('Halland','xl/13'),
            ('Jämtland','xl/23'),
            ('Jönköping','xl/6'),
            ('Kalmar','xl/8'),
            ('Kronoberg','xl/7'),
            ('Norrbotten','xl/25'),
            ('Skåne','xl/12'),
            ('Stockholm','xl/1'),
            ('Södermanland','xl/4'),
            ('Uppsala','xl/3'),
            ('Värmland','xl/17'),
            ('Västerbotten','xl/24'),
            ('Västernorrland','xl/22'),
            ('Västmanland','xl/19'),
            ('Västra götaland','xl/14'),
            ('Örebro','xl/18'),
            ('Östergötland','xl/5'),
    ],string='County')

    def action_submit(self):
        self.ensure_one()
        if self.name == _('New'):
            self.name = self.env['ir.sequence'].next_by_code('crm.iap.lead.mining.request') or _('New')
        results = self._perform_request()
        if results:
            self._create_leads_from_response(results)
            self.state = 'done'
        if self.lead_type == 'lead':
            return self.action_get_lead_action()
        elif self.lead_type == 'opportunity':
            return self.action_get_opportunity_action()




    bolagsform = {
        'Enskild firma': 'xb/EF',
        'Aktiebolag': 'xb/AB',
        'Ideella föreningar': 'xb/IF',
        'Hb & Kb': 'xb/HK',
        'Övriga bolagsformer': 'xb/OV',
        'Samfälligheter': 'xb/SA',
        'Sambruksförening': 'xb/SF',
        'Filialer':'xb/FI',
        'Ekonomisk förening':'xb/EK',
        'Enkla bolag': 'xb/EB',
        'Statliga & kommunala': 'xb/SK',
        'Bostadsförening': 'xb/BF',
        'Värdepappersfonder': 'xb/VP',
    }

    anstallda = {
        '0': 'xe/1',
        '1 - 4': 'xe/2',
        '5 - 9': 'xe/3',
        '10 - 19': 'xe/4',
        '20 - 49': 'xe/5',
        '50 - 99': 'xe/6',
        '100 - 199': 'xe/7',
        '200 - 999': 'xe/8',
        '> 1000': 'xe/9',
    }

    omsattning = 'xr/100-200'
    omsattning = 'xr/100-'
    omsattning = 'xr/-100'

    company_name = 'what/{name}'
    city = 'where/{city}'
    sni = "verksamhet/{sni}"

    a = """
    branch = {

    xv/PARTIHANDEL
    xv/JORDBRUK, SKOGSBRUK, JAKT & FISKE
    xv/FASTIGHETSVERKSAMHET
    xv/BRANSCH-, ARBETSGIVAR- & YRKESORG.
    xv/BYGG-, DESIGN- & INREDNINGSVERKSAMHET
    /xv/KULTUR, NÖJE & FRITID
    /xv/JURIDIK, EKONOMI & KONSULTTJÄNSTER
    /xv/DETALJHANDEL
    /xv/DATA, IT & TELEKOMMUNIKATION
    xv/PARTIHANDEL
    xv/HÄLSA & SJUKVÅRD
    xv/TILLVERKNING & INDUSTRI
    xv/BANK, FINANS & FÖRSÄKRING
    xv/UTBILDNING, FORSKNING & UTVECKLING
    xv/HOTELL & RESTAURANG
    /xv/TRANSPORT & MAGASINERING
    xv/TEKNISK KONSULTVERKSAMHET
    xv/REPARATION & INSTALLATION
    xv/HÅR & SKÖNHETSVÅRD
    xv/ÖVRIGA KONSUMENTTJÄNSTER
    xv/FÖRETAGSTJÄNSTER
    xv/MEDIA
    /xv/REKLAM, PR & MARKNADSUNDERSÖKNING
    xv/BEMANNING & ARBETSFÖRMEDLING
    xv/MOTORFORDONSHANDEL
    /xv/UTHYRNING & LEASING
    xv/AVLOPP, AVFALL, EL & VATTEN
    xv/LIVSMEDELSFRAMSTÄLLNING
    xv/RESEBYRÅ & TURISM
    xv/OFFENTLIG FÖRVALTNING & SAMHÄLLE
    /xv/AMBASSADER & INTERNATIONELLA ORG.

    }


    """
