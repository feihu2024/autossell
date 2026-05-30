import unittest
from fastapi.testclient import TestClient
from main import app
import re
import json


def camel_to_snake(camel_str):
    _camel_str = camel_str[1:]
    components = re.findall(r'[A-Z][^A-Z]*', _camel_str)
    return '_'.join(x.lower() for x in components)

class TestGeneralRouter(unittest.TestCase):
    client = TestClient(app)

    def test_good_detail(self):
        res = self.client.get("/schema/supplier/filter?page=1&page_size=1")
        assert res.status_code == 200
        obj = res.json()
        supplier = obj["data"][0]
        response = self.client.post("/admin/good/create", 
        json={
            "good": {
                "display": "1",
                "title": "卡卷3",
                "subtitle": "阿萨",
                "id": None,
                "supplier_id": "28",
                "share_ratio": None,
                "type": 0,
                "status": 1,
                "stock_cordon": "12",
                "expired_time": 1687104000,
                "introducer_id": None,
                "category_id": 9,
                "coinable_number": "100",
                "store_id": None,
                "fake_owner_name": None,
                "fake_owner_phone": None
            },
            "good_spec": [
                {
                "good_id@": "good.id",
                "image": "https://mall.yuanshuhao.top/assets/file/2023-06-19/46564506-0e74-11ee-bd98-5781948bf7c7.png",
                "value": "都市传说",
                "price": "3",
                "price_line": "2",
                "cost": "1",
                "stock": "6",
                "room": "1",
                "lower_num_people": "1",
                "upper_num_people": "6",
                "parent_fee": "1",
                "top_fee": "1",
                "supplier_fee": "1",
                "recommender_fee": "1"
                }
            ],
            "good_rule": {
                "good_id@": "good.id",
                "return_rule": "daf"
            },
            "delivery_rule": [
                
            ],
            "good_image": [
                {
                "good_id@": "good.id",
                "image": "https://mall.yuanshuhao.top/assets/file/2023-06-19/90dde994-0e74-11ee-bd98-5781948bf7c7.png"
                }
            ],
            "good_text": {
                "good_id@": "good.id",
                "description": None
            },
            "good_spec_detail": [
                {
                "good_spec_id@": "good_spec.0.id",
                "detail": "<p>的</p >"
                }
            ],
            "good_spec_combo": [
                {
                "good_spec_id@": "good_spec.0.id",
                "value": "套餐0",
                "price": "3",
                "amount": 1
                }
            ],
            "delivery_rule" : [
            {
               "delivery_fee" : 1,
               "good_id@" : "good.id",
               "is_reachable" : 1,
               "province" : "广东"
            },
            {
               "delivery_fee" : 2,
               "good_id@" : "good.id",
               "is_reachable" : 1,
               "province" : "浙江"
            }
        ]
        })

        assert response.status_code == 200
        obj = response.json()
        assert obj['good']['image_url'] is not None
        res_update = self.client.post('/update/v2', json=obj)
        assert res_update.status_code == 200


        spec = obj['good_spec'][0]

        url =f'/mall/good/detail?spec_id={spec["id"]}'
        res = self.client.get(url)
        assert res.status_code == 200, f"{res.json()['detail']}:{url}"

        good = obj['good']
        res = self.client.get(f'/mall/admin/good_details/get?good_id={good["id"]}')
        assert res.status_code == 200
        body = res.json()[0]
        assert len(body['TGoodSpecCombo']) > 0
        assert body['TGoodRule'] is not None

        update_data = obj
        update_data['good']['title'] = '卡卷3'
        update_data['good']['subtitle'] = '阿萨'
        update_data['good']['share_ratio'] = None
        update_data['good']['type'] = 0
        update_data['good']['status'] = 1
        update_data['good']['stock_cordon'] = '12'
        assert 'good_image' in update_data, update_data.keys()
        res = self.client.post('/mall/admin/good_details/update', json=update_data)
        assert res.status_code == 200, res.json()['detail']


    def test_get_good_list(self):
        res = self.client.get("/mall/admin/good_list/get?page=1&status=1&coinable=0")
        assert res.status_code==200, res.text




if __name__ == '__main__':
    unittest.main()
