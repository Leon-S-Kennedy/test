import random
from Utils import GetAddress

sender = "*********"  # 推送信息：发件人的邮箱
pass_ = "*********"  # 推送信息：发件人邮箱授权码
user = "*********"  # 推送信息：收件人的邮箱

username = "***********"  # 用户名（一般是手机号）
password = "*********"  # 密码（建议改为全小写字母，我在校园的登录很麻烦）

# 以下为需要抓包的信息
# url：登录接口，这个是一样的
# User_Agent：用户设备信息
# Referer：页面来源（这个或许根据学校有不同？）
url = "https://gw.wozaixiaoyuan.com/basicinfo/mobile/login/username"
User_Agent = str("***")
Referer = "https://servicewechat.com/wxce6d08f781975d91/186/page-frame.html"

# 这个是登录凭证（每次登录会变，修改密码会变，过一段时间（半个月？）会变）
jwsession="************************************"


# 这个是健康打卡的信息
class SaveData:
    latitude, longitude = 34.36721, 109.18456  # 更改位置请修改这里
    latitude, longitude = latitude + random.randint(-10, 10) * 1e-5, longitude + random.randint(-10, 10) * 1e-5

    # 这是默认学校位置
    country = "中国"
    city = "西安市"
    district = "临潼区"
    province = "陕西省"
    township = "斜口街道"
    street = "西环路"
    areacode = "610115"
    towncode = "610115005"
    citycode = "156610100"

    # 更新位置函数（这个函数一般不用，一般回家后用一下然后在config中记录即可，毕竟key不是我的，不太好意思用。）
    # 只需要修改上面的经纬度，然后在save.py中去掉注释，健康打卡的时候就会自动根据经纬度获取位置信息
    @classmethod
    def setAddress(cls, latitude, longitude):
        address = GetAddress(latitude, longitude)
        saveAddress = address.getSave()
        cls.country = saveAddress['country']
        cls.city = saveAddress['city']
        cls.district = saveAddress['district']
        cls.province = saveAddress['province']
        cls.township = saveAddress['township']
        cls.street = saveAddress['street']
        cls.areacode = saveAddress['areacode']
        cls.towncode = saveAddress['towncode']
        cls.citycode = saveAddress['citycode']
        print(f"位置加载成功！\n{saveAddress}")


# 这个是晚签到信息（因为都在学校内部，所以直接写死）
class DoSignData:
    latitude = 34.36721218532986 + random.randint(-100, 100) * 1e-6
    longitude = 109.18456922743056 + random.randint(-100, 100) * 1e-6
    country = "中国"
    province = "陕西省"
    city = "西安市"
    district = "临潼区"
    township = "斜口街道"
