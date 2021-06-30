# -*- coding: utf-8 -*-
import base64
import binascii
import json
import time

import requests as requests
import rsa

token = ''  # 获取验证码的token


def get_sp(servertime, nonce, password):
    pubkey = 'EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443'
    public_key = rsa.PublicKey(int(pubkey, 16), int('10001', 16))
    password_str = str(servertime) + '\t' + str(nonce) + '\n' + password
    sp = binascii.b2a_hex(rsa.encrypt(password_str.encode('utf8'), public_key)).decode('utf8')
    return sp


def login(user):
    # init nonce servertime
    session = requests.session()
    su = base64.b64encode(user.encode()).decode()
    # print(su)
    url = f"https://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su={su}&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.19)&_={int(time.time() * 1000)}"
    # print(url)
    headers = {
        'Accept': '*/*',
        'Host': 'login.sina.com.cn',
        'Referer': 'https://weibo.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    }
    response = session.request("GET", url, headers=headers)
    # print(response.text)
    result = json.loads(response.text.replace('sinaSSOController.preloginCallBack(', '')[:-1])
    nonce = result['nonce']
    servertime = result['servertime']
    rsakv = result['rsakv']
    pcid = result['pcid']
    if 'smsurl' in result.keys():
        ##########################
        # user is exist
        smsurl = result['smsurl']
        # print(smsurl)
        # send msg
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
        }
        response = session.request("GET", smsurl, headers=headers)
        # print(response.text)
        if response.json()['retcode'] == 20000000:
            print(response.json()['msg'])
            # wait 10s get verifycode
            time.sleep(10)
            url = "https://api.sl.willanddo.com/api/msg/getMsgList?lastId=0"
            payload = {}
            headers = {
                'token': token
            }
            response = session.request("GET", url, headers=headers, data=payload)
            result = response.json()['result'][-1]
            # print(result)
            content = result['content']
            verifyCode = content.split('验证码：')[-1].split('。此验证码')[0]
            print("验证码：", verifyCode)
            sp = get_sp(servertime=servertime,nonce=nonce,password=verifyCode)
            # login
            url = "https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)&wsseretry=servertime_error"

            payload = {'entry': 'weibo',
                       'gateway': '1',
                       'from': '',
                       'savestate': '7',
                       'qrcode_flag': 'false',
                       'useticket': '1',
                       'pagerefer': '',
                       'wsseretry': 'servertime_error',
                       'cfrom': '1',
                       'vsnf': '1',
                       'su': su,
                       'service': 'miniblog',
                       'servertime': str(servertime),
                       'nonce': nonce,
                       'pwencode': 'rsa2',
                       'rsakv': rsakv,
                       'sp': sp,
                       'sr': '1366*768',
                       'encoding': 'UTF-8',
                       'prelt': '19',
                       'url': 'https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
                       'returntype': ' META'
                       }
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                'Content-Length': '658',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Host': 'login.sina.com.cn',
                'Origin': 'https://weibo.com',
                'Referer': 'https://weibo.com/',
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
                'sec-ch-ua-mobile': '?0',
                'Sec-Fetch-Dest': 'iframe',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'cross-site',
                'Sec-Fetch-User': '?1',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
            }

            response = session.request("POST", url, headers=headers, data=payload)
            print('login')
            # print(response.cookies)
            cookie_dict = requests.utils.dict_from_cookiejar(response.cookies)
            return cookie_dict


        else:
            print(response.text)
    else:
        print('user is not activate')


if __name__ == '__main__':

    login("xxx") # 手机号

