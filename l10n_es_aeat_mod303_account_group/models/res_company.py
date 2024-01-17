# © 2022 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class ResCompany(models.Model):
    _inherit = "res.company"

    def get_account_from_template(self, account_template):
        """
        Cuando es llamado desde el 303, se sutituye la búsqueda
        a partir de la plantilla de cuenta por el grupo de cuentas
        que se deduce de dicha plantilla a través de la cuenta original
        """
        account = super().get_account_from_template(account_template)
        if account and self.env.context.get("use_account_group_id", False):
            return self.env["account.account"].search(
                [("group_id", "=", account.group_id.id)]
            )
        else:
            return account
