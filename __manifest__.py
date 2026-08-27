# -*- coding: utf-8 -*-
{
    'name': '1010 Anticipos contables',
    'summary': 'Gestionar el flujo de registro de pagos por anticipo para separar las cuentas por cobrar/pagar de los pagos normales y los anticipos.',
    'version': '18.0.1.0.3',
    'category': 'Accounting/Localizations',
    'author': 'Css Consultores 1010',
    'website': 'https://www.cssconsultores.com',
    'license': 'LGPL-3',
    'depends': ['base', 'account','save_base'],
    'data': [
        'views/res_config_settings_views.xml',
        'views/account_payment_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
