# © 2022 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, fields, models
from odoo.exceptions import Warning as UserError


class L10nEsVatBook(models.Model):
    _inherit = "l10n.es.vat.book"

    def _get_account_move_lines(self, map_line, taxes, account=None):
        return self.env["account.move.line"].search(
            self._account_move_line_domain(map_line, taxes, account=account)
        )

    def _account_move_line_domain(self, map_line, taxes, account=None):
        # Para anticipar que esto sea un addon que herede sin sobrescrituras
        #  de código, emulamos llamada a código original
        # domain = super()._account_move_line_domain(taxes, map_line, account=None)
        domain = self._account_move_line_domain_original(taxes, account=None)

        if map_line.account_group_id:
            # A partir de este punto, se espera que el último elemento del
            #  dominio sea el filtro por impuestos, sin cuenta, al haberla
            #  forzado a None, pasamos a filtrarlo por el grupo también
            tax_line_id_dom = domain.pop()
            domain += [
                "&",
                tax_line_id_dom,
                ("account_id.group_id", "=", map_line.account_group_id.id),
            ]

        return domain

    def _account_move_line_domain_original(self, taxes, account=None):
        # CÓDIGO ORIGINAL (https://github.com/OCA/l10n-spain/commit/4c6a2b6c9b9cfdda6937b973e266792e25d9c1dc)
        # ...
        # search move lines that contain these tax codes
        domain = [
            ("date", ">=", self.date_start),
            ("date", "<=", self.date_end),
            ("parent_state", "=", "posted"),
            "|",
            ("tax_ids", "in", taxes.ids),
        ]
        if account:
            domain += [
                "&",
                ("tax_line_id", "in", taxes.ids),
                ("account_id", "=", account.id),
            ]
        else:
            domain.append(("tax_line_id", "in", taxes.ids))
        return domain
        # ...

    def _calculate_vat_book(self):
        # CÓDIGO MODIFICADO A PARTIR DEL PRESENTE EN
        # https://github.com/OCA/l10n-spain/commit/4c6a2b6c9b9cfdda6937b973e266792e25d9c1dc
        """
            This function calculate all the taxes, from issued invoices,
            received invoices and rectification invoices
        """
        for rec in self:
            if not rec.company_id.partner_id.vat:
                raise UserError(_("This company doesn't have VAT"))
            rec._clear_old_data()
            map_lines = self.env["aeat.vat.book.map.line"].search([])
            for map_line in map_lines:
                taxes = map_line.get_taxes(rec)
                account = rec.get_account_from_template(map_line.tax_account_id)
                # inicio CÓDIGO MODIFICADO, PENDIENTE DE PR A OCA
                # lines = rec._get_account_move_lines(taxes, account=account)
                lines = rec._get_account_move_lines(map_line, taxes, account=account)
                # fin CÓDIGO MODIFICADO, PENDIENTE DE PR A OCA
                rec.create_vat_book_lines(lines, map_line.book_type, taxes)
            # Issued
            book_type = "issued"
            issued_tax_lines = rec.issued_line_ids.mapped("tax_line_ids")
            rectification_issued_tax_lines = rec.rectification_issued_line_ids.mapped(
                "tax_line_ids"
            )
            tax_summary_data_recs = rec._prepare_vat_book_tax_summary(
                issued_tax_lines + rectification_issued_tax_lines, book_type
            )
            rec._create_vat_book_tax_summary(tax_summary_data_recs)
            rec._create_vat_book_summary(rec.issued_tax_summary_ids, book_type)

            # Received
            book_type = "received"
            received_tax_lines = rec.received_line_ids.mapped("tax_line_ids")
            # flake8: noqa
            rectification_received_tax_lines = rec.rectification_received_line_ids.mapped(
                "tax_line_ids"
            )
            tax_summary_data_recs = rec._prepare_vat_book_tax_summary(
                received_tax_lines + rectification_received_tax_lines, book_type
            )
            rec._create_vat_book_tax_summary(tax_summary_data_recs)
            rec._create_vat_book_summary(rec.received_tax_summary_ids, book_type)

            # If we require to auto-renumber invoices received
            if rec.auto_renumber:
                rec_invs = self.env["l10n.es.vat.book.line"].search(
                    [("vat_book_id", "=", rec.id), ("line_type", "=", "received")],
                    order="invoice_date asc, ref asc",
                )
                i = 1
                for rec_inv in rec_invs:
                    rec_inv.entry_number = i
                    i += 1
                rec_invs = self.env["l10n.es.vat.book.line"].search(
                    [
                        ("vat_book_id", "=", rec.id),
                        ("line_type", "=", "rectification_received"),
                    ],
                    order="invoice_date asc, ref asc",
                )
                i = 1
                for rec_inv in rec_invs:
                    rec_inv.entry_number = i
                    i += 1
                # Write state and date in the report
            rec.write(
                {"state": "calculated", "calculation_date": fields.Datetime.now()}
            )
