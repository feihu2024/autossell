import unittest
from unittest import mock

from fastapi.testclient import TestClient

from main import app
from model.res.auth import LoginRes


def mock_request_wx_login(*args, **kwargs):
    class mock_res:
        status_code = 200

        def json(self):
            return {
                "openid": "test_openid",
                "unionid": "test_union_Id",
                "session_key": "test_session key",
                "errcode": 0,
                "errmesg": "ok"
            }

    return mock_res()


class TestUser(unittest.TestCase):
    client = TestClient(app)

    @mock.patch('requests.get', mock_request_wx_login)
    def test_wx_login(self):
        res = self.client.get('/mall/user/wx_login?code=test_code&user_id=-1')
        assert res.status_code == 200
        LoginRes.parse_obj(res.json())


if __name__ == '__main__':
    unittest.main()
