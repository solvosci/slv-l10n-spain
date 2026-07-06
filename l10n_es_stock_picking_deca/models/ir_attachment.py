# -*- coding: utf-8 -*-
from odoo import _, models
from odoo.exceptions import UserError


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    def unlink(self):
        if self:
            linked_pickings = self.env['stock.picking'].sudo().search([
                ('deca_attachment_id', 'in', self.ids),
            ])
            if linked_pickings:
                raise UserError(_(
                    "No se puede eliminar este adjunto porque está asociado "
                    "como documento DeCA a el/los siguiente(s) albarán(es): %s"
                ) % ', '.join(linked_pickings.mapped('name')))
        return super().unlink()
