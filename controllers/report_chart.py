from odoo import http
from odoo.http import request


class ChartController(http.Controller):

    @http.route('/gm/chart/tiktok/data', type='json', auth='user')
    def chart_tiktok_data(self):
        records = request.env['admin.work.report'].sudo().search([], order='week desc', limit=20)
        return [{
            'week': rec.week,
            'views': rec.total_views_tiktok,
            'comment': rec.total_comments_tiktok,
            'follow': rec.total_follow_tiktok,
            'keranjang': rec.total_keranjang_tiktok,
            'pembelian': rec.total_pembelian_tiktok,
        } for rec in reversed(records)]

    @http.route('/gm/chart/shopee/data', type='json', auth='user')
    def chart_shopee_data(self):
        records = request.env['admin.work.report'].sudo().search([], order='week desc', limit=20)
        return [{
            'week': rec.week,
            'views': rec.total_views,
            'comment': rec.total_comments,
            'follow': rec.total_follow,
            'keranjang': rec.total_keranjang,
            'pembelian': rec.total_pembelian,
        } for rec in reversed(records)]

    @http.route('/gm/chart/video/data', type='json', auth='user')
    def chart_video_data(self):
        records = request.env['admin.work.report'].sudo().search([], order='week desc', limit=20)
        return [{
            'week': rec.week,
            'fb_views': rec.total_fb_views,
            'fb_likes': rec.total_fb_likes,
            'ig_views': rec.total_ig_views,
            'ig_likes': rec.total_ig_likes,
            'tt_views': rec.total_tt_views,
            'tt_likes': rec.total_tt_likes,
            'yt_views': rec.total_yt_views,
            'yt_likes': rec.total_yt_likes,
        } for rec in reversed(records)]
    

    @http.route('/gm/chart/tiktok', type='http', auth='user', website=True)
    def chart_tiktok_page(self, **kwargs):
        return request.render("gm_sosmed_admin.chart_tiktok_template", {})

    @http.route('/gm/chart/shopee', type='http', auth='user', website=True)
    def chart_shopee_page(self, **kwargs):
        return request.render("gm_sosmed_admin.chart_shopee_template", {})

    @http.route('/gm/chart/video', type='http', auth='user', website=True)
    def chart_video_page(self, **kwargs):
        return request.render("gm_sosmed_admin.chart_video_template", {})
