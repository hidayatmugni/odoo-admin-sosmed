# -*- coding: utf-8 -*-
# from odoo.exceptions import ValidationError
from odoo.exceptions import ValidationError
from odoo import api, fields, models


class ProductKnowledge(models.Model):
    _name = 'product.knowledge'
    _description = 'Product Knowledge'

    report_id = fields.Many2one('admin.work.report', string="Laporan Mingguan")
    date = fields.Date(string="Date", default=fields.Date.context_today, store=True, required=True)
    product_name = fields.Char(string="Nama Product")
    notes = fields.Text(string='Notes')


    @api.constrains('date', 'report_id')
    def _check_date_within_range(self):
        for rec in self:
            if rec.report_id and rec.date:
                if not (rec.report_id.date_from <= rec.date <= rec.report_id.date_to):
                    raise ValidationError("Tanggal Studied Product di luar range laporan mingguan!")



    
