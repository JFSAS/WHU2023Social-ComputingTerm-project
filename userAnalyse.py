import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('data/data_short_emotion_snownlp.csv')
#从data中提取出level和score
data = data[['ulevel','score']]

#以level为横坐标，score为权重，数量为高度，作图
#作图
sns.set()
sns.set_style("whitegrid")
sns.set_context("paper")
sns.set_palette("Set2")
sns.set(font='SimHei')
plt.rcParams['axes.unicode_minus']=False
plt.figure(figsize=(10,10))
sns.countplot(x='ulevel',hue='score',data=data)
plt.savefig('data/ulevel_score.png')
