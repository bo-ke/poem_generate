# 基于Tencent DSG算法生成 char_embedding


## 文件配置

`pre_process.py`: 数据预处理

`train_data.txt`: `run pre_process.py`生成的训练数据


## word2vec的使用
`make`  

`./dsg -train input_file -output embedding_file -type 0 -size 50 -window 5 -negative 10 -hs 0 -sample 1e-4 -threads 1 -binary 1 -iter 5` 