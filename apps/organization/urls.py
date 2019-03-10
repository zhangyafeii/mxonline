# -*- coding: utf-8 -*-

"""
@Datetime: 2019/3/4
@Author: Zhang Yafei
"""
from django.urls import path, re_path

from organization.views import OrgView, AddUserAskView, OrgHomeView, OrgCoueseView, OrgTeacherView, OrgDescView
from organization.views import AddFavView, TeacherListView, TeacherDetailView

app_name = 'org'

urlpatterns = [
    # 课程机构列表页
    re_path(r'^list/', OrgView.as_view(), name='org_list'),
    re_path(r'^add_ask/', AddUserAskView.as_view(), name='add_ask'),
    path('home/<int:org_id>/', OrgHomeView.as_view(), name='org_home'),
    path('course/<int:org_id>/', OrgCoueseView.as_view(), name='org_course'),
    path('desc/<int:org_id>/', OrgDescView.as_view(), name='org_desc'),
    path('org_teacher/<int:org_id>/', OrgTeacherView.as_view(), name='org_teacher'),

    # 机构收藏
    re_path(r'^add_fav/$', AddFavView.as_view(), name="add_fav"),

    # 讲师列表页
    re_path(r'^teacher/list/$', TeacherListView.as_view(), name="teacher_list"),

    # 讲师详情页
    re_path(r'^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name="teacher_detail"),
]
