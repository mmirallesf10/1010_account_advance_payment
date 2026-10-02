# -*- coding: utf-8 -*-

from odoo import api, models, fields, _, osv
from odoo.tools import get_lang, SQL

class AccountAccount(models.Model):
    _inherit = "account.account"

    is_advance_payment = fields.Boolean(default=False,string="Es cuenta para anticipo?")
    