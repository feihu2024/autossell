from model.m_schema import *
from fastapi import APIRouter, Depends, Header, HTTPException, Request
from dao import d_admin, d_user, d_groupsir, d_order, d_db, d_partner
from model import m_admin
from typing import List
import datetime, re
from model import schema, m_schema
from service import express_service, share_fee_service
from common import Dao
from fastapi.responses import JSONResponse

async def verify_token(jinnengyuansession: str = Header(...)):
    #if jinnengyuansession != "fake-super-secret-token":
    if not d_admin.is_login(jinnengyuansession):
        raise HTTPException(status_code=400, detail="login invalid")

# async def verify_key(x_key: str = Header(...)):
#     if x_key != "fake-super-secret-key":
#         raise HTTPException(status_code=400, detail="X-Key header invalid")
#     return x_key

# router = APIRouter(dependencies=[Depends(verify_token), Depends(verify_key)])
router = APIRouter()
#
# @router.get(f'/users_data', response_model=m_admin.UserData, summary='查询会员总数 活跃会员 当日新增 男女比例')
# async def platform_userdata():
#     """
#     查询平台用户数据:  会员总数  活跃会员  当日新增  男女比例
#     """
#     user_data = d_admin.query_users()
#     return user_data
#
#
# @router.get(f'/silents_data', summary='查询不活跃用户名单')
# async def get_inactive_users(page: int = 1, page_size: int = 10) -> List[m_schema.CreateUser]:
#     """
#      获取非活跃用户名单
#     """
#     silents = d_admin.silent_users(page, page_size)
#     return [m_schema.CreateUser.parse_obj(t.__dict__) for t in silents]
#
#
# @router.get(f'/sales_data', response_model=m_admin.SaleData, summary='查询销售业绩')
# async def get_platform_data():
#     sale_data = d_admin.query_sales()
#     return sale_data


@router.post(f'/login', summary='管理登录')
async def admin_login(admin: m_admin.AdminRequest):
    """
    返回：jinnengyuansession携带到请求体head中，作为后端接口请求的token
    """
    username = admin.username
    password = admin.password
    res = d_admin.login_for_token(username, password)
    if res:
        content = {"message": "add cookie"}
        response = JSONResponse(content=content)
        token_val = res.get('token_val')
        response.set_cookie(key="jinnengyuansession", value=f"{token_val}")
        return {"key":"jinnengyuansession", "value":f"{token_val}", "user_id": res.get('user_id') }
    else:
        raise HTTPException(status_code=404, detail={'status': 404, 'massage': 'error'})

@router.post(f'/shop/login', summary='管理登录')
async def admin_login(admin: m_admin.AdminRequest):
    """
    返回：jinnengyuansession携带到请求体head中，作为后端接口请求的token
    """
    username = admin.username
    password = admin.password
    res = d_admin.login_shop_for_token(username, password)
    if res:
        content = {"message": "add cookie"}
        response = JSONResponse(content=content)
        token_val = res.get('token_val')
        response.set_cookie(key="jinnengyuansession", value=f"{token_val}")
        return {"key":"jinnengyuansession", "value":f"{token_val}", "user_id": res.get('user_id') }
    else:
        raise HTTPException(status_code=404, detail={'status': 404, 'massage': 'error'})

@router.get(f'/logintest', summary='获取测试token')
async def logintest():
    """
    返回：jinnengyuansession携带到请求体head中，作为后端接口请求的token
    """
    return d_admin.login_shop_token('admintest','kc1n6MVB',10)


