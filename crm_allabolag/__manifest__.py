# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo SA, Open Source Management Solution, third party addon
#    Copyright (C) 2024- Vertel AB (<https://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'CRM: Allabolag',
    'version': '14.0',
    'summary': 'Adding valuable internet-data to CRM contacts.',
    'category': 'Website',
    'description': """
Adding interesting and valuable internet-data to customer information in CRM. 
""",
    'author': 'Vertel AB',
    'website': 'https://vertel.se/apps/odoo-crm/crm_allabolag',
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'contributor': '',
    'maintainer': 'Vertel AB',
    'repository': 'https://github.com/vertelab/odoo-crm',
    'depends': ['crm_enrich_base', 'partner_allabolag' , 'utm'],
    'data': [
        'views/views.xml',
        'views/crm_allabolag_mining_views.xml',
        'security/ir.model.access.csv',
    ],
    'application': False,
}
