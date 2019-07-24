# -*- coding: utf-8 -*-
"""
@author: kebo
@contact: itachi971009@gmail.com

@version: 1.0
@file: api_match_name.py
@time: 2019-07-24 14:59

这一行开始写关于本文件的说明与解释
"""

from src.preprocess.poem_token_analysis import find_max_co_name_info, read_name_dict_data, load_helper_dict



def api_match_name(name):
    co_cnt, name_pair_dict, name_dict, black_list = load_helper_dict('../dataset')
    # 测试输入姓名，得到对应的”有缘人“
    target_name, score = find_max_co_name_info(name, name_pair_dict, co_cnt, name_dict, black_list)
    return target_name,score


if __name__ == '__main__':
    names = ['张立', '胡妍', '谢腾', '杨紫', ]
    for name in names:
        target_name, score = api_match_name(name)
        print('{} and {} match score:{}'.format(name, target_name, score))
