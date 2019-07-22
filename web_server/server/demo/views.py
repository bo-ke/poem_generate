# -*- coding: utf-8 -*-
"""
@author: kebo
@contact: itachi971009@gmail.com

@version: 1.0
@file: views.py
@time: 2019-07-17 17:44

这一行开始写关于本文件的说明与解释
"""

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django import forms


class Userform(forms.Form):
    user_name = forms.CharField()

# Create your views here.
def home(req):
    # return HttpResponse("Hello,words")
    return render_to_response("home.html")

def enter_a_name(req):
    if req.method=='POST':
        uf = Userform(req.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']


    return render_to_response("enter_a_name.html")


def match_name(req):
    return render_to_response("match_name.html")