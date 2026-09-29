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
        placeholder="E.g. http://deca.mycompany.com",
    )
    deca_report_id = fields.Many2one(
        related='company_id.deca_report_id',
        readonly=False,
        string="DeCA report",
    )
    deca_sign_required = fields.Boolean(
        related='company_id.deca_sign_required',
        readonly=False,
        compute="_compute_deca_sign_required",
        string="DeCA Sign required",
    )

    @api.onchange('deca_sign_required')
    def _onchange_deca_sign_required(self):
        if self.deca_sign_required:
            self.group_stock_sign_delivery = True

    @api.depends("deca_enabled")
    def _compute_deca_sign_required(self):
        enabled = self.filtered(lambda x: x.deca_enabled)
        enabled.deca_sign_required = True
        (self - enabled).deca_sign_required = False
