# -*- coding: utf-8 -*-

"""
@Datetime: 2019/2/27
@Author: Zhang Yafei
"""

from django.urls import re_path, path
from courses.views import VideoPlayView, CourseListView, CourseDetailView, CourseInfoView, CommentsView, AddComentsView

app_name = 'course'

urlpatterns = [
    # 课程列表页
    re_path(r'^list/$', CourseListView.as_view(), name="course_list"),
    # 课程详情页
    re_path(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="course_detail"),
    # 课程章节信息
    re_path(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name="course_info"),
    # 课程评论
    re_path(r'^comment/(?P<course_id>\d+)/$', CommentsView.as_view(), name="course_comments"),
    # 添加课程评论
    re_path(r'^add_comment/$', AddComentsView.as_view(), name="add_comment"),
    # 播放视频
    path('video/<int:video_id>', VideoPlayView.as_view(), name="video_play"),

]
