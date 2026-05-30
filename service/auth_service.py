import time

from jose import jwt

from config import SECRET
from model.inner import TokenInfo


def token_encode(user_id: int) -> str:
    """
    encode user_id as token
    :param user_id: user id
    :return: token string
    """
    data = {
        "user_id": user_id,
        "time": time.time()
    }
    token = jwt.encode(data, SECRET.SECRET_KEY, algorithm=SECRET.ALGORITHM)
    return token


def token_decode(token: str) -> TokenInfo:
    """
    decode token to get user id and time of login
    :param token: token from client
    :return: token information which includes user_id and login_time
    """
    data = jwt.decode(token=token, key=SECRET.SECRET_KEY, algorithms=SECRET.ALGORITHM)
    return TokenInfo.parse_obj(data)
