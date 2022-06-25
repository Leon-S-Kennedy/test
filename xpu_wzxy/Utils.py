import requests
import smtplib
import time
from email.mime.text import MIMEText
from email.utils import formataddr

"""
腾讯坐标拾取系统：https://lbs.qq.com/getPoint/
"""


# 获取jwsession的函数（因为导入后就不会变了，但是我们在登录后是变化的，只能以读文件的方式来获取）
def getJwsession(filePath):
    with open(filePath, "r", encoding="utf-8") as f:
        list = f.readlines()
        for line in list:
            if "jwsession" in line:
                return line.split('"')[1]


# 将登录后的jwsession缓存下来的函数（避免每次都要登录，登录比较麻烦）
def setJwsession(filePath, jwsession):
    new_jwsession = f'jwsession="{jwsession}"\n'
    with open(filePath, "r", encoding="utf-8") as f:
        list = f.readlines()
    with open(filePath, "w", encoding="utf-8") as f_w:
        for line in list:
            if "jwsession" in line:
                f_w.write(new_jwsession)
            else:
                f_w.write(line)


# 发送邮件的函数，参数在config.py文件中
def sendmail(sender, user, pass_, title, text):
    msg = MIMEText(text, 'plain', 'utf-8')  # 邮件的正文部分
    msg['From'] = formataddr(("我在校园", sender))  # 发件人邮箱昵称、发件人邮箱账号
    msg['Subject'] = title  # 邮件的主题，也可以说是标题
    server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器
    server.login(sender, pass_)  # 发件人邮箱账号、邮箱授权码
    server.sendmail(sender, [user, ], msg.as_string())  # 发件人邮箱账号、收件人邮箱账号、发送邮件
    server.quit()  # 关闭连接


# 记录日志文件的函数
def log(path, mylog):
    with open(path, "a+", encoding="utf-8") as log:
        log.write("--------------------------------------------------\n")
        log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}\n")
        log.write(f"{mylog}\n")


# 获取地址的类（key不是我的，要用自己申请）
class GetAddress:
    def __init__(self, latitude, longitude):
        api = f"https://apis.map.qq.com/ws/geocoder/v1/?key=A3YBZ-NC5RU-MFYVV-BOHND-RO3OT-ABFCR&location={latitude},{longitude}"
        response = requests.get(api).json()
        self.ad_info = response['result']['ad_info']
        self.address_reference = response['result']['address_reference']
        self.address_component = response['result']['address_component']

    # 对于晚签到的7个信息
    # 签到区域限定为学校，所以这个基本没用，请假了这个就不用签了
    def getSign(self):
        getSignData = {
            'country': self.ad_info['nation'],
            'province': self.ad_info['province'],
            'city': self.ad_info['city'],
            'district': self.ad_info['district'],
            'township': self.address_reference['town']['title'],
        }
        return getSignData

    # 对于健康打卡的9个信息
    def getSave(self):
        getSaveData = {
            'country': self.ad_info['nation'],
            'city': self.ad_info['city'],
            'district': self.ad_info['district'],
            'province': self.ad_info['province'],
            'township': self.address_reference['town']['title'],
            'street': self.address_component['street'],
            'areacode': self.ad_info['adcode'],  # 对应所在区县
            'towncode': self.address_reference['town']['id'],  # 对应所在街道
            'citycode': self.ad_info['city_code'],  # 对应所在市
        }
        return getSaveData
