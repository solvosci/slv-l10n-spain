# © 2026 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import _, models
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _name = 'stock.picking'
    _inherit = ['stock.picking', 'deca.document.mixin']

    def _get_deca_url_path(self):
        self.ensure_one()
        return "l10n_es_stock_picking_deca/deca"

    def _get_deca_document_name(self):
        self.ensure_one()
        return "DeCA_%s.pdf" % (self.name or self.id)

    def _check_deca_can_generate_extra(self):
        self.ensure_one()
        if self.picking_type_code != 'outgoing':
            raise UserError(_(
                "The DeCA document can only be generated for outgoing delivery orders."
            ))
        if self.state != 'done':
            raise UserError(_(
                "The delivery order must be in the 'Done' state to generate the DeCA document."
            ))
        if not self.signature:
            raise UserError(_(
                "The delivery order must be signed before generating the DeCA "
                "document. Please sign the delivery order first."
            ))