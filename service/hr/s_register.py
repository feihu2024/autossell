from model.vo.user import RegisterEmployeeVo
from model.schema import TUser
from dao import d_user


def register_employee(vo_user: RegisterEmployeeVo) -> dict:
    user = {key: val for key, val in vo_user.dict().items() if val is not None}
    t_user = TUser(**user)
    t_user = d_user.insert_user(t_user)
    return {
        "code": 0,
        "massage": "success",
        "user_id": t_user.id
    }