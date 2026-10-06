# -*- coding: utf-8 -*-

from odoo import api, models, fields, _, osv
from odoo.tools import get_lang, SQL

class AccountReport(models.Model):
    _inherit = 'account.report'

    @api.model
    def _get_options_account_type_domain(self, options):
        domain = super()._get_options_account_type_domain(options)
        # For aged partner balance reports, the advance payment logic is now handled in the SQL query
        # So we skip this domain modification for those reports
        if options.get('advance_payment', False) and domain:
            # Check if this is an aged partner balance report
            report_name = self.browse(options.get('report_id')).name if options.get('report_id') else ''
            if 'aged' in report_name.lower():
                # Return the standard domain, filtering is done in the SQL query
                return domain

            # For other reports, keep the original logic
            advance_payment = []
            all_domains = []
            selected_domains = []
            if not options.get('account_type') or len(options.get('account_type')) == 0:
                return []
            for opt in options.get('account_type', []):
                if opt['id'] == 'trade_receivable':
                    advance_payment = [('account_id.non_trade', '=', False),
                                       '|','&',('account_id.account_type', '=', 'asset_receivable'),('account_id.is_advance_payment', '=', False),
                                       '&',('account_id.account_type', '=', 'liability_payable'),('account_id.is_advance_payment', '=', True)]
                elif opt['id'] == 'trade_payable':
                    advance_payment = [('account_id.non_trade', '=', False),
                                       '|' , '&',('account_id.account_type', '=', 'liability_payable'),('account_id.is_advance_payment', '=', False),
                                       '&',('account_id.account_type', '=', 'asset_receivable'),('account_id.is_advance_payment', '=', True)]
                elif opt['id'] == 'non_trade_receivable':
                    advance_payment = [('account_id.non_trade', '=', True),
                                       '|','&',('account_id.account_type', '=', 'asset_receivable'),('account_id.is_advance_payment', '=', False),
                                       '&',('account_id.account_type', '=', 'liability_payable'),('account_id.is_advance_payment', '=', True)]
                elif opt['id'] == 'non_trade_payable':
                    advance_payment = [('account_id.non_trade', '=', True),
                                       '|' , '&',('account_id.account_type', '=', 'liability_payable'),('account_id.is_advance_payment', '=', False),
                                       '&',('account_id.account_type', '=', 'asset_receivable'),('account_id.is_advance_payment', '=', True)]
                if opt['selected']:
                    selected_domains.append(advance_payment)
                all_domains.append(advance_payment)
            return osv.expression.OR(selected_domains or all_domains)
        return domain
    