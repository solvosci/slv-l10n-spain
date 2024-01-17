# Copyright 2022 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "AEAT modelo 303 - Filtrado de mapeos por grupos de cuentas",
    "summary": """
        Altera el comportamiento por defecto de la generación del modelo 303
        para redefinir el filtro por cuenta y usar en su lugar el grupo de la cuenta
    """,
    "version": "15.0.1.0.0",
    "category": "Accounting & Finance",
    "website": "https://github.com/OCA/l10n-spain",
    "author": "Solvos",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["l10n_es_aeat_mod303"],
}
