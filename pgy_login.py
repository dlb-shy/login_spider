# -*- coding: utf-8 -*-
import hashlib
import time

import requests
session = requests.session()
import json

token = ''


def sign(_0x6ad198):
    _0x59d459 = "A4NjFqYu5wPHsO0XTdDgMa2r1ZQocVte9UJBvk6/7=yRnhISGKblCWi+LpfE8xzm3"
    _0x2d2acc = ''
    _0xf24116 = 0
    while _0xf24116 < 32:
        _0x312581 = ord(_0x6ad198[_0xf24116])
        _0xf24116 = _0xf24116 + 1
        _0x11fbd2 = ord(_0x6ad198[_0xf24116])
        _0xf24116 = _0xf24116 + 1
        if _0xf24116 < 32:
            _0x3381c3 = ord(_0x6ad198[_0xf24116])
        else:
            _0x3381c3 = 'nan'
        _0xf24116 = _0xf24116 + 1
        # print(_0x312581, _0x11fbd2, _0x3381c3)
        _0x3df8b2 = _0x312581 >> 0x2
        _0x1e474a = (_0x312581 & 0x3) << 0x4 | _0x11fbd2 >> 0x4
        if _0x3381c3 == 'nan':
            _0x208c02 = (_0x11fbd2 & 0xf) << 0x2
        else:
            _0x208c02 = (_0x11fbd2 & 0xf) << 0x2 | _0x3381c3 >> 0x6
        if _0x3381c3 == 'nan':
            _0x155a6e = 0
        else:
            _0x155a6e = _0x3381c3 & 0x3f
        # print(_0x3df8b2, _0x1e474a, _0x208c02, _0x155a6e)
        # if _0x11fbd2 == 0:
        #     _0x208c02 = _0x155a6e = 0x40
        if _0x3381c3 == 'nan':
            _0x155a6e = 0x40
        _0x2d2acc = _0x2d2acc + _0x59d459[_0x3df8b2] + _0x59d459[_0x1e474a] + _0x59d459[_0x208c02] + _0x59d459[_0x155a6e]
        # print(_0x2d2acc)
    # print(_0x2d2acc)
    return _0x2d2acc


def get_sign(url, t):
    # iamspam
    now_time = 1624970584034  # int(time.time() * 1000)
    if 'mcns' in url:
        key = 'iamspam'
    else:
        key = 'test'
    api_str = str(now_time) + key + url + t
    md5_str = hashlib.md5(api_str.encode('utf-8')).hexdigest()
    # print(now_time)
    # print(md5_str)
    x_s = sign(md5_str)
    x_t = now_time
    print(x_s)
    return x_t, x_s


def login_pgy(user, pwd):
    # register
    url = "https://www.xiaohongshu.com/fe_api/burdock/v2/shield/registerCanvas?p=cc&callFrom=web"

    payload = json.dumps({
      "sign": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36~~~false~~~zh-CN~~~24~~~8~~~4~~~-480~~~Asia/Shanghai~~~1~~~1~~~1~~~1~~~unknown~~~Win32~~~Chrome PDF Plugin::Portable Document Format::application/x-google-chrome-pdf~pdf,Chrome PDF Viewer::::application/pdf~pdf,Native Client::::application/x-nacl~,application/x-pnacl~~~~canvas winding:yes~canvas fp:af63627abb7f6d68a8cd864315e785a9~~~false~~~false~~~false~~~false~~~false~~~0;false;false~~~4;7;8~~~124.04347527516074",
      "id": "9b9f4d59283cea39a194022ad76aa9cb"
    })
    url_str = '/fe_api/burdock/v2/shield/registerCanvas?p=cc&callFrom=web'
    t = payload
    x_t, x_s = get_sign(url_str, t)
    headers = {
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
      'x-b3-traceid': '879915d9a01290a5',

      'x-sign': 'X6e6b2af96dec7817ca5f4ed2360b68d7',
      'x-s': x_s,
      'x-t': str(x_t),
      'Content-Type': 'application/json',
    }

    response = session.request("POST", url, headers=headers, data=payload)

    print(response.text)
    print(response.cookies)
    cookie_dict1 = requests.utils.dict_from_cookiejar(response.cookies)
    print(cookie_dict1)

    # send msg
    url = f"https://customer.xiaohongshu.com/api/cas/sendCode?phone={user}&zone=86"

    url_str = f'/api/cas/sendCode?phone={user}&zone=86'
    t = ""
    x_t, x_s = get_sign(url_str, t)
    headers = {
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
      'x-s': x_s,
      'x-t': str(x_t),
    }
    print(headers)
    response = session.request("GET", url, headers=headers,)
    print(response.text)
    print(response.cookies)
    cookie_dict2 = requests.utils.dict_from_cookiejar(response.cookies)
    cookie_dict2 = {**cookie_dict2, **cookie_dict1}

    # get VerifyCode
    time.sleep(10)
    url = "https://api.sl.willanddo.com/api/msg/getMsgList?lastId=0"
    payload = {}
    headers = {
        'token': token
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    result = response.json()['result'][-1]
    # print(result)
    content = result['content']
    verifyCode = content.split('验证码是: ')[-1].split('，5分钟')[0]

    # login
    url = f"https://customer.xiaohongshu.com/api/cas/loginWithVerifyCode"

    payload = json.dumps({"zone":"86","mobile": user,"verifyCode":verifyCode,"service":"https://business.xiaohongshu.com"})
    print(payload)
    url_str = '/api/cas/loginWithVerifyCode'
    t = payload
    x_t, x_s = get_sign(url_str, t)
    headers = {
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
      'x-s': x_s,
      'x-t': str(x_t),
      'Content-Type': 'application/json',
    }

    response = session.request("POST", url, headers=headers, data=payload)

    print('\n\n')
    print(response.status_code)
    print(response.text)

    print(response.cookies)
    cookie_dict3 = requests.utils.dict_from_cookiejar(response.cookies)
    cookie_dict3 = {**cookie_dict3, **cookie_dict2}
    cookie_str = ''
    for k,v in cookie_dict3.items():
        cookie_str = cookie_str + k + '=' + v + ';'
    print(cookie_dict3)


# login_pgy(user="", pwd="")

