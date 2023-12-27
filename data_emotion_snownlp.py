import snownlp 
import pandas as pd
import os
import logging
logging.basicConfig(level=logging.INFO,format = '%(asctime)s - %(levelname)s: %(message)s')
def dropdata(data):
    
    #去掉重复的评论
    data_d = data.drop_duplicates(subset=['comment'])
    print('had drop :',data.shape[0]-data_d.shape[0],'lines')
    #删去小于5个字的评论
    data_d = data_d[data_d['comment'].str.len()>5]
    #使行号连续
    data_d = data_d.reset_index(drop=True)
    return data_d
def emotion_score(data):
    #使用snownlp进行情感分析
    score = []
    for i in range(data.shape[0]) :
        logging.info('正在对第%d条评论进行情感分析',i)
        try :
            s = snownlp.SnowNLP(data.at[i,'comment'])
        except : 
            logging.error('第%d条评论情感分析失败',i)
            print(data.at[i,'comment'])
            continue
        score.append(s.sentiments*10)
    data['score_predict'] = score
    return data
if __name__ == '__main__' :
    data = pd.read_csv('data/data_2_short.csv')
    data = emotion_score(data)
    data.to_csv("data/data_short_emotion_snownlp_withoutdrop.csv")
    data = dropdata(data)
    data.to_csv("data/data_short_emotion_snownlp.csv")
    data = pd.read_csv('data/data_2_long.csv')
    data = emotion_score(data)
    data.to_csv("data/data_long_emotion_snownlp_withoutdrop.csv")
    data = dropdata(data)
    data.to_csv("data/data_long_emotion_snownlp.csv")
    

