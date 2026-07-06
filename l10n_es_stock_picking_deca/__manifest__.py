# -*- coding: utf-8 -*-
{
    'name': "Spain - DeCA on Outgoing Delivery Orders",
    'version': '17.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Administrative Control Document (DeCA) on outgoing delivery orders',
    'description': """
Administrative Control Document (DeCA)
=======================================

Adds the functionality needed to mark an outgoing delivery order
(stock.picking) as an Administrative Control Document (DeCA):

* Company configuration: enable DeCA, public base URL and stock.picking
  report to be used as the DeCA document.
* Button on the delivery order to generate / regenerate the DeCA document
  (attached PDF + public URL).
* Public controller (no authentication required) to retrieve the DeCA PDF
  from the generated URL.
* Protection of the linked attachment against deletion.
* QR code on the delivery order report configured as the DeCA report,
  pointing to the document's public URL.
""",
    'author': 'Custom',
    'license': 'AGPL-3',
    'depends': ['stock'],
    'external_dependencies': {
        'python': ['qrcode'],
    },
    'data': [
        # 'security/ir.model.access.csv',
        # 'wizard/stock_picking_deca_confirm_views.xml',
        'views/res_config_settings_views.xml',
        'views/stock_picking_views.xml',
        'report/stock_picking_report_templates.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
