#! python3
# -*-coding:utf-8-*-
import json
import os
import sys

import pywifi
import base64
import time
import requests


def wifi_list():
    wifi = pywifi.PyWiFi()  # 创建实例
    iface = wifi.interfaces()[0]  # 调用网卡
    iface.scan()  # 扫描
    time.sleep(2)  # 延迟两秒
    wifi_l = iface.scan_results()  # 所有WiFi数据
    wifi = [(i.ssid, i.signal, i) for i in wifi_l]
    # 根据信号强弱排序，并去除重复名称
    wifi.sort(key=lambda x: x[1], reverse=True)
    lTemp = {}
    for i in wifi:
        if i[0] not in lTemp.keys():
            lTemp[i[0]] = i[1]
    wifi = list(lTemp.items())
    return wifi


def cntwifi(l):  # 连接wifi：优先连接5G的
    suda_wifi = []
    for i in l:
        if "SUDA_WIFI_5G" == i[0]:
            suda_wifi.append(i)
        if "SUDA_WIFI" == i[0]:
            suda_wifi.append(i)
    suda_wifi.sort(reverse=True)
    if suda_wifi:
        print("正在连接的网络为：{}".format(suda_wifi[0][0]))
        wifi_n = suda_wifi[0][0]
    else:
        raise RuntimeError('无苏大WiFi！')

    profile = pywifi.Profile()  # 创建wifi配置实例
    profile.ssid = wifi_n  # 配置名称
    wifi = pywifi.PyWiFi()  # 创建wifi实例
    iface = wifi.interfaces()[0]  # 调用网卡
    profile = iface.add_network_profile(profile)  # 配置wifi信息
    iface.connect(profile)  # 连接wifi


def login(username, password, kind=1):
    '''
    登陆苏大网管
    :param username:学号
    :param password: 密码
    :param kind: 0-计时登陆，1-包月登陆
    :return:
    '''
    # data
    data = 'username={}&domain=&password={}&enablemacauth={}'.format(username,
                                                                     base64.b64encode(password.encode('utf-8')).decode(
                                                                         'utf8'), kind)
    if kind == 1:
        print('您采用的是包月登陆，当天连接WIFI，不需要再次登陆。')
    else:
        print('您采用的是计时登陆，当天连接WIFI，需要再次登陆。')
    # 头信息
    header = {
        'Host': 'a.suda.edu.cn',
        'Connection': 'keep-alive',
        'Content-Length': '77',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Origin': 'http://a.suda.edu.cn',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 8.0.0; zh-CN; MI 6 Build/OPR1.170623.027) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 Quark/2.5.2.940 Mobile Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'http://a.suda.edu.cn/index.php?url=aHR0cDovL3dnLnN1ZGEuZWR1LmNuLw==',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
    }
    while True:
        try:
            res = requests.post('http://a.suda.edu.cn/index.php/index/login',
                                data=data, headers=header)
            break
        except Exception as e:
            print("==========================================")
            print("Connection refused by the server..")
            print("Let me try again")
            print("Was a nice sleep, now let me continue...")
            continue
    res = res.content.decode("unicode-escape")  # 编码解析
    res = json.loads(res)  # 将返回的字典字符，转为字典
    print('结果:', res['info'])
    print('3s后自动关闭')
    time.sleep(3)


# input("回车结束")
def main():
    print('正在搜索WIFI...')
    wifi_l = wifi_list()  # WiFi列表
    print('正在连接苏大WIFI...')
    cntwifi(wifi_l)  # 连接wifi
    # 登陆：包月或者计时
    print('正在登陆...')
    # TODO: 输入学号密码，注意不要泄露
    login('学号', '密码')


if __name__ == '__main__':
    main()
