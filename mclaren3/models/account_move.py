from odoo import models,fields,api,_
#from datetime import timedelta, datetime
from odoo.exceptions import ValidationError, UserError, Warning
import datetime

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    prueba2 = fields.Boolean(string="Prueba")
