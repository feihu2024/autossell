from fastapi import Depends, FastAPI, Header, HTTPException, Request
from typing import List, Optional
import random, datetime
import string, uuid
from common import global_define

async def verify_token(request: Request,call_next, accept_encoding:Optional[str] = Header(None)):
    print('--------------------------header--------------------------')
    print(accept_encoding)
    print(request.headers)
    print(request.url)
    print(request.url.path)
    raise HTTPException(status_code=400, detail="x_token 未定义！")


#reversed dict
def reversed_dict(data:dict):
    re_data = {}
    for d in list(reversed(data.keys())):
        re_data[d] = data[d]
    return re_data

def get_randoms(num:int):
    token = string.ascii_letters + string.digits
    token = random.sample(token,num)
    token = ''.join(token)
    return token

def explain_headtoken(timeuser):
    mychar = global_define.valid_char
    token =  timeuser[int(len(timeuser)/2):] + timeuser[0:int(len(timeuser)/2)]
    for i, val in enumerate(mychar):
        if i==10:
            token = token.replace(val, ',')
        else:
            token = token.replace(val, str(i))
    return token

def get_headtoken(timeuser):
    token =  timeuser[int(len(timeuser)/2):] + timeuser[0:int(len(timeuser)/2)]
    return token

def get_current_zhouqi():
    date_list = str(datetime.date.today()).split('-')
    return int("%s%s"%(date_list[0],date_list[1]))


def is_simple_password(password):
    if len(password) < 6:  # 通常认为6个字符以下的密码是简单的
        return True
    if password.isdigit() or password.isalpha():  # 纯数字或纯字母的密码通常认为是简单的
        return True
    if password in global_define.common_passwords:
        return True
    # 可以添加更多的判断逻辑，例如检查是否为常见模式（如连续数字、键盘模式等）
    return False

def get_num32_randoms():
    return str.upper(str(uuid.uuid4()).replace('-',''))