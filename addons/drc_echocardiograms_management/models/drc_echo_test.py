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
    patient_id = fields.Many2one('drc.echo.patient', string='Paciente', select=True,
                                    help='Datos del paciente')
    date = fields.Datetime(string='Fecha', default=datetime.datetime.now())
    comment = fields.Text('Observaciones')

    template_sa_id = fields.Many2one('drc.echo.test.section.template',
                                  string='Plantilla sección sa',
                                  domain=[('denomination_type', '=', 'sa')])

    attribute_value_line_sa_ids = fields.One2many('drc.echo.test.section.attribute',
                                              'echo_test_id',
                                              string="Valores sección SA",
                                              domain=[('denomination_type', '=', 'sa')])

    template_sb_id = fields.Many2one('drc.echo.test.section.template',
                                  string='Plantilla sección sb',
                                  domain=[('denomination_type', '=', 'sb')])

    attribute_value_line_sb_ids = fields.One2many('drc.echo.test.section.attribute',
                                              'echo_test_id',
                                              string="Valores sección SB",
                                              domain=[('denomination_type', '=', 'sb')])

    template_sc_id = fields.Many2one('drc.echo.test.section.template',
                                  string='Plantilla sección sc',
                                  domain=[('denomination_type', '=', 'sc')])

    attribute_value_line_sc_ids = fields.One2many('drc.echo.test.section.attribute',
                                              'echo_test_id',
                                              string="Valores sección SC",
                                              domain=[('denomination_type', '=', 'sc')])

    template_sd_id = fields.Many2one('drc.echo.test.section.template',
                                  string='Plantilla sección sd',
                                  domain=[('denomination_type', '=', 'sd')])

    attribute_value_line_sd_ids = fields.One2many('drc.echo.test.section.attribute',
                                              'echo_test_id',
                                              string="Valores sección SD",
                                              domain=[('denomination_type', '=', 'sd')])

    template_se_id = fields.Many2one('drc.echo.test.section.template',
                                  string='Plantilla sección se',
                                  domain=[('denomination_type', '=', 'se')])
    attribute_value_line_se_ids = fields.One2many('drc.echo.test.section.attribute',
                                              'echo_test_id',
                                              string="Valores sección SE",
                                              domain=[('denomination_type', '=', 'se')])
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

    @api.onchange('template_sa_id', 'template_sb_id', 'template_sc_id', 'template_sd_id', 'template_se_id')
    def onchange_section_template(self):
        prefix_list = ['sa', 'sb', 'sc', 'sd', 'se']
        for prefix in prefix_list:
            template_id = self['template_' + prefix + '_id']
            if template_id:
                self['attribute_value_line_' + prefix + '_ids'] = [(5, 0, 0)]
                for attribute in template_id.attribute_ids.filtered(lambda r: r.is_template):
                    self['attribute_value_line_' + prefix + '_ids'] = [(0, 0, {
                        'section_value': attribute.section_value,
                        'unit': attribute.unit,
                        'interval': attribute.interval,
                        'denomination_type': prefix,
                        'is_template': False,
                    })]

    def set_to_sample_collection(self):
        return self.write({'state': 'sample_collection'})

    def set_to_test_in_progress(self):
        return self.write({'state': 'test_in_progress'})

    def cancel_test(self):
        return self.write({'state': 'cancel'})

    def print_lab_test(self):
        return self.env.ref('medical_lab_management.print_lab_test').report_action(self)


