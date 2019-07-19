# -*- coding: utf-8 -*-
"""
@author: kebo
@contact: itachi971009@gmail.com

@version: 1.0
@file: models.py
@time: 2019-07-17 17:44

这一行开始写关于本文件的说明与解释
"""

from django.db import models

# Create your models here.

class User_portrait(models):
    name = models.TextField()
    match_name = models.TextField()
    poem = models.TextField()
    children = models.TextField()