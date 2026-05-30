import requests
import urllib
import unittest
import random
from fastapi import FastAPI, Query
from fastapi.testclient import TestClient
from main import app

class TestGeneralRouter(unittest.TestCase):
    client = TestClient(app)

    def test_good_create(self):
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
            ]
        })

        assert response.status_code == 200
        obj = response.json()
        assert obj['good']['image_url'] is not None

        # import json
        # print(json.dumps(obj, indent=4, ensure_ascii=False))
        self.client.post('/update/v2', json=obj)

#    def test_card_order(self):
#        res = self.client.get('/schema/good/filter?type=0&page_size=1')
#        res['data']['good_id']
#        ## check order
#        res = self.client.get('/mall/order/card_detail?order_id=180')
#        assert res.status_code == 200, res.text
#        obj = res.json()
#        assert 'TSupplier' in obj, res.text
#        assert 'good' in obj, res.text
#        assert obj['good']['type'] == 0, obj['good']


if __name__ == '__main__':
    unittest.main()
