# © 2026 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    deca_enabled = fields.Boolean(
        related='company_id.deca_enabled',
        readonly=False,
        string="Enable DeCA",
    )
    deca_base_url = fields.Char(
        related='company_id.deca_base_url',
        readonly=False,
        string="DeCA document base URL",
    )
    deca_report_id = fields.Many2one(
        related='company_id.deca_report_id',
        readonly=False,
        string="DeCA report",
    )

    @api.onchange('deca_enabled')
    def _onchange_deca_enabled(self):
        # Enabling DeCA also requires signature on outgoing delivery orders.
        if self.deca_enabled:
            self.group_stock_sign_delivery = True
