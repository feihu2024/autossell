import logging
from setup.log import init_log
init_log()


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from urls import include_routers
from fastapi import Request
from fastapi import Response
import time
from fastapi import status
from fastapi import Depends
from fastapi import Header
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from dao import d_admin


app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

include_routers(app)

@app.on_event("startup")
async def startup():
    logging.info('Test log')
    from service.ai_image_generate_service import start_cleanup_daemon
    start_cleanup_daemon()


@app.on_event("shutdown")
async def shutdown():
    pass


@app.exception_handler(Exception)
async def value_error_handler(request, exc):
    error_detail = str(exc)  # 将detail转换为字符串形式
    return {"error": error_detail}

@app.middleware("http")
async def validate_users(request: Request, call_next):
    start_time = time.time()
    url_path = request.url.path
    if url_path.lower().startswith('/mall/admin') or url_path.lower().startswith('/admin'):
        if url_path.lower().startswith('/mall/admin/login') or url_path.lower().startswith('/mall/admin/login_out'):
            response: Response = await call_next(request)
            return response
        else:
            # print('------------------------------------------------')
            # print(request.cookies)
            if request.headers.get('kemaikemaisession'):
                cookie_val = request.headers.get('kemaikemaisession')
                new_cookie_val = d_admin.is_login(cookie_val)
                if new_cookie_val:
                    response: Response = await call_next(request)
                    response.headers["kemaikemaisession"] = f"{new_cookie_val}"
                    #response.set_cookie(key="kemaikemaisession", value=f"{new_cookie_val}")
                    return response
            response = JSONResponse(content={"status":404, "message": "please login"})
            response.headers["access-control-allow-headers"] = "content-type,kemaikemaisession"
            response.headers["Content-Type"] = "text/plain; charset=utf-8"
            response.headers["access-control-allow-origin"] = "*"
            response.headers["access-control-allow-methods"] = "DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT"
            response.headers["Connection"] = "keep-alive"
            return response
    else:
        response: Response = await call_next(request)
        # process_time = time.time() - start_time
        # response.headers["X-Process-Time"] = str(process_time)
        # response.status_code = status.HTTP_201_CREATED
        return response


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

