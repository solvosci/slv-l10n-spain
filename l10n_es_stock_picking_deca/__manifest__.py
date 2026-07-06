# -*- coding: utf-8 -*-
{
    'name': "España - DeCA en albaranes de salida",
    'version': '17.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Documento electrónico de Control Administrativo (DeCA) sobre albaranes de salida',
    'description': """
Documento electrónico de Control Administrativo (DeCA)
========================================================

Añade la funcionalidad necesaria para poder marcar un albarán de salida
(stock.picking) como Documento de Control Administrativo (DeCA):

* Configuración por empresa: activación de DeCA, URL base pública e informe
  de stock.picking a utilizar como documento DeCA.
* Botón en el albarán para generar / regenerar el documento DeCA (PDF
  adjunto + URL pública).
* Controlador público (sin autenticación) para consultar el PDF DeCA a
  partir de la URL generada.
* Protección del adjunto asociado frente a borrado.
* Código QR en el informe de albarán configurado como DeCA, apuntando a la
  URL pública del documento.
""",
    'author': 'Custom',
    'license': 'AGPL-3',
    'depends': ['stock'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/stock_picking_deca_confirm_views.xml',
        'views/res_config_settings_views.xml',
        'views/stock_picking_views.xml',
        'report/stock_picking_report_templates.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
