# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2021-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

{
    'name': "Echocardiology Test Management",
    'version': '16.0.1.1.0',
    'summary': """Manage Echocardiology Test""",
    'description': """Manage Medical Lab General Operations, Odoo15, Odoo 15""",
    'author': "Juan Manuel Mederos",
    'company': "Drc Sistemas",
    'website': "https://www.vitaritmo.com",
    'category': 'Medical',
    'depends': ['base', 'mail', 'contacts'],
    'data': [
        'security/drc_echo_users.xml',
        'security/ir.model.access.csv',
        'views/drc_echo_patient_view.xml',
        'views/drc_echo_section_unit_view.xml',
        'views/drc_echo_section_view.xml',
        #'views/drc_echo_section_value_view.xml',
        'views/dr_echo_test_view.xml',
    ],
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
