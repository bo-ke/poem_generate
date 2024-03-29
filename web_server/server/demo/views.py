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
from api import match_name,gen_photo,gen_poem,gen_name
from api import api_match_name,api_make_name,api_generate,api_gen_photo

# Create your views here.
def home(req):
    """

    :param req:
    :return:
    """
    # return HttpResponse("Hello,words")
    return render_to_response("home.html")

def enter_a_name(req):
    """

    :param req:
    :return:
    """
    return render_to_response("enter_a_name.html")


def match(req):
    """

    :param req:
    :return:
    """
    if req.method=='POST':
        # print(req.POST)
        name = req.POST['username']
        # print(name)
        name2,score = api_match_name(name)
        return render_to_response("match_name.html",{'name1':name,
                                                     'name2':name2})
    else:
        message = "Please use the right request"
        return HttpResponse(message)

def generate(req):
    """

    :param req:
    :return:
    """
    if req.method =='POST':
        info = req.POST['content']
        name1,name2 = info.split(",")
        poem_content = api_generate(name1,name2)
        print(poem_content)
        photo_name,hidden = api_gen_photo(name2)
        print(hidden)
        # hidden = "hidden"
        # hidden = "style{;}"
        print(photo_name)
        # photo_name = "杨紫2"
        return render_to_response("generate_poem.html",{"poem":poem_content,
                                                        "photo_name":photo_name,
                                                        "name1":name1,
                                                        "name2":name2,
                                                        "hidden":hidden})
    else:
        message = "Please use the right request"
        return HttpResponse(message)

def make_name(req):
    """

    :param req:
    :return:
    """
    if req.method=="POST":
        info=req.POST['content']
        # print(info)
        name1,name2 = info.split(",")
        # print(name1,name2)
        name_child = api_make_name(name1,name2)
        # name_child = "test"
        return render_to_response("make_name.html",{"name_son":name_child})
    else:
        message = "Please use the right requests"
        return HttpResponse(message)



if __name__ == '__main__':
    pass