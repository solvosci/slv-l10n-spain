# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    deca_enabled = fields.Boolean(
        string="Enable DeCA",
        help="Enables the generation of Administrative Control Documents "
             "(DeCA) for the outgoing delivery orders of this company.",
    )
    deca_base_url = fields.Char(
        string="DeCA document base URL",
        help="Public base URL used to build the DeCA document link. "
             "E.g. https://odoo.mycustomer.com",
    )
    deca_report_id = fields.Many2one(
        'ir.actions.report',
        string="DeCA report",
        domain=[('model', '=', 'stock.picking')],
        help="stock.picking report used to generate the DeCA document.",
    )
