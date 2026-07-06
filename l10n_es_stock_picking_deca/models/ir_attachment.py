# -*- coding: utf-8 -*-
from odoo import _, api, models
from odoo.exceptions import UserError


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    @api.ondelete(at_uninstall=False)
    def _unlink_except_deca_document(self):
        linked_pickings = self.env['stock.picking'].sudo().search([
            ('deca_attachment_id', 'in', self.ids),
        ])
        if linked_pickings:
            raise UserError(_(
                "This attachment cannot be deleted because it is linked as "
                "the DeCA document of the following delivery order(s): %s"
            ) % ', '.join(linked_pickings.mapped('name')))
