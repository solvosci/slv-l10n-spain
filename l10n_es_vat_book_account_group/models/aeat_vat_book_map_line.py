# © 2022 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class AeatVatBookMapLine(models.Model):
    _inherit = "aeat.vat.book.map.line"

    account_group_id = fields.Many2one(
        string="Account Group Restriction",
        comodel_name="account.group",
    )
