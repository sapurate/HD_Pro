import requests
import re

def doit(city,now_date,startTimeBegin,startTimeEnd):
    session_request = requests.session()
    login_url='http://134.200.26.196/api/oauth/token'
    result=session_request.post(
                login_url,
                data={
                    'client_id':'app_client',
                    'client_secret':'hollycrm_app_client',
                    'username':'%s'%citys["%s"%city],
                    'password':'Jzyx@0606',
                    'grant_type':'password',
                    'scope':'read write',
                    'errorCnt':'0',
                    'captcha_uid':'',
                    'captcha':'',
                    'deviceId':'',
                    'loginType':''
                },
            headers = dict(referer=login_url)
            )
    body_message=result.content.decode('utf-8')
    access_token=''.join(re.findall('"access_token":"(.*?)",',body_message))
    JSESSIONID = result.cookies.get_dict()['JSESSIONID']
    print(access_token)
    print(JSESSIONID)

    headers={
    'Host':'134.200.26.196',
    'Connection':'keep-alive',
    'Content-Length':'224',
    'Accept':'application/json, text/plain, */*',
    'Origin':'http://134.200.26.196',
    'access_token':'%s'%access_token,
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43',
    'Content-Type':'application/x-www-form-urlencoded',
    'Referer':'http://134.200.26.196/callrecord/callrecordNew',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cookie':'JSESSIONID=%s'%JSESSIONID
    }

    params = {
        'deptName': '',
        'projectName': '',
        'taskName': '',
        'city': '',
        'userCode': '',
        'handleUser': '',
        'startTimeBegin': '%s'%startTimeBegin,
        'startTimeEnd': '%s'%startTimeEnd,
        'endTimeBegin': '',
        'endTimeEnd': '',
        'handleResult': '',
        'isConn': '',
        'mobileNo': '',
        'page': '',
        'rows': '',
        'tenantId': '',
        'called': '',
        'qualityCondition': ''
        }
    req = requests.post("http://134.200.26.196/api/callRecord/download",headers=headers,data=params)
    print(req.cookies.get_dict())


    with open(r'C:\Users\Fei\Desktop\外呼记录\%s\%s.xlsx'%(now_date,city), 'wb') as file:
        file.write(req.content)

###定义事件
now_date = '2020-01-13' #必改
startTimeBegin = '%s 00:00:00'%now_date #必改
startTimeEnd = '%s 13:00:00'%now_date #必改
citys = {"襄阳":"xy_xuzhufei@hb","荆门":"jm_houqingyang@hb","宜昌":"yc_xuzhufei@hb","江汉":"jh_xuzhufei@hb",
         "荆门_本地":"jm_xuzhufei@hb","江汉_本地":"jh_xuzhufei02@hb"}
for city in citys:
    doit(city,now_date,startTimeBegin,startTimeEnd)
###执行事件