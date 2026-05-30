from model.vo.user import RegisterUser
from model.vo.car import RegisterCar
from model.schema import TUser, TCar
from typing import List

from dao import d_user
from dao import d_car


def check_auth():
    return True


def register_user(r_user: RegisterUser) -> dict:
    user = {key: val for key, val in r_user.dict().items() if val is not None}
    cars = user.pop('cars')
    t_user = TUser(**user)
    t_user = d_user.insert_user(t_user)

    if cars is not None and len(cars) > 0:
        t_cars = []
        for car in cars:
            car['user_id'] = t_user.id
            t_car = TCar(**car)
            t_cars.append(t_car)
        d_car.insert_cars(t_cars)

    return {
        "code": 0,
        "massage": "success",
        "user_id": t_user.id
    }


def register_cars(cars: List[RegisterCar]) -> dict:
    t_cars = [TCar(**car.dict()) for car in cars]
    d_car.insert_cars(t_cars)
    return {
        "code": 0,
        "massage": "Success"
    }

