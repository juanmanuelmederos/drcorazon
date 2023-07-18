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

from odoo import models, fields


class DrcEchoTestSectionValue(models.Model):
    _name = 'drc.echo.test.section.value'
    _description = "Valores de mediciones en la evaluación de ecocardiogramas"

    name = fields.Char(string="Nombre", required=True, help="Content type name")
    code = fields.Char(string="Código")


class DrcEchoTestSectionUnit(models.Model):
    _name = 'drc.echo.test.section.unit'
    _description = "Unidades de medidas en la evaluación de ecocardiogramas"

    name = fields.Char(string="Nombre", required=True, help="Content type name")
    code = fields.Char(string="Código")




