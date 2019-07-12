#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
some public io tools
# @Time    : 2019/7/12 12:39
# @Author  : MaCan (ma_cancan@163.com)
# @File    : io_utils.py
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import pickle
import os


def read_file(file_path, encoding='utf-8'):
    """
    读取一个文件
    :param file_path:
    :return:
    """
    if os.path.exists(file_path) and os.path.isfile(file_path):
       with open(file_path, 'r', encoding=encoding) as fd:
           for line in fd:
               yield line
    else:
        raise FileNotFoundError()
