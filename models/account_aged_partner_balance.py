# -*- coding: utf-8 -*-

from odoo import api, models, fields, _
from odoo.tools import get_lang, SQL

class AgedPartnerBalanceCustomHandler(models.AbstractModel):
    _inherit = 'account.aged.partner.balance.report.handler'

    def _report_custom_engine_aged_receivable(self, expressions, options, date_scope, current_groupby, next_groupby, offset=0, limit=None, warnings=None):
        options['advance_payment'] = True
        return super()._report_custom_engine_aged_receivable(expressions, options, date_scope, current_groupby, next_groupby, offset=offset,limit=limit,warnings=warnings)

    def _report_custom_engine_aged_payable(self, expressions, options, date_scope, current_groupby, next_groupby, offset=0, limit=None, warnings=None):
        options['advance_payment'] = True
        return super()._report_custom_engine_aged_payable(expressions, options, date_scope, current_groupby, next_groupby, offset=offset,limit=limit,warnings=warnings)
    