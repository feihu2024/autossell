from fastapi import FastAPI, Depends
# from service.auth import s_login
from router import admin, mall, supplier, finance
# import router.supplier.user
from router.admin import manage, package, package_order, good_spec, settings, groupsir, balance, good, busines_service, video_config
from router import file, r_schema, r_query, r_update, r_create, r_wx
from router.mall import autobody, user, home, address, good, order, \
    account, platform, vtask, adbrand, video_parse, ai_image_generate, video_to_prompt, video_upload
# from router.finance import shuser
from router.task import sucai, clockup, tuan

def include_routers(app: FastAPI):
    # app.include_router(r_query.router, prefix='/query', tags=['query'])
    # app.include_router(r_update.router, prefix='/update', tags=['update'])
    # app.include_router(r_create.router, prefix='/create', tags=['create'])
    # 1
    app.include_router(r_wx.router, prefix='/wx', tags=['wx'])
    #
    # app.include_router(supplier.user.router, prefix='/supplier/user', tags=['/supplier/user'])
    #
    # app.include_router(flash_good.router, prefix='/mall/package', tags=['/mall/package'])
    # app.include_router(flash_order.router, prefix='/mall/package_order', tags=['/mall/package'])
    #
    # # mall home
    # 2
    app.include_router(mall.home.router, prefix='/web/home', tags=['/web/home'])
    #
    # # mall user
    # 3
    app.include_router(mall.user.router, prefix='/web/user', tags=['/web/user'])
    #
    # # user account
    # 4
    app.include_router(mall.account.router, prefix='/web/account', tags=['/web/account'])
    #
    # # good collects
    # 5
    app.include_router(mall.good.router, prefix='/web/product', tags=['/web/product'])
    #
    # # mall order
    # 6
    app.include_router(mall.order.router, prefix='/web/order', tags=['/web/order'])
    #
    # # user address
    # app.include_router(mall.address.router, prefix='/mall/address', tags=['mall/address'])
    #
    # # mall package
    # # app.include_router(mall.package.router, prefix='/mall/package', tags=['/mall/package'])
    #
    # # mall store
    # app.include_router(mall.store.router, prefix='/mall/store', tags=['/mall/store'])
    #
    # # mall platform
    # 7
    app.include_router(mall.platform.router, prefix='/web/platform', tags=['/web/platform'])
    # 7
    app.include_router(mall.vtask.router, prefix='/web/vtask', tags=['/web/vtask'])
    #
    app.include_router(mall.adbrand.router, prefix='/web/brand', tags=['/web/brand'])
    #
    app.include_router(mall.autobody.router, prefix='/web/autobody', tags=['/web/autobody'])
    # # video parse / ai image / video to prompt (小程序调用)
    app.include_router(mall.video_parse.router, prefix='/web/video/parse', tags=['/web/video/parse'])
    app.include_router(mall.ai_image_generate.router, prefix='/web/video/generate', tags=['/web/video/generate'])
    app.include_router(mall.video_to_prompt.router, prefix='/web/video/to_prompt', tags=['/web/video/to_prompt'])
    # video upload (小程序调用)
    app.include_router(mall.video_upload.router, prefix='/web/video/upload', tags=['/web/video/upload'])
    # # video config (管理端配置)
    app.include_router(admin.video_config.router, prefix='/autoselladmin/video_config', tags=['/autoselladmin/video_config'])
    # # mall admin
    app.include_router(admin.manage.router, prefix='/autoselladmin/manage', tags=['/autoselladmin/manage'])
    #
    # # admin
    # # admin package
    # app.include_router(admin.package.router, prefix='/', tags=['/'])
    #
    # # good
    # app.include_router(admin.good.router, prefix='/admin/good', tags=['/admin/good'])
    #
    # # admin package order
    # app.include_router(admin.package_order.router, prefix='/admin/package_order', tags=['/admin/package_order'])
    # app.include_router(admin.good_spec.router, prefix='/admin/good_spec', tags=['/admin/good_spec'])
    #
    # # admin settings
    # app.include_router(admin.settings.router, prefix='/admin/settings', tags=['/admin/settings'])
    #
    # #admin gropsir
    # app.include_router(admin.groupsir.router, prefix='/admin/groupsir', tags=['/admin/groupsir'])
    # 8
    app.include_router(admin.balance.router, prefix='/autoselladmin/balance', tags=['/autoselladmin/balance'])
    #
    # #admin service
    # app.include_router(admin.busines_service.router, prefix='/admin/service', tags=['/admin/service'])
    #
    # #任务薅羊毛
    # app.include_router(mytask.router, prefix='/task/mytask', tags=['/task/mytask'])
    # app.include_router(sucai.router, prefix='/task/sucai', tags=['/task/sucai'])
    # app.include_router(clockup.router, prefix='/task/clockup', tags=['/task/clockup'])
    app.include_router(tuan.router, prefix='/autoselladmin/groupsir', tags=['/autoselladmin/groupsir'])
    #
    # # file
    app.include_router(file.router, prefix='/assets', tags=['/assets'])
    # app.include_router(r_schema.router, prefix='/schema', tags=['schema'])
    #
    # # balance user
    # app.include_router(finance.shuser.router, prefix='/finance/shuser', tags=['/finance/shuser'])
    pass
