# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.osv import expression

class AccountMove(models.Model):
    _inherit = 'account.move'

    def _get_payments_widget_domain(self):
        self.ensure_one()
        res_domain = super()._get_payments_widget_domain()
        advance_payments = self.env['account.payment'].search(
            [('is_advance_payments', '=', True), ('partner_id', '=', self.partner_id.id),('state','=','paid')])
        pay_term_lines = advance_payments.move_id.line_ids \
            .filtered(lambda line: line.account_id.account_type in (
        'asset_receivable', 'liability_payable') and not line.reconciled and (
                                               line.amount_residual != 0.00 or line.amount_residual_currency != 0.00))


        if pay_term_lines:
            new_filter = ['|',('account_id', 'in', pay_term_lines.account_id.ids),]
            new_filter.extend(res_domain)
            res_domain = new_filter
        return res_domain

