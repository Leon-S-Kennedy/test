import json
from Utils import *
from config import *

text = ""  # 初始化邮件内容
title = ""  # 初始化邮件标题


# 登录函数（登录时不能打开我在校园，登录不上建议改密码，清缓存，然后过一会再登录。能不登录就不登录吧。）
def login():
    global text, title, jwsession

    loginUrl = f"{url}?username={username}&password={password}"
    loginHeader = {
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "User-Agent": User_Agent,
        "Content-Type": "application/json;charset=UTF-8",
        "Content-Length": "2",
        "Host": "gw.wozaixiaoyuan.com",
        "Accept-Language": "en-us,en",
        "Accept": "application/json, text/plain, */*",
    }
    loginData = "{}"
    session1 = requests.session()
    loginResponse = session1.post(url=loginUrl, headers=loginHeader, data=loginData)  # 发送登录请求

    if json.loads(loginResponse.text)["code"] == 0:
        text = "晚签到登录成功！\n"
        jwsession = loginResponse.headers['JWSESSION']
        setJwsession("config.py", jwsession)
        return True
    else:
        text = "晚签到登录失败！\n"
        text += f"{json.loads(loginResponse.text)['message']}"
        title = "晚签到登录失败"
        return False


# 获取签到信息函数（只有你存在还未签到的任务时才能正确签到，否则不会签到）
def getSignMessage():
    global text, title, id, logId

    getUrl = "https://student.wozaixiaoyuan.com/sign/getSignMessage.json"
    getHeader = {
        "Host": "student.wozaixiaoyuan.com",
        "content-type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip,compress,br,deflate",
        "Connection": "keep-alive",
        "User-Agent": User_Agent,
        "Referer": Referer,
        "Content-Length": "13",
        "JWSESSION": getJwsession("config.py"),
    }
    getData = "page=1&size=5"
    session2 = requests.session()
    getResponse = session2.post(getUrl, headers=getHeader, data=getData)
    if json.loads(getResponse.text)['code'] == 0:
        if json.loads(getResponse.text)['data'][0]['type'] == 0:
            id = json.loads(getResponse.text)['data'][0]['id']
            logId = json.loads(getResponse.text)['data'][0]['logId']
            text += "成功获取签到信息!\n"
            return 0
        else:
            text += '有3种情况：\n打卡还没开始,已经打卡过了,打卡时间已过(可能补救？)'
            title = '签到信息有误'
            return 1
    else:
        text += "获取签到页面失败！"
        title = "获取签到页面失败"
        return 2


# 签到函数（地点在学校范围内（鲜橙大临潼校区，其他学校的需要修改信息））
def doSign():
    global text, title
    signUrl = "https://student.wozaixiaoyuan.com/sign/doSign.json"
    signData = {
        "id": str(logId),
        "signId": str(id),
        "latitude": DoSignData.latitude,
        "longitude": DoSignData.longitude,
        "country": DoSignData.country,
        "province": DoSignData.province,
        "city": DoSignData.city,
        "district": DoSignData.district,
        "township": DoSignData.township
    }
    # signDataEncode = str(signData).encode("utf-8")
    signHeader = {
        "Host": "student.wozaixiaoyuan.com",
        "Connection": "keep-alive",
        #"Content-Length": "360",
        "charset": "utf-8",
        "content-type": "application/json",
        "jwsession": getJwsession("config.py"),
        "User-Agent": User_Agent,
        "Accept-Encoding": "gzip,compress,br,deflate",
        "Referer": "https://servicewechat.com/wxce6d08f781975d91/186/page-frame.html",
    }

    session3 = requests.session()
    signResponse = session3.post(signUrl, headers=signHeader, json=signData)
    if json.loads(signResponse.text)['code'] == 0:
        text += f"恭喜您，今日晚签到成功！"
        title = "晚签到成功"
    else:
        text += f"晚签到失败!原因为：\n{str(signResponse.text)}"
        title = '晚签到失败'


# 执行函数，正确的情况下会打卡，如果失败建议自己手动打卡
# 无论正确或者失败都会发送邮件并记录日志
def excute():
    flag2 = getSignMessage()
    if flag2 == 2:
        flag1 = login()
        if flag1:
            flag2 = getSignMessage()
            if flag2 == 0:
                doSign()
    elif flag2 == 0:
        doSign()
    print(title)
    print(text)
    sendmail(sender, user, pass_, title, text)
    log("mylog.txt", text)


if __name__ == '__main__':
    excute()
