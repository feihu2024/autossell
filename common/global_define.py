#资金变动类型  3和13 重复
balance_type = {
    1:"销售收益",  #推荐收益
    2:"分红收益",
    3:"分享收益",
    4:"用户转账转入",  # 转账
    5:"商品购买",
    6:"余额用户提现",
    7:"推荐收益",
    8:"用户转账转出",  # 转账
    9:"分红",  #大公排分润
    10:"兑换券",  #赠予优惠券
    11:"购物置换",  #大公复购
    12:"复购直推收益",
    13:"商品购买消券",
    14:"管理增金额",
    15:"管理增购物券",
    16:"推荐余额用户提现",
    17:"资金池分润",
    18:"视频分发购买",
    19:"视频分发消费",
    20:"激活收益",
    21:"卡密激活间推奖",
    22:"团长收益",
    23:"团间接收益",
    24:"间接分享",
    25:"间推收益",
    26:"推荐收益（普）",  #普通商品
    27:"间推收益（普）",
    28:"分享收益（普）",
    29:"间接分享（普）",
    30:"团长收益（普）",
    31:"团间接收益（普）",
    32:"供货收益（普）",
    33:"推荐收益（礼包）",  #卡密商品
    34:"激活收益（礼包）",
    35:"分享收益（礼包）",
    36:"间接分享（礼包）",
    37:"团长收益（礼包）",
    38:"团间接收益（礼包）",
    39:"供货收益（礼包）",
    40:"推荐收益（分发）",  #任务相关
    41:"间推收益（分发）",
    42:"团长收益（分发）",
    43:"团间接收益（分发）",
    44:"供货收益（分发）",
    45:"间推收益（礼包）",
    46:"居间收益（普）",
    47:"居间收益（礼包）",
    48:"居间收益（分发）",
    49:"购物券收益（分发）",
    50:"市代收益（普）",
}

#订单相关配置
setting_orders = {
    "return_flash_order_income_days": 20,  # 新用户默认收益天数
    "rerun_flash_order_times":24,  #秒杀退货最低时限，小时   替换为t_settings里面的flash_order_owner_times 配置
    "card_income_times":7,  #卡券订单未完结情况下，超过规定天数，分配收益
    "body_income_times": 14,  # 实体订单未完结情况下，超过规定天数，分配收益
    "good_stock_cordon":10,  #默认 库存警戒线，如果t_good中stock_cordon为none
}

#导出相关配置
setting_orders_export = {
    "order_send_list": "发货订单导出",  # 发货导出类型
    "sucai_user_list": "用户任务导出",  # 发货导出类型
    "sucai_user_list_xlsx": "用户任务导出EXCEL"  # 发货导出类型
}

#提现相关配置，第一项定义返回锁定余额比例，第二项提现扣除比例
"""
|  0 | 粉丝      |  fans
|  1 | 会员      |  member
|  2 | 老板      |  boss
|  3 | 大老板    |  bigboss
"""
setting_withdraw = {
    "fans": [0.12, 0.1],
    "member": [0.1, 0.1],
    "boss": [0.08, 0.1],
    "bigboss": [0.06, 0.1]
}

valid_char = ["%p", "*l", "!z", "e@", "&g", "D", "B", "$j", "r", "(h", "m"]

#批发商角色  # 1联营会员，ws2_proportion，wholesale1   2仓库主，ws3_proportion，wholesale2  3巨省会员，ws1_proportion，wholesale3
wholesale_role = {"wholesale1": 100, "wholesale2": 200, "wholesale3": 300}
#批发商角色奖励积分
wholesale_role_coin = {"wholesale1": 0, "wholesale2": 0, "wholesale3": 0}
#升级批发商额度（单位：分）
wholesale_amount = 1
#排队批发商分润次数
wholesale_shoperorderfee = {"wholesale1": 3, "wholesale2": 3, "wholesale3": 3}

#平台奖励
platform_prize = {
    "prize1": 0,  #  推荐3个批发商奖励一
    "prize2": 0,   #  推荐5个批发商奖励二
    "prize3": 0,  #  成为粉丝平台奖励积分
    "prize4": 0,  #  新注册会员领取奖励积分
}

#腾旭地图参数配置
jsapi_key = 'KZZBZ-VN2WQ-U6N5F-46GP4-RVX5S-HIFKX'

