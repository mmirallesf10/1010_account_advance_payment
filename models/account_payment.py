# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class AccountPaymentInnerit(models.Model):
    _inherit = 'account.payment'

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if self._context.get('set_is_advance_payments'):
            res['is_advance_payments'] = self.env.company.has_account_advance_payments
        return res

    is_advance_payments = fields.Boolean(string='Es anticipo',default=False)
    change_nature_payment = fields.Boolean(string='Modificar naturaleza del pago',
                                           compute='_compute_change_nature_payment',
                                           store=True)
    destination_account_advance_id = fields.Many2one(
        comodel_name='account.account',
        string='Destination Account Advance',
        store=True, readonly=False,
        compute='_compute_destination_account_advance_id',
        domain="[('account_type', 'in', ('asset_receivable', 'liability_payable'))]",
        check_company=True)

    @api.depends('state')
    def _compute_change_nature_payment(self):
        for move in self:
            move.change_nature_payment = bool(not move.env.user.has_group(
                '1010_account_advance_payment.group_account_advance_payment_user') or move.state != 'draft' or not move.env.company.has_account_advance_payments)

    def _prepare_move_line_default_vals(self, write_off_line_vals=None, force_balance=None):
        """ Change account to advance account """
        res = super()._prepare_move_line_default_vals(write_off_line_vals=write_off_line_vals, force_balance=force_balance)
        if self.is_advance_payments and self.destination_account_advance_id:
            receivable_payable_line = res[1]
            receivable_payable_line['account_id'] = self.destination_account_advance_id.id
        return res

    @api.model
    def _get_trigger_fields_to_synchronize(self):
        res = super()._get_trigger_fields_to_synchronize()
        new_value = ('is_advance_payments',)
        res += new_value
        return res

    @api.depends('partner_id', 'partner_type')
    def _compute_destination_account_advance_id(self):
        self.destination_account_advance_id = False
        for pay in self:
            if pay.partner_type == 'customer':
                # Receive money from invoice or send money to refund it.
                if pay.partner_id and pay.partner_id.with_company(
                        pay.company_id).account_receivable_advance_id:
                    pay.destination_account_advance_id = pay.partner_id.with_company(
                        pay.company_id).account_receivable_advance_id
                elif self.env.company.account_receivable_advance_id:
                    pay.destination_account_advance_id = self.env.company.account_receivable_advance_id
                else:
                    pay.destination_account_advance_id = self.env['account.account'].with_company(pay.company_id).search([
                        *self.env['account.account']._check_company_domain(pay.company_id),
                        ('account_type', '=', 'asset_receivable'),
                        ('deprecated', '=', False),
                    ], limit=1)
            elif pay.partner_type == 'supplier':
                # Send money to pay a bill or receive money to refund it.
                if pay.partner_id and pay.partner_id.with_company(pay.company_id).account_payable_advance_id:
                    pay.destination_account_advance_id = pay.partner_id.with_company(pay.company_id).account_payable_advance_id
                elif self.env.company.account_payable_advance_id:
                    pay.destination_account_advance_id = self.env.company.account_payable_advance_id
                else:
                    pay.destination_account_advance_id = self.env['account.account'].with_company(pay.company_id).search([
                        *self.env['account.account']._check_company_domain(pay.company_id),
                        ('account_type', '=', 'liability_payable'),
                        ('deprecated', '=', False),
                    ], limit=1)


