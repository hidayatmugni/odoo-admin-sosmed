from odoo.exceptions import ValidationError
from datetime import timedelta
from datetime import date
from odoo import api, fields, models
import logging


_logger = logging.getLogger(__name__)


class AdminWorkReport(models.Model):
    _name = 'admin.work.report'
    _description = 'Laporan Mingguan Karyawan'

    name = fields.Char(string="Nama Laporan", compute="_compute_name", store=True, readonly=True)
    week = fields.Integer(string="Minggu Ke",compute="_compute_week", store=True, readonly=True)

# ==============================Comments per tab==================================
    plan_comment = fields.Text(string="Comment Plan")
    report_views_comment = fields.Text(string="Comment Report Views (Stream + Video)")
    article_comment = fields.Text(string="Comment Artikel & Video")
    product_comment = fields.Text(string="Comment Studied Product")

    
    # ===========hitung total jam plan perhari=======================
    total_duration_monday = fields.Float(string="Total Durasi Senin (menit)", compute="_compute_total_durations", store=True)
    total_duration_tuesday = fields.Float(string="Total Durasi Selasa (menit)", compute="_compute_total_durations", store=True)
    total_duration_wednesday = fields.Float(string="Total Durasi Rabu (menit)", compute="_compute_total_durations", store=True)
    total_duration_thursday = fields.Float(string="Total Durasi Kamis (menit)", compute="_compute_total_durations", store=True)
    total_duration_friday = fields.Float(string="Total Durasi Jumat (menit)", compute="_compute_total_durations", store=True)
    total_duration_saturday = fields.Float(string="Total Durasi Sabtu (menit)", compute="_compute_total_durations", store=True)


      # Name otomastis
    @api.depends('week')
    def _compute_name(self):
        for rec in self:
            if rec.week:
                rec.name = f"Week {rec.week}"
            else:
                rec.name = "Week -"


    date_from = fields.Date(string="Tanggal Mulai", required=True)
    date_to = fields.Date(string="Tanggal Selesai", compute='_compute_date_to', store=True)

    # Chek Hari senin
    @api.constrains('date_from')
    def _check_date_from_monday(self):
        for rec in self:
            if rec.date_from and rec.date_from.weekday() != 0:
                raise ValidationError("Tanggal Mulai (date_from) harus hari Senin.")
            
    @api.model
    def default_get(self, fields):
        res = super(AdminWorkReport, self).default_get(fields)
        today = date.today()
        # Geser ke Senin minggu ini
        monday = today - timedelta(days=today.weekday())
        res['date_from'] = monday
        return res

            
    # defaul week 1 start senin
    @api.depends('date_from')
    def _compute_week(self):
        for rec in self:
            if rec.date_from:
                rec.week = rec.date_from.isocalendar().week
            else:
                rec.week = 0

    # date to otomastis 6 hari
    @api.depends('date_from')
    def _compute_date_to(self):
        for rec in self:
            if rec.date_from:
                rec.date_to = rec.date_from + timedelta(days=6)
            else:
                rec.date_to = False
    
     # validasi eror di luar 6 hari
    @api.constrains('date_from')
    def _check_date_from_overlap(self):
        for rec in self:
            if not rec.date_from:
                continue
            date_to = rec.date_to or (rec.date_from + timedelta(days=6))
            overlapping = self.search([
                ('id', '!=', rec.id),
                ('date_from', '<=', date_to),
                ('date_to', '>=', rec.date_from)
            ])
            if overlapping:
                raise ValidationError("Tanggal laporan ini sudah digunakn dilaporan mingguan lain. Harap pilih tanggal lain.")
            

    user_id = fields.Many2one('res.users', 
                            string="User",
                            default=lambda self: self.env.user,
                            readonly=True,
                            required=True)
    comment = fields.Text(string='Notes')

# ========================= relational ===================================================================
    shopee_stream_ids = fields.One2many('content.report.stream.shopee', 'report_id', string="Streaming Shopee")
    tiktok_stream_ids = fields.One2many('content.report.stream.tiktok', 'report_id', string="Streaming TikTok")
    video_ids = fields.One2many('content.report.video', 'report_id', string="Video Sosmed")
    study_ids = fields.One2many('product.knowledge', 'report_id', string="Studi Produk")
    article_video_ids = fields.One2many('article.video.report', 'report_id', string="Article & Video")

