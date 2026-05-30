# -*- coding: utf-8 -*-
# flake8: noqa
import time
from config import QINIU

from qiniu import Auth, put_file, etag, urlsafe_base64_encode
from qiniu.compat import is_py2, is_py3

def get_upload_token(upname: str) -> str:
    """
    七牛上传token
    :param upname: 上传文件名
    :return: token string
    """
    # 构建鉴权对象
    q = Auth(QINIU.accessKey, QINIU.secretKey)
    # 要上传的空间
    bucket_name = QINIU.bucketName
    #有效期2小时的key
    extime = int(time.time()) + 60*2*60*60
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, upname, extime)
    return token

def get_download_url(httpurl: str) -> str:
    """
    七牛资源下载
    :httpurl: 如：http://task.yxiaozhu.com/5f59dace081de.jpg
    :return: http://task.yxiaozhu.com/5f59dace081de.jpg?e=1719126477&token=Mply7-4INH5tRfYBrYc8MTT-l2_0xhwUhXI4R7_i:BgAmqkA7x8MxR9mUULxq0-_RDzQ=
    """
    # 构建鉴权对象
    q = Auth(QINIU.accessKey, QINIU.secretKey)
    # 要上传的空间
    bucket_name = QINIU.bucketName
    #有效期2小时的key
    extime = int(time.time()) + 60*2*60*60
    # 生成上传 Token，可以指定过期时间等
    token = q.private_download_url(httpurl, expires=extime)
    return token

def qiniu_upload(filepath: str, upload_name: str):
    #需要填写你的 Access Key 和 Secret Key
    access_key = QINIU.accessKey
    secret_key = QINIU.secretKey
    #构建鉴权对象
    q = Auth(access_key, secret_key)
    #要上传的空间
    bucket_name = QINIU.bucketName
    #上传后保存的文件名
    # key = 'my-python-logo.png'
    key = upload_name
    #生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)
    #要上传文件的本地路径
    localfile = filepath
    #  dir(info)的属性、方法：
    # ['_ResponseInfo__check_json', '_ResponseInfo__response', '__class__', '__delattr__', '__dict__', '__dir__',
    #  '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__',
    #  '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__',
    #  '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'connect_failed',
    #  'exception', 'json', 'need_retry', 'ok', 'req_id', 'status_code', 'text_body', 'x_log']
    #info.text_body，返回文本str：‘{"hash":"Ft3_zcPtzqR9B-aZ1q5RaLxfLXze","key":"15cc3ae2-e818-11ef-9e46-00163e410368.jpg"}’
    #info.status_code，返回数字： 200
    ret, info = put_file(token, key, localfile, version='v2')
    if info.status_code == 200:
        return info.text_body
    else:
        return False
    # print(info)
    # assert ret['key'] == key
    # assert ret['hash'] == etag(localfile)