#
# @router.post(f'/shop_login', summary='资金运营商家登录')
# async def shop_login(admin: m_admin.AdminRequest):
#     """
#     username:tom password:abcd
#     """
#     username = admin.username
#     password = admin.password
#     shop_info: List[m_schema.SShShop] = d_db.filter_sh_shop(items={'user_name': username, 'user_pass':password}, search_items={},
#                                                             set_items={})
#     if shop_info:
#         res = d_admin.login_shop_token(username, password, shop_info[0].id)
#         if shop_info[0].parent_id != 0:
#             pinpai_info: List[m_schema.SShShop] = d_db.filter_sh_shop(items={'id':shop_info[0].parent_id}, search_items={},
#                                                             set_items={})
#         else:
#             pinpai_info = shop_info
#         token_val = res.get('token_val')
#         return {"key":"kemaikemaisession", "value":f"{token_val}", "user_id": res.get('user_id'), "data":shop_info[0], "pinpai_data":pinpai_info[0] }
#     else:
#         raise HTTPException(status_code=404, detail={'status': 404, 'massage': 'error'})

@router.post(f'/login_out', summary='管理退出登录')
async def login_out():
    content = {"message": "del cookie"}
    response = JSONResponse(content=content)
    response.set_cookie(key="kemaikemaisession", value="****************")
    return response
#
# @router.post(f'/daily_add', response_model=int, summary='根据日期查询每日新增')
# async def user_daily_add(day: datetime.date = datetime.date.today()) -> int:
#     """
#     根据日期查询当日新增
#     """
#     return d_admin.query_daily_add(day)
#
#
# @router.get(f'/mall_tips', response_model=None, summary='查询商城提示 比如发货提现提醒')
# async def get_mall_tips():
#     return None
#
#
# @router.get(f'/get_relationships', summary='返回某个用户的推荐关系（上下层级都包括）')
# async def get_user_relationship(user_id:int = 0):
#     if user_id>0:
#         return d_user.get_recommend_users_tree(user_id)
#     else:
#         return {"status":400, "detail": "非法用户id"}

@router.post(f'/get_user_info', dependencies=[Depends(verify_token)], summary='返回某个用户的基本信息')
async def get_user_info(request: Request):
    jinnengyuansession = request.headers.get('jinnengyuansession')
    user_id = d_admin.get_login_id(jinnengyuansession)
    if user_id>0:
        return d_admin.get_admin_by_id(user_id)
    else:
        return {"status":400, "detail": "login error!"}

@router.post(f'/admin_update', dependencies=[Depends(verify_token)], response_model=str, summary='管理信息修改')
async def update_admin(item: SAdmin) -> str:
    d_db.update_admin(item)
    return "success"

@router.post(f'/admin_create', dependencies=[Depends(verify_token)], response_model=SAdmin, summary='创建管理员')
async def create_admin(item: CreateAdmin) -> SAdmin:
    dict_item = dict(item)
    for k,v in dict_item.items():
        if v is not None:
            v = str(v)
            v = v.replace(" ", "")
            get_search = re.search(r"'", v, flags=0)
            get_search2 = re.search(r'%27', v, flags=0)
            get_search3 = re.search(r'unionselect', v, flags=0)
            if get_search or get_search2 or get_search3:
               raise HTTPException(status_code=404, detail='bad way~~~~~~')

    return d_db.insert_admin(item)


