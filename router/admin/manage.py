from fastapi import APIRouter
from .good import router as good_router
from .user import router as user_router
from .order import router as order_router
from .store import router as store_router
from .supplier import router as supplier_router
from .banner import router as banner_router
from .check import router as check_router
from .member import router as member_router
from .bagpass import router as bagpass_router
from .found import router as found_router
from .video_task import router as vtask_router
from .user_ad import router as user_ad_router
from .autobody import router as autobody_router
from .video_parse import router as video_parse_router
from .ai_image_generate import router as ai_image_generate_router
from .video_to_prompt import router as video_to_prompt_router
from .video_upload import router as video_upload_router

router = APIRouter()
router.include_router(good_router)
router.include_router(user_router)
router.include_router(order_router)
# router.include_router(store_router)   #商家
router.include_router(supplier_router)  #供应商
router.include_router(banner_router)  # banner与直通车
router.include_router(check_router)  #首单礼品， 复购配置
router.include_router(member_router)  #会员管理
router.include_router(bagpass_router)  #礼包卡密管理
router.include_router(found_router)  #资金池管理
router.include_router(vtask_router)  #视频任务管理
router.include_router(user_ad_router)  #品牌广告管理
router.include_router(autobody_router)  #智能体管理
router.include_router(video_parse_router)  #视频链接解析
router.include_router(ai_image_generate_router)  #AI图片生成
router.include_router(video_to_prompt_router)  #视频反推提示词
router.include_router(video_upload_router)  #视频上传+时长校验