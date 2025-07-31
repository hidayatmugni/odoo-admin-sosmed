from odoo import api, models, fields
from datetime import timedelta

class PlanReport(models.Model):
    _name = 'plan.report'
    _description = 'Weekly Work Plan'

    report_id = fields.Many2one('admin.work.report', string='Weekly Report')
    date = fields.Date(required=True,string=' ')
    day_name = fields.Selection([
        ('mon', 'Senin'),
        ('tue', 'Selasa'),
        ('wed', 'Rabu'),
        ('thu', 'Kamis'),
        ('fri', 'Jumat'),
        ('sat', 'Sabtu')
        ],string=' ')
    
    task = fields.Char(string='Task')
    duration = fields.Integer(string='Duration (Menit)')
    notes = fields.Text(string='Notes')

    
    @api.onchange('report_id')
    def _onchange_set_day_name(self):
        if self.env.context.get('default_day_name'):
            self.day_name = self.env.context['default_day_name']
    
    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if self.env.context.get('default_day_name'):
            res['day_name'] = self.env.context['default_day_name']
        return res
    
    @api.onchange('day_name', 'report_id')
    def _onchange_set_date(self):
        """Atur tanggal otomatis berdasarkan hari dan laporan"""
        if self.day_name and self.report_id and self.report_id.date_from:
            day_map = {
                'mon': 0, 'tue': 1, 'wed': 2,
                'thu': 3, 'fri': 4, 'sat': 5
            }
            offset = day_map.get(self.day_name, 0)
            self.date = self.report_id.date_from + timedelta(days=offset)
