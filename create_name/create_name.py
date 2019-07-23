#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 08:35:30 2019

@author: lbj
"""

import numpy as np
import re
import os
import gensim

#path1 = '/home/lbj/Desktop/my_tensorflow_poems-master/'

def name_vector():
    embedding_model = gensim.models.Word2Vec.load('word_embedded_model')
    index2boy = dict()
    index2girl = dict()
    boyname_vec = []
    girlname_vec = []
    temp = []
    temp2 = []
    with open('boy_n.txt') as f:
        for nm in f.readlines():
            nm = nm.strip()
            if nm not in temp and nm:
                try:
                    boyname_vec.append(embedding_model[nm])
                    index2boy[len(index2boy)] = nm
                    temp.append(nm)
                except:
                    continue
            
            
    with open('girl_n.txt') as f:
        for nm in f.readlines():
            nm = nm.strip()
            if nm not in temp2 and nm:
                try:
                    index2girl[len(index2girl)] = nm
                    girlname_vec.append(embedding_model[nm])
                    temp2.append(nm)
                except:
                    continue
    return embedding_model,index2boy,np.array(boyname_vec),index2girl,np.array(girlname_vec)

def create_name(father_name,mother_name,is_girl=True):
    embedding_model,boyindex,boyname_vec,girlindex,girlname_vec = name_vector()
    father_vec = embedding_model[father_name[-1]]
    mother_vec = embedding_model[mother_name[-1]]
    if is_girl:
        father_part = np.argmax(np.dot(girlname_vec,father_vec))     #######
        mother_part = np.argmax(np.dot(girlname_vec,mother_vec)) 
        father_part_name = girlindex[father_part]
        mother_part_name = girlindex[mother_part]
        if father_part_name==father_name[-1]:
            f_t = np.dot(girlname_vec,father_vec)
            f_t[np.argmax(f_t)] = min(f_t)
            father_part = np.argmax(f_t)
            father_part_name = girlindex[father_part]
        if mother_part_name==mother_name[-1]:
            m_t = np.dot(girlname_vec,mother_vec)
            m_t[np.argmax(m_t)] = min(m_t)
            mother_part = np.argmax(m_t)
            mother_part_name = girlindex[mother_part]
    else:
        father_part = np.argmax(np.dot(boyname_vec,father_vec))     #######
        mother_part = np.argmax(np.dot(boyname_vec,mother_vec)) 
        father_part_name = boyindex[father_part]
        mother_part_name = boyindex[mother_part]
        if father_part_name==father_name[-1]:
            f_t = np.dot(boyname_vec,father_vec)
            f_t[np.argmax(f_t)] = min(f_t)
            father_part = np.argmax(f_t)
            father_part_name = boyindex[father_part]
        if mother_part_name==mother_name[-1]:
            m_t = np.dot(boyname_vec,mother_vec)
            m_t[np.argmax(m_t)] = min(m_t)
            mother_part = np.argmax(m_t)
            mother_part_name = boyindex[mother_part]
    return father_name[0]+father_part_name+mother_part_name
 
if __name__ == "__main__":
    print(create_name('张立','胡妍',is_girl=False))