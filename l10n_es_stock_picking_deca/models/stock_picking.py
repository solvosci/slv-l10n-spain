# -*- coding: utf-8 -*-
import base64
import logging

from odoo import _, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    deca_is_deca = fields.Boolean(
        string="Documento DeCA",
        copy=False,
        help="Indica que este albarán tiene generado un documento DeCA.",
    )
    # Campo de tipo URL (widget 'url' sobre Char; el ORM de Odoo no dispone
    # de un fieldtype nativo "Url").
    deca_url = fields.Char(
        string="URL DeCA",
        copy=False,
    )
    deca_attachment_id = fields.Many2one(
        'ir.attachment',
        string="PDF DeCA",
        copy=False,
    )
    deca_generation_date = fields.Datetime(
        string="Fecha generación DeCA",
        copy=False,
    )
    deca_generated_by_id = fields.Many2one(
        'res.users',
        string="Generado por",
        copy=False,
    )

    # Campo técnico auxiliar para condicionar la vista sin necesidad de
    # exponer directamente company_id.deca_enabled en los attrs.
    deca_company_enabled = fields.Boolean(
        related='company_id.deca_enabled',
        string="DeCA activo en empresa",
    )

    def action_generate_deca(self):
        """Botón 'Generar documento DeCA'.

        Si el documento ya existía, abre un asistente de confirmación antes
        de regenerarlo. Si no existía, lo genera directamente.
        """
        self.ensure_one()
        self._check_deca_can_generate()

        if self.deca_is_deca:
            return {
                'type': 'ir.actions.act_window',
                'name': _("Regenerar documento DeCA"),
                'res_model': 'stock.picking.deca.confirm.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {'default_picking_id': self.id},
            }

        self._generate_deca_document()
        return True

    def _check_deca_can_generate(self):
        self.ensure_one()
        if not self.company_id.deca_enabled:
            raise UserError(_(
                "La funcionalidad DeCA no está activada para la empresa %s."
            ) % self.company_id.display_name)
        if self.picking_type_code != 'outgoing':
            raise UserError(_(
                "El documento DeCA sólo se puede generar para albaranes de salida."
            ))
        if self.state != 'done':
            raise UserError(_(
                "El albarán debe estar en estado 'Hecho' para generar el documento DeCA."
            ))
        if not self.signature:
            raise UserError(_(
                "El albarán debe estar firmado antes de generar el documento "
                "DeCA. Por favor, firme el albarán primero."
            ))

    def _generate_deca_document(self):
        """Genera (o regenera) el PDF DeCA, lo adjunta al picking y calcula
        su URL pública. Sustituye el adjunto anterior si existía."""
        self.ensure_one()
        company = self.company_id
        report = company.deca_report_id

        if not report:
            raise UserError(_(
                "No hay ningún informe configurado como documento DeCA en "
                "la configuración de la empresa %s."
            ) % company.display_name)
        if not company.deca_base_url:
            raise UserError(_(
                "No hay ninguna URL base configurada para DeCA en la "
                "configuración de la empresa %s."
            ) % company.display_name)

        is_regeneration = bool(self.deca_is_deca)
        old_attachment = self.deca_attachment_id

        pdf_content, _report_type = self.env['ir.actions.report'].sudo()._render_qweb_pdf(
            report.id, self.ids
        )

        attachment = self.env['ir.attachment'].sudo().create({
            'name': "DeCA_%s.pdf" % (self.name or self.id),
            'type': 'binary',
            'datas': base64.b64encode(pdf_content),
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/pdf',
        })

        deca_url = "%s/l10n_es_stock_picking_deca/deca/%s" % (
            company.deca_base_url.rstrip('/'), self.id
        )

        self.write({
            'deca_is_deca': True,
            'deca_attachment_id': attachment.id,
            'deca_url': deca_url,
            'deca_generation_date': fields.Datetime.now(),
            'deca_generated_by_id': self.env.user.id,
        })

        # El attachment anterior deja de estar referenciado por el picking,
        # por lo que ya puede eliminarse sin activar la protección de
        # ir.attachment.unlink().
        if old_attachment:
            old_attachment.sudo().unlink()

        if is_regeneration:
            self.message_post(body=_(
                "Documento DeCA regenerado por %(user)s. Nueva URL: %(url)s"
            ) % {'user': self.env.user.name, 'url': deca_url})
        else:
            self.message_post(body=_(
                "Documento DeCA generado por %(user)s. URL: %(url)s"
            ) % {'user': self.env.user.name, 'url': deca_url})

        _logger.info("DeCA %s para picking %s (%s)",
                     "regenerado" if is_regeneration else "generado",
                     self.name, deca_url)
