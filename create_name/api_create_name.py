# -*- coding: utf-8 -*-
"""
@author: kebo
@contact: itachi971009@gmail.com

@version: 1.0
@file: api_create_name.py
@time: 2019-07-24 14:53

这一行开始写关于本文件的说明与解释

起名接口文件
"""

from create_name import create_name

def api_make_name(name_dad,name_mum,is_girl=True):
    """

    :param name_dad:
    :param name_mum:
    :param is_girl:
    :return: 孩子名字
    """
    child_name = create_name(name_dad,name_mum,is_girl)
    return child_name


if __name__ == '__main__':
    print(api_make_name('张立','胡妍',is_girl=False))