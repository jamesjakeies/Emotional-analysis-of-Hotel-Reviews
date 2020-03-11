import requests
import json
import jsonpath
import csv
import time
import random
requests.packages.urllib3.disable_warnings()
def get_html(data):
    try:
        headers = {
            'authority': 'm.ctrip.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'cookieorigin': 'https://m.ctrip.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            'content-type': 'application/json',
            'accept': '*/*',
            'origin': 'https://m.ctrip.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'referer': 'https://m.ctrip.com/webapp/hotel/HotelDetail/dianping/1452125.html',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
            'cookie': '_abtest_userid=d8247778-3f12-4ba0-a80f-a81aab371e9e; Session=SmartLinkCode=U155952&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=&SmartLinkLanguage=zh; _RGUID=63c39cb7-4004-4ead-8d64-8d62acf326b5; _RDG=280c832962b4c124881d186dd5b514e892; _RSG=jw410TBd3F6rQoyiAMZar8; MKT_CKID=1581309837466.pzo1z.fqd9; _ga=GA1.2.1561439562.1581309838; MKT_Pagesource=PC; login_uid=332B57BF83F8816F84A22047C4D6C242; login_type=0; nfes_isSupportWebP=1; BNBCityID=17split%E6%9D%AD%E5%B7%9Esplithangzhousplit2020-02-17split2020-02-20split0; hoteluuid=3lSN2Dolz31c2G5a; appFloatCnt=17; Union=OUID=index&AllianceID=4897&SID=155952&SourceID=&createtime=1581923076&Expires=1582527875898; HotelCityID=14split%E8%8B%8F%E5%B7%9EsplitSuzhousplit2020-2-17split2020-02-18split0; _jzqco=%7C%7C%7C%7C1581923088505%7C1.838110988.1581309837464.1581923107888.1581929345366.1581923107888.1581929345366.undefined.0.0.67.67; __zpspc=9.21.1581929345.1581929345.1%232%7Csp0.baidu.com%7C%7C%7C%25E6%2590%25BA%25E7%25A8%258B%7C%23; GUID=09031130311970672882; _bfa=1.1581309834715.2dcmvn.1.1581929560241.1582252969252.25.668.228032; _RF1=221.218.143.104',
        }

        params = (
            ('', ''),
            ('_fxpcqlniredt', '09031130311970672882'),
        )
        response = requests.post('https://m.ctrip.com/restapi/soa2/16765/gethotelcomment', headers=headers,
                                 params=params,data=data)
        html=response.text
        #print(html)
        return html
    except Exception as e:
        time.sleep(random.uniform(6,9))
def get_infos(html,page):
    # 逻辑1：np_1 ==0,就直接2到5
    # 逻辑2:np_1 不等0分两种，np_4=0 np_4budeng0
    pages = []
    try:
        html=json.loads(html)
        userNickName = jsonpath.jsonpath(html, '$..othersCommentList[*].userNickName')
        baseRoomName = jsonpath.jsonpath(html, '$..othersCommentList[*].baseRoomName')
        checkInDate = jsonpath.jsonpath(html, '$..othersCommentList[*].checkInDate')
        postDate = jsonpath.jsonpath(html, '$..othersCommentList[*].postDate')
        content = jsonpath.jsonpath(html, '$..othersCommentList[*].content')
        ratingPoint = jsonpath.jsonpath(html, '$..othersCommentList[*].ratingPoint')
        travelType = jsonpath.jsonpath(html, '$..othersCommentList[*].travelType')
        imageList = jsonpath.jsonpath(html, '$..othersCommentList[*].imageList')
        titles = []
        title = jsonpath.jsonpath(html, '$..tdk.title')
        print(postDate)
        for i in range(len(postDate)):
            titles.append(title)
            pages.append(page)
        infos = zip(pages,userNickName,baseRoomName, checkInDate, postDate, content, ratingPoint, travelType, imageList, titles)
        with open('山东舜和.csv', 'a', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            for _ in infos:
                writer.writerow(_)
    except Exception as e:
        print(e)
def main():
    for page in range(1,690):
        print(page)
        data = {"hotelId":474311,"pageIndex":page,"tagId":0,"pageSize":10,"groupTypeBitMap":2,"needStatisticInfo":0,"order":0,"basicRoomName":"","travelType":-1,"head":{"cid":"09031130311970672882","ctok":"","cver":"1.0","lang":"01","sid":"8888","syscode":"09","auth":"","xsid":"","extension":[]}}
        data = json.dumps(data).encode(encoding='utf-8')
        html=get_html(data)
        get_infos(html,page)
        time.sleep(random.uniform(3,5))
if __name__ == '__main__':
    main()