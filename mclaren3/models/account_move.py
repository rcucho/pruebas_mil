from odoo import models,fields,api,_
#from datetime import timedelta, datetime
from odoo.exceptions import ValidationError, UserError, Warning
import datetime

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    jasatec_os = fields.Char(string='O/S')
    jasatec_constancia = fields.Char(string='Constancia')
    jasatec_fecha = fields.Date(string='Fecha calculada') #, compute='_compute_fecha')
    
    def _post(self, soft=True):
        for record in self:
            if record.journal_id.type in ['bank','cash']:
                record.name = 'AA'+ record.name

        res =  super()._post(soft = soft)
        return res

    
    
    @api.depends('jasatec_fecha')
    def _onchange_fecha(self):
        for record in self:
            jasatec_fecha = record.invoice_date + datetime.timedelta(days=28)
    
class Crmga(models.Model):
    _inherit = 'crm.lead'
    
    mclaren = fields.Boolean(compute='_compute_mclaren_crm', store=True)
    currency_partner = fields.Many2one(comodel_name='res.currency', string='Moneda', compute='_compute_currency_partner', inverse='_inverse_currency_partner', store=True, readonly=False)
    
    def _inverse_currency_partner(self) :
        pass

    @api.depends('partner_id')
    def _compute_currency_partner(self) :
        for record in self :
            record.currency_partner = record.partner_id.property_product_pricelist.currency_id
    
    def _compute_mclaren_crm(self):
        for record in self:
            record.mclaren = True
    
    @api.depends(lambda self: ['tag_ids', 'stage_id', 'team_id'] + self._pls_get_safe_fields())       
    def _compute_probabilities(self):
        super()._compute_probabilities()
        self.mclaren = True
        if self.mclaren == True:
            for record in self:
                record.probability = record.probability * 0
                #if record.partner_id:
                if record.stage_id.name == 'Calificado':
                    record.probability = 25
                    #if record.quotation_count:
                if record.stage_id.name == 'Propuesta':
                    record.probability = 75
                if record.stage_id.is_won == True:
                    record.probability = 100         
                if record.lost_reason:
                    record.probability = record.probability * 0
        return

 
class Partner23(models.Model):
    _inherit = 'res.partner'
    
    partner_masivo = fields.Boolean(string='Subida masiva', store = True, readonly=True)
    
    @api.model
    def create(self, values):
        res= super().create(values)
        if self.env.context.get('import_file'):
        #raise UserError(str(self._context))
            res.partner_masivo = True   
        return res

 
class FleetRic(models.Model):
    _inherit = 'fleet.vehicle'
    fecha_ini = fields.Date(string="Impuesto Vehicular - Cronograma")
    fecha_fin = fields.Date(string="Impuesto Vehicular - Vencimiento",compute='_compute_fecha_fin')
    
    @api.depends('fecha_ini')
    def _compute_fecha_fin(self):
        for record in self:
            record.fecha_fin = record.fecha_ini + datetime.timedelta(days=1095)
    
