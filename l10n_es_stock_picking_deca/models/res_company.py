# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    deca_enabled = fields.Boolean(
        string="DeCA activo",
        help="Activa la generación de Documentos de Control Administrativo "
             "(DeCA) para los albaranes de salida de esta empresa.",
    )
    deca_base_url = fields.Char(
        string="URL base documento DeCA",
        help="URL base pública utilizada para construir el enlace de "
             "consulta del documento DeCA. Ej: https://odoo.micliente.com",
    )
    deca_report_id = fields.Many2one(
        'ir.actions.report',
        string="Informe DeCA",
        domain=[('model', '=', 'stock.picking')],
        help="Informe de stock.picking que se utilizará para generar el "
             "documento DeCA.",
    )
