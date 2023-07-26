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

from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _


class DrcEchoPatient(models.Model):
    _name = 'drc.echo.patient'
    _rec_name = 'patient'
    _description = 'Patient'

    patient = fields.Many2one('res.partner', string='Nombre del paciente', required=True)
    patient_image = fields.Binary(string='Foto')
    patient_id = fields.Char(string='ID del paciente', readonly=True)
    name = fields.Char(string='ID del paciente', compute='compute_patient_id', store=True)
    first_name = fields.Char(string='', default=lambda self: _('New'))
    second_name = fields.Char(string='', default=lambda self: _('New'))
    middle_dad_name = fields.Char(string='', default=lambda self: _('New'))
    last_mom_name = fields.Char(string='', default=lambda self: _('New'))
    title = fields.Selection([
         ('ms', 'Sra'),
         ('mister', 'Sr'),
    ], string='Title', default='mister', required=True)
    emergency_contact = fields.Many2one(
        'res.partner', string='Emergency Contact')
    gender = fields.Selection(
        [('h', 'Hombre'), ('m', 'Mujer'),
         ('o', 'Otro')], 'Género', required=False, default='m')
    dob = fields.Date(string='Fecha de nacimiento', required=False)
    age = fields.Char(string='Edad', compute='compute_age', store=True)
    blood_group = fields.Selection(
        [('A+', 'A+ve'), ('B+', 'B+ve'), ('O+', 'O+ve'), ('AB+', 'AB+ve'),
         ('A-', 'A-ve'), ('B-', 'B-ve'), ('O-', 'O-ve'), ('AB-', 'AB-ve')],
        'Blood Group')
    visa_info = fields.Char(string='Visa Info', size=64)
    id_proof_number = fields.Char(string='ID de prueba')
    note = fields.Text(string='Nota')
    date = fields.Datetime(string='Date Requested', default=lambda s: fields.Datetime.now(), invisible=True)
    phone = fields.Char(string="Teléfono", required=False)
    email = fields.Char(string="Correo", required=False)
    weight = fields.Float(string="Peso", required=False)
    size = fields.Char(string="Talla", required=False)

    @api.depends('dob')
    def compute_age(self):
        for data in self:
            if data.dob:
                dob = fields.Datetime.from_string(data.dob)
                date = fields.Datetime.from_string(data.date)
                delta = relativedelta(date, dob)
                data.age = str(delta.years) + ' ' + 'years'
            else:
                data.age = ''

    @api.depends('dob', 'gender')
    def compute_patient_id(self):
        for data in self:
            if data.dob:
                dob = fields.Datetime.from_string(data.dob)
                data.name = str(data.gender[0].upper()) + str(dob.year)[2:] \
                            + str(dob.month).zfill(2) + str(dob.day).zfill(2)

    @api.onchange('gender')
    def onchange_gender(self):
        self.compute_patient_id()

    #def create(self, vals):
        #sequence = self.env['ir.sequence'].next_by_code('lab.patient')
        #vals['name'] = sequence or _('New')
        #result = super(DrcEchoPatient, self).create(vals)
        #return result

    @api.onchange('patient')
    def detail_get(self):
        self.phone = self.patient.phone
        self.email = self.patient.email

