# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2019-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Anusha P P @ cybrosys and Niyas Raphy @ cybrosys(odoo@cybrosys.com)
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

import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class DrcEchoTest(models.Model):
    _name = 'drc.echo.test'
    _inherit = ['mail.thread']
    _description = 'Echocardiology Test'

    name = fields.Char(string='Código', size=16, readonly=True, required=True, help="ID de prueba", default=lambda *a: '#')
    test_patient_id = fields.Many2one('drc.echo.patient', string='Paciente', select=True,
                                    help='Datos del paciente')
    date = fields.Datetime(string='Requested Date')
    comment = fields.Text('Comment')

    template_sa_id = fields.Many2one('drc.echo.test.section.template',
                                  string='Plantilla sección sa',
                                  domain=[('section_code_type', '=', 'sa')])

    attribute_value_line_sa_ids = fields.One2many('drc.echo.test.section.attribute',
                                              'echo_test_id',
                                              string="Valores sección SA",
                                              domain=[('section_code_type', '=', 'sa')])

    template_sb_id = fields.Many2one('drc.echo.test.section.template',
                                  string='Plantilla sección sb',
                                  domain=[('section_code_type', '=', 'sb')])

    attribute_value_line_sb_ids = fields.One2many('drc.echo.test.section.attribute',
                                              'echo_test_id',
                                              string="Valores sección SB",
                                              domain=[('section_code_type', '=', 'sb')])

    template_sc_id = fields.Many2one('drc.echo.test.section.template',
                                  string='Plantilla sección sc',
                                  domain=[('section_code_type', '=', 'sc')])

    attribute_value_line_sc_ids = fields.One2many('drc.echo.test.section.attribute',
                                              'echo_test_id',
                                              string="Valores sección SC",
                                              domain=[('section_code_type', '=', 'sc')])

    template_sd_id = fields.Many2one('drc.echo.test.section.template',
                                  string='Plantilla sección sd',
                                  domain=[('section_code_type', '=', 'sd')])

    attribute_value_line_sd_ids = fields.One2many('drc.echo.test.section.attribute',
                                              'echo_test_id',
                                              string="Valores sección SD",
                                              domain=[('section_code_type', '=', 'sd')])

    template_se_id = fields.Many2one('drc.echo.test.section.template',
                                  string='Plantilla sección se',
                                  domain=[('section_code_type', '=', 'se')])
    attribute_value_line_se_ids = fields.One2many('drc.echo.test.section.attribute',
                                              'echo_test_id',
                                              string="Valores sección SE",
                                              domain=[('section_code_type', '=', 'se')])
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sample_collection', 'Sample Collected'),
        ('test_in_progress', 'Test In Progress'),
        ('completed', 'Completed'),
        ('cancel', 'Cancelled'),

    ], string='Status', readonly=True, copy=False, index=True, tracking=True, default='draft')

    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].next_by_code('drc.echo.request')
        vals['name'] = sequence or '/'
        return super(DrcEchoTest, self).create(vals)

    def set_to_sample_collection(self):
        return self.write({'state': 'sample_collection'})

    def set_to_test_in_progress(self):
        return self.write({'state': 'test_in_progress'})

    def cancel_test(self):
        return self.write({'state': 'cancel'})

    def print_lab_test(self):
        return self.env.ref('medical_lab_management.print_lab_test').report_action(self)