#============================ hitung report viewss ====================================================
    # ==== Shopee ====
    total_views = fields.Integer(string="Total Views", compute="_compute_stream_totals", store=True)
    total_likes = fields.Integer(string="Total Likes", compute="_compute_stream_totals", store=True)
    total_comments = fields.Integer(string="Total Comments", compute="_compute_stream_totals", store=True)
    total_follow = fields.Integer(string="Total Follow", compute="_compute_stream_totals", store=True)
    total_keranjang = fields.Integer(string="Total Keranjang", compute="_compute_stream_totals", store=True)
    total_pembelian = fields.Integer(string="Total Pembelian", compute="_compute_stream_totals", store=True)
    # ==== Compute report shopee =====
    @api.depends('shopee_stream_ids.views', 'shopee_stream_ids.likes', 'shopee_stream_ids.comment',
                 'shopee_stream_ids.follow', 'shopee_stream_ids.keranjang', 'shopee_stream_ids.pembelian')
    def _compute_stream_totals(self):
        for rec in self:
            rec.total_views = sum(rec.shopee_stream_ids.mapped('views'))
            rec.total_likes = sum(rec.shopee_stream_ids.mapped('likes'))
            rec.total_comments = sum(rec.shopee_stream_ids.mapped('comment'))
            rec.total_follow = sum(rec.shopee_stream_ids.mapped('follow'))
            rec.total_keranjang = sum(rec.shopee_stream_ids.mapped('keranjang'))
            rec.total_pembelian = sum(rec.shopee_stream_ids.mapped('pembelian'))


    # ==== Tiktok ====
    total_views_tiktok = fields.Integer(string="Total Views TikTok", compute="_compute_stream_totals_tiktok", store=True)
    total_likes_tiktok = fields.Integer(string="Total Likes TikTok", compute="_compute_stream_totals_tiktok", store=True)
    total_comments_tiktok  = fields.Integer(string="Total Comments", compute="_compute_stream_totals_tiktok", store=True)
    total_follow_tiktok  = fields.Integer(string="Total Follow", compute="_compute_stream_totals_tiktok", store=True)
    total_keranjang_tiktok  = fields.Integer(string="Total Keranjang", compute="_compute_stream_totals_tiktok", store=True)
    total_pembelian_tiktok  = fields.Integer(string="Total Pembelian", compute="_compute_stream_totals_tiktok", store=True)
    # ==== Compute report Tiktok =====
    @api.depends('tiktok_stream_ids.views', 'tiktok_stream_ids.likes',  'tiktok_stream_ids.comment',
                 'tiktok_stream_ids.follow', 'tiktok_stream_ids.keranjang','tiktok_stream_ids.pembelian',)
    def _compute_stream_totals_tiktok(self):
        for rec in self:
            rec.total_views_tiktok = sum(rec.tiktok_stream_ids.mapped('views'))
            rec.total_likes_tiktok = sum(rec.tiktok_stream_ids.mapped('likes'))
            rec.total_comments_tiktok = sum(rec.tiktok_stream_ids.mapped('comment'))
            rec.total_follow_tiktok = sum(rec.tiktok_stream_ids.mapped('follow'))
            rec.total_keranjang_tiktok = sum(rec.tiktok_stream_ids.mapped('keranjang'))
            rec.total_pembelian_tiktok = sum(rec.tiktok_stream_ids.mapped('pembelian'))

    # === VIDEO REPORT ===
    total_fb_views = fields.Integer(string="Total FB Views", compute="_compute_video_totals", store=True)
    total_fb_likes = fields.Integer(string="Total FB Likes", compute="_compute_video_totals", store=True)
    total_ig_views = fields.Integer(string="Total IG Views", compute="_compute_video_totals", store=True)
    total_ig_likes = fields.Integer(string="Total IG Likes", compute="_compute_video_totals", store=True)
    total_tt_views = fields.Integer(string="Total TikTok Views", compute="_compute_video_totals", store=True)
    total_tt_likes = fields.Integer(string="Total TikTok Likes", compute="_compute_video_totals", store=True)
    total_yt_views = fields.Integer(string="Total YouTube Views", compute="_compute_video_totals", store=True)
    total_yt_likes = fields.Integer(string="Total YouTube Likes", compute="_compute_video_totals", store=True)
    # ==== Compute report Video =====
    @api.depends(
        'video_ids.fb_views', 'video_ids.fb_likes',
        'video_ids.ig_views', 'video_ids.ig_likes',
        'video_ids.tt_views', 'video_ids.tt_likes',
        'video_ids.yt_views', 'video_ids.yt_likes',
    )
    def _compute_video_totals(self):
        for rec in self:
            rec.total_fb_views = sum(rec.video_ids.mapped('fb_views'))
            rec.total_fb_likes = sum(rec.video_ids.mapped('fb_likes'))
            rec.total_ig_views = sum(rec.video_ids.mapped('ig_views'))
            rec.total_ig_likes = sum(rec.video_ids.mapped('ig_likes'))
            rec.total_tt_views = sum(rec.video_ids.mapped('tt_views'))
            rec.total_tt_likes = sum(rec.video_ids.mapped('tt_likes'))
            rec.total_yt_views = sum(rec.video_ids.mapped('yt_views'))
            rec.total_yt_likes = sum(rec.video_ids.mapped('yt_likes'))