@router.get(f'/level_filter', response_model=FilterResLevel, summary='后端管理角色列表')
async def level_filter(
        id: Optional[str] = None,
        title: Optional[str] = None,
        l_id: Optional[str] = None,
        l_title: Optional[str] = None,
        s_title: Optional[str] = None,
        order_by: Optional[str] = None,
        page: int = 1,
        page_size: int = 20) -> FilterResLevel:
    """
    1. 按照字段查询`?field1=value1&field2=value2`
    2. 按照范围查询，大于某个值`?field=value,`, 表示filed大于value
    3. 按照范围查询，小于某个值`?field=,value`， 表示field小于value
    4. 按照范围查询，范围值`?field=value1,value2`，表示搜索field大于等于value1，小于等于value2
    5. page是页数，第一页为1
    6. page_size为每一页大小， 默认20
    7. 如果是日期，请使用时间戳，十位的时间戳，单位：秒
    8. 所有字符串字段均可搜索，需要在字段前加个前缀`s_`,例如搜索`username`包含`zhang`， 则可以这样`s_username=zhang`写,这里只是一个假设
    9. 字段的多选择（in关系），需要在字段前加前缀`l_`,并且以逗号`,`隔开,例如要找出`id=2`或者`id=3`的样本，可以这样写`?l_id=2,3`
    """

    items = dict()
    search_items = dict()
    set_items = dict()

    if id is not None:
        values = id.split(',')
        if len(values) == 1:
            val = values[0]
            items['id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['id_start'] = int(val)

            val = values[1]
            if val != '':
                items['id_end'] = int(val)

    if title is not None:
        values = title.split(',')
        if len(values) == 1:
            val = values[0]
            items['title'] = val
        else:
            val = values[0]
            if val != '':
                items['title_start'] = val

            val = values[1]
            if val != '':
                items['title_end'] = val

    if s_title is not None:
        search_items['title'] = '%' + s_title + '%'

    if l_id is not None:
        values = l_id.split(',')
        values = [int(val) for val in values]
        set_items['id'] = values

    if l_title is not None:
        values = l_title.split(',')
        values = [val for val in values]
        set_items['title'] = values

    order_items = dict()
    if order_by is not None:
        orders = order_by.split(',')
        for order in orders:
            if order.startswith('-'):
                order_items[order[1:]] = 'desc'
            else:
                order_items[order] = 'asc'
    data = d_db.filter_level(items, search_items, set_items, order_items, page, page_size)
    c = d_db.filter_count_level(items, search_items, set_items)

    return FilterResLevel(data=data, total=c)

@router.get(f'/admin_filter', dependencies=[Depends(verify_token)], response_model=FilterResAdmin)
async def filter_admin(
        id: Optional[str] = None,
        username: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        level_id: Optional[str] = None,
        password: Optional[str] = None,
        id_card: Optional[str] = None,
        gender: Optional[str] = None,
        register_time: Optional[str] = None,
        last_active_time: Optional[str] = None,
        status: Optional[str] = None,
        business_id: Optional[str] = None,
        admin_id: Optional[str] = None,
        l_id: Optional[str] = None,
        l_username: Optional[str] = None,
        l_phone: Optional[str] = None,
        l_email: Optional[str] = None,
        l_level_id: Optional[str] = None,
        l_password: Optional[str] = None,
        l_id_card: Optional[str] = None,
        l_gender: Optional[str] = None,
        l_register_time: Optional[str] = None,
        l_last_active_time: Optional[str] = None,
        l_status: Optional[str] = None,
        l_business_id: Optional[str] = None,
        l_admin_id: Optional[str] = None,
        s_username: Optional[str] = None,
        s_phone: Optional[str] = None,
        s_email: Optional[str] = None,
        s_password: Optional[str] = None,
        s_id_card: Optional[str] = None,
        s_gender: Optional[str] = None,
        s_status: Optional[str] = None,
        order_by: Optional[str] = None,
        page: int = 1,
        page_size: int = 20) -> FilterResAdmin:
    """
    1. 按照字段查询`?field1=value1&field2=value2`
    2. 按照范围查询，大于某个值`?field=value,`, 表示filed大于value
    3. 按照范围查询，小于某个值`?field=,value`， 表示field小于value
    4. 按照范围查询，范围值`?field=value1,value2`，表示搜索field大于等于value1，小于等于value2
    5. page是页数，第一页为1
    6. page_size为每一页大小， 默认20
    7. 如果是日期，请使用时间戳，十位的时间戳，单位：秒
    8. 所有字符串字段均可搜索，需要在字段前加个前缀`s_`,例如搜索`username`包含`zhang`， 则可以这样`s_username=zhang`写,这里只是一个假设
    9. 字段的多选择（in关系），需要在字段前加前缀`l_`,并且以逗号`,`隔开,例如要找出`id=2`或者`id=3`的样本，可以这样写`?l_id=2,3`
    """

    items = dict()
    search_items = dict()
    set_items = dict()

    if id is not None:
        values = id.split(',')
        if len(values) == 1:
            val = values[0]
            items['id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['id_start'] = int(val)

            val = values[1]
            if val != '':
                items['id_end'] = int(val)

    if username is not None:
        values = username.split(',')
        if len(values) == 1:
            val = values[0]
            items['username'] = val
        else:
            val = values[0]
            if val != '':
                items['username_start'] = val

            val = values[1]
            if val != '':
                items['username_end'] = val

    if phone is not None:
        values = phone.split(',')
        if len(values) == 1:
            val = values[0]
            items['phone'] = val
        else:
            val = values[0]
            if val != '':
                items['phone_start'] = val

            val = values[1]
            if val != '':
                items['phone_end'] = val

    if email is not None:
        values = email.split(',')
        if len(values) == 1:
            val = values[0]
            items['email'] = val
        else:
            val = values[0]
            if val != '':
                items['email_start'] = val

            val = values[1]
            if val != '':
                items['email_end'] = val

    if level_id is not None:
        values = level_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['level_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['level_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['level_id_end'] = int(val)

    if password is not None:
        values = password.split(',')
        if len(values) == 1:
            val = values[0]
            items['password'] = val
        else:
            val = values[0]
            if val != '':
                items['password_start'] = val

            val = values[1]
            if val != '':
                items['password_end'] = val

    if id_card is not None:
        values = id_card.split(',')
        if len(values) == 1:
            val = values[0]
            items['id_card'] = val
        else:
            val = values[0]
            if val != '':
                items['id_card_start'] = val

            val = values[1]
            if val != '':
                items['id_card_end'] = val

    if gender is not None:
        values = gender.split(',')
        if len(values) == 1:
            val = values[0]
            items['gender'] = val
        else:
            val = values[0]
            if val != '':
                items['gender_start'] = val

            val = values[1]
            if val != '':
                items['gender_end'] = val

    if register_time is not None:
        values = register_time.split(',')
        if len(values) == 1:
            val = values[0]
            items['register_time'] = datetime.fromtimestamp(int(val))
        else:
            val = values[0]
            if val != '':
                items['register_time_start'] = datetime.fromtimestamp(int(val))

            val = values[1]
            if val != '':
                items['register_time_end'] = datetime.fromtimestamp(int(val))

    if last_active_time is not None:
        values = last_active_time.split(',')
        if len(values) == 1:
            val = values[0]
            items['last_active_time'] = datetime.fromtimestamp(int(val))
        else:
            val = values[0]
            if val != '':
                items['last_active_time_start'] = datetime.fromtimestamp(int(val))

            val = values[1]
            if val != '':
                items['last_active_time_end'] = datetime.fromtimestamp(int(val))

    if status is not None:
        values = status.split(',')
        if len(values) == 1:
            val = values[0]
            items['status'] = val
        else:
            val = values[0]
            if val != '':
                items['status_start'] = val

            val = values[1]
            if val != '':
                items['status_end'] = val

    if business_id is not None:
        values = business_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['business_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['business_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['business_id_end'] = int(val)

    if admin_id is not None:
        values = admin_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['admin_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['admin_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['admin_id_end'] = int(val)

    if s_username is not None:
        search_items['username'] = '%' + s_username + '%'

    if s_phone is not None:
        search_items['phone'] = '%' + s_phone + '%'

    if s_email is not None:
        search_items['email'] = '%' + s_email + '%'

    if s_password is not None:
        search_items['password'] = '%' + s_password + '%'

    if s_id_card is not None:
        search_items['id_card'] = '%' + s_id_card + '%'

    if s_gender is not None:
        search_items['gender'] = '%' + s_gender + '%'

    if s_status is not None:
        search_items['status'] = '%' + s_status + '%'

    if l_id is not None:
        values = l_id.split(',')
        values = [int(val) for val in values]
        set_items['id'] = values

    if l_username is not None:
        values = l_username.split(',')
        values = [val for val in values]
        set_items['username'] = values

    if l_phone is not None:
        values = l_phone.split(',')
        values = [val for val in values]
        set_items['phone'] = values

    if l_email is not None:
        values = l_email.split(',')
        values = [val for val in values]
        set_items['email'] = values

    if l_level_id is not None:
        values = l_level_id.split(',')
        values = [int(val) for val in values]
        set_items['level_id'] = values

    if l_password is not None:
        values = l_password.split(',')
        values = [val for val in values]
        set_items['password'] = values

    if l_id_card is not None:
        values = l_id_card.split(',')
        values = [val for val in values]
        set_items['id_card'] = values

    if l_gender is not None:
        values = l_gender.split(',')
        values = [val for val in values]
        set_items['gender'] = values

    if l_register_time is not None:
        values = l_register_time.split(',')
        values = [datetime.fromtimestamp(int(val)) for val in values]
        set_items['register_time'] = values

    if l_last_active_time is not None:
        values = l_last_active_time.split(',')
        values = [datetime.fromtimestamp(int(val)) for val in values]
        set_items['last_active_time'] = values

    if l_status is not None:
        values = l_status.split(',')
        values = [val for val in values]
        set_items['status'] = values

    if l_business_id is not None:
        values = l_business_id.split(',')
        values = [int(val) for val in values]
        set_items['business_id'] = values

    if l_admin_id is not None:
        values = l_admin_id.split(',')
        values = [int(val) for val in values]
        set_items['admin_id'] = values

    order_items = dict()
    if order_by is not None:
        orders = order_by.split(',')
        for order in orders:
            if order.startswith('-'):
                order_items[order[1:]] = 'desc'
            else:
                order_items[order] = 'asc'
    data = d_db.filter_admin(items, search_items, set_items, order_items, page, page_size)
    c = d_db.filter_count_admin(items, search_items, set_items)

    return FilterResAdmin(data=data, total=c)

@router.post(f'/modify_platform_regist', dependencies=[Depends(verify_token)], summary='修改注册协议')
async def modify_platform_regist(item: SPlatformLaw):
    item.id = 49
    d_db.update_platform_law(item)
    return "success"

@router.post(f'/modify_platform_self', dependencies=[Depends(verify_token)], summary='修改隐私政策')
async def modify_platform_self(item: SPlatformLaw):
    item.id = 50
    d_db.update_platform_law(item)
    return "success"

@router.get(f'/getregist', dependencies=[Depends(verify_token)], response_model=m_schema.SPlatformLaw, summary='后端回显注册协议')
async def get_platform_text():
    platform_id = 49
    return d_db.get_platform_law(platform_law_id=platform_id)

@router.get(f'/getself', dependencies=[Depends(verify_token)], response_model=m_schema.SPlatformLaw, summary='后端回显隐私政策')
async def get_platform_self():
    platform_id = 50
    return d_db.get_platform_law(platform_law_id=platform_id)

@router.get(f'/get_invited_user', dependencies=[Depends(verify_token)], summary='分页获取直推（团队）用户列表')
async def get_invited_user(request: Request, user_id:int = 0, page:int = 1):
    """
    分页获取推荐用户列表
    """
    return d_user.get_invited_user_to_page(user_id, page)

@router.post(f'/user/set/sh_agent', dependencies=[Depends(verify_token)], response_model=str, summary='修改会员市代身份')
async def update_admin(item: m_admin.SdAgent) -> str:
    """
     user_id:      '用户id', default=0)
    sd_agent:     '市代设置', default=0)
    """
    uinfo=d_user.get_user_by_id(item.user_id)
    if uinfo:
        if item.sd_agent > 0:
            if uinfo.is_tuan > 0:
                d_user.update_user_sd_agent(item.user_id, item.sd_agent)
                return "success"
            else:
                return "请先设置团长"
        else: #取消
            d_user.update_user_sd_agent(item.user_id, 0)
            return "success"
    else:
        return "未知用户"



