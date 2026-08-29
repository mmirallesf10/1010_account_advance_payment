# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.osv import expression

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def action_account_advance_payment_reconcile(self):
        wizard = self.env['account.reconcile.wizard'].with_context(
            active_model='account.move.line',
            active_ids=self.ids,
            allow_partials=True,
        ).new({})
        return wizard.reconcile()

