# © 2022 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_sii_exempt_cause(self, applied_taxes):
        """
        El estándar indica que, en caso de que la posición fiscal sea de tipo
        "exportaciones" (gen_type=3), se debe forzar la exención fiscal "E2".
        Con este ajuste se atiende a la indicada por parametrización en la
        posición fiscal (de haberla).
        Se podría revisar también en el producto, pero se obvia por falta de
        necesidad del cliente
        """
        exempt_cause = super()._get_sii_exempt_cause(applied_taxes)
        gen_type = self._get_sii_gen_type()
        if gen_type == 3:
            if (
                self.fiscal_position_id.sii_exempt_cause
                and self.fiscal_position_id.sii_exempt_cause != "none"
            ):
                exempt_cause = self.fiscal_position_id.sii_exempt_cause
        return exempt_cause
