import hashlib
import json
import re
import time
import uuid
from typing import Optional, List

import requests
from fastapi.exceptions import HTTPException

from config import DigitalChain
from model.jxhh_request import OrderBody
from model.mall_res import GoodResponse, GoodResponseData, GoodDetailResponseData, SpecsOption, SpecsValue, \
    PreOrderResponseData

space_pat = re.compile(r'\s')

domain = 'http://api.jxhh.com'


def recommend(page: int, limit: int = 10, source: int = 0) -> GoodResponse:
    query = {
        'page': page,
        'limit': limit,
        'source': source
    }
    base = domain + '/v2/Goods/Lists'

    url = build_url(base=base, query=query)
    header = build_header(query=query)

    res = requests.get(url=url, headers=header)
    assert res.status_code == 200
    goods = [GoodResponseData.parse_obj(item) for item in res.json()['data']['list']]
    return GoodResponse(data=goods)


def good_detail(id: int) -> GoodDetailResponseData:
    api = domain + f'/v2/Goods/Detail'
    query = {
        'id': f'{id}'
    }

    res = request(url=api, query=query)

    return GoodDetailResponseData.parse_obj(res.get('data'))


def get_details(good_ids: List[int]) -> List[GoodDetailResponseData]:
    L = len(good_ids)
    return_data = []
    api = domain + f'/v2/Goods/GetBulkGoodDetail'
    for start_idx in range(0, L, 20):
        end_idx = start_idx + 20
        end_idx = min(end_idx, L)
        new_good_ids = good_ids[start_idx:end_idx]
        new_good_ids = [f'{id}' for id in new_good_ids]
        body = {
            'ids': ','.join(new_good_ids)
        }
        res = request(api, body=json.dumps(body))
        items = [GoodDetailResponseData.parse_obj(item) for item in res.get('data')]
        return_data.extend(items)
    return return_data


def get_specs_options(good_ids: List[int], sku_ids: list[int]) -> List[SpecsOption]:
    items = get_details(good_ids=good_ids)
    items = [filter_specs(sku_id=sku_id, item=item) for sku_id, item in zip(sku_ids, items)]
    return items


def get_specs_details(good_ids: List[int], sku_ids: List[int]) -> List[GoodDetailResponseData]:
    items = get_details(good_ids=good_ids)
    items = [update_detail_by_sku_id(sku_id=sku_id, item=item) for sku_id, item in zip(sku_ids, items)]
    return items

def pre_order(order: OrderBody) -> PreOrderResponseData:
    api = domain + '/v2/order/beforeCheck'
    res = request(api, body=order.json())
    return PreOrderResponseData.parse_obj(res['data'])


def update_detail_by_sku_id(item: GoodDetailResponseData, sku_id: int) -> GoodDetailResponseData:
    specs_option = filter_specs(sku_id=sku_id, item=item)
    item.cover = specs_option.image
    item.market_price = specs_option.market_price
    item.sale_price = specs_option.sale_price
    item.stock = specs_option.stock
    item.specs.values = [
        SpecsValue(id=specs_option.id, name=specs_option.spec_value_names)]
    return item


def filter_specs(sku_id: int, item: GoodDetailResponseData) -> Optional[SpecsOption]:
    for specs in item.specs.options:
        if sku_id == specs.id:
            return specs
    return None


def request(url: str, query: Optional[dict] = None, body: str = "") -> dict:
    if query is None:
        header = build_header(body=body)
        res = requests.post(url=url, headers=header, data=body)
    else:
        url = build_url(base=url, query=query)
        header = build_header(query=query)
        res = requests.get(url=url, headers=header)
    body = res.json()
    if body is None:
        raise HTTPException(status_code=200, detail=body['message'])
    return body


def search(search_words: str, page: int, limit: int = 10, source: int = 0) -> GoodResponse:
    query = {
        'page': page,
        'limit': limit,
        'source': source,
        'search_words': search_words
    }
    base = 'http://api.jxhh.com/v2/Goods/Lists'

    url = build_url(base=base, query=query)
    header = build_header(query=query)

    res = requests.get(url=url, headers=header)
    assert res.status_code == 200
    goods = [GoodResponseData.parse_obj(item) for item in res.json()['data']['list']]
    return GoodResponse(data=goods)


def build_header(query: Optional[dict] = None, body: str = '') -> dict:
    nonce = uuid.uuid4().hex
    timestamp = time.time() * 1000
    timestamp = f"{int(timestamp)}"
    header = {
        'Api-App-Key': DigitalChain.app_key,
        'Api-Time-Stamp': timestamp,
        'Api-Nonce': nonce
    }
    sign_str = sign(header=header, query=query, body=body)
    header['Api-Sign'] = sign_str
    return header


def build_url(base: str, query: Optional[dict]) -> str:
    return f"{base}?{query_str(query)}"


def sign(header: dict, query: Optional[dict] = None, body: str = '') -> str:
    secret = DigitalChain.app_secret

    data = header.copy()
    if query is not None:
        data.update(query)

    sorted_data = sorted(data)
    sign_str = ''
    for key in sorted_data:
        sign_str += f"{key}{data[key]}"
    sign_str += secret
    sign_str += re.sub(space_pat, '', body)

    sign_str = hashlib.sha1(sign_str.encode()).hexdigest()
    sign_str = hashlib.md5(sign_str.encode()).hexdigest()
    sign_str = sign_str.upper()

    return sign_str


def query_str(query: dict) -> str:
    return "&".join([f"{key}={value}" for key, value in query.items()])


if __name__ == '__main__':
    # res = search('毛衣', 1)
    #
    # print(res)
    # print('end')
    #
    # res = good_detail(10000)
    # print(res)

    res = get_details(list(range(10000, 10035)))
    print(res)
