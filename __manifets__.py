# -*- coding: utf-8 -*-
# ============= Programmer : Mugni ================
{
    "name": "Admin Sosial Media",
    "summary": "Tools Manage Report Sosial Media",
    "description": """
Admin Work Statistic and Report
    """,
    "author": "Mugni Hidayat",
    "website": "https://www.yourcompany.com",
    "category": "Sales",
    "version": "1.2",
    "depends": ["base", "web"],
    "data": [
        # Security
        "security/admin_work_security.xml",
        "security/ir_rules_security.xml,
        "security/ir.model.access.csv",
        # report
        "report/admin_work_templates.xml",
        "report/admin_work_reports.xml",
        # views
        "views/admin_work_views.xml",
        # chart action
        "views/chart_action.xml",
        # views content
        "views/content_report_stream_tiktok_views.xml",
        "views/content_report_stream_shopee_views.xml",
        "views/content_report_video_views.xml",
        "views/product_knowledge_views.xml",
        "views/article_video_views.xml",
        # Chart views
        "views/chart_tiktok_template.xml",
        "views/chart_shopee_template.xml",
        "views/chart_video_template.xml",
        # menu
        "views/admin_work_menus.xml",
    ],
    "application": True,
    "installable": True,
    "license": "OPL-1",
}
