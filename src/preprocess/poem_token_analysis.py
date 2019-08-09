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
import pickle

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
            if words[i] < words[j]:
                rst.append((words[i], words[j]))
            else:
                rst.append((words[j], words[i]))
    return rst


def token_distance(line, co_tokens=None):
    """
    统计两个共现字词之间的距离
    :param line 古诗词
    :param co_tokens 需要统计的字词对列表
    :reutrn 返回共现单词以及两个字词之间的距离
    """
    line = re.sub('[。,，.?!！？￥%&\'\\"]', '', line.strip())
    distances = []
    for token_pair in co_tokens:
        flag_1 = re.search(token_pair[0], line)
        flag_2 = re.search(token_pair[1], line)
        if flag_1 is not None and flag_2 is not None:
            try:
                distance = flag_2.span()[0] - flag_1.span()[0]
                distances.append(token_pair, distance)
            except IndexError as e:
                print(e)
    return distances


def word_count_and_sorted(spark, data, filter_dict):
    """
    共现词频统计
    """
    data = data \
        .rdd \
        .distinct()\
        .flatMap(lambda x: combine_word(x[0], filter_dict))\
        .map(lambda word: (word, 1))\
        .reduceByKey(lambda x, y: x + y)\
        .map(lambda x: (x[1], x[0]))\
        .sortByKey(False)\
        .map(lambda x: Row(word=x[1], count=x[0]))
    return spark.createDataFrame(data)


def calc_distance(data):
    """
    统计两个共现词之间的编辑距离
    """
    pass

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
    name_dict = {}
    for row in range(1, nrow):
        name = tabel.cell(row, 1).value
        sex = tabel.cell(row, 4).value
        name_dict[name] = sex
    return name_dict


def read_name_dict_data(file_path):
    """
    按行读取文件
    :param file_path 文件路径
    :return list
    """
    datas = {}
    with open(file_path, 'r', encoding='utf-8') as fd:
        for line in fd:
            try:
                line = line.strip().split()
                datas[line[0]] = line[1]
            except IndexError as e:
                print(e)
    return datas


def load_co_token_cnt(path):
    """
    加载共现的字词列表
    :param path 字词列表路径
    """
    if not os.path.exists(path) or not os.path.isfile(path):
        raise FileNotFoundError('{} file not found...'.format(path))
    co_cnt = {}
    idx = 0
    with open(path, 'r', encoding='utf-8') as fd:
        for line in fd:
            line = json.loads(line.strip())
            co_cnt[(line['word']['_1'], line['word']['_2'])] = idx
            idx += 1
    co_cnt = {k:(idx - v)/idx for k,v in co_cnt.items()}
    return co_cnt


def name_match(co_cnt, names):
    """
    通过名，使用姓名进行替换
    """
    new_co_cnt = {}
    name_pair_dict = {}
    for name_pair, prob in co_cnt.items():
        p1, p2 = [], []
        for name in names:
            if name_pair[0] == name[1:]:
                p1.append(name)
            elif name_pair[1] == name[1:]:
                p2.append(name)
        # print(p1, p2)
        for i in range(len(p1)):
            for j in range(len(p2)):
                name1, name2 = sorted_name(p1[i], p2[j])
                new_co_cnt[(name1, name2)] = max(
                    new_co_cnt.get((name1, name2), 0.0), prob)
                
                def add_name_to_dict(key, value, name_pair_dict):
                    if name_pair_dict.get(key, None) is None:
                        tmp = set()
                        tmp.add(value)
                        name_pair_dict[key] = tmp
                    else:
                        tmp = name_pair_dict[key]
                        tmp.add(value)
                        name_pair_dict[key] = tmp
                add_name_to_dict(name1, name2, name_pair_dict)
                add_name_to_dict(name2, name1, name_pair_dict)

    # find max score pair
    max_score_name_pair = {}
    for name, pairs in name_pair_dict.items():
        max_score = 0
        pair = None
        for p in pairs:
            name1, name2 = sorted_name(name, p)
            score = new_co_cnt.get((name1, name2))
            if score > max_score:
                pair = (name, p)
                max_score = score
        max_score_name_pair[pair] = max_score
    return new_co_cnt, name_pair_dict, max_score_name_pair


def sorted_name(name1, name2):
    if name1 < name2:
        return name1, name2
    return name2, name1


