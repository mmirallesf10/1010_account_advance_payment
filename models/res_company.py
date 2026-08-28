from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    has_account_advance_payments = fields.Boolean(string='Activar el flujo de pagos de anticipos contables')

    account_receivable_advance_id = fields.Many2one('account.account', company_dependent=True,
                                                     string="Cuenta por cobrar anticipo",
                                                     domain="[('account_type', '=', 'asset_receivable')]")

    account_payable_advance_id = fields.Many2one('account.account', company_dependent=True,
                                                  string="Cuenta por pagar anticipo",
                                                  domain="[('account_type', '=', 'liability_payable')]")