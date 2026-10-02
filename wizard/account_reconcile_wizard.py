# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class AccountReconcileWizard(models.TransientModel):
    _inherit = 'account.reconcile.wizard'

    @api.depends('force_partials')
    def _compute_allow_partials(self):
        super()._compute_allow_partials()
        if 'allow_partials' in self._context:
            for wizard in self:
                wizard.allow_partials = self._context.get('allow_partials')



