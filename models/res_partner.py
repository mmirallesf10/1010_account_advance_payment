# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

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