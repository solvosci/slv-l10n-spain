# © 2022 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, fields, models
from odoo.exceptions import Warning as UserError


class L10nEsVatBook(models.Model):
    _inherit = "l10n.es.vat.book"

    # TODO código replaced total, a buscar solución que lo evite
    def _calculate_vat_book(self):
        """
        This function calculate all the taxes, from issued invoices,
        received invoices and rectification invoices
        """
        for rec in self:
            if not rec.company_id.partner_id.vat:
                raise UserError(_("This partner doesn't have VAT"))
            rec._clear_old_data()
            # Searches for all possible usable lines to report
            moves = rec._get_account_move_lines()
            for book_type in ["issued", "received"]:
                map_lines = self.env["aeat.vat.book.map.line"].search(
                    [("book_type", "=", book_type)]
                )
                taxes = self.env["account.tax"]
                accounts = {}
                for map_line in map_lines:
                    line_taxes = map_line.get_taxes(rec)
                    taxes |= line_taxes
                    if map_line.tax_account_id:
                        account = rec.get_account_from_template(map_line.tax_account_id)
                        accounts.update({tax: account for tax in line_taxes})
                # Filter in all possible data using sets for improving performance
                if accounts:
                    lines = moves.filtered(
                        lambda line: line.tax_ids & taxes
                        or (
                            line.tax_line_id in taxes
                            # ----------- CÓDIGO OCA ORIGINAL ----------- 
                            # and accounts.get(line.tax_line_id, line.account_id)
                            # == line.account_id
                            # --------- FIN CÓDIGO OCA ORIGINAL --------- 
                            # ----------- CÓDIGO SOLVOSCI --------------- 
                            and (
                                (
                                    # El apunte clava el mapeo por cuenta o no hay cuenta que clavar
                                    accounts.get(line.tax_line_id, line.account_id)
                                    == line.account_id

                                )
                                or
                                (
                                    # El apunte está en una cuenta del mismo grupo que la cuenta a clavar
                                    accounts.get(line.tax_line_id, False)
                                    and accounts[line.tax_line_id].group_id
                                    == line.account_id.group_id
                                )
                            )
                            # --------- FIN CÓDIGO SOLVOSCI -------------
                        )
                    )
                else:
                    lines = moves.filtered(
                        lambda line: (line.tax_ids | line.tax_line_id) & taxes
                    )
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
            rectification_received_tax_lines = (
                rec.rectification_received_line_ids.mapped("tax_line_ids")
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
