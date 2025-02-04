
from odoo import api, fields, models, _


class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _description="Doctor Records"
    _inherit="mail.thread"


    name=fields.Char(String='Name',required=True, tracking=True)
    gender=fields.Selection([('male','Male'),('female','Female')],String='Gender',tracking=True)
    ref=fields.Char(String='Reference',required=True)
    active=fields.Boolean(default=True)

    def name_get(self):
        res=[]
        for rec in self:
            res.append((rec.id, f'{rec.ref} - {rec.name}'))
        return res
