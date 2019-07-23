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


import os
import json
import time
import re

from pyspark import SparkConf, Row
from pyspark.sql import SparkSession


def combine_words(line, filter_dict=None):
    """
    将古诗词进行分字, 并进行共现组合
    :param line:
    :return:
    """
    line = re.sub('[。,，.?!！？￥%&\'\\"]', '', line.strip())
    if filter_dict is None:
        words = list(line)
    else:
        words = [x for x in list(line) if x in filter_dict]
    rst = []
    for i in range(len(words)):
        for j in range(i, len(words)):
            if words[i] == words[j]:
                continue
            if words[i] < words[j]:
                rst.append(((words[i], words[j]), line))
            else:
                rst.append(((words[j], words[i]), line))
    return rst


def load_and_split(spark, filter_dict):
    """

    :param spark:
    :param filter_dict:
    :return:
    """
    data = spark.read.text('poem2.txt')
    data.show()
    seg = data.rdd.distinct().flatMap(lambda x: combine_words(x[0], filter_dict))
    ss = seg.map(lambda x: Row(a=x[0], b=x[1]))
    spark.createDataFrame(ss).show(200)
    return seg


def word_count_and_sorted(spark, data):
    data = data\
        .map(lambda x: (x[0], (1, x[1])))\
        .reduceByKey(lambda x, y: x[0] + y[0])\
        .map(lambda x: (x[1], x[0]))\
        .sortByKey(False)\
        .map(lambda x: Row(word=x[1], count=x[0]))
    return spark.createDataFrame(data)


def load_local_name_record(path):
    """
    加载班级信息名录，只统计班级同学名称的字，减少计算量
    :param path:
    :return:
    """
    import xlrd
    book = xlrd.open_workbook(path)
    tabel = book.sheet_by_index(0)
    nrow = tabel.nrows
    contain_token_dict = set()
    for row in range(1, nrow):
        name = tabel.cell(row, 1).value[1:]
        contain_token_dict = contain_token_dict.union(set(list(name)))
    return contain_token_dict


def _filer(line):
    pass
if __name__ == '__main__':
    path = '/Users/macan/Desktop/chinese-poetry-master' # 古诗词路径
    class_name_tabel_path = '/Users/macan/Desktop/Vcamp/2019Vcamp 3班班级通讯录.xlsx' # 班级通讯录路劲
    # 加载班级通讯录，得到同学姓名信息
    filter_dict = load_local_name_record(class_name_tabel_path)

    # docs = load_poem(path)
    # save_poem_content(docs, 'poem.txt')

    conf = SparkConf()
    spark = SparkSession \
        .builder \
        .appName('co-word-count') \
        .master('local[*]') \
        .config(conf=conf) \
        .getOrCreate()

    filter_dict = set()
    filter_dict.add('a')
    filter_dict.add('c')
    seg = load_and_split(spark, filter_dict)
    counts = word_count_and_sorted(spark, seg)
    counts.show(100)
    spark.stop()


