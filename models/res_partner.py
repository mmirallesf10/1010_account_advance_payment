# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    account_receivable_advance_id = fields.Many2one('account.account', company_dependent=True,
                                                    string="Cuenta por cobrar anticipo",
                                                    domain="[('account_type', '=', 'liability_payable')]")

    account_payable_advance_id = fields.Many2one('account.account', company_dependent=True,
                                                 string="Cuenta por pagar anticipo",
                                                 domain="[('account_type', '=', 'asset_receivable')]")

    is_accounts_locked = fields.Boolean('Cuentas bloqueadas', copy=False, default=False)