def find_max_co_name_info(name, name_pair_dict, co_cnt, name_dict, black_list):
    """
    输入一个姓名，找到其最大共现的姓名
    note: 需要先加载co_cnt.pkl 得到co_cnt 字典对象，
        加载name_pair_dict.pkl 得到name_pair_dict对象
    :param name 输入的姓名
    :param name_pair_dict 姓名pair字典
    :param co_cnt 姓名pair与得分的字典
    :param name_dict 姓名与性别的对应字典
    :param blcak_list 黑名单列表，出现在该名单的人物，不上榜
    :return target_name:匹配的姓名, score:得分
    """
    target_name = name_pair_dict.get(name, '')
    if target_name == '':
        # raise Exception('众里寻ta千百度，也没找到{}的有缘人'.format(name))
        return None,0.0
    max_score = 0
    tname = None
    ns = {}
    sex_flag = name_dict.get(name)
    for tn in target_name:
        if black_list is not None and tn in black_list:
            continue
        if name_dict.get(tn) == sex_flag:
            continue
        name1, name2 = sorted_name(name, tn)
        score = co_cnt.get((name1, name2), 0.0)
        ns[tn] = score
        if max_score < score:
            max_score = score
            tname = tn
    return tname, max_score


def load_helper_dict(path):
    """
    加载相关辅助文件信息
    :param path 文件所在的目录
    """
    # 1.读取共现表
    with open(os.path.join(path, 'co_cnt.pkl'), 'rb') as fd:
        co_cnt = pickle.load(fd)
    # 2. 读取姓名对应表
    with open(os.path.join(path, 'name_pair_dict.pkl'), 'rb') as fd:
        name_pair_dict = pickle.load(fd)
    # 3. 读取姓名和性别对应信息
    name_dict = read_name_dict_data(os.path.join(path, 'name_dict.txt'))

    # 4. 读取黑名单，该姓名不上榜
    black_list = set()
    with open(os.path.join(path, 'black_list.txt'), 'r', encoding='utf-8') as fd:
        for line in fd:
            black_list.add(line.strip())

    return co_cnt, name_pair_dict, name_dict, black_list


if __name__ == '__main__':
    # path = '/Users/macan/Desktop/chinese-poetry-master' # 古诗词路径
    # class_name_tabel_path = '/Users/macan/Desktop/Vcamp/2019Vcamp 3班班级通讯录.xlsx' # 班级通讯录路劲
    # # 姓名名录数据
    # name_dict_path = '../../dataset/name_dict.txt'
    # # 加载班级通讯录，得到同学姓名信息
    # if os.path.exists(name_dict_path) and os.path.isfile(name_dict_path):
    #     print('load local name dict form <{}>'.format(name_dict_path))
    #     name_dict = read_name_dict_data(name_dict_path)
    # else:
    #     print('get name dict from class name excel file.')
    #     name_dict = load_local_name_record(class_name_tabel_path)
    #     with open('../../dataset/name_dict.txt', 'w', encoding='utf-8') as fd:
    #         for name, sex in name_dict.items():
    #             fd.write(name + '\t' + sex + '\n')
    # filter_dict = name_dict.keys()
    # # 去除姓
    # filter_dict = [x[1:] for x in filter_dict]
    # print('name filter dict size:{}'.format(len(filter_dict)))

    # # # 读取古诗词数据
    # # docs = load_poem(path)
    # # save_poem_content(docs, 'poem.txt')

    # conf = SparkConf()
    # spark = SparkSession \
    #     .builder \
    #     .appName('co-word-count') \
    #     .master('local[*]') \
    #     .config(conf=conf) \
    #     .getOrCreate()
    # data = spark.read.text('poem.txt').distinct()
    # data.show()
    # #data.rdd.flatmap(lambda x: token_distance(x[0])).reduceByKey()
    # counts = word_count_and_sorted(spark, data, filter_dict)
    # counts.show(2000)
    # print(counts.count())
    # counts.repartition(1).write.json('../../dataset/co-token-cnt')
    # spark.stop()
    
    # os.rename('../../dataset/co-token-cnt/.pa')
    # 手动将保存的计算结果文件名改为co_token_cnt.json
    path = '../../dataset/co_token_cnt.json'
    co_cnt = load_co_token_cnt(path)
    #print(co_cnt)
    name_dict = read_name_dict_data('../../dataset/name_dict.txt')
    names = name_dict.keys()
    # 得到姓名对和其得分的map
    co_cnt, name_pair_dict, max_name_pair_dict = name_match(co_cnt, names)
    print(names)

    # 将其保存到文件中
    with open('../../dataset/co_cnt.pkl', 'wb') as fd:
        pickle.dump(co_cnt, fd)

    #得到姓名对，并且保存到文件中
    # name_pair_dict = {k[0]: k[1] for k, _ in names.items()}
    with open('../../dataset/name_pair_dict.pkl', 'wb') as fd:
        pickle.dump(name_pair_dict, fd)
