"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path, include
from django.views.static import serve
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib import admin
import xadmin

from users.views import IndexView, LoginView, LogoutView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyView

urlpatterns = [
    # path('admin/', admin.site.urls),
    # re_path('^$', TemplateView.as_view(template_name='index.html'), name='index'),
    re_path('^$', IndexView.as_view(), name='index'),
    re_path('^xadmin/', xadmin.site.urls),
    re_path('^login/$', LoginView.as_view(), name='login'),
    re_path('^logout/$', LogoutView.as_view(), name='logout'),
    re_path('^register/$', RegisterView.as_view(), name='register'),
    re_path('^captcha/', include('captcha.urls')),
    path('active/<str:active_code>', ActiveUserView.as_view(), name='user_active'),
    re_path('^forget_pwd/$', ForgetPwdView.as_view(), name='forget_pwd'),
    path('reset/<str:active_code>', ResetView.as_view(), name='reset_pwd'),
    path('modify_pwd/', ModifyView.as_view(), name='modify_pwd'),

    # 课程机构url配置
    re_path('^org/', include('organization.urls', namespace='org')),

    # 课程url配置
    re_path('^course/', include('courses.urls', namespace='course')),

    # 用户url配置
    re_path('^users/', include('users.urls', namespace='users')),

    # 配置上传文件的访问处理函数
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),

    # 配置静态文件的访问处理函数
    # path('static/<path:path>', serve, {'document_root': settings.STATIC_ROOT}, name='static'),

    # 富文本相关url
    path('ueditor/',include('DjangoUeditor.urls')),

]

# 全局404页面配置
handler404 = 'users.views.page_not_found'

# 群居500页面配置
handler500 = 'users.views.page_error'
