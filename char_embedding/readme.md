# 基于Tencent DSG算法生成 char_embedding


## 文件配置

`pre_process.py`: 数据预处理

`train_data.txt`: `run` `pre_process.py`生成的训练数据

`data/` 训练数据以及输出embedding目录 
>`data/train_data.txt`   
`data/embedding_300.bin`


## 生成训练数据
`run` `pre_process.py`生成的训练数据


## 生成char embedding
进到word2vec/trunk目录下`run`  

`make`  

`./dsg -train ../../data/train_data.txt -output ../../data/embedding_300.bin -type 0 -size 300 -window 2 -negative 10 -hs 0 -sample 1e-4 -threads 4 -binary 1 -iter 30` 