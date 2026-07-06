# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    deca_enabled = fields.Boolean(
        related='company_id.deca_enabled',
        readonly=False,
        string="DeCA activo",
    )
    deca_base_url = fields.Char(
        related='company_id.deca_base_url',
        readonly=False,
        string="URL base documento DeCA",
    )
    deca_report_id = fields.Many2one(
        related='company_id.deca_report_id',
        readonly=False,
        string="Informe DeCA",
    )

    @api.onchange('deca_enabled')
    def _onchange_deca_enabled(self):
        # Activar DeCA implica exigir la firma de los albaranes de salida.
        if self.deca_enabled:
            self.group_stock_sign_delivery = True
