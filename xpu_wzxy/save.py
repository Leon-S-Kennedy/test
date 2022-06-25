import hashlib
from urllib.parse import urlencode
import json
from xpu_wzxy.Utils import *
from xpu_wzxy.config import *

text = ""  # 初始化邮件内容
title = ""  # 初始化邮件标题


# 登录函数（登录时不能打开我在校园，登录不上建议改密码，清缓存，然后过一会再登录。能不登录就不登录吧。）
def login():
    global text, jwsession, title

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
    loginResponse = session1.post(loginUrl, headers=loginHeader, data=loginData)  # 发送登录请求

    if json.loads(loginResponse.text)["code"] == 0:
        text = "健康打卡登录成功！\n"
        jwsession = loginResponse.headers['JWSESSION']
        setJwsession("config.py", jwsession)
        return True
    else:
        text = "健康打卡登录失败！\n"
        text += f"{json.loads(loginResponse.text)['message']}"
        title = "健康打卡登录失败"
        return False


# 健康打卡函数（answers根据自己健康打卡的问题来决定）
# signatureHeader的格式感谢”时周“大佬。
def save():
    global text, title

    saveUrl = "https://student.wozaixiaoyuan.com/health/save.json"
    curTime = int(round(time.time() * 1000))
    saveData = {
        "answers": '["0","1","1","1","0","湖北省荆州市石首市笔架山街道"]',  # 在此自定义answers字段
        "latitude": SaveData.latitude,
        "longitude": SaveData.longitude,
        "country": SaveData.country,
        "city": SaveData.city,
        "district": SaveData.district,
        "province": SaveData.province,
        "township": SaveData.township,
        "street": SaveData.street,
        "areacode": SaveData.areacode,  # 临潼区
        "towncode": SaveData.towncode,  # 斜口街道
        "citycode": SaveData.citycode,  # 西安市
        "timestampHeader": curTime,
        "signatureHeader": hashlib.sha256(f"{SaveData.province}_{curTime}_{SaveData.city}".encode("utf-8")).hexdigest(),
    }
    data = urlencode(saveData)
    Content_Length = len(data)
    saveHeader = {
        "Host": "student.wozaixiaoyuan.com",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "User-Agent": User_Agent,
        "Referer": Referer,
        "Content-Length": str(Content_Length),
        "JWSESSION": getJwsession("config.py"),
    }
    session2 = requests.session()
    saveResponse = session2.post(saveUrl, headers=saveHeader, data=data).json()
    if saveResponse['code'] == 0:
        text += "恭喜您，今日健康打卡成功！"
        title = "健康打卡成功"
        return False
    else:
        text += f"健康打卡失败!原因为：\n{str(saveResponse)}"
        title = "健康打卡失败"
        return True


# 执行函数，正确的情况下会打卡，如果失败建议自己手动打卡
# 无论正确或者失败都会发送邮件并记录日志
def excute():
    # SaveData.setAddress(SaveData.latitude,SaveData.longitude)      #更改健康打卡位置时请去掉注释（位置在配置文件中修改）
    isErr = save()
    if isErr:
        flag = login()
        if flag:
            save()
    print(title)
    print(text)
    sendmail(sender, user, pass_, title, text)
    log("mylog.txt", text)


if __name__ == '__main__':
    excute()
