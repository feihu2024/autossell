from dao import d_order, d_db, d_admin
from fastapi import APIRouter, Body, Depends, Header, Request
from model.mall import m_order
from model import m_schema
from router import r_schema
import datetime
from config import DIRS, DOMAIN
from pathlib import Path
import uuid
from common import global_define
from pydantic import Field
from typing import Optional, List
import math
from router.admin.user import verify_token
from pydantic import BaseModel, Field
from fastapi.exceptions import HTTPException

router = APIRouter(dependencies=[Depends(verify_token)])


@router.post(f'/send_order/get', response_model=m_order.ASendMsgList, summary='获取订单列表')
async def get_sends(item: m_order.AOrderRequest) -> m_order.ASendMsgList:
    """
    供应商，暂时不设置
    规格、价格，zdyspec,这个里存的是json，需要解析,如：{"规格":"1瓶装","库存":"0","克重":"0","成本":"0","售价":"199","会员价":"0","直推":"0"}
    收货人地址，consignee_address
    备注，detail
    状态，status_id  (字段以标注，swager)
    """
    return await d_order.get_send_orders(item, order='desc')

@router.post(f'/send_order/shoper/get', response_model=m_order.ASendMsgList, summary='获取商家订单列表')
async def get_sends_shoper(request: Request, item: m_order.AOrderRequestShoper) -> m_order.ASendMsgList:
    """
    供应商，暂时不设置
    规格、价格，zdyspec,这个里存的是json，需要解析,如：{"规格":"1瓶装","库存":"0","克重":"0","成本":"0","售价":"199","会员价":"0","直推":"0"}
    收货人地址，consignee_address
    备注，detail
    状态，status_id  (字段以标注，swager)
    """
    welcomesession = request.headers.get('jinnengyuansession')
    user_id = d_admin.get_login_id(welcomesession)
    if not user_id:
        raise HTTPException(status_code=400, detail='please login')
    item.supplier_id = user_id
    return await d_order.get_send_shoper_orders(item, order='desc')

class Updatedetail(BaseModel):
    order_id: int = Field(title='订单id')
    detail: str = Field(title='备注内容')

@router.post(f'/send_order/export', summary='发货订单导出')
async def get_export(item: m_order.AOrderRequest):
    """
    根据搜索条件，获取发货订单导出
    """
    data = await d_order.get_send_orders(item, order='desc')
    data_d = data.data
    data_t = data.total
    down_url = ""
    if data_t > 0:
        file_type = 'file'
        file_date = f'{datetime.date.today()}'
        file_name = f'{uuid.uuid1()}export.csv'
        file_dir = Path(DIRS.assets_dir) / file_type / file_date
        file_dir.mkdir(parents=True, exist_ok=True)
        file_path = file_dir / file_name
        content = "线上订单号,下单时间,买家id,卖家备注,买家留言,运费,付款金额,收货人姓名（必填）,手机（必填）,省份（必填）,城市（必填）,区县（必填）,地址（必填）,商品编码（必填）,商品名称,颜色及规格,数量（必填）,商品单价（必填）,状态,规格编码 \r\n"
        # for i in data_d:
        #     d = dict(i)
        #     if d['s_Order'] is None or d['s_Good'] is None or d['s_GoodSpec'] is None:
        #         continue
        #     if d['s_Order'].paid_amount is None:
        #         d['s_Order'].paid_amount = 0
        #     if d['s_Order'].paid_balance is None:
        #         d['s_Order'].paid_balance = 0
        #     content += ','.join([str(d['s_Order'].id), str(d['s_Order'].create_time), str(d['s_Order'].paider_id),'','',str(d['s_Order'].delivery_fee), str(d['s_Order'].paid_amount + d['s_Order'].paid_balance), \
        #                          str(d['s_Order'].consignee_name), str(d['s_Order'].consignee_phone), str(d['s_Order'].consignee_province), str(d['s_Order'].consignee_city), str(d['s_Order'].consignee_area), str(d['s_Order'].consignee_description), \
        #                          str(d['s_Order'].good_id), str(d['s_Good'].title), "/".join([str(d['s_GoodSpec'].value), str(d['s_GoodSpec'].spec_num)]), str(d['s_Order'].number), str(d['s_Order'].sale_price), str(d['s_Order'].status_id)])
        #     content += '\r\n'
        content += d_order.create_export_content(data_d)
        with open(str(file_path), 'a') as f:
            f.write(content)
        pages = math.ceil(data_t / item.page_size)
        for c in range(2, pages):
            item.page = c
            data = await d_order.get_send_orders(item, order='desc')
            content = d_order.create_export_content(data.data)
            with open(str(file_path), 'a') as f:
                f.write(content)

    down_url = DOMAIN + '/' + str(file_path)
    d_order.insert_exportfile(m_schema.CreateExportFile(
        user_id=0,
        export_url=down_url,
        type=global_define.setting_orders_export['order_send_list']
    ))
    return down_url

@router.post(f'/return_order/get', response_model=m_order.AOrderMsgList, summary='获取退货订单列表')
async def get_returns(item: m_order.AOrderRequest) -> m_order.AOrderMsgList:
    return await d_order.get_return_orders(item)
