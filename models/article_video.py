from odoo.exceptions import ValidationError
from odoo import api, fields, models


class ArticleVideoReport(models.Model):
    _name = 'article.video.report'
    _description = 'Article & Video Report'

    report_id = fields.Many2one('admin.work.report', string='Laporan Mingguan', ondelete='cascade')

    date = fields.Date(string='Tanggal', default=fields.Date.context_today)

    # Artikel
    article_title = fields.Char(string='Judul Artikel')
    article_content = fields.Char(string='Konten Artikel')
    article_action = fields.Char(string='Aksi Artikel')

    # Video
    video_type = fields.Char(string='Tipe Video') 
    video_title = fields.Char(string='Judul Video')
    video_content = fields.Char(string='Konten Video')
    video_action = fields.Char(string='Aksi Video')

    # Checklist dan catatan
    notes = fields.Text(string='Catatan')

    @api.constrains('date', 'report_id')
    def _check_date_within_range(self):
        for rec in self:
            if rec.report_id and rec.date:
                if not (rec.report_id.date_from <= rec.date <= rec.report_id.date_to):
                    raise ValidationError("Tanggal Report Article & Video di luar range laporan mingguan!")
