# © 2022 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class ResCompany(models.Model):
    _inherit = "res.company"

    def get_account_from_template(self, account_template):
        """
        Cuando es llamado desde el 303, se sutituye la búsqueda
        a partir de la plantilla de cuenta por el grupo de cuentas
        proporcionado
        """
        if "use_account_group_id" in self.env.context:
            account_group_id = self.env.context.get("use_account_group_id", False)
            accounts = self.env["account.account"].browse([])
            if account_group_id:
                accounts += accounts.search(
                    [("group_id", "=", account_group_id.id)]
                )
            return accounts
        else:
            return super().get_account_from_template(account_template)
