from odoo.exceptions import ValidationError
from odoo import api, fields, models

class ContentReportVideo(models.Model):
    _name = 'content.report.video'
    _description = 'Laporan Video Sosial Media'

    report_id = fields.Many2one('admin.work.report', string="Laporan Mingguan")
    date = fields.Date(string="Tanggal", default=fields.Date.context_today)
    jam_fb = fields.Float(string="Jam Upload FB")
    fb_views = fields.Integer(string="FB Views")
    fb_likes = fields.Integer(string="FB Likes")

    jam_ig = fields.Float(string="Jam Upload IG")
    ig_views = fields.Integer(string="IG Views")
    ig_likes = fields.Integer(string="IG Likes")

    jam_tt = fields.Float(string="Jam Upload TT")
    tt_views = fields.Integer(string="TikTok Views")
    tt_likes = fields.Integer(string="TikTok Likes")

    jam_yt = fields.Float(string="Jam Upload YT")
    yt_views = fields.Integer(string="YouTube Views")
    yt_likes = fields.Integer(string="YouTube Likes")
    notes = fields.Text(string="Notes")


    @api.constrains('date', 'report_id')
    def _check_date_within_range(self):
        for rec in self:
            if rec.report_id and rec.date:
                if not (rec.report_id.date_from <= rec.date <= rec.report_id.date_to):
                    raise ValidationError("Tanggal Report Video Sosmed di luar range laporan mingguan!")