#升级会员奖励积分，当前成交单支付金额的倍数：支付金额 *  multiple_coin
multiple_coin = 0
#升级会员奖励积分，固定额度
level_coin = 0
#新用户通知
#new_user_notice = f"您好！\n 我们很高兴地通知您，您的100元新人消费金已经到账，请您尽快查收。\n 此外，为了回馈广大会员的支持与厚爱，我们特别推出了一项优惠活动：在购买任意商品时，您将额外获得100元消费金。\n 我们承诺，您可以在全网范围内比较我们的价格，我们始终以诚信和品质赢得您的信任和满意。\n 特此通知！\n  祝您生活愉快"
new_user_notice = f"感谢您选择加入我们的大家庭！在这里，我们致力于为您提供卓越的服务和独一无二的体验。如果您在使用过程中遇到任何问题或需要帮助，请随时联系我们的客服团队。我们始终在线，为您提供贴心的服务和支持。"
#new_user_coin_notice = f"欢迎加入团个仓，请至个人中心领取66元新人福利。  "
new_user_coin_notice = f"欢迎加入非常市集。  "
#推荐会员赠送积分额度
recommend_coin = 0

#薅羊毛任务：链接处理状态
link_stat = ["抖音链接无效","小红书链接无效","快手链接无效"]
#不合格原因
nopass = ["抖音链接打不开","小红书链接打不开","快手链接打不开"]
#链接审核状态  0未操作,1链接未审核,2链接已审核
link_stat = ["未操作","链接未审核","链接已审核"]
#打卡审核状态  0未打卡,1未审核,2已审核
pic_stat = ["未打卡","未审核","已审核"]
#任务状态 ,0表示视频类,1表示图文类
task_ctype = ["视频","图文"]
#发布平台
pub_platform = ["抖音","小红书","视频号","快手","朋友圈","参与证明","微博", "QQ小世界", "哔哩哔哩"]

#薅羊毛团长操作类型
groupsir_type = ["推荐入团", "管理入团", "出团", "升级团长", "取消团长", "转移入团"]
#团长级别 团长名，固定分成，比例分成
groupsir_level = [
    {"id":1, "gname":"一级团长", "lines":100, "proportion":10},
    {"id":2, "gname":"二级团长", "lines":200, "proportion":11},
    {"id":3, "gname":"三级团长", "lines":300, "proportion":12}
]
#回收没有下载的素材，超时时间设置,秒
taskuser_expires = 25 * 60
#薅羊毛黑名单
ts_blacklist = [1,2,3,1297]

#进件配置：证件类型
lic_type = {
    "contact": "超级管理",
    "license":"营业执照",
    "certificate":"登记证书",
    "finance":"金融许可",
    "card":"经营者",
    "other":"其他",
    "ubo":"受益人",
    "biz":"线下场景",
    "mp":"公众号",
    "mini":"小程序",
    "app":"app应用",
    "web":"网站场景",
    "wework":"企业微信"
}
#进件配置  证件名称
lic_type_name = ["身份证", "营业执照","登记证书","单位证明函","金融机构","法人身份证"]

#房间配置
room_config = {
  "room_balance": 50000, # 默认创建房间奖金额度
  "room_bouns":48,  #房间满员时，主人获得奖金，给推荐人的比例50%
  "up_partner":2, #升级合伙人需要多少个报单商品订单
  "contribute":1, #贡献值增加额度
  "max_contribute":2, #贡献值最高额度
}

#简单密码
common_passwords = ['123456', 'password', '12345678', 'qwerty', '123321', 'abc123']

#下载地址
#http://d0d02f4937ikukjipuyya.mlcfjihua.cn:8284/2025-03-23/4feb6398-0789-11f0-9179-00163e410368export.csv
download_url = "http://d0d02f4937ikukjipuyya.mlcfjihua.cn:8284/"

#提现配置
withdraw_config = {
  "max_balance": 50000, # 提现最高额，分
  "ded_bouns":0.1,  #平台扣除比例10%
  "low_balance": 10000, # 提现最高额，分
}

#会员级别  0粉丝,1会员,2核心会员
users_level = [
    {"id":0, "gname":"粉丝"},
    {"id":1, "gname":"VIP"},
    {"id":2, "gname":"区代"},
    {"id":3, "gname":"市代"}
]

#身份级别  身份0普通1小团长2大团长
wholesale_level = [
    {"id":0, "gname":"普通"},
    {"id":1, "gname":"小团长"},
    {"id":2, "gname":"大团长"}
]
#视频分发身份级别  0达人,1店长,2服务商,3分公司
video_level = [
    {"id":0, "gname":"普通"},
    {"id":1, "gname":"达人"},
    {"id":2, "gname":"店长"},
    {"id":3, "gname":"服务商"},
    {"id":4, "gname":"分公司"}
]

#Redis配置
REDIS_HOST='localhost'
REDIS_PORT=6379
REDIS_LAYER_LIST = 'layerlist'   #公排到额复购用户列表

#临时托管期限（小时）
max_entrust_len = 24 * 10