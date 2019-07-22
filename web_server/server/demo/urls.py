# -*- coding: utf-8 -*-
"""
@author: kebo
@contact: itachi971009@gmail.com

@version: 1.0
@file: urls.py
@time: 2019-07-17 18:09

这一行开始写关于本文件的说明与解释
"""

from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name='home'),
    path('enter_a_name',views.enter_a_name,name='enter_a_name'),
    path('match_name',views.match_name,name='match_name')
]