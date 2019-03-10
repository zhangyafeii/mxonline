# -*- coding: utf-8 -*-

"""
@Datetime: 2019/2/26
@Author: Zhang Yafei
"""
import xadmin
from xadmin import views

from users import models


class BaseSetting(object):
    """ 主题功能设置 """
    enable_themes = True
    use_bootswatch = True


class GlogalSettings(object):
    site_title = '幕学后台管理系统'
    site_footer = '幕学在线网'
    menu_style = 'accordion'


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']
    model_icon = 'fa fa-address-book-o'


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(models.EmailVerifyRecord, admin_class=EmailVerifyRecordAdmin)
xadmin.site.register(models.Banner, admin_class=BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlogalSettings)