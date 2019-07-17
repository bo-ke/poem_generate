#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
#@Time    : 2019/7/12 12:54
# @Author  : MaCan (ma_cancan@163.com)
# @File    : poem_token_analysis.py
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import os
import json
import time
import re
import zhconv

from pyspark import SparkConf, Row
from pyspark.sql import SparkSession

import sys
# sys.path.append('../..')
# from src.preprocess.io_utils import read_file


formats = {
    #'youmengying':['content'],
    #'ci':['paragraphs', 'rhythmic'],
    #'json': ['paragraphs', 'title'],
    'json': ['paragraphs'],
    #'shijing': ['content', 'title', 'chapter', 'section'],
    #'wudai': ['paragraphs', 'title']
}

def _parser(datas, category='json'):
    """
    解析不同类型json数据
    幽梦影：content
    ci宋词:paragraphs， rhythmic
    wudai:paragraphs, title
    json宋：paragraphs, title
    诗经:content, title, chapter, section
    :param datas:
    :param filter_dict 只统计字典中的字
    :return:
    """
    docs = []
    for data in datas:
        if type(data) == str:
            print(datas)
            continue
        fm = formats.get(category, None)
        content = ''
        for f in fm:
            doc = data.get(f, '')
            if doc == '':
                continue
            content += ''.join(doc)
        content = zhconv.convert(content, 'zh-cn')
        docs.append(content)
    return docs


def load_poem(file_path):
    """
    读取古诗词
    :param file_path:
    :return:
    """
    if not os.path.isdir(file_path):
        raise FileNotFoundError
    for dir in os.listdir(file_path):
        curr_dir = os.path.join(file_path, dir)
        if not os.path.isdir(curr_dir) or dir not in formats.keys():
            continue

        print('now process dir: \'{}\''.format(dir))
        for file in os.listdir(curr_dir):
            curr_file = os.path.join(curr_dir, file)
            if not os.path.isfile(curr_file) or file[-4:] != 'json':
                continue
            # if 'tang' not in file:
            #     continue
            print('\t file: {}'.format(curr_file))

            with open(curr_file, 'r', encoding='utf-8') as fd:
                data = json.load(fd)
                #print(data)
                # 解析当前文件的古诗词信息
                doc = _parser(data, dir)
                yield doc


def save_poem_content(docs, save_path):
    """
    将古诗词的文本形式存储到文件中，用于词的共现统计
    :param docs:
    :param save_path:
    :return:
    """
    with open(save_path, 'w', encoding='utf-8') as fd:
        for doc in docs:
            for line in doc:
                fd.write(line + '\n')


def combine_word(line, filter_dict, split=False):
    """
    将古诗词进行分字或者分词, 并进行共现组合
    :param line:
    :param filter_dict:
    :param split:是否对名切分成字进行统计
    :return:
    """
    def contains_name():
        names = []
        for name in filter_dict:
            if re.search(name, line) is not None:
                names.append(name)
        return names

    line = re.sub('[。,，.?!！？￥%&\'\\"]', '', line.strip())
    if filter_dict is None:
        words = list(line)
    else:
        if split:
            tmp = set()
            [[tmp.add(t) for t in list(x)] for x in filter_dict]
            filter_dict = tmp
            words = [x for x in list(line) if x in filter_dict]
        else:
            words = [x for x in filter_dict if re.search(x, line) is not None]
            # print(words)
    rst = []
    for i in range(len(words)):
        for j in range(i, len(words)):
            if words[i] == words[j]:
                continue
            # if words[i] < words[j]:
            #     rst.append(((words[i], words[j]), line))
            # else:
            #     rst.append(((words[j], words[i]), line))
            if words[i] < words[j]:
                rst.append((words[i], words[j]))
            else:
                rst.append((words[j], words[i]))
    return rst


def load_and_split(spark, filter_dict):
    """

    :param spark:
    :param filter_dict:
    :return:
    """
    data = spark.read.text('poem.txt').distinct()
    data.show()
    seg = data.rdd.flatMap(lambda x: combine_word(x[0], filter_dict))
    return seg


def word_count_and_sorted(spark, data):
    data = data\
        .map(lambda word: (word, 1))\
        .reduceByKey(lambda x, y: x + y)\
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
    name_dict = set()
    for row in range(1, nrow):
        name = tabel.cell(row, 1).value
        name_dict.add(name)
    return name_dict


def read_line_data(file_path):
    """
    按行读取文件
    :param file_path 文件路径
    :return list
    """
    datas = []
    with open(file_path, 'r', encoding='utf-8') as fd:
        for line in fd:
            datas.append(line.strip())
    return datas


if __name__ == '__main__':
    path = '/Users/macan/Desktop/chinese-poetry-master' # 古诗词路径
    class_name_tabel_path = '/Users/macan/Desktop/Vcamp/2019Vcamp 3班班级通讯录.xlsx' # 班级通讯录路劲
    # 姓名名录数据
    name_dict_path = 'dataset/name_dict.txt'
    # 加载班级通讯录，得到同学姓名信息
    if os.path.exists(name_dict_path) and os.path.isfile(name_dict_path):
        print('load local name dict form <{}>'.format(name_dict_path))
        filter_dict = read_line_data(name_dict_path)
    else:
        print('get name dict from class name excel file.')
        filter_dict = load_local_name_record(class_name_tabel_path)
        with open('dataset/name_dict.txt', 'w', encoding='utf-8') as fd:
            for line in filter_dict:
                fd.write(line + '\n')
    # 去除姓
    filter_dict = [x[1:] for x in filter_dict]
    print('name filter dict size:{}'.format(len(filter_dict)))

    # 读取古诗词数据
    docs = load_poem(path)
    save_poem_content(docs, 'poem.txt')

    conf = SparkConf()
    spark = SparkSession \
        .builder \
        .appName('co-word-count') \
        .master('local[*]') \
        .config(conf=conf) \
        .getOrCreate()

    seg = load_and_split(spark, filter_dict)
    counts = word_count_and_sorted(spark, seg)
    counts.show(2000)
    print(counts.count())
    spark.stop()


