# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class AccountPaymentInnerit(models.Model):
    _inherit = 'account.payment'

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if self._context.get('set_is_advance_payments'):
            res['is_advance_payments'] = self.env.company.has_accounting_advance_payments
        return res

    is_advance_payments = fields.Boolean(string='Es anticipo',default=False)
    change_nature_payment = fields.Boolean(string='Modificar naturaleza del pago',
                                           compute='_compute_change_nature_payment',
                                           store=True)

    @api.depends('state')
    def _compute_change_nature_payment(self):
        for move in self:
            move.change_nature_payment = bool(not move.env.user.has_group('1010_account_advance_payment.group_account_advance_payment_user') or move.state != 'draft')

