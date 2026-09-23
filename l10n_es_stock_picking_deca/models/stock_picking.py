# © 2026 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import _, models
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _name = 'stock.picking'
    _inherit = ['stock.picking', 'deca.document.mixin']

    def _get_deca_url_path(self):
        self.ensure_one()
        return "deca/pick"

    def _get_deca_document_name(self):
        self.ensure_one()
        return "DeCA_%s.pdf" % (self.name or self.id)

    def _check_deca_can_generate_extra(self):
        not_outgoings = self.filtered(lambda x: x.picking_type_code != "outgoing")
        if not_outgoings:
            raise UserError(_(
                "The DeCA document can only be generated for outgoing delivery orders.\n\n"
                "Incorrect transfers selected: %s"
            ) % ", ".join(not_outgoings.mapped("name")))
        not_done = self.filtered(lambda x: x.state != "done")
        if not_done:
            raise UserError(_(
                "Delivery orders must be in the 'Done' state to generate the DeCA document.\n\n"
                "Incorrect transfers selected: %s"
            ) % ", ".join(not_done.mapped("name")))
        not_signed = self.filtered(lambda x: not x.picking_signature)
        if not_signed:
            raise UserError(_(
                "Delivery order must be signed before generating the DeCA "
                "document. Please sign the delivery order first.\n\n"
                "Incorrect transfers selected: %s"
            ) % ", ".join(not_signed.mapped("name")))
