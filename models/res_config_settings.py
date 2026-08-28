# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    has_account_advance_payments = fields.Boolean(string='Activar el flujo de pagos de anticipos contables',
                                                     related="company_id.has_account_advance_payments",
                                                     readonly=False, implied_group='1010_account_advance_payment.group_has_account_advance_payments')

    account_receivable_advance_id = fields.Many2one('account.account', company_dependent=True,
                                                     string="Cuenta por cobrar anticipo",
                                                     related="company_id.account_receivable_advance_id",
                                                     domain="[('account_type', '=', 'asset_receivable')]",
                                                    readonly=False)

    account_payable_advance_id = fields.Many2one('account.account', company_dependent=True,
                                                  string="Cuenta por pagar anticipo",
                                                 related="company_id.account_payable_advance_id",
                                                  domain="[('account_type', '=', 'liability_payable')]",
                                                 readonly=False)

    @api.onchange('has_account_advance_payments')
    def _onchange_has_account_advance_payments(self):
        if self.has_account_advance_payments:
            self.env['res.partner'].search(
                [('is_accounts_locked', '=', True)]).is_accounts_locked = False
        else:
            self.env['res.partner'].search(
                [('is_accounts_locked', '=', False)]).is_accounts_locked = True