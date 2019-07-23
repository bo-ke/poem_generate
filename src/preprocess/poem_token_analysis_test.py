#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
分析结果的使用 测试
#@Time    : 2019/7/22 12:54
# @Author  : MaCan (ma_cancan@163.com)
# @File    : poem_token_analysis.py
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import sys
import pickle
sys.path.append('../..')
from src.preprocess.poem_token_analysis import find_max_co_name_info, read_name_dict_data, load_helper_dict



if __name__ == "__main__":
    names = ['张立', '胡妍', '谢腾', '杨紫',]
    co_cnt, name_pair_dict, name_dict, black_list = load_helper_dict('../../dataset')
    # 测试输入姓名，得到对应的”有缘人“
    for name in names:
        target_name, score = find_max_co_name_info(name, name_pair_dict, co_cnt, name_dict, black_list)
        print('{} and {} match score:{}'.format(name, target_name, score))
