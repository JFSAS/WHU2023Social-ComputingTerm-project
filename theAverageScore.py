import pandas
import numpy
import matplotlib.pyplot as plt
import seaborn as sns
from snownlp import SnowNLP
import logging 
import jieba
import jieba.analyse
logging.basicConfig(level=logging.INFO,format = '%(asctime)s - %(levelname)s: %(message)s')
data_short = pandas.read_csv('data/data_short_emotion_snownlp.csv')
data_long = pandas.read_csv('data/data_long_emotion_snownlp.csv')
data_long = data_long.reset_index(drop=True)
data_short_withoutdrop = pandas.read_csv('data/data_short_emotion_snownlp_withoutdrop.csv')
data_long_withoutdrop = pandas.read_csv('data/data_long_emotion_snownlp_withoutdrop.csv')
def get_meanScore():
    #短评情感分析结果
    actual_score_mean = (data_short['score'].mean()*data_short.shape[0]+data_long['score'].mean()*data_long.shape[0])/(data_short.shape[0]+data_long.shape[0])
    predict_score_mean = data_short['score_predict'].mean()
    actual_score_mean_withoutdrop = (data_short_withoutdrop['score'].mean()*data_short_withoutdrop.shape[0]+data_long_withoutdrop['score'].mean()*data_long_withoutdrop.shape[0])/(data_short_withoutdrop.shape[0]+data_long_withoutdrop.shape[0])
    predict_score_mean_withoutdrop = data_short_withoutdrop['score_predict'].mean()
    print('去重后的总体评分为',actual_score_mean_withoutdrop)#短评和长评的平均分
    print('去重后的总体预测评分为',predict_score_mean_withoutdrop)
    print('总体评分为',actual_score_mean)#短评和长评的平均分
    print('总体预测评分为',predict_score_mean)
    
    with open('data/meanScore','w') as f:
        f.write('actual_score_mean :'+str(actual_score_mean)+'\n')
        f.write('predict_score_mean :'+str(predict_score_mean)+'\n' )
        f.write('actual_score_mean_withoutdrop :'+str(actual_score_mean_withoutdrop)+'\n')
        f.write('predict_score_mean_withoutdrop :'+str(predict_score_mean_withoutdrop) )
#数据预处理
def pos_dataAnalyse(data):
    comment= ''
    for idex,row in data.iterrows() :
        string = row['comment']
        if len(string) < 10 :
            continue
        if SnowNLP(string).sentiments > 0.5 :
            comment+=string
        
        logging.info('正在拼接第%d条评论',idex)
    return comment

def neg_dataAnalyse(data):
    comment= ''
    for idex,row in data.iterrows() :
        string = row['comment']
        if len(string) < 10 :
            continue
        if SnowNLP(string).sentiments < 0.5:
            comment+=string
        logging.info('正在拼接第%d条评论',idex)
    return comment
def get_keyword():
    print("getting keyword")
    comment = ''
    #将所有正面评论拼接成一个str
    comment += pos_dataAnalyse(data_long)
    comment += pos_dataAnalyse(data_short)
    s = SnowNLP(comment)
    poskeyword = jieba.analyse.extract_tags(comment, topK=2, withWeight=False, allowPOS=('n'))#用结巴提取关键词
    poskeyword += jieba.analyse.extract_tags(comment, topK=3, withWeight=False, allowPOS=('a'))#用结巴提取关键词
    #poskeyword = s.keywords(5) #提取5正面个关键词
    #将所有负面评论拼接成一个str
    comment = ''
    comment += neg_dataAnalyse(data_long)
    comment += neg_dataAnalyse(data_short)
    s = SnowNLP(comment)
    negkeyword = jieba.analyse.extract_tags(comment, topK=2, withWeight=False, allowPOS=('n',))#用结巴提取关键词
    negkeyword += jieba.analyse.extract_tags(comment, topK=3, withWeight=False, allowPOS=('a',))
    #negkeyword = s.keywords(5) #提取5个负面关键词
    print('writing keyword.txt')
    with open("keyword_4.txt",'w') as f:
        f.write('sentiment rate= 0.5 \npositive keyword:')
        for word in poskeyword :    
            f.write(word +'  ')
        f.write('negative keyword:')
        for word in negkeyword :
            f.write(word+ '  ')

    with open("comment",'w') as f:
        f.write(comment)
    
def main():
    get_meanScore()
    get_keyword()

if __name__ == '__main__' :
    main()