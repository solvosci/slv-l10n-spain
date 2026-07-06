# © 2026 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import base64

from odoo import http
from odoo.http import request
from werkzeug.exceptions import Forbidden


class StockPickingDecaController(http.Controller):

    @http.route(
        '/deca/pick/<string:hash_code>',
        type='http',
        auth='public',
        methods=['GET'],
        csrf=False,
    )
    def get_deca_document_pick(self, hash_code, **kwargs):
        # A generic method is defined in order to support other formats
        # (like eCMR) or even models
        return self.get_deca_document(hash_code, **kwargs)

    def get_deca_document(
        self, 
        hash_code,
        model="stock.picking",
        attach_field="deca_attachment_id",
        default_filename="DeCA.pdf",
        **kwargs
    ):                
        doc = request.env[model].sudo().search([("deca_hash", "=", hash_code)])

        if not doc.exists() or not doc.deca_is_generated or not doc[attach_field]:
            raise Forbidden()

        attachment = doc[attach_field]
        pdf_content = base64.b64decode(attachment.datas or b'')

        if not pdf_content:
            raise Forbidden()

        headers = [
            ('Content-Type', 'application/pdf'),
            ('Content-Disposition', 'inline; filename="%s"' % (attachment.name or default_filename)),
            ('Content-Length', len(pdf_content)),
        ]
        return request.make_response(pdf_content, headers=headers)
