# coding:utf8
import sys
import os
import torch as t
from generation.data import get_data
from generation.model import PoetryModel
from torch import nn
from generation.utils import Visualizer
import tqdm
from torchnet import meter
import ipdb
# import main
from generation.main import Config
from generation.main import gen

def test(boy_name, girl_name):
    opt = Config()
    if boy_name == "张立":
        opt.prefix_words = "两情若是久长时，又岂在朝朝暮暮。"
    elif boy_name == "李鸿斌":
        opt.prefix_words = "曾经沧海难为水，除却巫山不是云。"
    elif boy_name == "唐梅芝":
        opt.prefix_words = "此情可待成追忆，只是当时已惘然。"
    elif boy_name == "张一山":
        opt.prefix_words = "结发为夫妻，恩爱两不疑。"
    else:
        opt.prefix_words = "借问江潮与海水，何似君情与妾心。"
    opt.data_path = 'data/'
    opt.pickle_path = 'tang.npz'  # 预处理好的二进制文件
    opt.author = None  # 只学习某位作者的诗歌
    opt.constrain = None  # 长度限制
    opt.category = 'poet.tang'  # 类别，唐诗还是宋诗歌(poet.song)
    opt.lr = 1e-3
    opt.weight_decay = 1e-4
    opt.use_gpu = False
    opt.epoch = 20
    opt.batch_size = 128
    opt.maxlen = 125  # 超过这个长度的之后字被丢弃，小于这个长度的在前面补空格
    opt.plot_every = 20  # 每20个batch 可视化一次
    opt.env = 'poetry'  # visdom env
    opt.max_gen_len = 200  # 生成诗歌最长长度
    opt.debug_file = '/tmp/debugp'
    opt.model_path = 'checkpoints/tang_199.pth'  # 预训练模型路径
    tran_dict = {"高梽强": "高志强", "胡钰培": "胡玉培", "张鑫": "张金", "谭官鑫": "谭官金", "覃营晟": "覃营盛", "张琦": "张奇", "刘晗": "刘含"}
    if boy_name in tran_dict: boy_name = tran_dict[boy_name]
    if girl_name in tran_dict: girl_name = tran_dict[girl_name]
    if len(girl_name) == 2:
        opt.start_words = "我爱" + girl_name
    elif len(girl_name) == 3:
        opt.start_words = "爱" + girl_name
    opt.acrostic = True  # 是否是藏头诗
    opt.model_prefix = 'checkpoints/tang'  # 模型保存路径
    res = gen(opt)
    return res

if __name__ == '__main__':
    res = test("唐梅芝","刘昊然")
    print(res)