# =====================================End Report========================================================

# ============tab senin-sabtu=======================#
    monday_plan_ids = fields.One2many(
    'plan.report', 'report_id', string='Senin',
    domain=[('day_name', '=', 'mon')])
    tuesday_plan_ids = fields.One2many(
        'plan.report', 'report_id', string='Selasa',
        domain=[('day_name', '=', 'tue')])
    wednesday_plan_ids = fields.One2many(
        'plan.report', 'report_id', string='Rabu',
        domain=[('day_name', '=', 'wed')])
    thursday_plan_ids = fields.One2many(
        'plan.report', 'report_id', string='Kamis',
        domain=[('day_name', '=', 'thu')])
    friday_plan_ids = fields.One2many(
        'plan.report', 'report_id', string='Jumat',
        domain=[('day_name', '=', 'fri')])
    saturday_plan_ids = fields.One2many(
        'plan.report', 'report_id', string='Sabtu',
        domain=[('day_name', '=', 'sat')])
    
# ===========hitung total jam plan perhari=======================
    @api.depends(
    'monday_plan_ids.duration',
    'tuesday_plan_ids.duration',
    'wednesday_plan_ids.duration',
    'thursday_plan_ids.duration',
    'friday_plan_ids.duration',
    'saturday_plan_ids.duration',
    )
    def _compute_total_durations(self):
        for rec in self:
            rec.total_duration_monday = sum(line.duration for line in rec.monday_plan_ids) / 60.0
            rec.total_duration_tuesday = sum(line.duration for line in rec.tuesday_plan_ids) / 60.0
            rec.total_duration_wednesday = sum(line.duration for line in rec.wednesday_plan_ids) / 60.0
            rec.total_duration_thursday = sum(line.duration for line in rec.thursday_plan_ids) / 60.0
            rec.total_duration_friday = sum(line.duration for line in rec.friday_plan_ids) / 60.0
            rec.total_duration_saturday = sum(line.duration for line in rec.saturday_plan_ids) / 60.0

# ====================== COpy Plan Previous week ================================== 
    def copy_previous_week_plan(self):
        for rec in self:
            _logger.info("===> Start copying plan for report ID: %s", rec.id)

            if not rec.date_from:
                raise ValidationError("Silakan isi 'Tanggal Mulai' terlebih dahulu.")

            previous_date = rec.date_from - timedelta(days=7)

            previous_report = self.search([
                ('user_id', '=', rec.user_id.id),
                ('date_from', '<=', previous_date),
                ('date_to', '>=', previous_date)
            ], limit=1)

            if not previous_report:
                raise ValidationError("Tidak ditemukan laporan minggu sebelumnya.")

            plans_by_day = {
                'mon': [], 'tue': [], 'wed': [], 'thu': [], 'fri': [], 'sat': []
            }

            for plan in previous_report.monday_plan_ids + previous_report.tuesday_plan_ids + \
                        previous_report.wednesday_plan_ids + previous_report.thursday_plan_ids + \
                        previous_report.friday_plan_ids + previous_report.saturday_plan_ids:

                if not plan.date or not plan.day_name:
                    continue

                try:
                    day_offset = (plan.date - previous_report.date_from).days
                    new_date = rec.date_from + timedelta(days=day_offset)

                    plans_by_day[plan.day_name].append((0, 0, {
                        'date': new_date,
                        'day_name': plan.day_name,
                        'task': plan.task,
                        'duration': plan.duration,
                        'notes': plan.notes,
                    }))
                except KeyError:
                    _logger.warning("Unknown day_name '%s' in plan %s", plan.day_name, plan.id)

            if all(not items for items in plans_by_day.values()):
                raise ValidationError("Laporan minggu sebelumnya tidak memiliki data plan.")

            # Kosongkan dan isi ulang semua sekalian
            rec.write({
                'monday_plan_ids': [(5, 0, 0)] + plans_by_day['mon'],
                'tuesday_plan_ids': [(5, 0, 0)] + plans_by_day['tue'],
                'wednesday_plan_ids': [(5, 0, 0)] + plans_by_day['wed'],
                'thursday_plan_ids': [(5, 0, 0)] + plans_by_day['thu'],
                'friday_plan_ids': [(5, 0, 0)] + plans_by_day['fri'],
                'saturday_plan_ids': [(5, 0, 0)] + plans_by_day['sat'],
            })

            _logger.info("===> Plan copied successfully for report ID: %s", rec.id)

        return True
