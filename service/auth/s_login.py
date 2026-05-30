from fastapi.security import OAuth2PasswordBearer
import time
from config import SECRET
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status

from dao import d_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def login_for_token(username: str, password: str):
    user = d_user.get_user_by_username(username=username)
    if not user:
        return {
            'code': 1,
            'token': '',
            'massage': 'No username'
        }
    if user.password == password:
        data = {
            'user_id': user.id,
            'role_id': user.role_id,
            'time': time.time()
        }
        token = jwt.encode(data, SECRET.SECRET_KEY, algorithm=SECRET.ALGORITHM)
        return {
            'code': 0,
            'token': token,
            'massage': 'Success'
        }
    else:
        return {
            'code': 1,
            'token': '',
            'massage': 'Password error'
        }


def login_by_email(email: str, password: str):
    user = d_user.get_user_by_email(email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "No user was found"}
        )
    if user.password == password:
        data = {
            'user_id': user.id,
            'role_id': user.role_id,
            'time': time.time()
        }
        token = jwt.encode(data, SECRET.SECRET_KEY, algorithm=SECRET.ALGORITHM)
        return {
            'code': 0,
            'token': token,
            'massage': 'Success',
            'id': user.id,
            'company_id': user.company_id
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Password was wrong."}
        )


async def get_token_info(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        tokenInfo = jwt.decode(token, SECRET.SECRET_KEY, algorithms=SECRET.ALGORITHM)
        user_id: int = tokenInfo.get("user_id")
        role_id: int = tokenInfo.get("role_id")
        if user_id is None:
            raise credentials_exception
        if role_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return tokenInfo
