from odoo.exceptions import ValidationError
from odoo import api, models, fields


class ContentReportStreamShopee(models.Model):
    _name = 'content.report.stream.shopee'
    _description = 'Report Live Streaming Shopee'

    date = fields.Date(string="Tanggal", default=fields.Date.context_today, required=True)
    jam = fields.Float(string="Jam Mulai Streaming (WIB)", required=True)
    views = fields.Integer(string="Viewers")
    likes = fields.Integer(string="Likes")
    durasi = fields.Float(string="Durasi (Menit)")
    comment = fields.Integer(string="Komentar")
    follow = fields.Integer(string="Follow")
    pembelian = fields.Integer(string="Pembelian")
    keranjang = fields.Integer(string="Keranjang")
    notes = fields.Text(string="Catatan")
    report_id = fields.Many2one('admin.work.report', string="Laporan Mingguan")


    @api.constrains('date', 'report_id')
    def _check_date_within_range(self):
        for rec in self:
            if rec.report_id and rec.date:
                if not (rec.report_id.date_from <= rec.date <= rec.report_id.date_to):
                    raise ValidationError("Tanggal Shopee Stream di luar range laporan mingguan!")

