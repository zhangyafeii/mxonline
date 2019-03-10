# -*- coding: utf-8 -*-

"""
@Datetime: 2019/3/4
@Author: Zhang Yafei
"""
import re
from django import forms

from operation.models import UserAsk


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        """
        验证手机号是否合法
        """
        mobile = self.cleaned_data['mobile']
        regex_mobile = '^1[358]\d{9}$|^147\d{8}$|^176\d{8}$'
        p = re.compile(regex_mobile)
        if re.match(p, mobile):
            return mobile
        raise forms.ValidationError('手机号吗非法', code='mobile_valid')

