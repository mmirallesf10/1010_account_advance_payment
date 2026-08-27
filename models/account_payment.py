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

