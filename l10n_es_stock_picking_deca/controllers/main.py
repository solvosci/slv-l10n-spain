# -*- coding: utf-8 -*-
import base64

from odoo import http
from odoo.http import request
from werkzeug.exceptions import Forbidden


class StockPickingDecaController(http.Controller):

    @http.route(
        '/l10n_es_stock_picking_deca/deca/<int:picking_id>',
        type='http',
        auth='public',
        website=False,
        csrf=False,
    )
    def deca_document(self, picking_id, **kwargs):
        picking = request.env['stock.picking'].sudo().browse(picking_id)

        if not picking.exists() or not picking.deca_is_deca or not picking.deca_attachment_id:
            raise Forbidden()

        attachment = picking.deca_attachment_id
        pdf_content = base64.b64decode(attachment.datas or b'')

        if not pdf_content:
            raise Forbidden()

        headers = [
            ('Content-Type', 'application/pdf'),
            ('Content-Disposition', 'inline; filename="%s"' % (attachment.name or 'DeCA.pdf')),
            ('Content-Length', len(pdf_content)),
        ]
        return request.make_response(pdf_content, headers=headers)
