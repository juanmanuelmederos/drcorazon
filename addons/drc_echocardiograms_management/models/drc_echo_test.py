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

    attribute_value_line_all_ids = fields.One2many('drc.echo.test.section.attribute',
                                              'echo_test_id',
                                              string="Valores capturados",
                                              )

    template_sa_id = fields.Many2one('drc.echo.test.section.template',
                                  string='',
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
        ('draft', 'Captura de datos'),
        ('review', 'Revisión'),
        ('completed', 'Completado'),
        ('cancel', 'Cancelado')

    ], string='Status', readonly=True, copy=False, index=True, tracking=True, default='draft')

    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].next_by_code('drc.echo.request')
        vals['name'] = sequence or '/'
        return super(DrcEchoTest, self).create(vals)

    def _get_default_template(self):
        prefix_list = ['sa', 'sb', 'sc', 'sd', 'se']
        for prefix in prefix_list:
            default_template = self.env['drc.echo.test.section.template']\
                                    .search([('denomination_type', '=', prefix)], limit=1)
            self['template_' + prefix + '_id']= default_template.id

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        if self.patient_id:
            self._get_default_template()
            self.set_section_attributes_by_temmplate()

    def set_section_attributes_by_temmplate(self):
        prefix_list = ['sa', 'sb', 'sc', 'sd', 'se']
        for prefix in prefix_list:
            template_id = self['template_' + prefix + '_id']
            if template_id:
                self['attribute_value_line_' + prefix + '_ids'] = [(5, 0, 0)]
                item_values = []
                for attribute in template_id.attribute_ids.filtered(lambda r: r.is_template):
                    item_values.append((0, 0, {
                        'section_value': attribute.section_value,
                        'unit': attribute.unit,
                        'interval': attribute.interval,
                        'denomination_type': prefix,
                        'is_template': False,
                    }))
                if item_values:
                    self['attribute_value_line_' + prefix + '_ids'] = item_values
                    #field_attribute_name = 'attribute_value_line_' + prefix + '_ids'
                    #self.update(field_attribute_name = item_values)


    def set_to_review(self):
        return self.write({'state': 'review'})

    def set_to_completed(self):
        return self.write({'state': 'completed'})

    def set_to_draft(self):
        return self.write({'state': 'draft'})

    def cancel_test(self):
        return self.write({'state': 'cancel'})

    def print_lab_test(self):
        return self.env.ref('medical_lab_management.print_lab_test').report_action(self)


