# © 2022 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class L10nEsAeatMod303Report(models.Model):
    _inherit = "l10n.es.aeat.mod303.report"

    def _get_move_line_domain(self, date_start, date_end, map_line):
        report = self.with_context(use_account_group_id=True)
        return super(L10nEsAeatMod303Report, report)._get_move_line_domain(
            date_start, date_end, map_line
        )
