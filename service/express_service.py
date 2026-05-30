#!/usr/bin/env python
# encoding: utf-8
import logging, random, requests, ssl, json
import config
import urllib.request as urllib2
from urllib.parse import urlencode

def query_express(number: str):
    """
    查询物流信息
    :param number: 物流单号
    :return:
    """
    url = f'https://slypass3.market.alicloudapi.com/express3?number={number}'
    headers = {"Authorization": f"APPCODE {config.WL.app_code}"}
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        logging.error(res.request.url)
        logging.error(res.request.headers)
    re_res = res.json()
    re_res['number'] = number
    #return res.json()
    return re_res

def query_express2(number: str):
    """
    查询物流信息
    :param number: 物流单号
    :return:
    """
    host = 'https://wuliu.market.alicloudapi.com'
    path = '/kdi'
    method = 'GET'
    appcode = config.WL.app_code
    querys = f"no={number}"
    url = host + path + '?' + querys
    header = {"Authorization": 'APPCODE ' + appcode}
    res = requests.get(url, headers=header)
    if res.status_code != 200:
        logging.error(res.request.url)
        logging.error(res.request.headers)
    re_res = res.json()
    re_res['number'] = number
    #return res.json()
    return re_res

# 注意，CST_ptdie100该模板ID仅为调试使用，调试结果为"status": "OK" ，即表示接口调用成功，然后联系客服报备自己的专属签名模板ID，以保证短信稳定下发
# def query_duanxin(number: str, data: str):
#     host = 'https://dfsns.market.alicloudapi.com'
#     path = '/data/send_sms'
#     method = 'POST'
#     appcode = '你自己的AppCode'
#     querys = ''
#     bodys = {}
#     url = host + path
#
#     bodys['content'] = '''code:%s''' % data
#     bodys['template_id'] = '''CST_ptdie100'''
#     bodys['phone_number'] = '''%s''' % number
#     post_data = urllib.urlencode(bodys)
#     # request = urllib2.Request(url, post_data)
#     request = urllib.request.Request(url=url, data=post_data, method='POST')
#     request.add_header('Authorization', 'APPCODE ' + appcode)
#     #//根据API的要求，定义相对应的Content-Type
#     request.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
#     ctx = ssl.create_default_context()
#     ctx.check_hostname = False
#     ctx.verify_mode = ssl.CERT_NONE
#     #urllib.request.urlopen(url, context=context)
#     # import urllib.request
#     #
#     # request = urllib.request.Request('http://www.example.com')
#     # with urllib.request.urlopen(request) as response:
#     #     html = response.read()
#     response = urllib.request.urlopen(request, context=ctx)
#     content = response.read().decode("utf-8", 'ignore')
#     # if (content):
#     #     print(content)
#     return content

def query_duanxin(phone: str, code: str = None):
    host = 'https://dfsns.market.alicloudapi.com'
    path = '/data/send_sms'
    method = 'POST'
    appcode = '397f6bc551ce40ce928a78e15029913c'
    querys = ''
    bodys = {}
    url = host + path
    if not code:
        code = str(random.randint(100000, 999999))
    bodys['content'] = '''code:%s''' % code
    bodys['template_id'] = '''CST_ptdie100'''
    bodys['phone_number'] = '''%s''' % phone
    post_data = urlencode(bodys).encode("utf-8")
    request = urllib2.Request(url, data=post_data, method=method)
    request.add_header('Authorization', 'APPCODE ' + appcode)
    # // 根据API的要求，定义相对应的Content - Type
    request.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    response = urllib2.urlopen(request, context=ctx)
    # content = response.read().decode("utf-8", 'ignore')
    content = response.read().decode("utf-8")
    # content = response.read()
    return content

