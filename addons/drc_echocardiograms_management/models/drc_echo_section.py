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

from odoo import models, fields, api

DENOMINATION_TYPE = [
    ('sa', 'APROXIMACIONES PARAESTERNALES'),
    ('sb', 'APROXIMACIONES APICALES'),
    ('sc', 'APROXIMACIONES SUBCOSTALES'),
    ('sd', 'APROXIMACIONES SUPRAESTERNALES'),
    ('se', 'OTRAS APROXIMACIONES')
]


class DrcEchoTestSectionTemplate(models.Model):
    _name = 'drc.echo.test.section.template'
    _description = "Secciones plantillas de mediciones en la evaluación de ecocardiogramas"
    _inherit = ['mail.thread']

    name = fields.Char(string="Sección", required=True, help="Nombre de la sección de análisis")
    section_code = fields.Char(string="Test Code", required=True)
    attribute_ids = fields.One2many('drc.echo.test.section.attribute', 'section_id', string="Attribute")
    denomination_type = fields.Selection(DENOMINATION_TYPE, string="Tipo de aproximación", default='0')


    @api.model
    def create(self, values):
        # Add code here
        res = super(DrcEchoTestSectionTemplate, self).create(values)
        res.attribute_ids.write({'is_template': True})
        return res

    def write(self, values):
        res = super(values, self).write(values)
        self.attribute_ids.write({'is_template': True})
        return res

class DrcEchoTestSectionAttribute(models.Model):
    _name = 'drc.echo.test.section.attribute'
    _rec_name = 'section_value'
    _description = "Atributos de mediciones en la evaluación de ecocardiogramas"

    section_value = fields.Char(string="N.Variable")
    denomination_type = fields.Selection(DENOMINATION_TYPE, string="Tipo de aproximación")
    unit = fields.Many2one('drc.echo.test.section.unit', string="UM")
    result_value = fields.Char(string="Valor")
    interval = fields.Char(string="Intervalo R")
    section_id = fields.Many2one('drc.echo.test.section.template', string="Plantilla de sección")
    echo_test_id = fields.Many2one('drc.echo.test', string="Prueba de ecocardiograma")
    is_template = fields.Boolean(string="Es plantilla")