#
# @router.post(f'/card_list/get', response_model=m_order.AOrderMsgList, summary='获取卡券商品订单')
# async def get_cards(item: m_order.AOrderRequest) -> m_order.AOrderMsgList:
#     # f_good_type: m_schema.FilterResGoodType = await r_schema.filter_good_type(type='卡券')
#     # s_good_type: List[m_schema.SGoodType] = f_good_type.data
#     # item.good_type = 0
#     return await d_order.get_all_orders(item, order='desc')
#
#
# @router.post(f'/complete_card/get', response_model=m_order.AOrderMsgList, summary='获取完结卡券订单')
# async def get_complete_cards(item: m_order.AOrderRequest) -> m_order.AOrderMsgList:
#     f_good_type: m_schema.FilterResGoodType = await r_schema.filter_good_type(type='卡券')
#     s_good_type: List[m_schema.SGoodType] = f_good_type.data
#     item.good_type = s_good_type[0].id
#
#     f_order_state: m_schema.FilterResOrderState = await r_schema.filter_order_state(state='已完结', belong='finish')
#     s_order_state: List[m_schema.SOrderState] = f_order_state.data
#     item.order_status_id = s_order_state[0].id
#     return await d_order.get_all_orders(item)


@router.post(f'/complete_order/get', response_model=m_order.AOrderMsgList, summary='获取完结订单列表')
async def get_completes(item: m_order.AOrderRequest) -> m_order.AOrderMsgList:
    f_status: m_schema.FilterResOrderState = await r_schema.filter_order_state(state='已完结', belong='finish')
    s_order_state: List[m_schema.SOrderState] = f_status.data
    item.order_status_id = s_order_state[0].id
    return await d_order.get_all_orders(item)


@router.post(f'/return_order_end/get', response_model=m_order.AOrderMsgList, summary='获取退货完结订单')
async def get_complete_return_real(item: m_order.AOrderRequest):
    f_good_type: m_schema.FilterResGoodType = await r_schema.filter_good_type(type='实体')
    s_good_type: List[m_schema.SGoodType] = f_good_type.data
    item.good_type = s_good_type[0].id

    f_order_state: m_schema.FilterResOrderState = await r_schema.filter_order_state(state='退货已签收', belong='return')
    s_order_state: List[m_schema.SOrderState] = f_order_state.data
    item.order_status_id = s_order_state[0].id
    return await d_order.get_return_orders(item)
#
# @router.get(f'/order_income/get', response_model=m_order.AOrderIncome, summary='订单收益目录')
# async def get_order_income() -> m_order.AOrderIncome:
#     total_income: int = await d_order.get_total_income()
#     current_income: int = await d_order.get_current_income()
#     month_income: int = await d_order.get_month_income()
#     income = m_order.AOrderIncome(total_income=total_income,
#                                   current_income=current_income,
#                                   month_income=month_income)
#     return income

@router.post(f'/order/update_delivery', response_model=str, summary='订单发货')
async def update_order(item: m_schema.SOrder) -> str:
    """
    delivery_company   第三方物流公司,
    delivery_track_code    物流单号，
    status_id： 0待付款、1待发货、2待收货、3已完成
    """
    item.delivery_time = datetime.datetime.now()
    d_db.update_order(item)
    return "success"

@router.post(f'/order/update_detail', summary='修改订单备注')
async def update_detail(item: Updatedetail):
    if d_order.update_order_detail(item.order_id, item.detail):
        return "success"
    else:
        return "error"

@router.post(f'/order/update_detail_tut', summary='修改订单备注教程')
async def update_detail_tut(item: Updatedetail):
    if d_order.update_order_detail_tut(item.order_id, item.detail):
        return "success"
    else:
        return "error"


@router.post(f'/send_list/export_ls', summary='获取导出文件列表')
async def get_export_ls(item: m_order.SearchExportFile):
    return d_order.search_exportfile(item)

@router.get(f'/send_list/get_export_url', summary='转化可访下载链接')
async def get_export_url(path_url: str = ''):
    """
    提参方式：?path_url=http://web.mlcfjihua.cn/assets/file/2025-03-23/4feb6398-0789-11f0-9179-00163e410368export.csv
    """
    path_index = 0
    re_url = 'error'
    try:
        path_index = path_url.index("file/")
    except:
        path_index = 0
    if path_index:
        path_index += 5
        re_url = f"{global_define.download_url}{path_url[path_index:]}"
    return re_url

@router.post(f'/send_list/import_delivery', summary='导入待发货物流号，并发货', response_model=str)
async def import_delivery(data: str = Body(..., title="物流单", embed=True)) -> str:
    """
    每行数据格式如： 订单号，收货人姓名，手机，物流号\n
    """
    re_data = ""
    data = data.strip()
    data = data.lstrip()
    data = data.rstrip()
    data = data.replace(" ", "")
    data = data.replace("\r\n", "\n")
    data = data.replace("\r", "\n")
    data = data.replace("，", ",")
    data_list = data.split("\n")
    for li in data_list:
        if li.find('---') > 0:
            re_data += li
            continue
        li_list = li.split(',')
        if len(li_list) != 4:
            re_data += f"{li}---格式错误\n"
            continue
        order_data = d_order.get_import_order(int(li_list[0]), li_list[1], li_list[2])
        if order_data is None or not order_data:
            re_data += f"{li}---数据错误\n"
            continue

        update_mode = m_schema.SOrder(
            id=int(li_list[0]),
            delivery_track_code=li_list[3],
            delivery_time=datetime.datetime.now(),
            status_id=2
        )
        d_db.update_order(update_mode)
        re_data += f"{li}---成功\n"

    return re_data
