import requests
import json
import logging
import csv
logging.basicConfig(level=logging.INFO,format = '%(asctime)s - %(levelname)s: %(message)s')
datas= []
Base_url = 'https://api.bilibili.com/pgc/review/short/list?media_id=28370944&ps=20&sort=0'
headers = {
    'authority': 'api.bilibili.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cookie': "buvid3=C50DFBFC-98DB-7CC9-8B18-3F24B89EA98902206infoc; b_nut=1695641302; i-wanna-go-back=-1; b_ut=7; _uuid=CC422CD10-B981-8A4D-287E-E681FD36BCAA02943infoc; buvid_fp=01a5037d9c44c085e6281ab82bac2853; DedeUserID=1024344964; DedeUserID__ckMd5=cb922a57364f5a75; header_theme_version=CLOSE; rpdid=|(m~YkJuJuu0J'uYm~|~Yk~l; CURRENT_QUALITY=80; enable_web_push=DISABLE; innersign=0; bsource=search_bing; SESSDATA=3980400e%2C1718711832%2Cb38ce%2Ac2CjAHu5q6j8IZvpqOYMXEE0RCesoKQY9HM3Yp7lJXRyqY-FtCQpRD0ZABKadzRFDq1NgSVm84NWdkbGRmRkdJdWhBdUdCeDRzb290T1V4VHZRdG51SFZCSnZFaG5SY2xEdFpBM0RGbjJLOXB6WWEtX3lsQlVCOTFRNU9ldWwzRVVacWdKeWdRZC1BIIEC; bili_jct=ac5088153d6069b4fb3077f6b2097714; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDM0MTkwNDUsImlhdCI6MTcwMzE1OTc4NSwicGx0IjotMX0.adKWiMvjY0RLbHEvjB1AX9wqFLb1EFTWF9teNXslOcU; bili_ticket_expires=1703418985; sid=8rge8iel; CURRENT_BLACKGAP=0; buvid4=F122C51B-89DA-EA1A-2722-6351DBA4D0BD10780-022102714-qyaL1DibeR15%2BsbZnQDPWw%3D%3D; CURRENT_FNVAL=4048; b_lsid=CE1210B9D_18C8D6EB447; home_feed_column=4; browser_resolution=1207-822; bp_video_offset_1024344964=877624726721134592; PVID=3",
    'origin': 'https://www.bilibili.com',
    'referer': Base_url,
    'sec-ch-ua': '"Chromium";v="106", "Microsoft Edge";v="106", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47'
}


def getnextJson(next) :
    url = Base_url + '&cursor=%d'%next
    logging.info('scraping %s..',url)
    response = requests.get(url,headers=headers)
    if response.status_code != 200 :
        logging.error('get invalid tatus code %s while scraping %s',response.status_code,url)
    return json.loads(response.text)

def Json_parse_short(Json) :
    data=[]
    for i in range(len(Json['data']['list'])) :
        tmp = {}
        tmp["uname"] = Json['data']['list'][i]['author']['uname']
        tmp["uid"] = Json['data']['list'][i]['author']["mid"]
        tmp["ulevel"] = Json['data']['list'][i]['author']["level"]
        tmp["comment"] = Json['data']['list'][i]['content']
        tmp["score"] = Json['data']['list'][i]["score"]
        data.append(tmp)
    return data
def Json_parse_long(Json) :
    data=[]
    for i in range(len(Json['data']['list'])) :
        tmp = {}
        tmp["uname"] = Json['data']['list'][i]['author']['uname']
        tmp["uid"] = Json['data']['list'][i]['author']["mid"]
        tmp["ulevel"] = Json['data']['list'][i]['author']["level"]
        tmp["comment"] = Json['data']['list'][i]['content']
        tmp["score"] = Json['data']['list'][i]["score"]
        tmp["title"] = Json['data']['list'][i]["title"]
        data.append(tmp)
    return data
def getnextcursor(Json) :
    return Json['data']['next']

def init_short() :
    response = requests.get(Base_url,headers=headers) 
    Json = json.loads(response.text)
    data = Json_parse_short(Json)
    datas.extend(data)
    next = getnextcursor(Json)
    return next
def init_long() :   
    response = requests.get(Base_url,headers=headers) 
    Json = json.loads(response.text)
    data = Json_parse_long(Json)
    datas.extend(data)
    next = getnextcursor(Json)
    return next
def main_short() :
    next = init_short()
    i = 0
    while(True) : 
        i+=1
        logging.info('already get %d comments',(i)*20)
        Json = getnextJson(next)
        #如果没有下一页了，就退出.next=0时返回的已经是空的了
        if Json['data']['next'] == 0 :
            break
        data = Json_parse_short(Json)
        datas.extend(data)
        next = getnextcursor(Json)

def main_long() :
    global Base_url
    Base_url = 'https://api.bilibili.com/pgc/review/long/list?media_id=28370944&ps=20&sort=0'
    next = init_long()
    i=0
    while(True) : 
        i+=1
        logging.info('already get %d comments',(i)*20)
        Json = getnextJson(next)
        #如果没有下一页了，就退出.next=0时返回的已经是空的了
        if Json['data']['next'] == 0 :
            break
        data = Json_parse_long(Json)
        datas.extend(data)
        next = getnextcursor(Json)

        

if __name__ == '__main__' :
    #爬取短评长评,所有评论
    main_short()
    print(len(datas))
    with open('data/data_2_short.csv','w',encoding='utf-8') as f :
        headers = {"uname","uid","ulevel","comment","score"}
        wc = csv.DictWriter(f,headers,lineterminator='\n')
        wc.writeheader()
        wc.writerows(datas)
    print('一共得到',len(datas),'条短评')
    datas = []
    main_long()
    print(datas)
    with open('data/data_2_long.csv','w',encoding='utf-8') as f :
        headers = {"uname","uid","ulevel","score","title","comment"}
        wc = csv.DictWriter(f,headers,lineterminator='\n')
        wc.writeheader()
        wc.writerows(datas)
    print('一共得到',len(datas),'条长评')
    