# -*- coding: utf-8 -*-
from odoo import fields, models


class StockPickingDecaConfirmWizard(models.TransientModel):
    _name = 'stock.picking.deca.confirm.wizard'
    _description = 'Confirmación de regeneración de documento DeCA'

    picking_id = fields.Many2one(
        'stock.picking',
        string="Albarán",
        required=True,
    )

    def action_confirm(self):
        self.ensure_one()
        self.picking_id._generate_deca_document()
        return {'type': 'ir.actions.act_window_close'}
