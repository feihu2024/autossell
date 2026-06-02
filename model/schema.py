# coding: utf-8
from sqlalchemy import CHAR, Column, DECIMAL, Float, Integer, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import LONGTEXT, MEDIUMTEXT, TINYINT, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class TAddress(Base):
    __tablename__ = 't_address'
    __table_args__ = {'comment': '地址表，用于存放表的地址，一个用户可以有多个地址'}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, comment='外键')
    province = Column(VARCHAR(20), comment='省')
    city = Column(VARCHAR(20), comment='市')
    area = Column(VARCHAR(20), comment='区')
    street = Column(VARCHAR(20), comment='街道')
    description = Column(VARCHAR(400), comment='详细地址')
    consignee = Column(String(25), comment='收货人姓名')
    phone = Column(String(25), comment='收货人电话')
    default_val = Column(TINYINT, comment='1:默认  0:非默认')


class TAdmin(Base):
    __tablename__ = 't_admin'
    __table_args__ = {'comment': '管理员的表'}

    id = Column(Integer, primary_key=True)
    username = Column(String(45))
    phone = Column(String(45))
    email = Column(String(45))
    level_id = Column(Integer)
    password = Column(String(100))
    id_card = Column(String(45))
    gender = Column(String(20))
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    last_active_time = Column(TIMESTAMP)
    status = Column(String(20))
    business_id = Column(Integer, server_default=text("'0'"), comment='商家ID_busiess_content')
    admin_id = Column(Integer, server_default=text("'0'"), comment='所属商家管理id')
    user_pic = Column(String(512), comment='头像url')
    user_info = Column(Text, comment='用户备注')


class TAutobody(Base):
    __tablename__ = 't_autobody'
    __table_args__ = {'comment': '阿里百炼智能体表'}

    id = Column(Integer, primary_key=True, comment='标识id')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    type_id = Column(Integer, nullable=False, server_default=text("'0'"), comment='所属智能体分类id')
    at_name = Column(String(255), comment='智能体名称')
    describe = Column(Text, comment='智能体描述')
    cover = Column(Text, comment='智能体封面图')
    at_id = Column(String(500), comment='智能体ID')
    order_id = Column(Integer, nullable=False, server_default=text("'0'"), comment='优先级排序')
    stat = Column(TINYINT, server_default=text("'0'"), comment='状态,0正常1关闭')
    update_time = Column(TIMESTAMP, comment='更新时间')
    preview_video = Column(Text, comment='智能体封面图')
    auto_tag = Column(Text, comment='智能体标签')
    del_stat = Column(TINYINT, server_default=text("'0'"), comment='删除,0正常1删除')


class TAutobodyFile(Base):
    __tablename__ = 't_autobody_file'
    __table_args__ = {'comment': '智能体知识库文件表'}

    id = Column(Integer, primary_key=True, comment='标识id')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    autobody_id = Column(Integer, nullable=False, server_default=text("'0'"), comment='所属智能体id')
    title = Column(String(255), comment='文件名称')
    describe = Column(Text, comment='文件描述')
    url = Column(String(500), comment='文件地址')


class TAutobodyType(Base):
    __tablename__ = 't_autobody_type'
    __table_args__ = {'comment': '智能体分类表'}

    id = Column(Integer, primary_key=True, comment='标识id')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    title = Column(String(255), comment='类型标题')
    describe = Column(Text, comment='类型描述')
    cover = Column(String(500), comment='封面图')


class TBagCagegory(Base):
    __tablename__ = 't_bag_cagegory'
    __table_args__ = {'comment': '礼包卡密批次分类表'}

    id = Column(Integer, primary_key=True, comment='标识id')
    pc_name = Column(String(120), comment='批次名称')
    pc_num = Column(Integer, server_default=text("'0'"), comment='批次数量')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    endtime = Column(TIMESTAMP, comment='结束时间')
    bag_id = Column(Integer, server_default=text("'0'"), comment='礼包id')


class TBagPas(Base):
    __tablename__ = 't_bag_pass'
    __table_args__ = {'comment': '礼包卡密表'}

    id = Column(Integer, primary_key=True, comment='标识id')
    pass_num = Column(String(120), comment='加密编号(十六进制)')
    pc_name = Column(String(120), comment='批次名称')
    pc_num = Column(Integer, server_default=text("'0'"), comment='批次数量')
    pc_id = Column(Integer, server_default=text("'0'"), comment='批次id(不可重复)')
    stat = Column(TINYINT, server_default=text("'0'"), comment='是否激活,默认0未激活1已激活2过期未用')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    startime = Column(TIMESTAMP, comment='激活时间')
    user_id = Column(Integer, server_default=text("'0'"), comment='激活会员id')
    endtime = Column(TIMESTAMP, comment='结束时间')
    cate_id = Column(Integer, server_default=text("'0'"), comment='批次分类id')


class TBalance(Base):
    __tablename__ = 't_balance'
    __table_args__ = {'comment': '用户账户余额表，用户的余额历史记录，不可修改，只能增加'}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, comment='外键')
    change = Column(Integer, nullable=False, server_default=text("'0'"), comment='变动金额')
    balance = Column(Integer, nullable=False, comment='余额')
    type = Column(VARCHAR(20), comment='类型')
    description = Column(VARCHAR(100), comment='详细描述')
    create_time = Column(TIMESTAMP, comment='创建时间')
    user_withdraw_id = Column(Integer)
    operator_id = Column(Integer, comment='操作员ID')
    out_trade_no = Column(String(64))
    good_id = Column(VARCHAR(100), comment='收益商品id')
    good_title = Column(Text, comment='收益商品标题名称')
    good_num = Column(VARCHAR(100), comment='收益商品数量')
    titlelog = Column(VARCHAR(100), comment='标题记录')
    user_nick = Column(String(45), comment='用户昵称')
    phone = Column(VARCHAR(45), comment='联系方式')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='注册时间')


class TBalanceGive(Base):
    __tablename__ = 't_balance_give'
    __table_args__ = {'comment': '管理员分配余额或积分记录'}

    id = Column(Integer, primary_key=True)
    user_ids = Column(VARCHAR(600), comment='分配用户，逗号分隔的用户id')
    coin = Column(Integer, nullable=False, server_default=text("'0'"), comment='分配积分总额')
    balance = Column(Integer, nullable=False, comment='分配余额总额')
    type = Column(TINYINT(1), comment='类型，1为余额，2为积分')
    description = Column(Text, comment='分配明细')
    create_time = Column(TIMESTAMP, comment='创建时间')
    operator_id = Column(Integer, comment='操作员ID')
    sucess_num = Column(Integer, nullable=False, comment='分配成功数量')
    give_txt = Column(VARCHAR(150), comment='打款备注信息')


class TBanner(Base):
    __tablename__ = 't_banner'
    __table_args__ = {'comment': 'banner管理表，商城小程序里首页的头部的广告图'}

    id = Column(Integer, primary_key=True)
    image = Column(String(256), comment='图片url')
    title = Column(String(100), comment='主标题')
    subtitle = Column(String(500), comment='视频地址')
    width = Column(Integer, comment='图片宽度')
    height = Column(Integer, comment='图片高度')
    create_time = Column(TIMESTAMP, comment='创建时间')
    description = Column(String(100), comment='详情')
    good_id = Column(Integer, comment='商品id')
    ban_label = Column(String(45), comment='标签')
    type_id = Column(TINYINT, comment='0:banner   1:直通车')
    good_spec_id = Column(Integer)
    ba_stat = Column(TINYINT, server_default=text("'0'"), comment='小程序端展示状态,默认0正常展示')
    video = Column(String(256), comment='视频url')
    is_video = Column(TINYINT, server_default=text("'0'"), comment='是否展示视频0:使用imag图片地址1:使用video视频地址')
    class_id = Column(Integer, server_default=text("'0'"), comment='广告分类id')


class TBannerType(Base):
    __tablename__ = 't_banner_type'
    __table_args__ = {'comment': 'banner广告分类表'}

    id = Column(Integer, primary_key=True, comment='标识id')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    title = Column(String(255), comment='类型标题')
    describe = Column(Text, comment='类型描述')
    cover = Column(String(500), comment='封面图')


class TBigorderFour(Base):
    __tablename__ = 't_bigorder_four'
    __table_args__ = {'comment': '四项公排表'}

    id = Column(Integer, primary_key=True, comment='标识id')
    layer_id = Column(Integer, server_default=text("'0'"), comment='行号(所在层数)')
    cur_layer_id = Column(Integer, server_default=text("'0'"), comment='当前行号从左到右排序号')
    cur_layer_total = Column(Integer, server_default=text("'0'"), comment='当前行排序总数量')
    parent_id = Column(Integer, server_default=text("'0'"), comment='上级对应序号')
    order_id = Column(Integer, nullable=False, server_default=text("'0'"), comment='大公排id')


class TBigorderInitbag(Base):
    __tablename__ = 't_bigorder_initbag'
    __table_args__ = {'comment': '初始礼包表'}

    id = Column(Integer, primary_key=True, comment='主键id')
    bag_name = Column(String(100), comment='礼包名称')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    tuan_id = Column(Integer, server_default=text("'0'"), comment='所属团长id')
    price_total = Column(Integer, server_default=text("'0'"), comment='总价格')
    invited_money = Column(Integer, server_default=text("'0'"), comment='直推金额')
    layer_every = Column(Integer, server_default=text("'0'"), comment='每层复购金额')
    layer_num = Column(Integer, server_default=text("'0'"), comment='复购层数（含直推）')
    grant_num = Column(Integer, server_default=text("'0'"), comment='赠予兑换券额度')
    bag_cont = Column(Text, comment='礼包介绍')
    bag_type = Column(TINYINT, comment='礼包类型0正常1大团长复购礼包')
    phone = Column(VARCHAR(45), comment='团长电话')
    bag_pic = Column(VARCHAR(512), comment='图像url')
    fund_one = Column(Integer, server_default=text("'0'"), comment='归集初级资金池额度')
    fund_two = Column(Integer, server_default=text("'0'"), comment='归集高级资金池额度')
    fund_three = Column(Integer, server_default=text("'0'"), comment='归集顶级资金池额度')


class TBigorderLog(Base):
    __tablename__ = 't_bigorder_log'
    __table_args__ = {'comment': '复购日志表'}

    id = Column(Integer, primary_key=True, comment='主键id')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    user_id = Column(Integer, server_default=text("'0'"), comment='复购用户id')
    price_total = Column(Integer, server_default=text("'0'"), comment='总价格')
    invited_money = Column(Integer, server_default=text("'0'"), comment='直推金额')
    layer_every = Column(Integer, server_default=text("'0'"), comment='每层复购金额')
    layer_num = Column(Integer, server_default=text("'0'"), comment='复购层数（含直推）')
    grant_num = Column(Integer, server_default=text("'0'"), comment='赠予兑换券额度')
    bag_cont = Column(Text, comment='复购分润结构[{layer:1,user:2,balance:100,order:1}]')


class TBigorderSet(Base):
    __tablename__ = 't_bigorder_set'
    __table_args__ = {'comment': '礼包复购配置参数'}

    id = Column(Integer, primary_key=True, comment='序号id')
    set_name = Column(String(100), comment='配置参数关键字名称')
    val_int = Column(Integer, server_default=text("'0'"), comment='数字值')
    val_str = Column(String(500), comment='文本值')
    set_cont = Column(Text, comment='配置项介绍')


class TBigorderThree(Base):
    __tablename__ = 't_bigorder_three'
    __table_args__ = {'comment': '三项公排表'}

    id = Column(Integer, primary_key=True, comment='标识id')
    layer_id = Column(Integer, server_default=text("'0'"), comment='行号(所在层数)')
    cur_layer_id = Column(Integer, server_default=text("'0'"), comment='当前行号从左到右排序号')
    cur_layer_total = Column(Integer, server_default=text("'0'"), comment='当前行排序总数量')
    parent_id = Column(Integer, server_default=text("'0'"), comment='上级对应序号')
    order_id = Column(Integer, nullable=False, server_default=text("'0'"), comment='大公排id')


class TBigorderTwo(Base):
    __tablename__ = 't_bigorder_two'
    __table_args__ = {'comment': '两项公排表'}

    id = Column(Integer, primary_key=True, comment='标识id')
    layer_id = Column(Integer, index=True, server_default=text("'0'"), comment='行号(所在层数)')
    cur_layer_id = Column(Integer, server_default=text("'0'"), comment='当前行号从左到右排序号')
    cur_layer_total = Column(Integer, server_default=text("'0'"), comment='当前行排序总数量')
    parent_id = Column(Integer, index=True, server_default=text("'0'"), comment='上级对应序号')
    order_id = Column(Integer, nullable=False, index=True, server_default=text("'0'"), comment='大公排id')


class TBusinessContent(Base):
    __tablename__ = 't_business_content'
    __table_args__ = {'comment': '特约商户进件表'}

    id = Column(Integer, primary_key=True, comment='标识id')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    business_code = Column(VARCHAR(150), comment='业务申请编号')
    contact_type = Column(CHAR(20), comment='超级管理员类型LEGAL：经营者/法人,SUPER：经办人')
    contact_name = Column(VARCHAR(150), comment='超级管理员姓名')
    contact_id_doc_type = Column(CHAR(100), comment='当超级管理员类型是经办人时，请上传超级管理员证件类型')
    contact_license_info = Column(Integer, server_default=text("'0'"), comment='超管license表ID,授权函license_copy_other1')
    contact_openid = Column(CHAR(100), comment='该字段选填，若上传为超级管理员签约时，会校验微信号是否与该微信OpenID一致')
    contact_mobile_phone = Column(CHAR(50), comment='联系手机')
    contact_email = Column(CHAR(100), comment='联系邮箱')
    subject_type = Column(CHAR(50), comment='主体类型需与营业执照/登记证书上一致')
    subject_finance_institution = Column(TINYINT, server_default=text("'0'"), comment='是否是金融机构,0不是(false),1是(true)')
    subject_business_license_info = Column(Integer, server_default=text("'0'"), comment='营业执照license表ID')
    subject_certificate_info = Column(Integer, server_default=text("'0'"), comment='登记证书license表ID')
    subject_certificate_letter_copy = Column(Integer, server_default=text("'0'"), comment='单位证明函照片license表ID')
    subject_finance_institution_info = Column(Integer, server_default=text("'0'"), comment='金融机构许可证信息license表ID')
    subject_identity_info = Column(Integer, server_default=text("'0'"), comment='经营者/法人身份证件license表ID')
    subject_ubo_info_list = Column(CHAR(20), comment='最终受益人信息列表(UBO),license表ID：1,2,3')
    business_merchant_shortname = Column(VARCHAR(150), comment='商户简称')
    business_service_phone = Column(CHAR(20), comment='客服电话')
    business_sales_scenes_type = Column(CHAR(255), comment='经营场景类型如:SALES_SCENES_STORE,SALES_SCENES_MP')
    sales_biz_store_info = Column(Integer, server_default=text("'0'"), comment='线下场所场景license表ID')
    sales_mp_info = Column(Integer, server_default=text("'0'"), comment='公众号场景license表ID')
    sales_mini_program_info = Column(Integer, server_default=text("'0'"), comment='小程序场景license表ID')
    sales_app_info = Column(Integer, server_default=text("'0'"), comment='App场景license表ID')
    sales_web_info = Column(Integer, server_default=text("'0'"), comment='互联网网站场景license表ID')
    sales_wework_info = Column(Integer, server_default=text("'0'"), comment='企业微信场景license表ID')
    settlement_id = Column(CHAR(50), comment='入驻结算规则ID')
    settlement_qualification_type = Column(CHAR(50), comment='所属行业')
    settlement_qualifications = Column(Integer, server_default=text("'0'"), comment='特殊资质图片license表ID')
    settlement_activities_id = Column(CHAR(50), comment='优惠费率活动ID')
    settlement_activities_rate = Column(CHAR(50), comment='优惠费率活动值')
    settlement_debit_activities_rate = Column(CHAR(50), comment='非信用卡活动费率值')
    settlement_credit_activities_rate = Column(CHAR(50), comment='信用卡活动费率值')
    settlement_activities_additions = Column(Integer, server_default=text("'0'"), comment='优惠费率活动补充材料license表ID')
    bank_account_type = Column(CHAR(100), comment='账户类型')
    bank_account_name = Column(VARCHAR(150), comment='开户名称')
    bank_account_bank = Column(VARCHAR(150), comment='开户银行')
    bank_address_code = Column(CHAR(100), comment='开户银行省市编码')
    bank_branch_id = Column(CHAR(100), comment='开户银行联行号')
    bank_name = Column(VARCHAR(300), comment='开户银行全称（含支行）')
    bank_account_number = Column(CHAR(100), comment='银行账号')
    addition_msg = Column(VARCHAR(600), comment='补充说明')
    addition_info = Column(Integer, server_default=text("'0'"), comment='补充材料license表ID')
    audit_stat = Column(TINYINT, server_default=text("'0'"), comment='状态,0未提交,1提交成功,2提交失败,3审核成功,4审核失败')
    subject_ubo_id_owner = Column(TINYINT, server_default=text("'1'"), comment='法人是否是收益人')


class TBusinessLicense(Base):
    __tablename__ = 't_business_license'
    __table_args__ = {'comment': '特约商户证件场景表'}

    id = Column(Integer, primary_key=True, comment='标识id')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    business_id = Column(Integer, server_default=text("'0'"), comment='特约主表id')
    lic_name = Column(VARCHAR(150), comment='证件名称，如：营业执照')
    lic_type = Column(CHAR(100), comment='证件类型:contact超管,license营业,certificate登记证书,finance金融许可,card经营者,other其他,ubo受益人,biz线下场景,mp公众号mini小程序,app,web网站场景wework企业微信')
    lic_type_name = Column(String(150), comment='证件类型名称')
    lic_number = Column(CHAR(100), comment='证件号码')
    lic_copy = Column(String(300), comment='证件正面照片')
    lic_copy_wx = Column(String(150), comment='证件正面微信MediaID')
    lic_copy_back = Column(String(300), comment='证件反面照片')
    lic_copy_back_wx = Column(String(150), comment='证件反面微信MediaID')
    lic_copy_other1 = Column(String(300), comment='附加照片1')
    lic_copy_other1_wx = Column(String(150), comment='附加照片1微信MediaID')
    lic_copy_other2 = Column(String(300), comment='附加照片2')
    lic_copy_other2_wx = Column(String(150), comment='附加照片2微信MediaID')
    lic_copy_array = Column(Text, comment='多张照片pic1,pic2')
    lic_copy_array_wx = Column(Text, comment='多张照片微信MediaID')
    lic_period_begin = Column(TIMESTAMP, comment='证件有效期开始时间')
    lic_period_end = Column(TIMESTAMP, comment='证件有效期结束时间')
    lic_person1 = Column(VARCHAR(150), comment='证件上的名称1,如公司名称,省份证姓名')
    lic_person2 = Column(VARCHAR(150), comment='证件上的名称2,如法人姓名')
    lic_address = Column(String(500), comment='证件地址')
    lic_person_video = Column(String(300), comment='视频材料')
    lic_person_video_wx = Column(String(150), comment='视频材料微信MediaID')
    lic_period_end_long = Column(TINYINT, server_default=text("'0'"), comment='证件是否长期有效')


class TCart(Base):
    __tablename__ = 't_cart'
    __table_args__ = {'comment': '购物车表'}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, comment='用户编号')
    good_id = Column(Integer, comment='商品编号')
    amount = Column(Integer, comment='购买数量')
    creat_time = Column(TIMESTAMP, comment='创建时间')
    good_spec_id = Column(Integer)
    good_option_id = Column(Integer, server_default=text("'0'"), comment='商品选项id')
    good_option_name = Column(VARCHAR(100), comment='选项名称')
    zdyspec = Column(Text, comment='用户所选自定义规格')


class TCategory(Base):
    __tablename__ = 't_category'
    __table_args__ = {'comment': '此表使用中   对应商品的四大分类，商品种类'}

    id = Column(Integer, primary_key=True)
    cname = Column(String(128), comment='分类名称')
    parent_category_id = Column(Integer, server_default=text("'0'"), comment='上级分类id，默认0为顶级分类')


class TCity(Base):
    __tablename__ = 't_city'
    __table_args__ = {'comment': '地区表省，市，区'}

    id = Column(Integer, primary_key=True)
    cname = Column(String(128))
    parid = Column(Integer, server_default=text("'0'"), comment='上级地区id，默认0为顶级地区')
    status = Column(TINYINT(1), server_default=text("'0'"), comment='地区状态')


class TCoin(Base):
    __tablename__ = 't_coin'
    __table_args__ = {'comment': '用户的积分历史记录'}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, comment='外键')
    change = Column(Integer, nullable=False, server_default=text("'0'"), comment='变动')
    coin = Column(Integer, nullable=False, comment='积分')
    type = Column(VARCHAR(20), nullable=False, comment='类型')
    description = Column(VARCHAR(100), comment='详细')
    create_time = Column(TIMESTAMP, comment='创建时间')
    out_trade_no = Column(String(64))
    user_nick = Column(String(45), comment='用户昵称')
    phone = Column(VARCHAR(45), comment='联系方式')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='注册时间')


class TCombo(Base):
    __tablename__ = 't_combo'

    id = Column(Integer, primary_key=True)
    good_id = Column(Integer)
    title = Column(String(45))
    amount = Column(Integer)
    price = Column(Integer)


class TComment(Base):
    __tablename__ = 't_comment'
    __table_args__ = {'comment': '平台用户反馈留言表'}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, comment='会员id')
    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    phone = Column(VARCHAR(45), comment='联系方式')
    content = Column(Text, comment='留言内容')
    status = Column(TINYINT, server_default=text("'0'"), comment='留言处理状态 ')


class TCouponTag(Base):
    __tablename__ = 't_coupon_tag'
    __table_args__ = {'comment': '卡券标签表'}

    id = Column(Integer, primary_key=True, unique=True)
    status = Column(TINYINT, server_default=text("'0'"), comment='标签状态：0为正常，-1为删除')
    tname = Column(String(45), comment='标签名称')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='标签创建时间')
    pro_id = Column(Integer, server_default=text("'0'"), comment='所属行业id，t_store_profession表id')
    operator_id = Column(Integer, comment='操作员ID')


class TDeliveryRule(Base):
    __tablename__ = 't_delivery_rule'
    __table_args__ = {'comment': '商品的邮寄规则，例如有的区域可以运送，有的不行，然后有的区域是免邮费，有的不能免邮费，这里记录这些规则'}

    id = Column(Integer, primary_key=True)
    good_id = Column(Integer, comment='商品id')
    spec_id = Column(Integer, comment='规格id')
    province = Column(VARCHAR(45), comment='省')
    city = Column(VARCHAR(45), comment='市')
    area = Column(VARCHAR(45), comment='区')
    is_reachable = Column(TINYINT(1), comment='是否可抵达    0：不可抵达     1：可抵达')
    delivery_fee = Column(Integer, server_default=text("'0'"), comment='邮寄费用')


class TExportFile(Base):
    __tablename__ = 't_export_files'
    __table_args__ = {'comment': '导出文件列表'}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, server_default=text("'0'"), comment='用户id')
    export_url = Column(VARCHAR(256), comment='文件生成地址')
    type = Column(VARCHAR(20), comment='类型')
    description = Column(VARCHAR(100), comment='详细描述')
    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')


class TFlashOrder(Base):
    __tablename__ = 't_flash_order'
    __table_args__ = {'comment': '秒杀订单表'}

    id = Column(Integer, primary_key=True, unique=True)
    package_id = Column(Integer, comment='包id')
    status = Column(TINYINT, nullable=False, comment='状态   0：未付款    1：已付款    2：未发货    3：已发货    4：已签收     5：退货申请    6：退货中    7：已退货    8：取消交易')
    create_time = Column(TIMESTAMP, comment='下单时间')
    paid_time = Column(TIMESTAMP, comment='付款时间')
    user_id = Column(Integer, nullable=False, comment='用户id')
    number = Column(Integer, comment='商品数量')
    flash_price = Column(Integer, comment='秒杀单价')
    flash_cost = Column(Integer, comment='秒杀成本')
    out_trade_no = Column(String(64))
    paid_amount = Column(Integer, comment='支付金额')
    paid_balance = Column(Integer, comment='余额支付金额')
    single_status = Column(TINYINT(1), comment='是否单份代卖')
    sold = Column(Integer, comment='已售出商品数量')
    whole_status = Column(TINYINT(1), comment='是否整份代码,暂时废弃,统一启用single_status字段判断')
    spec_id = Column(Integer, comment='规格id')
    put_on_time = Column(TIMESTAMP, comment='上架时间,计算收益时使用')
    detail = Column(Text, comment='订单备注,+=更新')
    is_assign_income = Column(TINYINT(1), server_default=text("'0'"), comment='是否分配收益')
    complete_time = Column(TIMESTAMP, comment='订单完结时间')
    return_sold = Column(Integer, server_default=text("'0'"), comment='已提货数量')


class TFlashOrderReturn(Base):
    __tablename__ = 't_flash_order_return'
    __table_args__ = {'comment': '秒杀订单退货收益表'}

    id = Column(Integer, primary_key=True, unique=True, comment='主键id')
    user_id = Column(Integer, server_default=text("'0'"), comment='用户id')
    income_days = Column(Integer, server_default=text("'0'"), comment='剩余秒杀退货收益天数')
    latest_time = Column(TIMESTAMP, comment='最近一次退货时间')
    latest_income_user = Column(Integer, server_default=text("'0'"), comment='最近一次退货收益')
    latest_income_layer = Column(Integer, server_default=text("'0'"), comment='最近一次退货层级收益')
    latest_income_toper = Column(Integer, server_default=text("'0'"), comment='最近一次退货见点收益')
    latest_income_groupsir = Column(Integer, server_default=text("'0'"), comment='最近一次退货团长收益')


class TPackageOrderStatus(Base):
    __tablename__ = 't_flash_order_status'

    id = Column(Integer, primary_key=True)
    title = Column(String(45))


class TFund(Base):
    __tablename__ = 't_fund'
    __table_args__ = {'comment': '资金池表'}

    id = Column(Integer, primary_key=True, comment='标识id编号')
    zhouqi = Column(Integer, server_default=text("'0'"), comment='属期数字(年+月202401)')
    good_id = Column(Integer, server_default=text("'0'"), comment='商品id')
    order_id = Column(Integer, server_default=text("'0'"), comment='订单id')
    balance = Column(Integer, server_default=text("'0'"), comment='金额')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    fenpei_time = Column(TIMESTAMP, comment='分配时间')
    status = Column(TINYINT, server_default=text("'0'"), comment='状态(0未分配，1已分配)')


class TFundFplog(Base):
    __tablename__ = 't_fund_fplog'
    __table_args__ = {'comment': '资金池合伙人分配记录表'}

    id = Column(Integer, primary_key=True, comment='标识id编号')
    zhouqi = Column(Integer, server_default=text("'0'"), comment='属期数字(年+月202401)')
    balance_fen = Column(Integer, server_default=text("'0'"), comment='分红金额')
    balance_total = Column(Integer, server_default=text("'0'"), comment='总金额')
    balance = Column(Integer, server_default=text("'0'"), comment='余额')
    user_id = Column(Integer, server_default=text("'0'"), comment='合伙人id')
    user_phone = Column(CHAR(100), comment='电话')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    user_name = Column(CHAR(100), comment='合伙人昵称')
    prom = Column(Integer, server_default=text("'0'"), comment='分红比例除以100')
    user_id_fen = Column(Text, comment='分红时计数的合伙人ID1,2,3')


class TFundPartner(Base):
    __tablename__ = 't_fund_partner'
    __table_args__ = {'comment': '合伙人关系记录表'}

    id = Column(Integer, primary_key=True, comment='标识id编号')
    zhouqi = Column(Integer, server_default=text("'0'"), comment='属期数字(年+月202401)')
    user_id = Column(Integer, server_default=text("'0'"), comment='合伙人会员id')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    parent_id = Column(Integer, server_default=text("'0'"), comment='上级合伙人id')


class TFundPond(Base):
    __tablename__ = 't_fund_pond'
    __table_args__ = {'comment': '资金池周期表'}

    id = Column(Integer, primary_key=True, comment='序号id')
    date_num = Column(String(100), comment='期id(初级one20250818,高级two20250818,顶级three20250818)')
    stat = Column(TINYINT, server_default=text("'0'"), comment='是否结算,默认0待结算1已结算')
    balance = Column(Integer, server_default=text("'0'"), comment='金额')
    run_balance = Column(Integer, server_default=text("'0'"), comment='执行金额')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    end_time = Column(TIMESTAMP, comment='截止时间')
    run_time = Column(TIMESTAMP, comment='执行时间')
    users = Column(Text, comment='当前达标人(逗号分开的会员id)')
    detail = Column(Text, comment='备注')
    ftype = Column(TINYINT, server_default=text("'0'"), comment='资金类型:0初级1高级2顶级')
    users_time = Column(TIMESTAMP, comment='会员归集时间')


class TFundPondLog(Base):
    __tablename__ = 't_fund_pond_log'
    __table_args__ = {'comment': '资金池集资记录表'}

    id = Column(Integer, primary_key=True, comment='序号id')
    add_balance = Column(Integer, server_default=text("'0'"), comment='增加金额')
    all_balance = Column(Integer, server_default=text("'0'"), comment='资金余额')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    source_id = Column(Integer, server_default=text("'0'"), comment='来源商品id')
    source_cont = Column(String(200), comment='来源备注')


class TFundRunLog(Base):
    __tablename__ = 't_fund_run_log'
    __table_args__ = {'comment': '资金池执行记录表'}

    id = Column(Integer, primary_key=True, comment='序号id')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    user_id = Column(Integer, server_default=text("'0'"), comment='用户id')
    user_phone = Column(String(100), comment='用户电话')
    weight = Column(Integer, server_default=text("'0'"), comment='当前权重')
    run_balance = Column(Integer, server_default=text("'0'"), comment='执行金额')
    stat = Column(TINYINT, server_default=text("'0'"), comment='是否成功,默认0成功1失败')


class TFundWeightLog(Base):
    __tablename__ = 't_fund_weight_log'
    __table_args__ = {'comment': '资金池权重增加记录表'}

    id = Column(Integer, primary_key=True, comment='序号id')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    user_id = Column(Integer, server_default=text("'0'"), comment='推荐人用户id')
    user_phone = Column(String(100), comment='用户电话')
    weight = Column(Integer, server_default=text("'0'"), comment='增加权重')
    all_balance = Column(Integer, server_default=text("'0'"), comment='权重余额')
    add_rec = Column(Integer, server_default=text("'0'"), comment='增加推荐有效人数')
    all_rec = Column(Integer, server_default=text("'0'"), comment='总推荐有效人数')
    source_id = Column(Integer, server_default=text("'0'"), comment='权重来源会员,购买礼包的会员')


class TFundZqlog(Base):
    __tablename__ = 't_fund_zqlog'
    __table_args__ = {'comment': '资金池属期分配记录表'}

    id = Column(Integer, primary_key=True, comment='标识id编号')
    zhouqi = Column(Integer, server_default=text("'0'"), comment='属期id')
    balance = Column(Integer, server_default=text("'0'"), comment='分配金额')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    fenpei_num = Column(Integer, server_default=text("'0'"), comment='分配人数')
    status = Column(TINYINT, server_default=text("'0'"), comment='分配成功0分配失败1')
    fenpei_users = Column(Text, comment='备注')
    user_id = Column(Integer, server_default=text("'0'"), comment='获奖用户id')
    balance_pro = Column(Float, server_default=text("'0'"), comment='分配百分比')


class TGood(Base):
    __tablename__ = 't_good'
    __table_args__ = {'comment': '商品表'}

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(VARCHAR(45), comment='产品名称')
    is_flash_sale = Column(Integer, comment='是否参加秒杀')
    category_id = Column(Integer, comment='大类别ID   关联t_category表')
    type = Column(TINYINT, server_default=text("'1'"), comment='0:普通商品 1:报单商品')
    num_sale = Column(Integer, comment='销量')
    image_url = Column(Text, comment='主图片url')
    priority = Column(Integer, comment='优先级  越小越好')
    add_coin = Column(Integer, comment='购买后给予多少积分')
    model_id = Column(Integer, server_default=text("'0'"), comment='所属团长id')
    expired_time = Column(TIMESTAMP, comment='过期时间')
    parent_good_id = Column(Integer, comment='如果是套餐产品，这个是父商品id')
    title = Column(VARCHAR(256), comment='主标题        如糖醋鱼的标题是美食')
    subtitle = Column(VARCHAR(256), comment='副标题')
    stock_cordon = Column(Integer, comment='库存警戒线')
    status = Column(TINYINT, server_default=text("'1'"), comment='0: 下架   1: 上架 ')
    details = Column(VARCHAR(256), comment='商品详情描述')
    supplier_id = Column(Integer, comment='供应商id')
    share_ratio = Column(Integer, comment='分成比例')
    create_time = Column(TIMESTAMP, comment='添加时间')
    last_update_time = Column(TIMESTAMP, comment='最后修改时间')
    saleable = Column(TINYINT(1), server_default=text("'1'"), comment='0：下架  1：上架')
    click_count = Column(Integer, comment='点击量')
    transmit_count = Column(Integer, comment='转发量')
    coinable = Column(TINYINT, server_default=text("'0'"), comment='0:不可以使用优惠券1:可使用')
    price_line = Column(Integer, comment='商品划价线')
    introducer_id = Column(Integer, comment='介绍人id')
    sell_high = Column(Integer, comment='最高售价')
    sell_low = Column(Integer, comment='最低售价')
    cost_high = Column(Integer, comment='最高成本')
    cost_low = Column(Integer, comment='最低成本')
    display = Column(TINYINT, server_default=text("'1'"), comment='显示位置          1:顶部       0:底部')
    coinable_number = Column(Integer, comment='优惠券可用额度')
    is_package = Column(TINYINT)
    fake_owner_name = Column(String(45), comment='临时数据   负责人名称')
    fake_owner_phone = Column(String(45), comment='临时数据   负责人电话')
    unavailable_date = Column(String(45), comment='不可用时间')
    available_time = Column(String(45))
    usage_rule = Column(String(45))
    refund_rule = Column(String(45))
    order_expired_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='订单过期时间，用户下单后这个日期会被复制code_expired_time，后期修改不影响已下单过期时间')
    cover_url = Column(VARCHAR(256), comment='封面图片url')
    video_url = Column(VARCHAR(256), comment='视频url')
    is_wholesale = Column(TINYINT(1), server_default=text("'0'"), comment='是不是成为批发商商品，0为默认普通产品，1为批发商产品')
    zdyspec = Column(Text, comment='自定义规格')
    sale_type = Column(TINYINT(1), server_default=text("'0'"), comment='商品经营类型，0自营，1商家产品')
    admin_id = Column(Integer, server_default=text("'0'"), comment='所属商家管理id')
    admin_audit = Column(Integer, server_default=text("'0'"), comment='商家商品审核状态0未审核1审核通过2未通过')
    admin_info = Column(VARCHAR(256), comment='审核说明')
    video_level = Column(TINYINT(1), server_default=text("'0'"), comment='视频分发身份0达人,1店长,2服务商,3分公司')
    video_num = Column(Integer, server_default=text("'0'"), comment='获取合成视频条数')
    is_video = Column(TINYINT(1), server_default=text("'0'"), comment='是否视频分发礼包产品,设置为1')
    live_mid_uid = Column(Integer, server_default=text("'0'"), comment='居间人id')
    live_mid_money = Column(Integer, server_default=text("'0'"), comment='居间人收益')


class TGoodCategory(Base):
    __tablename__ = 't_good_category'
    __table_args__ = {'comment': '此表不用'}

    id = Column(Integer, primary_key=True)
    title = Column(VARCHAR(128), comment='小类别名称   比如火锅、烧烤')
    general_id = Column(Integer, comment='大类id     关联t_category表')


class TGoodImage(Base):
    __tablename__ = 't_good_image'
    __table_args__ = {'comment': '一个商品存在多张图片'}

    id = Column(Integer, primary_key=True)
    image = Column(VARCHAR(256), comment='商品图片url')
    good_id = Column(Integer, comment='商品id')


class TGoodIntroducer(Base):
    __tablename__ = 't_good_introducer'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(45), comment='介绍人名称')
    phone = Column(VARCHAR(25), comment='介绍人电话')
    address = Column(VARCHAR(100), comment='介绍人住址')
    id_card = Column(String(25), comment='介绍人身份证')


class TGoodModel(Base):
    __tablename__ = 't_good_model'

    id = Column(Integer, primary_key=True, unique=True)
    model = Column(String(25))


class TGoodOption(Base):
    __tablename__ = 't_good_option'
    __table_args__ = {'comment': '商品选项表'}

    id = Column(Integer, primary_key=True)
    good_id = Column(Integer, nullable=False, comment='商品id')
    good_spec_id = Column(Integer, comment='商品规格ID')
    opt_name = Column(VARCHAR(100), comment='选项名称')
    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    status = Column(TINYINT(1), server_default=text("'0'"), comment='0为正常状态，-1是删除')
    operator_id = Column(Integer, comment='操作员ID')


class TGoodPackage(Base):
    __tablename__ = 't_good_package'
    __table_args__ = {'comment': '商品套餐表，包含套餐商品下的菜品等'}

    id = Column(Integer, primary_key=True)
    number = Column(String(20), comment='商品份数')
    price = Column(String(20), comment='单价')
    title = Column(VARCHAR(100), comment='商品标题')
    create_time = Column(TIMESTAMP, comment='创建时间')
    good_id = Column(Integer, comment='商品id')


class TGoodPerson(Base):
    __tablename__ = 't_good_person'

    id = Column(Integer, primary_key=True)
    good_id = Column(Integer, comment='商品编号')
    person_id = Column(Integer, comment='人数id')


class TGoodPersonState(Base):
    __tablename__ = 't_good_person_state'
    __table_args__ = {'comment': '套餐商品人数'}

    id = Column(Integer, primary_key=True)
    title = Column(String(100), comment='使用人数')


class TGoodPriority(Base):
    __tablename__ = 't_good_priority'

    id = Column(Integer, primary_key=True)
    title = Column(String(100))


class TGoodRule(Base):
    __tablename__ = 't_good_rule'

    id = Column(Integer, primary_key=True)
    good_id = Column(Integer, comment='商品id')
    create_time = Column(TIMESTAMP, comment='创建时间')
    validate_day = Column(String(100), comment='有效期    例如： 2023.04.19   至  2024.04.19')
    unuseful_day = Column(String(100), comment='不可用日期     例如： 2023.05.01 至 2024.05.07')
    useful_time = Column(String(100), comment='可用时间      例如：24小时可用       14:00-20:00可用等')
    use_rule = Column(String(512), comment='使用规则')
    return_rule = Column(String(100), comment='退货规则')
    room = Column(TINYINT, comment='0:不可使用包间     1：可使用包间')
    title = Column(String(256))
    value = Column(String(256))


class TGoodSpec(Base):
    __tablename__ = 't_good_spec'
    __table_args__ = {'comment': '一个商品存在多个规格    关联商品表'}

    good_id = Column(Integer, comment='商品id')
    price = Column(Integer, comment='售价')
    cost = Column(Integer, comment='成本')
    value = Column(VARCHAR(128), comment='规格的值    例如：糖醋里脊的甜口、酸口')
    id = Column(Integer, primary_key=True, unique=True)
    stock = Column(Integer, comment='库存')
    price_line = Column(Integer, comment='划价线')
    image = Column(String(256), comment='图片url')
    is_sub_good = Column(TINYINT, server_default=text("'0'"))
    num_sale = Column(Integer, comment='销量')
    parent_fee = Column(Integer, server_default=text("'0'"), comment='分层奖，上一级的奖励')
    top_fee = Column(Integer, server_default=text("'0'"), comment='见点奖，第一高级会员分成')
    recommender_fee = Column(Integer, server_default=text("'0'"), comment='售出奖，推荐人的奖励')
    supplier_fee = Column(Integer, server_default=text("'0'"), comment='供货收益')
    lower_num_people = Column(Integer, comment='人数下限')
    upper_num_people = Column(Integer, comment='人数上限')
    room = Column(String(45), comment='包间')
    post = Column(Text)
    status = Column(TINYINT, server_default=text("'1'"), comment='0: 下架   1: 上架 ')
    share_fee = Column(Integer, server_default=text("'0'"), comment='分享商品收益')
    is_default = Column(TINYINT(1), server_default=text("'0'"), comment='是否默认规格')
    spec_num = Column(VARCHAR(200), comment='商品规格编号')
    profit = Column(Integer, server_default=text("'0'"), comment='产品利润')
    eqlevel_fee = Column(Integer, server_default=text("'0'"), comment='平级奖 直推关系下见点收益的推荐人收益')
    wholesale_fee = Column(Integer, server_default=text("'0'"), comment='批发商返利')
    wholesale_price = Column(Integer, server_default=text("'0'"), comment='批发价')
    purchase_price = Column(Integer, server_default=text("'0'"), comment='进价')
    freight_txt = Column(Integer, server_default=text("'0'"), comment='运费')
    taxation_txt = Column(Integer, server_default=text("'0'"), comment='税费')
    recommender2_fee = Column(Integer, server_default=text("'0'"), comment='额外的推荐人奖励')
    kg_num = Column(Integer, server_default=text("'0'"), comment='商品克重（克）')
    is_pifa = Column(TINYINT(1), server_default=text("'0'"), comment='是否批发商品,默认0,1为是')
    is_single = Column(TINYINT(1), server_default=text("'0'"), comment='是否单份代卖,默认0单份,1为整份')
    pifa_num = Column(Integer, comment='单份批发商品数量')
    unitprice_diff = Column(Integer, comment='单份批发商品差价')
    random_fee = Column(Integer, server_default=text("'0'"), comment='给批发商的随机分润')
    tuan_uid = Column(Integer, server_default=text("'0'"), comment='团长分润id')
    retuan_uid = Column(Integer, server_default=text("'0'"), comment='上级团长分润id')
    tuan_fee = Column(Integer, server_default=text("'0'"), comment='团长分润')
    retuan_fee = Column(Integer, server_default=text("'0'"), comment='上级团长分润')


class TGoodSpecCombo(Base):
    __tablename__ = 't_good_spec_combo'

    id = Column(Integer, primary_key=True)
    good_spec_id = Column(Integer)
    value = Column(String(45))
    price = Column(Integer)
    amount = Column(String(256), comment='数量')


class TGoodSpecDetail(Base):
    __tablename__ = 't_good_spec_detail'

    id = Column(Integer, primary_key=True)
    good_spec_id = Column(Integer, index=True)
    detail = Column(LONGTEXT)


class TGoodSpecImage(Base):
    __tablename__ = 't_good_spec_image'
    __table_args__ = {'comment': '该规格的图片'}

    id = Column(Integer, primary_key=True)
    spec_id = Column(Integer, comment='规格id')
    image = Column(String(256), comment='图片url')


class TGoodStore(Base):
    __tablename__ = 't_good_store'

    id = Column(Integer, primary_key=True)
    good_id = Column(Integer)
    store_id = Column(Integer)


class TGoodText(Base):
    __tablename__ = 't_good_text'

    id = Column(Integer, primary_key=True)
    good_id = Column(Integer, comment='商品id')
    description = Column(LONGTEXT, comment='图文详情   图片和文字放在一起')
    create_time = Column(TIMESTAMP, comment='创建时间')


class TGoodType(Base):
    __tablename__ = 't_good_type'

    id = Column(Integer, primary_key=True)
    type = Column(String(25))


class TGroupsir(Base):
    __tablename__ = 't_groupsir'
    __table_args__ = {'comment': '团购团长表'}

    id = Column(Integer, primary_key=True, unique=True, comment='团长id')
    user_id = Column(Integer, server_default=text("'0'"), comment='关联t_user表id')
    parent_id = Column(Integer, server_default=text("'0'"), comment='0:表示团长，非0表示下级成员')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='成团时间和入团')
    status = Column(TINYINT, server_default=text("'0'"), comment='0: 启用   1: 暂停  -1：出团或解散')
    is_empower = Column(TINYINT, server_default=text("'0'"), comment='0: 未授权   1:已授权（可以使用所有商品秒杀包）')
    notes = Column(VARCHAR(512), comment='团员备注')


class TGroupsirlog(Base):
    __tablename__ = 't_groupsirlog'
    __table_args__ = {'comment': '生成记录表'}

    id = Column(Integer, primary_key=True)
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    user_id = Column(Integer, comment='变动账号id')
    groupsir_id = Column(Integer, comment='团长id')
    admin_id = Column(Integer, comment='操作员id')
    logtype = Column(String(120), comment='变动类型：入团、出团、建团、消团')


class TLevel(Base):
    __tablename__ = 't_level'

    id = Column(Integer, primary_key=True, unique=True)
    title = Column(String(45))


class TLockBalance(Base):
    __tablename__ = 't_lock_balance'
    __table_args__ = {'comment': '锁定额历史记录表'}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, comment='外键')
    change = Column(Integer, server_default=text("'0'"), comment='变动')
    lock_balance = Column(Integer, comment='锁定金额')
    type = Column(VARCHAR(20), comment='类型')
    description = Column(VARCHAR(100), comment='描述')
    create_time = Column(TIMESTAMP, comment='创建时间')
    out_trade_no = Column(String(64))


class TModel(Base):
    __tablename__ = 't_model'
    __table_args__ = {'comment': '规格表，已被遗弃'}

    id = Column(Integer, primary_key=True, unique=True)
    product_id = Column(Integer)


class TNotice(Base):
    __tablename__ = 't_notice'
    __table_args__ = {'comment': '系统通知表'}

    id = Column(Integer, primary_key=True)
    user_ids = Column(VARCHAR(600), comment='通知用户，逗号分隔的用户id;值为all则表示所有用户')
    type = Column(VARCHAR(20), comment='类别：系统通知、收益通知')
    title = Column(VARCHAR(300), comment='标题')
    description = Column(Text, comment='通知内容')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='通知时间')
    status = Column(TINYINT, comment='0: 正常  -1: 删除')


class TOrder(Base):
    __tablename__ = 't_order'
    __table_args__ = {'comment': '商品订单表（不包含秒杀订单)    1.创建时间与支付时间有本质区别'}

    id = Column(Integer, primary_key=True, unique=True, comment='订单id')
    good_id = Column(Integer, comment='商品id')
    paider_id = Column(Integer, comment='付款人id')
    sale_price = Column(Integer, comment='售价      记录客户购买时的商品价格（因为价格可能变动）')
    cost_price = Column(Integer, comment='成本       记录客户购买时的商品成本（因为成本可能变动）')
    create_time = Column(TIMESTAMP, comment='创建时间    与支付时间有本质区别')
    paid_time = Column(TIMESTAMP, comment='支付时间')
    status_id = Column(TINYINT, nullable=False, comment='状态id:0待付款、1待发货、2待收货、3已完成')
    number = Column(Integer, comment='商品数量')
    consignee_address = Column(VARCHAR(128), comment='收货人地址')
    consignee_phone = Column(VARCHAR(25), comment='收货人联系电话')
    store_id = Column(Integer, comment='店铺id')
    paid_amount = Column(Integer, comment='实际第三方支付的金额     用于标记除客户账户以外支付的金额（比如微信、银行卡)')
    delivery_fee = Column(Integer, comment='运费金额')
    spec_id = Column(Integer, comment='规格编号')
    paid_coin = Column(Integer, comment='实际支付的优惠券用于标记客户账户内支付的优惠券')
    delivery_track_code = Column(VARCHAR(25), comment='第三方物流单号  比如顺丰的单号')
    paid_channel_id = Column(Integer, comment='第三方支付渠道    比如微信支付  银行卡支付等')
    consignee_name = Column(VARCHAR(25), comment='收货人名称')
    delivery_time = Column(TIMESTAMP, comment='发货时间')
    good_name = Column(VARCHAR(45), comment='商品名称    记录客户购买时的商品名称（因为名称可能变动）')
    paid_track_code = Column(VARCHAR(45), comment='第三方支付流水号    比如微信支付提供的支付编码')
    paider_name = Column(String(100), comment='付款人姓名')
    paider_phone = Column(String(100), comment='付款人电话')
    paider_address = Column(VARCHAR(128), comment='付款人地址')
    supplier_id = Column(Integer, comment='商家id')
    paid_balance = Column(Integer, comment='实际支付的余额         用于标记客户账户内支付的余额')
    paid_lock_balance = Column(Integer, comment='实际支付的锁定额        用于标记客户账户内支付的锁定额')
    delivery_company = Column(VARCHAR(45), comment='第三方物流公司   比如圆通、顺丰等')
    complete_time = Column(TIMESTAMP, comment='订单完结时间')
    use_balance = Column(TINYINT(1), comment='是否使用余额')
    use_coin = Column(TINYINT(1), comment='是否使用积分')
    consignee_province = Column(String(45))
    consignee_description = Column(String(450))
    consignee_city = Column(String(45))
    consignee_area = Column(String(45))
    consignee_street = Column(String(45))
    out_trade_no = Column(String(64), comment='商户单号')
    code = Column(String(45), comment='虚拟消费券的code')
    code_expired_time = Column(TIMESTAMP, comment='虚拟消费券的过期时间')
    is_display = Column(TINYINT(1), nullable=False, server_default=text("'1'"), comment='是否可以展示')
    recommender_id = Column(Integer, comment='推荐人Id')
    detail = Column(Text, comment='订单备注,+=更新')
    is_assign_income = Column(TINYINT(1), server_default=text("'0'"), comment='是否分配收益')
    parent_uid = Column(Integer, server_default=text("'0'"), comment='层级收益人id')
    top_uid = Column(Integer, server_default=text("'0'"), comment='顶级收益人id')
    invited_uid = Column(Integer, server_default=text("'0'"), comment='直推收益人id')
    supplier_uid = Column(Integer, server_default=text("'0'"), comment='供货介绍收益人id')
    good_option_id = Column(Integer, server_default=text("'0'"), comment='商品选项id')
    good_option_name = Column(VARCHAR(100), comment='选项名称')
    user_detail = Column(String(300), comment='用户下单信息备注')
    zdyspec = Column(Text, comment='用户所选自定义规格')
    wholesale_id = Column(Integer, server_default=text("'0'"), comment='成为批发商类型的id')
    tuan_uid = Column(Integer, server_default=text("'0'"), comment='团长分润id')
    zdyspec_good = Column(Text, comment='选规格后商品规格')
    zdyspec_good_index = Column(Text, comment='用户所选自定义规格库存')
    isfirst = Column(TINYINT(1), server_default=text("'0'"), comment='是否首单礼包订单,默认0非首单礼包订单')
    detail_tut = Column(Text, comment='订单教程备注')
    is_video = Column(TINYINT(1), server_default=text("'0'"), comment='是否视频分发礼包产品订单,设置为1')
    act_uid = Column(Integer, server_default=text("'0'"), comment='激活收益人id卡密所属人')
    invited_two_uid = Column(Integer, server_default=text("'0'"), comment='间推收益人id')
    share_invited_uid = Column(Integer, server_default=text("'0'"), comment='分享推荐收益人id')
    share_invited_two_uid = Column(Integer, server_default=text("'0'"), comment='分享间推收益人id')
    retuan_uid = Column(Integer, server_default=text("'0'"), comment='间推团长分润id')
    is_user_price = Column(Integer, server_default=text("'0'"), comment='是否会员价订单,默认0为售价')
    live_mid_uid = Column(Integer, server_default=text("'0'"), comment='居间人id')
    live_mid_money = Column(Integer, server_default=text("'0'"), comment='居间人收益')
    ad_id = Column(Integer, server_default=text("'0'"), comment='来源广告id')
    sh_agent_id = Column(Integer, server_default=text("'0'"), comment='市代id')


class TOrderBatch(Base):
    __tablename__ = 't_order_batch'
    __table_args__ = {'comment': '订单批次表，例如五个商品同时购买，生成了五个订单，但是这五个订单是一个批次'}

    id = Column(Integer, primary_key=True)
    create_time = Column(TIMESTAMP)


class TOrderCheck(Base):
    __tablename__ = 't_order_check'
    __table_args__ = {'comment': '核销记录表'}

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, comment='订单id')
    check_num = Column(Integer, comment='核销数量')
    check_time = Column(TIMESTAMP, comment='核销时间')
    worker_id = Column(Integer, comment='核销人id，对应店铺的人员')
    check_amount = Column(Integer, comment='核销金额')


class TOrderReturn(Base):
    __tablename__ = 't_order_return'
    __table_args__ = {'comment': '退货订单表'}

    id = Column(Integer, primary_key=True, comment='退货编号')
    returner_name = Column(VARCHAR(45), comment='退款人姓名   对应订单表的付款人')
    returner_phone = Column(VARCHAR(45), comment='退款人电话   对应订单表的付款人')
    returner_address = Column(VARCHAR(100), comment='退款人地址   对应订单表的付款人')
    delivery_fee = Column(Integer, comment='退货运费')
    return_amount = Column(Integer, comment='第三方支付退款额度    比如退还微信10元')
    return_submit_time = Column(TIMESTAMP, comment='退货申请时间')
    return_reason = Column(String(128), comment='退货原因')
    order_id = Column(Integer, nullable=False, comment='订单编号     关联订单表')
    good_id = Column(Integer, nullable=False, comment='商品id')
    return_num = Column(Integer, comment='退货商品数量')
    store_id = Column(Integer, comment='店铺id')
    return_delivery_track_code = Column(VARCHAR(45), comment='第三方退货物流单号')
    status_id = Column(TINYINT, server_default=text("'3'"), comment='状态id     对应退款协商中、未处理、已退货')
    consignee_name = Column(String(100), comment='收货人姓名')
    consignee_phone = Column(String(100), comment='收货人电话')
    consignee_address = Column(String(100), comment='收货人地址')
    return_balance = Column(Integer, comment='客户账户余额退还额度')
    return_lock_balance = Column(Integer, comment='客户账户锁定额退还额度')
    return_coin = Column(Integer, comment='客户账户积分退还额度')
    return_delivery_company = Column(String(45), comment='第三方物流公司')
    return_paid_track_code = Column(String(45), comment='第三方退款流水号')


class TOrderReturnState(Base):
    __tablename__ = 't_order_return_state'

    id = Column(Integer, primary_key=True)
    state = Column(String(25), comment='退换货状态')


class TOrderReturnType(Base):
    __tablename__ = 't_order_return_type'
    __table_args__ = {'comment': '订单退货类型表'}

    id = Column(Integer, primary_key=True)
    type = Column(String(45), comment='类型')


class TOrderSource(Base):
    __tablename__ = 't_order_source'
    __table_args__ = {'comment': '商城订单的商品来源表'}

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, comment='订单id')
    source_id = Column(Integer, comment='订单来源，来再t_flash_order.id，如果是空或者-1表示平台')
    amount = Column(Integer, comment='商品数量')
    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    order_user_id = Column(Integer, server_default=text("'0'"), comment='订单购买用户id')
    package_user_id = Column(Integer, server_default=text("'0'"), comment='秒杀包用户id')


class TOrderState(Base):
    __tablename__ = 't_order_state'
    __table_args__ = {'comment': '订单状态表'}

    id = Column(Integer, primary_key=True)
    state = Column(VARCHAR(45), comment='订单状态')
    belong = Column(VARCHAR(100), comment='所属订单类别   比如发货  退货')


class TPackage(Base):
    __tablename__ = 't_package'
    __table_args__ = {'comment': '秒杀包表，记录商品，数量，以及价格等信息'}

    id = Column(Integer, primary_key=True, unique=True)
    good_id = Column(Integer, comment='产品id')
    amount = Column(Integer, comment='份数;the number of good in one amount一个包包含的产品的数量')
    flash_sale_price = Column(Integer, comment='秒杀价格;in cent,秒杀价格')
    num = Column(Integer, comment='包个数;一共有多少个包')
    stock = Column(Integer, comment='剩余包数量')
    seller_id = Column(Integer, comment='发布商品的卖家，如果id为空或者0，则为官方卖家')
    spec_id = Column(Integer, comment='规格id')
    share_fee = Column(Integer, comment='让利金额')
    status = Column(Integer, server_default=text("'0'"), comment='状态：-1删除, 默认0/null正常')
    devide_cost = Column(Integer, server_default=text("'0'"), comment='分润成本，商品规格分润之 和')


class TPackageExpress(Base):
    __tablename__ = 't_package_express'

    id = Column(Integer, primary_key=True)
    flash_order_id = Column(Integer)
    status = Column(Integer, comment='1: 申请中  2:  已发货  3: 拒绝发货退款  4：已签收  5:未使用  6:已使用')
    address_id = Column(Integer, comment='邮寄地址id')
    amount = Column(Integer, comment='邮寄数量')
    express_num = Column(String(128), comment='物流号')
    apply_time = Column(TIMESTAMP, comment='申请发货时间')
    delivery_time = Column(TIMESTAMP, comment='发货时间')
    complete_time = Column(TIMESTAMP, comment='签收或完成时间')
    detail = Column(Text, comment='订单备注,+=更新')


class TPackageExpressStatus(Base):
    __tablename__ = 't_package_express_status'

    id = Column(Integer, primary_key=True)
    title = Column(String(45))


class TPackageTime(Base):
    __tablename__ = 't_package_time'
    __table_args__ = {'comment': '秒杀包的秒杀时段'}

    id = Column(Integer, primary_key=True)
    start_time = Column(Integer, comment='开始时间;9*3600表示9:00')
    end_time = Column(Integer, comment='结束时间;以秒为单位')


class TPackageTimePair(Base):
    __tablename__ = 't_package_time_pair'
    __table_args__ = {'comment': '记录秒杀包和秒杀时段的关系'}

    id = Column(Integer, primary_key=True)
    package_id = Column(Integer)
    package_time_id = Column(Integer)
    status = Column(Integer, comment='状态; 0: 未激活, 1: 激活')
    package_num = Column(Integer, server_default=text("'0'"), comment='此时段秒杀包库存')


class TPayChannel(Base):
    __tablename__ = 't_pay_channel'

    id = Column(Integer, primary_key=True)
    type = Column(String(45), comment='支付方式')


class TPlatformLaw(Base):
    __tablename__ = 't_platform_law'

    id = Column(Integer, primary_key=True)
    create_time = Column(TIMESTAMP, comment='创建时间')
    admin_id = Column(Integer, comment='操作员id')
    law = Column(MEDIUMTEXT, comment='法律文本 用户协议')
    privacy = Column(MEDIUMTEXT, comment='法律文本 用户协议')
    purchase = Column(MEDIUMTEXT, comment='法律文本 用户协议')
    flash_law = Column(MEDIUMTEXT, comment='法律文本 用户协议')
    withdraw_law = Column(MEDIUMTEXT, comment='法律文本 用户协议')


class TPlatformNotice(Base):
    __tablename__ = 't_platform_notice'
    __table_args__ = {'comment': '平台通知表'}

    id = Column(Integer, primary_key=True)
    title = Column(String(128), comment='通知内容')
    create_time = Column(TIMESTAMP, comment='创建时间')
    admin_id = Column(Integer, comment='添加人id    对应哪个管理员')


class TPoster(Base):
    __tablename__ = 't_poster'
    __table_args__ = {'comment': '海报文件列表'}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, server_default=text("'0'"), comment='用户id')
    poster_url = Column(String(256), comment='海报文件地址')
    status = Column(String(20), comment='状态')
    description = Column(String(100), comment='描述')
    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')


class TPrize(Base):
    __tablename__ = 't_prize'
    __table_args__ = {'comment': '平台给用户的各种奖励记录表'}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, comment='会员id')
    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    status = Column(Integer, nullable=False, comment='奖励值')


class TRandompro(Base):
    __tablename__ = 't_randompro'
    __table_args__ = {'comment': '成为商户随机分润表'}

    id = Column(Integer, primary_key=True)
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    pro_oneid = Column(Integer, comment='收益人id')
    pro_twoid = Column(Integer, comment='分成人id')
    pro_price = Column(Integer, comment='分成价格')
    pro_num = Column(Float, server_default=text("'0'"), comment='分成比例')
    pro_balance = Column(Integer, server_default=text("'0'"), comment='分成获得额')
    order_id = Column(Integer, server_default=text("'0'"), comment='订单id')
    out_trade_no = Column(String(256), comment='商户单号')
    details = Column(String(900), comment='备注字段')


class TRoomContributelog(Base):
    __tablename__ = 't_room_contributelog'
    __table_args__ = {'comment': '房间贡献值记录表'}

    id = Column(Integer, primary_key=True, comment='标识id编号')
    room_id = Column(Integer, server_default=text("'0'"), comment='房间id')
    contribute_val = Column(Integer, server_default=text("'0'"), comment='贡献值额度')
    user_id = Column(Integer, server_default=text("'0'"), comment='受益人id')
    source_id = Column(Integer, server_default=text("'0'"), comment='来源人id')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')


class TRoomgold(Base):
    __tablename__ = 't_roomgold'
    __table_args__ = {'comment': '房间表，七人间'}

    id = Column(Integer, primary_key=True)
    level = Column(TINYINT, server_default=text("'0'"), comment='房间级别')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='注册时间')
    start_time = Column(TIMESTAMP, comment='开始时间')
    end_time = Column(TIMESTAMP, comment='结束时间')
    status_val = Column(TINYINT, server_default=text("'0'"), comment='房间状态0:默认  1:进行中 2已结束')
    balance = Column(Integer, server_default=text("'0'"), comment='奖金金额')
    partner_id = Column(Integer, server_default=text("'0'"), comment='分裂时记录上级房间id')
    position_one = Column(Integer, server_default=text("'0'"), comment='位置1')
    contribute_one = Column(TINYINT, server_default=text("'0'"), comment='位置1的贡献值')
    position_two = Column(Integer, server_default=text("'0'"), comment='位置2')
    contribute_two = Column(TINYINT, server_default=text("'0'"), comment='位置2的贡献值')
    position_three = Column(Integer, server_default=text("'0'"), comment='位置3')
    contribute_three = Column(TINYINT, server_default=text("'0'"), comment='位置3的贡献值')
    position_four = Column(Integer, server_default=text("'0'"), comment='位置4')
    contribute_four = Column(TINYINT, server_default=text("'0'"), comment='位置4的贡献值')
    position_five = Column(Integer, server_default=text("'0'"), comment='位置5')
    contribute_five = Column(TINYINT, server_default=text("'0'"), comment='位置5的贡献值')
    position_six = Column(Integer, server_default=text("'0'"), comment='位置6')
    contribute_six = Column(TINYINT, server_default=text("'0'"), comment='位置6的贡献值')
    position_seven = Column(Integer, server_default=text("'0'"), comment='位置7')
    contribute_seven = Column(TINYINT, server_default=text("'0'"), comment='位置7的贡献值')
    position_one_time = Column(TIMESTAMP, comment='位置一加入时间')
    position_two_time = Column(TIMESTAMP, comment='位置二加入时间')
    position_three_time = Column(TIMESTAMP, comment='位置三加入时间')
    position_four_time = Column(TIMESTAMP, comment='位置四加入时间')
    position_five_time = Column(TIMESTAMP, comment='位置五加入时间')
    position_six_time = Column(TIMESTAMP, comment='位置六加入时间')
    position_seven_time = Column(TIMESTAMP, comment='位置七加入时间')


class TSdGuest(Base):
    __tablename__ = 't_sd_guest'
    __table_args__ = {'comment': '山东协会报名人员表'}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, comment='小程序会员id')
    topic_id = Column(Integer, comment='主题id')
    user_name = Column(String(120), comment='顾客姓名')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    phone = Column(String(45), comment='电话')
    user_num = Column(Integer, server_default=text("'0'"), comment='报名人数')
    price = Column(Integer, server_default=text("'0'"), comment='每人单价')
    total = Column(Integer, server_default=text("'0'"), comment='报名总额')
    status = Column(TINYINT, server_default=text("'0'"), comment='报名状态,0下单未支付,1下单已支付,2报名成功')
    short_var1 = Column(String(300), comment='短文1')
    short_var2 = Column(String(300), comment='短文2')
    short_var3 = Column(String(300), comment='短文3')
    short_var4 = Column(String(300), comment='短文4')
    short_var5 = Column(String(300), comment='短文5')
    short_var6 = Column(String(300), comment='短文6')
    short_var7 = Column(String(300), comment='短文7')
    short_var8 = Column(String(300), comment='短文8')
    short_var9 = Column(String(300), comment='短文9')


class TSdTopic(Base):
    __tablename__ = 't_sd_topic'
    __table_args__ = {'comment': '山东协会报名主题表'}

    id = Column(Integer, primary_key=True)
    tp_name = Column(String(300), comment='报名主题名称')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    cover_url = Column(String(256), comment='封面图片url')
    reg_num = Column(Integer, comment='报名人数')
    details = Column(Text, comment='主题详情描述')
    reg_field = Column(String(900), comment='报名字段')
    reg_status = Column(TINYINT, server_default=text("'0'"), comment='是否收费,0免费,1收费')
    price = Column(Integer, server_default=text("'0'"), comment='收费金额（每人）')
    status = Column(TINYINT, server_default=text("'0'"), comment='产品状态,0正常,1禁用')


class TSetting(Base):
    __tablename__ = 't_settings'
    __table_args__ = {'comment': '系统设置表'}

    id = Column(Integer, primary_key=True, unique=True, comment='标识id，修改时从1开始对应recommend_num之后的字段')
    recommend_num = Column(Integer, server_default=text("'0'"), comment='定义推荐系升级人数')
    flash_order_income = Column(Float, server_default=text("'0'"), comment='定义秒杀产品24小时停留收益比千分之')
    tuan_order_income = Column(Float, server_default=text("'0'"), comment='定义团长秒杀产品收益比（千分之）')
    flash_order_max = Column(Integer, server_default=text("'0'"), comment='秒杀用户持单量限制(未完成出售订单)')
    flash_order_money_max = Column(Integer, server_default=text("'0'"), comment='秒杀用户持单总金额限制(未完成出售订单)')
    flash_order_active_user = Column(Integer, server_default=text("'0'"), comment='秒杀并支付多少单，普通会员晋升活跃会员')
    consume_money_active_user = Column(Integer, server_default=text("'0'"), comment='完成商品订单达到指定额度，普通会员晋升活跃会员')
    many_high_user = Column(Integer, server_default=text("'0'"), comment='直推多少个活跃会员，晋升高级会员')
    many_top_user = Column(Integer, server_default=text("'0'"), comment='直推多少个高级会员，晋升顶级会员')
    flash_order_income_retio = Column(Float, server_default=text("'0'"), comment='秒杀人退货收益比（千分之）')
    flash_order_income_layer = Column(Float, server_default=text("'0'"), comment='秒杀人退货层级收益比（百分之）')
    flash_order_income_toper = Column(Float, server_default=text("'0'"), comment='秒杀人退货顶级收益比(百分比)')
    flash_order_income_groupsir = Column(Float, server_default=text("'0'"), comment='秒杀人退货团长收益比(百分比)')
    flash_order_owner_times = Column(Integer, server_default=text("'0'"), comment='秒杀包持有人退货时间限制（小时）')
    parent_user_limit = Column(Integer, server_default=text("'0'"), comment='推广人升级顶级时，留给原上级的人数')
    flash_order_income_subsidy = Column(Integer, server_default=text("'0'"), comment='团队补贴,秒杀的退款收益， 给直接推荐人 的一份')
    random_proportion = Column(Float, server_default=text("'0'"), comment='定义批发商随机分成比例益比（百分之）')
    random_max = Column(Integer, server_default=text("'0'"), comment='定义批发商随机分成最大分配次数')
    random_low = Column(Integer, server_default=text("'0'"), comment='定义批发商随机分成最小分配次数')
    ws1_proportion = Column(Float, server_default=text("'0'"), comment='wholesale1批发商随机分成比例益比（百分之）')
    ws2_proportion = Column(Float, server_default=text("'0'"), comment='wholesale2批发商随机分成比例益比（百分之）')
    ws3_proportion = Column(Float, server_default=text("'0'"), comment='wholesale3批发商随机分成比例益比（百分之）')


class TShConsumption(Base):
    __tablename__ = 't_sh_consumption'
    __table_args__ = {'comment': '会员在店铺消费表'}

    id = Column(Integer, primary_key=True)
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    pro_name = Column(String(120), comment='消费产品名称')
    balance = Column(Integer, server_default=text("'0'"), comment='消费金额')
    shop_id = Column(Integer, comment='店铺id')
    pinpai_id = Column(Integer, comment='品牌id')
    manager_id = Column(Integer, comment='操作员id')
    user_id = Column(Integer, comment='消费会员id')
    shareuser_id = Column(Integer, comment='分成会员id')
    shareuser_balance = Column(Integer, comment='分成会员获得金额')
    pro_id = Column(Integer, server_default=text("'0'"), comment='消费产品ID')
    user_phone = Column(String(120), comment='消费者电话')
    user_name = Column(String(120), comment='消费者姓名')
    lbalance = Column(Integer, server_default=text("'0'"), comment='余额')
    lgivefee = Column(Integer, server_default=text("'0'"), comment='增额')
    lgivebalance = Column(Integer, server_default=text("'0'"), comment='已分配额')
    lgivetarget = Column(Integer, server_default=text("'0'"), comment='可分配额')
    cons_type = Column(TINYINT, server_default=text("'0'"), comment='消费类型,0储值消费,1第三方消费')


class TShCzyushe(Base):
    __tablename__ = 't_sh_czyushe'
    __table_args__ = {'comment': '充值预设表'}

    id = Column(Integer, primary_key=True)
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    yushe_name = Column(String(120), comment='产品名称')
    balance = Column(Integer, server_default=text("'0'"), comment='余额')
    givefee = Column(Integer, server_default=text("'0'"), comment='增额')
    givetarget = Column(Integer, server_default=text("'0'"), comment='可分配额')
    shop_id = Column(Integer, comment='店铺id')
    pinpai_id = Column(Integer, comment='品牌id')
    status = Column(TINYINT, server_default=text("'0'"), comment='产品状态,0正常,1禁用')


class TShProduct(Base):
    __tablename__ = 't_sh_product'
    __table_args__ = {'comment': '产品表'}

    id = Column(Integer, primary_key=True)
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    pro_name = Column(String(120), comment='产品名称')
    price = Column(Integer, server_default=text("'0'"), comment='产品价格（单位分）')
    shop_id = Column(Integer, comment='店铺id')
    pinpai_id = Column(Integer, comment='品牌id')
    status = Column(TINYINT, server_default=text("'0'"), comment='产品状态,0正常,1禁用')


class TShRose(Base):
    __tablename__ = 't_sh_rose'
    __table_args__ = {'comment': '商家角色'}

    id = Column(Integer, primary_key=True)
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    shop_id = Column(Integer, comment='店铺id')
    pinpai_id = Column(Integer, comment='品牌id')
    rose_name = Column(String(256), comment='角色名称')
    status = Column(TINYINT, server_default=text("'0'"), comment='商家状态,0正常,1禁用')


class TShShop(Base):
    __tablename__ = 't_sh_shop'
    __table_args__ = {'comment': '品牌与商家'}

    id = Column(Integer, primary_key=True)
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    shop_name = Column(String(256), comment='品牌/店铺名称')
    phone = Column(String(45), comment='电话')
    user_name = Column(String(45), comment='用户名')
    user_pass = Column(String(45), comment='密码')
    province = Column(VARCHAR(45), comment='省份')
    city = Column(String(45), comment='城市')
    area = Column(String(45), comment='区域')
    street = Column(String(45), comment='街道')
    address = Column(String(45), comment='详细地址')
    status = Column(TINYINT, server_default=text("'0'"), comment='商家状态,0正常,1注销')
    type = Column(TINYINT, comment='商家类型;   0: 品牌  1:商家')
    parent_id = Column(Integer, comment='上级品牌id')
    shop_id = Column(Integer, server_default=text("'0'"), comment='用户所属店铺id')
    rose_id = Column(Integer, server_default=text("'0'"), comment='角色id')
    latitude = Column(DECIMAL(18, 15), server_default=text("'0.000000000000000'"), comment='纬度地区')
    longitude = Column(DECIMAL(18, 15), server_default=text("'0.000000000000000'"), comment='经度地区')


class TShUser(Base):
    __tablename__ = 't_sh_user'
    __table_args__ = {'comment': '商家用户表'}

    id = Column(Integer, primary_key=True)
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    shop_id = Column(Integer, comment='店铺id')
    pinpai_id = Column(Integer, comment='品牌id')
    user_name = Column(String(120), comment='用户名称')
    user_nicheng = Column(String(120), comment='用户昵姓名')
    phone = Column(String(45), comment='电话')
    balance = Column(Integer, server_default=text("'0'"), comment='余额')
    givefee = Column(Integer, server_default=text("'0'"), comment='增额')
    givebalance = Column(Integer, server_default=text("'0'"), comment='已分配额')
    givetarget = Column(Integer, server_default=text("'0'"), comment='可分配额')
    recommenda = Column(Integer, server_default=text("'0'"), comment='平台推荐人')
    recommendb = Column(Integer, server_default=text("'0'"), comment='转发推荐人')
    user_level = Column(Integer, server_default=text("'0'"), comment='用户级别')
    status = Column(TINYINT, server_default=text("'0'"), comment='商家状态,0正常,1禁用')


class TShUserlevel(Base):
    __tablename__ = 't_sh_userlevel'
    __table_args__ = {'comment': '用户级别表'}

    id = Column(Integer, primary_key=True)
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    level_name = Column(String(120), comment='级别名称')
    propo = Column(Integer, server_default=text("'0'"), comment='消费分成比例（百分比）')
    shop_id = Column(Integer, comment='店铺id')
    pinpai_id = Column(Integer, comment='品牌id')
    status = Column(TINYINT, server_default=text("'0'"), comment='级别状态,0正常,1默认')


class TShoperorderfee(Base):
    __tablename__ = 't_shoperorderfee'
    __table_args__ = {'comment': '批发商商品排队分润表'}

    id = Column(Integer, primary_key=True, comment='标识id')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    good_id = Column(Integer, comment='商品d')
    order_id = Column(Integer, comment='订单id')
    user_id = Column(Integer, comment='排队批发商id')
    fee_num = Column(Integer, server_default=text("'0'"), comment='剩余分润次数')
    fee_time = Column(TIMESTAMP, comment='最近一次分润时间')
    gtype = Column(TINYINT, server_default=text("'0'"), comment='商品分类,0表示未定义,1联营会员2仓库主3巨省会员')
    fee_count = Column(Integer, server_default=text("'0'"), comment='总分润次数')


class TStore(Base):
    __tablename__ = 't_store'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), comment='店铺名称')
    phone = Column(String(45), comment='电话')
    province = Column(VARCHAR(45), comment='省份')
    city = Column(String(45), comment='城市')
    area = Column(String(45), comment='区域')
    street = Column(String(45), comment='街道')
    address = Column(String(45), comment='详细地址')
    status = Column(TINYINT, comment='店铺状态')
    owner = Column(VARCHAR(45), comment='店铺负责人')
    recommender_id = Column(Integer, comment='推荐人id   对应某个用户')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='注册时间')
    type = Column(TINYINT, server_default=text("'0'"), comment='店铺类型：0为企业，1为个体')
    expired_time = Column(TIMESTAMP, comment='合同到期时间')
    open_time = Column(Integer, comment='开始营业时间   9*3600表示9:00')
    close_time = Column(Integer, comment='结束营业时间   9*3600表示9:00，以秒为单位')
    image = Column(String(256), comment='商家门头图片')
    owner_id = Column(Integer, comment='负责人id')
    supplier_id = Column(Integer, comment='商家id')
    company_name = Column(String(128), comment='公司名称')
    reject_reason = Column(String(100), comment='驳回原因')
    reject_time = Column(TIMESTAMP, comment='驳回时间')
    reject_admin_id = Column(Integer, comment='管理员id   记录是谁驳回的')
    is_default = Column(TINYINT(1), comment='默认店铺')
    commit_way = Column(TINYINT, server_default=text("'0'"), comment='提交方式:0,营业执照; 1身份证')
    social_credit_code = Column(String(128), comment='统一社会信用代码')
    transactor_id = Column(Integer, server_default=text("'0'"), comment='办理人ID')
    recommend_id = Column(Integer, server_default=text("'0'"), comment='推荐人ID')
    parent_id = Column(Integer, server_default=text("'0'"), comment='上一级店铺ID')
    latitude = Column(DECIMAL(18, 15), server_default=text("'0.000000000000000'"), comment='纬度地区')
    longitude = Column(DECIMAL(18, 15), server_default=text("'0.000000000000000'"), comment='经度地区')
    profession_id = Column(Integer, server_default=text("'0'"), comment='店铺行业ID')
    business_area_id = Column(Integer, server_default=text("'0'"), comment='商圈ID')
    refine_steps = Column(Integer, server_default=text("'0'"), comment='完善步骤：1、2、3、4......')
    consume_aver = Column(Integer, server_default=text("'0'"), comment='人均消费')
    usable_room = Column(Integer, server_default=text("'0'"), comment='包间是否可用，默认0,可用为1')


class TStoreAmount(Base):
    __tablename__ = 't_store_amount'
    __table_args__ = {'comment': '商家金额表'}

    id = Column(Integer, primary_key=True)
    type = Column(TINYINT, comment='变动类型')
    change = Column(Integer, comment='资金变动额      +10    -5')
    amount = Column(Integer, comment='资金总额')
    create_time = Column(TIMESTAMP, comment='创建时间')
    store_id = Column(Integer, comment='店铺id')


class TStoreBusinessArea(Base):
    __tablename__ = 't_store_business_area'
    __table_args__ = {'comment': '店铺地区商圈表'}

    id = Column(Integer, primary_key=True, unique=True)
    city_id = Column(Integer, server_default=text("'0'"), comment='地区ID，t_city表Id')
    area_name = Column(String(45), comment='商圈名称')
    latitude = Column(DECIMAL(18, 15), server_default=text("'0.000000000000000'"), comment='纬度地区')
    longitude = Column(DECIMAL(18, 15), server_default=text("'0.000000000000000'"), comment='经度地区')
    area_radius = Column(Integer, server_default=text("'0'"), comment='半径，CM')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    operator_id = Column(Integer, comment='操作员ID')


class TStoreChangeType(Base):
    __tablename__ = 't_store_change_type'
    __table_args__ = {'comment': '商家资金变动类型'}

    id = Column(Integer, primary_key=True)
    type = Column(VARCHAR(100), comment='资金变动类型')


class TStoreContract(Base):
    __tablename__ = 't_store_contract'
    __table_args__ = {'comment': '商家合同表'}

    contract = Column(String(256), comment='合同照片')
    id = Column(Integer, primary_key=True)
    store_id = Column(Integer, comment='商家编号')
    create_time = Column(TIMESTAMP, comment='创建时间')
    expired_time = Column(TIMESTAMP, comment='到期时间')


class TStoreIncome(Base):
    __tablename__ = 't_store_income'
    __table_args__ = {'comment': '商家收入表'}

    id = Column(Integer, primary_key=True)
    income_add = Column(Integer, comment='收入增加额')
    income_total = Column(Integer, comment='商家总收入')
    create_time = Column(TIMESTAMP, comment='创建时间')
    store_id = Column(Integer, comment='商家id')


class TStoreLicense(Base):
    __tablename__ = 't_store_license'
    __table_args__ = {'comment': '商家证件表    营业执照等'}

    id = Column(Integer, primary_key=True)
    license = Column(VARCHAR(256), comment='营业执照文本')
    store_id = Column(Integer, comment='商家id')
    create_time = Column(TIMESTAMP, comment='更新时间')
    license_type = Column(String(45), comment='商家证件类型：营业执照,税务登记证,组织机构代码证,质量认证,卫生认证')
    status = Column(Integer, server_default=text("'0'"), comment='默认0，-1为删除')


class TStoreMembership(Base):
    __tablename__ = 't_store_membership'
    __table_args__ = {'comment': '用户在店铺消费过  即成为此店的会员'}

    id = Column(Integer, primary_key=True)
    store_id = Column(Integer, comment='商家id')
    user_id = Column(Integer, comment='用户id')
    status = Column(String(45))
    create_time = Column(TIMESTAMP)
    expired_time = Column(TIMESTAMP, comment='过期时间')


class TStoreOwner(Base):
    __tablename__ = 't_store_owner'
    __table_args__ = {'comment': '商家负责人表'}

    id = Column(Integer, primary_key=True)
    name = Column(String(100), comment='负责人姓名')
    phone = Column(String(100), comment='电话')
    password = Column(VARCHAR(100), comment='密码（哈希值）')
    id_card = Column(String(100), comment='身份证号')
    front_image = Column(String(256), comment='身份证正面照')
    back_image = Column(String(256), comment='身份证背面照')
    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    user_role = Column(TINYINT(1), server_default=text("'0'"), comment='商铺管理角色：0负责人，1财务，2收银员，3辅员，4其他')
    parent_id = Column(Integer, server_default=text("'0'"), comment='隶属关系：0顶级，大于0为上一级id')
    open_id = Column(String(45), comment='微信openID')
    union_id = Column(String(45), comment='微信unionID')
    status = Column(TINYINT(1), server_default=text("'0'"), comment='商铺账户状态：0正常，-1删除')
    remark = Column(String(400), comment='账户备注')
    login_code = Column(String(260), comment='用户登录code')
    login_time = Column(TIMESTAMP, comment='会员登录时间')
    store_id = Column(Integer, server_default=text("'0'"), comment='店铺ID')


class TStoreProfession(Base):
    __tablename__ = 't_store_profession'
    __table_args__ = {'comment': '店铺行业表'}

    id = Column(Integer, primary_key=True, unique=True)
    pname = Column(String(45), comment='行业名称')
    coupon_add_path = Column(String(256), comment='创建此行业卡券时的跳转路径')
    coupon_fix_path = Column(String(256), comment='修改此行业卡券时的跳转路径')
    parent_id = Column(Integer, server_default=text("'0'"), comment='上级ID，默认是0表示顶级')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='店铺创建时间')
    operator_id = Column(Integer, comment='操作员ID')
    pro_other = Column(String(256), comment='行业相关备注')


class TStoreState(Base):
    __tablename__ = 't_store_state'

    id = Column(Integer, primary_key=True)
    status = Column(String(25), comment='商家类型')


class TStoreTag(Base):
    __tablename__ = 't_store_tag'
    __table_args__ = {'comment': '店铺标签的关系表'}

    id = Column(Integer, primary_key=True, unique=True)
    store_id = Column(Integer, server_default=text("'0'"), comment='商家ID')
    tag_id = Column(Integer, server_default=text("'0'"), comment='标签ID')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='标签关系创建时间')
    operator_id = Column(Integer, comment='操作员ID')


class TStoreTransactor(Base):
    __tablename__ = 't_store_transactor'
    __table_args__ = {'comment': '商家办理人表'}

    id = Column(Integer, primary_key=True, unique=True)
    type = Column(TINYINT, comment='办理人类型：0法人办理、1代理人办理')
    tname = Column(String(45), comment='办理人姓名')
    certificate_type = Column(TINYINT, comment='证件类型：0法人证件、1个人身份证证件')
    certificate_num = Column(String(128), comment='证件号码')
    license1 = Column(VARCHAR(256), comment='证件照地址1')
    license2 = Column(VARCHAR(256), comment='证件照地址2')
    license3 = Column(VARCHAR(256), comment='证件照地址3')
    license4 = Column(VARCHAR(256), comment='证件照地址4')
    certificate_phone = Column(String(45), comment='电话')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='注册时间')
    operator_id = Column(Integer, comment='操作员ID')
    store_id = Column(Integer, server_default=text("'0'"), comment='店铺ID')


class TSupplier(Base):
    __tablename__ = 't_supplier'
    __table_args__ = {'comment': '商家和供应商'}

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(128), comment='商家名称')
    phone = Column(String(45), comment='电话')
    province = Column(VARCHAR(45), comment='省份')
    city = Column(String(45), comment='城市')
    area = Column(String(45), comment='区域')
    street = Column(String(45), comment='街道')
    address = Column(String(45), comment='详细地址')
    status = Column(TINYINT, comment='商家状态')
    owner = Column(VARCHAR(45), comment='商家负责人')
    recommender_id = Column(Integer, comment='推荐人id   对应某个用户')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='注册时间')
    type = Column(TINYINT, comment='商家类型;   0: 商家  1:供应商')
    expired_time = Column(TIMESTAMP, comment='合同到期时间')
    open_time = Column(Integer, comment='开始营业时间   9*3600表示9:00')
    close_time = Column(Integer, comment='结束营业时间   9*3600表示9:00，以秒为单位')
    image = Column(String(256), comment='商家门头图片')
    owner_id = Column(Integer, comment='负责人id')
    category = Column(TINYINT, server_default=text("'1'"), comment='供应商类型  2：供应商   1：商家')
    balance = Column(Integer, comment='余额；以分为单位')
    reject_reason = Column(String(256), comment='驳回原因')
    reject_admin_id = Column(Integer, comment='管理员id   记录是谁审批的')
    reject_time = Column(TIMESTAMP, comment='驳回时间')
    company_name = Column(String(128), comment='公司名称')
    license1 = Column(VARCHAR(256), comment='营业执照证件地址')
    license2 = Column(VARCHAR(256), comment='证件地址2')
    license3 = Column(VARCHAR(256), comment='证件地址3')
    license4 = Column(VARCHAR(256), comment='备注文本')


class TSupplierAmount(Base):
    __tablename__ = 't_supplier_amount'
    __table_args__ = {'comment': '商家金额表'}

    id = Column(Integer, primary_key=True)
    type = Column(TINYINT, comment='变动类型')
    change = Column(Integer, comment='资金变动额      +10    -5')
    amount = Column(Integer, comment='资金总额')
    create_time = Column(TIMESTAMP, comment='创建时间')
    supplier_id = Column(Integer, comment='商家id')
    order_id = Column(Integer, comment='订单id')
    description = Column(String(100), comment='描述')


class TSupplierChangeType(Base):
    __tablename__ = 't_supplier_change_type'
    __table_args__ = {'comment': '商家资金变动类型'}

    id = Column(Integer, primary_key=True)
    type = Column(VARCHAR(100), comment='资金变动类型')


class TSupplierIncome(Base):
    __tablename__ = 't_supplier_income'
    __table_args__ = {'comment': '供应商的余额历史记录，不可修改，只能增加'}

    id = Column(Integer, primary_key=True)
    supplier_id = Column(Integer, nullable=False, comment='外键,供应商id')
    change = Column(Integer, nullable=False, server_default=text("'0'"), comment='变动金额')
    balance = Column(Integer, nullable=False, comment='余额')
    type = Column(VARCHAR(20), comment='类型')
    description = Column(VARCHAR(100), comment='详细描述')
    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    user_withdraw_id = Column(Integer)
    operator_id = Column(Integer, comment='操作员ID')
    out_trade_no = Column(String(64))


class TSupplierLicense(Base):
    __tablename__ = 't_supplier_license'
    __table_args__ = {'comment': '商家证件表    营业执照等'}

    id = Column(Integer, primary_key=True)
    license = Column(VARCHAR(256), comment='营业执照文本')
    supplier_id = Column(Integer, comment='商家id')
    create_time = Column(TIMESTAMP, comment='更新时间')


class TSupplierMembership(Base):
    __tablename__ = 't_supplier_membership'
    __table_args__ = {'comment': '用户在店铺消费过  即成为此店的会员'}

    id = Column(Integer, primary_key=True)
    supplier_id = Column(Integer, comment='商家id')
    user_id = Column(Integer, comment='用户id')
    status = Column(String(45))
    create_time = Column(TIMESTAMP)
    expired_time = Column(TIMESTAMP, comment='过期时间')


class TSupplierOwner(Base):
    __tablename__ = 't_supplier_owner'
    __table_args__ = {'comment': '商家人员角色表'}

    id = Column(Integer, primary_key=True)
    name = Column(String(100), comment='负责人姓名')
    phone = Column(String(100), comment='电话')
    password = Column(VARCHAR(100), comment='密码（哈希值）')
    id_card = Column(String(100), comment='身份证号')
    front_image = Column(String(256), comment='身份证正面照')
    back_image = Column(String(256), comment='身份证背面照')
    open_id = Column(String(45))
    union_id = Column(String(45))
    level_id = Column(TINYINT(1), comment='角色id    0：负责人     1：财务人员      2：核销人员')


class TSupplierState(Base):
    __tablename__ = 't_supplier_state'

    id = Column(Integer, primary_key=True)
    status = Column(String(25), comment='商家类型')


class TSupplierType(Base):
    __tablename__ = 't_supplier_type'
    __table_args__ = {'comment': '供应商类型表'}

    id = Column(Integer, primary_key=True)
    type_ = Column(String(100), comment='类型')


class TTask(Base):
    __tablename__ = 't_task'
    __table_args__ = {'comment': '任务表'}

    id = Column(Integer, primary_key=True, comment='标识id')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    title = Column(String(255), comment='任务标题')
    describe = Column(Text, comment='任务描述')
    top = Column(Integer, comment='任务上限')
    big = Column(Integer, comment='单号最大领取量')
    received = Column(Integer, comment='已领取量')
    stat = Column(TINYINT, server_default=text("'0'"), comment='0未开启,1进行中,2打开中,3已结束')
    style = Column(Text, comment='图样地址七牛oss,逗号分割多个图样地址')
    verfy = Column(Text, comment='任务完成后打卡证明格式,逗号分割打卡平台名称')
    run_time = Column(TIMESTAMP, comment='进行中时间')
    clock_time = Column(TIMESTAMP, comment='打卡时间')
    expired_time = Column(TIMESTAMP, comment='结束时间')
    down = Column(Integer, comment='素材下载次数')
    upload = Column(Integer, comment='素材上传数量')
    ctype = Column(TINYINT, server_default=text("'0'"), comment='任务分类,0表示视频类,1表示图文类')
    islink = Column(TINYINT, server_default=text("'0'"), comment='是否开启链接上传,0否,1是')
    start_time = Column(TIMESTAMP, comment='开始时间')
    verfy_num = Column(Integer, server_default=text("'0'"), comment='打卡项数目')
    is_auto = Column(TINYINT, server_default=text("'0'"), comment='是否自动处理状态,0自动,1手动')
    cover = Column(String(500), comment='封面图')


class TTaskclockup(Base):
    __tablename__ = 't_taskclockup'
    __table_args__ = {'comment': '用户打卡表'}

    id = Column(Integer, primary_key=True, comment='标识id')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    task_id = Column(Integer, comment='参与任务id')
    tuser_id = Column(Integer, comment='素材id')
    topic_id = Column(Integer, comment='话题id')
    user_id = Column(Integer, server_default=text("'0'"), comment='参与会员id')
    manage_id = Column(Integer, server_default=text("'0'"), comment='审核人id')
    ctype = Column(TINYINT, server_default=text("'0'"), comment='任务分类,0表示视频截图类,1表示图文类')
    content = Column(Text, comment='截图地址或图文内容')
    verfy_name = Column(VARCHAR(60), comment='平台名称')
    status = Column(TINYINT, server_default=text("'0'"), comment='状态,0未审核,1合格,2不合格')
    stat_time = Column(TIMESTAMP, comment='审核时间')
    stat_count = Column(Integer, server_default=text("'0'"), comment='统计浏览次数')
    user_acc = Column(VARCHAR(90), comment='打卡平台账号')


class TTasktopic(Base):
    __tablename__ = 't_tasktopic'
    __table_args__ = {'comment': '任务话题表'}

    id = Column(Integer, primary_key=True, comment='标识id')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    task_id = Column(Integer, comment='参与任务id')
    topic_name = Column(Text, comment='任务话题内容')
    topic_comment = Column(Text, comment='任务评论内容')
    status = Column(TINYINT, server_default=text("'0'"), comment='状态,0正常')
    ts_num = Column(Integer, server_default=text("'0'"), comment='素材数量')


class TTaskuser(Base):
    __tablename__ = 't_taskuser'
    __table_args__ = {'comment': '素材与用户领取任务表'}

    id = Column(Integer, primary_key=True, comment='标识id')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='素材上传时间')
    user_time = Column(TIMESTAMP, comment='会员领取时间')
    task_url = Column(String(500), comment='七牛oss素材地址')
    task_id = Column(Integer, comment='参与任务id')
    user_id = Column(Integer, server_default=text("'0'"), comment='参与会员id,0表示未领取')
    phone = Column(VARCHAR(45), comment='联系方式')
    address = Column(VARCHAR(255), comment='地址')
    upload = Column(Integer, server_default=text("'0'"), comment='打卡上传数量')
    down = Column(Integer, server_default=text("'0'"), comment='素材下载次数')
    verfy_upload = Column(Text, comment='打卡证明格式{key:url}|{}')
    topic_id = Column(Integer, comment='所属话题id')
    link_stat = Column(TINYINT, server_default=text("'0'"), comment='链接审核状态,0未操作,1链接未审核,2链接已审核')
    pic_stat = Column(TINYINT, server_default=text("'0'"), comment='截图审核状态,0未打卡,1未审核,2已审核,')
    nopass = Column(String(500), comment='不合格原因选项')
    nopass_txt = Column(Text, comment='不合格原因文本')
    filename = Column(String(300), comment='生成token的文件名称')
    status = Column(TINYINT, server_default=text("'0'"), comment='状态,0正常,-1删除')
    recovery = Column(Integer, server_default=text("'0'"), comment='回收次数')


class TTranAccount(Base):
    __tablename__ = 't_tran_account'
    __table_args__ = {'comment': '余额转账记录'}

    id = Column(Integer, primary_key=True, comment='标识id编号')
    user_out = Column(Integer, server_default=text("'0'"), comment='转让人id')
    user_out_phone = Column(CHAR(20), comment='转让人电话')
    user_out_name = Column(CHAR(20), comment='转让人姓名')
    user_out_balance = Column(Integer, server_default=text("'0'"), comment='转让人余额')
    user_get = Column(Integer, server_default=text("'0'"), comment='收钱人id')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    user_get_phone = Column(CHAR(20), comment='收钱人电话')
    user_get_name = Column(CHAR(20), comment='收钱人姓名')
    user_get_balance = Column(Integer, server_default=text("'0'"), comment='收钱人余额')
    balance = Column(Integer, server_default=text("'0'"), comment='金额')


class TTsrecoverylog(Base):
    __tablename__ = 't_tsrecoverylog'
    __table_args__ = {'comment': '素材超时回收记录表'}

    id = Column(Integer, primary_key=True)
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='回收时间')
    user_id = Column(Integer, server_default=text("'0'"), comment='会员账号id')
    ts_id = Column(Integer, server_default=text("'0'"), comment='回收素材id')
    task_id = Column(Integer, server_default=text("'0'"), comment='回收素材任务id')
    phone = Column(VARCHAR(45), comment='会员联系方式')
    address = Column(VARCHAR(255), comment='地址')
    logtype = Column(String(120), server_default=text("'自动回收'"), comment='自动回收、手动回收')


class TUser(Base):
    __tablename__ = 't_user'
    __table_args__ = {'comment': 'user'}

    id = Column(Integer, primary_key=True, unique=True, comment='标识id')
    username = Column(VARCHAR(45), comment='用户名')
    email = Column(VARCHAR(45), comment='邮箱')
    open_id = Column(String(45), comment='openID from wechat channel')
    union_id = Column(String(45), comment='unionID from tecent')
    password = Column(VARCHAR(45), comment='密码（哈希值）')
    nickname = Column(VARCHAR(45), comment='昵称')
    phone = Column(VARCHAR(45), comment='联系方式')
    id_card = Column(VARCHAR(45), comment='身份证')
    level_id = Column(Integer, server_default=text("'0'"), comment='用户等级 默认是0粉丝,1会员,2核心会员')
    status = Column(TINYINT, comment='0: 已实名   1: 未实名,被is_agree替代')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='注册时间')
    avatar = Column(VARCHAR(512), comment='头像url')
    invited_user_id = Column(Integer, comment='邀请人id')
    coin = Column(Integer, comment='积分')
    gender = Column(TINYINT, comment='0:  男  1:  女')
    last_active_time = Column(TIMESTAMP, comment='最近登录时间')
    name = Column(VARCHAR(45), comment='用户名')
    is_agree = Column(TINYINT(1), server_default=text("'0'"), comment='是否已经校验')
    parent_id = Column(Integer, comment='父级用户')
    parent_id_history = Column(VARCHAR(45), comment='曾经的上级(ID之间逗号分隔)')
    level_one_time = Column(TIMESTAMP, comment='升级he合伙人会员时间')
    level_two_time = Column(TIMESTAMP, comment='升级老板会员时间')
    level_three_time = Column(TIMESTAMP, comment='升级大老板会员时间')
    level_top_time = Column(TIMESTAMP, comment='升级推广顶级时间')
    wholesale_id = Column(Integer, server_default=text("'0'"), comment='身份0普通1小团长2大团长')
    wholesale_amount = Column(Integer, server_default=text("'0'"), comment='批发商品累计消费额')
    paidui = Column(Integer, server_default=text("'0'"), comment='排队分次数')
    tuan_id = Column(Integer, server_default=text("'0'"), comment='所属团id,0表示未入团人员,>0表示所属团长id')
    tran_pass = Column(CHAR(100), comment='转账密码')
    invited_code = Column(String(126), comment='邀请码')
    bigorder_id = Column(Integer, server_default=text("'0'"), comment='公排id')
    layer_id = Column(Integer, server_default=text("'0'"), comment='行号(所在层数)')
    cur_layer_id = Column(Integer, server_default=text("'0'"), comment='当前行号从左到右排序号')
    cur_layer_total = Column(Integer, server_default=text("'0'"), comment='当前行排序总数量')
    bigorder_parent_id = Column(Integer, server_default=text("'0'"), comment='上级对应序号')
    entrust_status = Column(TINYINT, server_default=text("'0'"), comment='委托状态0未接受1临时托管中2永久托管')
    light_status = Column(TINYINT, comment='熄灯状态0正常1熄灯')
    voucher_total = Column(Integer, server_default=text("'0'"), comment='商品购买券数量')
    endorders_total = Column(Integer, server_default=text("'0'"), comment='完成订单数量')
    doubule_id = Column(Integer, server_default=text("'0'"), comment='是否分身大于0为分身id')
    entrust_startime = Column(TIMESTAMP, comment='开启托管时间')
    entrust_endtime = Column(TIMESTAMP, comment='结束托管时间')
    pai_buydui = Column(Integer, server_default=text("'0'"), comment='排队复购次数')
    bagorder_num = Column(Integer, server_default=text("'0'"), comment='礼包购买数')
    weight_num = Column(Integer, server_default=text("'0'"), comment='权重指数')
    fund_weight_num = Column(Integer, server_default=text("'1'"), comment='分红权重指数')
    video_level = Column(TINYINT, server_default=text("'0'"), comment='视频任务分发级别,1达人,2店长3,服务商,4分公司 ')
    is_tuan = Column(Integer, server_default=text("'0'"), comment='视频团长和身份id')
    ercode = Column(VARCHAR(512), comment='个人二维码')
    sh_agent = Column(TINYINT, server_default=text("'0'"), comment='市代身份 ')
    sh_agent_id = Column(Integer, server_default=text("'0'"), comment='市代id')


class TUser250810(Base):
    __tablename__ = 't_user_250810'
    __table_args__ = {'comment': 'user'}

    id = Column(Integer, primary_key=True, unique=True, comment='标识id')
    username = Column(VARCHAR(45), comment='用户名')
    email = Column(VARCHAR(45), comment='邮箱')
    open_id = Column(String(45), comment='openID from wechat channel')
    union_id = Column(String(45), comment='unionID from tecent')
    password = Column(VARCHAR(45), comment='密码（哈希值）')
    nickname = Column(VARCHAR(45), comment='昵称')
    phone = Column(VARCHAR(45), comment='联系方式')
    id_card = Column(VARCHAR(45), comment='身份证')
    level_id = Column(Integer, server_default=text("'0'"), comment='用户等级 默认是0粉丝,1会员,2核心会员')
    status = Column(TINYINT, comment='0: 已实名   1: 未实名,被is_agree替代')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='注册时间')
    avatar = Column(VARCHAR(512), comment='头像url')
    invited_user_id = Column(Integer, comment='邀请人id')
    coin = Column(Integer, comment='积分')
    gender = Column(TINYINT, comment='0:  男  1:  女')
    last_active_time = Column(TIMESTAMP, comment='最近登录时间')
    name = Column(VARCHAR(45), comment='用户名')
    is_agree = Column(TINYINT(1), server_default=text("'0'"), comment='是否已经校验')
    parent_id = Column(Integer, comment='父级用户')
    parent_id_history = Column(VARCHAR(45), comment='曾经的上级(ID之间逗号分隔)')
    level_one_time = Column(TIMESTAMP, comment='升级he合伙人会员时间')
    level_two_time = Column(TIMESTAMP, comment='升级老板会员时间')
    level_three_time = Column(TIMESTAMP, comment='升级大老板会员时间')
    level_top_time = Column(TIMESTAMP, comment='升级推广顶级时间')
    wholesale_id = Column(Integer, server_default=text("'0'"), comment='身份0普通1小团长2大团长')
    wholesale_amount = Column(Integer, server_default=text("'0'"), comment='批发商品累计消费额')
    paidui = Column(Integer, server_default=text("'0'"), comment='排队分次数')
    tuan_id = Column(Integer, server_default=text("'0'"), comment='所属团id,0表示未入团人员,>0表示所属团长id')
    tran_pass = Column(CHAR(100), comment='转账密码')
    invited_code = Column(String(126), comment='邀请码')
    bigorder_id = Column(Integer, server_default=text("'0'"), comment='公排id')
    layer_id = Column(Integer, server_default=text("'0'"), comment='行号(所在层数)')
    cur_layer_id = Column(Integer, server_default=text("'0'"), comment='当前行号从左到右排序号')
    cur_layer_total = Column(Integer, server_default=text("'0'"), comment='当前行排序总数量')
    bigorder_parent_id = Column(Integer, server_default=text("'0'"), comment='上级对应序号')
    entrust_status = Column(TINYINT, server_default=text("'0'"), comment='委托状态0未接受1临时托管中2永久托管')
    light_status = Column(TINYINT, comment='熄灯状态0正常1熄灯')
    voucher_total = Column(Integer, server_default=text("'0'"), comment='商品购买券数量')
    endorders_total = Column(Integer, server_default=text("'0'"), comment='完成订单数量')
    doubule_id = Column(Integer, server_default=text("'0'"), comment='是否分身大于0为分身id')
    entrust_startime = Column(TIMESTAMP, comment='开启托管时间')
    entrust_endtime = Column(TIMESTAMP, comment='结束托管时间')
    pai_buydui = Column(Integer, server_default=text("'0'"), comment='排队复购次数')
    bagorder_num = Column(Integer, server_default=text("'0'"), comment='礼包购买数')


class TUserAccount(Base):
    __tablename__ = 't_user_account'
    __table_args__ = {'comment': '用户的账户信息，包括余额，锁定额，积分，以及冻结额'}

    id = Column(Integer, primary_key=True, comment='账户id')
    user_id = Column(Integer, nullable=False, comment='用户id')
    balance = Column(Integer, nullable=False, server_default=text("'0'"), comment='余额')
    lock_balance = Column(Integer, nullable=False, server_default=text("'0'"), comment='推荐金额')
    coin = Column(Integer, nullable=False, server_default=text("'0'"), comment='优惠券额度')
    description = Column(String(100), comment='详细描述')
    create_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='记录生成时间')
    freeze_balance = Column(Integer, server_default=text("'0'"), comment='冻结额 单位：分')
    update_time = Column(TIMESTAMP)
    forecast_one = Column(Integer, server_default=text("'0'"), comment='初级资金池分润预测值')
    forecast_two = Column(Integer, server_default=text("'0'"), comment='高级资金池分润预测值')
    forecast_three = Column(Integer, server_default=text("'0'"), comment='顶级资金池分润预测值')
    prop_one = Column(Float(5), server_default=text("'0.0000'"), comment='初级资金池分润预测比值')
    prop_two = Column(Float(5), server_default=text("'0.0000'"), comment='高级资金池分润预测比值')
    prop_three = Column(Float(5), server_default=text("'0.0000'"), comment='顶级资金池分润预测比值')
    nvideo = Column(Integer, server_default=text("'0'"), comment='用户剩余视频条数')


class TUserAd(Base):
    __tablename__ = 't_user_ad'
    __table_args__ = {'comment': '用户名片广告表'}

    id = Column(Integer, primary_key=True)
    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    user_id = Column(Integer, nullable=False, server_default=text("'0'"), comment='用户id')
    user_name = Column(String(100), comment='用户昵称')
    user_phone = Column(String(100), comment='用户电话')
    qr_code_user = Column(String(500), comment='用户微信')
    qr_code_enterprise = Column(String(500), comment='企业微信')
    adbrand_id = Column(Integer, nullable=False, server_default=text("'0'"), comment='广告品牌id')
    is_del = Column(TINYINT, server_default=text("'0'"), comment='是否删除,0正常,1删除')
    del_brand = Column(Integer, server_default=text("'0'"), comment='项目是否删除,1删除')


class TUserAdUinfo(Base):
    __tablename__ = 't_user_ad_uinfo'
    __table_args__ = {'comment': '名片广告用户信息表'}

    id = Column(Integer, primary_key=True)
    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    user_id = Column(Integer, nullable=False, server_default=text("'0'"), comment='用户id')
    user_name = Column(String(100), comment='用户昵称')
    user_phone = Column(String(100), comment='用户电话')
    qr_code_user = Column(String(500), comment='用户微信')
    qr_code_enterprise = Column(String(500), comment='企业微信')
    is_del = Column(TINYINT, server_default=text("'0'"), comment='是否删除,0正常,1删除')


class TUserAdbrand(Base):
    __tablename__ = 't_user_adbrand'
    __table_args__ = {'comment': '广告品牌活动表'}

    id = Column(Integer, primary_key=True)
    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    title = Column(String(255), comment='广告品牌标题')
    ad_id = Column(Integer, nullable=False, server_default=text("'0'"), comment='Banner图片id')
    describe = Column(Text, comment='详情描述 (富文本)')
    qr_code = Column(String(500), comment='企业微信二维码')
    qual_pic = Column(Text, comment='营业执照、许可证等资质图片（最多4张)')
    video = Column(Text, comment='品牌宣传视频，支持mp4格式 ')
    good_id = Column(Text, comment='绑定商品ID')
    poster_share = Column(Text, comment='品牌宣传视频，支持mp4格式 ')
    is_del = Column(TINYINT, server_default=text("'0'"), comment='是否删除,0正常,1删除')
    share_title = Column(String(255), comment='分享标题')
    share_pic = Column(String(500), comment='分享海报图')
    is_default = Column(Integer, server_default=text("'0'"), comment='项目是否默认,1默认')
    information = Column(Text, comment='资料介绍')
    customer_case = Column(Text, comment='客户案例')
    is_show_good = Column(TINYINT, server_default=text("'0'"), comment='是否展示商品介绍，默认0显示，1为隐藏')


class TUserAdbrandFile(Base):
    __tablename__ = 't_user_adbrand_file'
    __table_args__ = {'comment': '广告模板文件列表'}

    id = Column(Integer, primary_key=True)
    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    adbrand_id = Column(Integer, nullable=False, server_default=text("'0'"), comment='广告模板id')
    file_name = Column(String(100), comment='文件名称')
    file_size = Column(Integer, nullable=False, server_default=text("'0'"), comment='文件大小KB')
    file_url = Column(String(500), comment='文件地址')
    file_type = Column(String(100), comment='文件类型pdf,doc,xls')
    is_del = Column(TINYINT, server_default=text("'0'"), comment='是否删除,0正常,1删除')
    menu_id = Column(Integer, nullable=False, server_default=text("'0'"), comment='项目菜单id')


class TUserAdbrandMenu(Base):
    __tablename__ = 't_user_adbrand_menu'
    __table_args__ = {'comment': '项目菜单表'}

    id = Column(Integer, primary_key=True)
    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    adbrand_id = Column(Integer, nullable=False, server_default=text("'0'"), comment='广告模板id')
    m_name = Column(String(100), comment='导航名称')
    pic_url = Column(String(500), comment='模块主图')
    m_title = Column(String(100), comment='模块标题')
    m_type = Column(TINYINT, server_default=text("'0'"), comment='类型0表示内容型,1表示文件列表型')
    text_one = Column(Text, comment='图文简介')
    text_two = Column(Text, comment='富文本内容')
    is_del = Column(TINYINT, server_default=text("'0'"), comment='是否删除,0正常,1删除')
    is_hide = Column(TINYINT, server_default=text("'0'"), comment='是否隐藏,0正常,1隐藏')


class TUserBank(Base):
    __tablename__ = 't_user_bank'
    __table_args__ = {'comment': '用户银行卡信息'}

    id = Column(Integer, primary_key=True)
    bank_name = Column(VARCHAR(128), comment='开户行')
    username = Column(VARCHAR(100), comment='户主姓名')
    id_card = Column(VARCHAR(45), comment='银行卡号')
    user_id = Column(Integer, comment='用户id')
    phone = Column(String(25), comment='户主电话')
    bank_address = Column(String(100), comment='开户行地址')
    is_default = Column(TINYINT(1))


class TUserFav(Base):
    __tablename__ = 't_user_favs'
    __table_args__ = {'comment': '用户收藏的产品'}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    good_id = Column(Integer, nullable=False)
    create_time = Column(TIMESTAMP)
    spec_id = Column(Integer, comment='规格id')


class TUserLevel(Base):
    __tablename__ = 't_user_level'
    __table_args__ = {'comment': '用户会员等级'}

    id = Column(Integer, primary_key=True, unique=True)
    title = Column(String(45))


class TUserPaymentHistory(Base):
    __tablename__ = 't_user_payment_history'
    __table_args__ = {'comment': '用户所有的支付记录'}

    id = Column(Integer, primary_key=True)
    fee = Column(Integer)
    create_time = Column(TIMESTAMP)
    description = Column(String(256))


class TUserPhoneCode(Base):
    __tablename__ = 't_user_phone_code'
    __table_args__ = {'comment': '用户电话校验表'}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    code = Column(String(15), comment='6位验证码')
    expired_time = Column(Integer, comment='按秒计算')
    send_time = Column(TIMESTAMP, comment='短信发送时间')
    employee_id = Column(Integer)
    store_owner_id = Column(Integer, comment='店主管id')
    worker_id = Column(Integer, comment='普通员工id')
    phone = Column(String(45), comment='电话号码')


class TUserWithdraw(Base):
    __tablename__ = 't_user_withdraw'

    id = Column(Integer, primary_key=True)
    amount = Column(Integer, comment='提现金额，单位分')
    user_withdraw_status_id = Column(Integer, server_default=text("'0'"), comment='状态0待审批1已经提现2已经驳回')
    create_time = Column(TIMESTAMP, comment='申请时间')
    update_time = Column(TIMESTAMP, comment='更新时间')
    user_id = Column(Integer)
    type_id = Column(TINYINT, comment='提现类型')
    user_bank_id = Column(String(256), comment='当类型为银行卡时，该字段指向银行卡号，或支付宝账号')
    operator_id = Column(Integer)
    fee_type = Column(TINYINT(1), server_default=text("'0'"), comment='扣费类型')
    fee_pro = Column(Float(5), server_default=text("'0.0000'"), comment='扣费比例')
    out_batch_no = Column(VARCHAR(50), comment=' 商户系统内部的商家批次单号，要求此参数只能由数字、大小写字母组成，在商户系统内部唯一')
    batch_name = Column(VARCHAR(50), comment='该笔批量转账的名称')
    batch_remark = Column(VARCHAR(50), comment='转账说明，UTF8编码，最多允许32个字符')
    out_detail_no = Column(VARCHAR(50), comment=' 商户系统内部区分转账批次单下不同转账明细单的唯一标识，要求此参数只能由数字、大小写字母组成')
    user_name = Column(VARCHAR(50), comment=' 姓名')
    user_phone = Column(VARCHAR(50), comment=' 电话')
    fee_balance = Column(Integer, server_default=text("'0'"), comment='实际提现金额')
    deduct_balance = Column(Integer, server_default=text("'0'"), comment='扣除或返锁定额金额')
    money_pic = Column(String(256), comment='截图回传')
    user_bank_other = Column(String(256), comment='关于账号其他备注信息')
    surp_balance = Column(Integer, comment='剩余余额')
    surp_local_balance = Column(Integer, comment='剩余推荐余额')


class TUserWithdrawStatus(Base):
    __tablename__ = 't_user_withdraw_status'

    id = Column(Integer, primary_key=True)
    title = Column(String(45))


class TUserWithdrawType(Base):
    __tablename__ = 't_user_withdraw_type'
    __table_args__ = {'comment': '用户提现类型表'}

    id = Column(Integer, primary_key=True)
    title = Column(String(25), comment='标注')


class TVideoArticle(Base):
    __tablename__ = 't_video_article'
    __table_args__ = {'comment': '视频文章表'}

    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, nullable=False, server_default=text("'0'"), comment='文章分类id')
    description = Column(Text, comment='详细描述')
    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    operator_id = Column(Integer, comment='操作员ID')
    cover = Column(String(500), comment='封面图')
    cover_video = Column(String(500), comment='封面视频')
    is_del = Column(TINYINT, server_default=text("'0'"), comment='是否删除,0正常,1删除')
    title = Column(String(200), comment='文章标题')
    title_tit = Column(String(200), comment='文章副标题')
    auther = Column(String(200), comment='作者')
    proc_id = Column(Integer, comment='礼包id')
    pic_id = Column(Integer, comment='0图片1视频')
    avatar = Column(VARCHAR(512), comment='头像url')
    share_word = Column(String(500), comment='分享钩子语')
    share_label = Column(Text, comment='分享标签，按逗号分割')
    share_title = Column(String(200), comment='微信分享标题')
    share_pic = Column(String(500), comment='分享卡片图')
    is_draft = Column(TINYINT, server_default=text("'0'"), comment='是否是草稿,0正常,1是')
    video_level = Column(Integer, comment='默认0表示普通,1达人,2店长3,服务商,4分公司')
    order_id = Column(Integer, nullable=False, server_default=text("'0'"), comment='排序id')


class TVideoArticleList(Base):
    __tablename__ = 't_video_article_list'
    __table_args__ = {'comment': '视频文章模块列表表'}

    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, nullable=False, server_default=text("'0'"), comment='文章内容类型,0可复制文本,1编辑器,2视频')
    article_id = Column(Integer, nullable=False, server_default=text("'0'"), comment='所属video_article文章id')
    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    operator_id = Column(Integer, comment='操作员ID')
    content = Column(Text, comment='文章模块内容')
    is_del = Column(TINYINT, server_default=text("'0'"), comment='是否删除,0正常,1删除')


class TVideoArticleType(Base):
    __tablename__ = 't_video_article_type'
    __table_args__ = {'comment': '文章分类表'}

    id = Column(Integer, primary_key=True, comment='标识id')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    title = Column(String(255), comment='类型标题')
    describe = Column(Text, comment='类型描述')
    cover = Column(String(500), comment='封面图')


class TVideoContent(Base):
    __tablename__ = 't_video_content'
    __table_args__ = {'comment': '培训视频内容表'}

    id = Column(Integer, primary_key=True)
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    content_name = Column(String(256), comment='视频名称')
    content_url = Column(String(256), comment='视频播放URL（https开头完整路径）')
    group_id = Column(Integer, server_default=text("'0'"), comment='所属分组id，t_video_group表id')


class TVideoGroup(Base):
    __tablename__ = 't_video_group'
    __table_args__ = {'comment': '培训视频分组表'}

    id = Column(Integer, primary_key=True)
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    group_name = Column(String(256), comment='分组名称')


class TVideoRecharge(Base):
    __tablename__ = 't_video_recharge'
    __table_args__ = {'comment': '生成与使用充值码表'}

    id = Column(Integer, primary_key=True, comment='标识id')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    good_id = Column(Integer, server_default=text("'0'"), comment='礼包商品id')
    good_name = Column(String(40), comment='礼包名称')
    admin_name = Column(String(40), comment='操作员名字')
    user_id = Column(Integer, server_default=text("'0'"), comment='指定用户id')
    user_phone = Column(String(40), comment='指定用户电话')
    user_name = Column(String(40), comment='指定指定用户昵称')
    video_level = Column(TINYINT(1), server_default=text("'0'"), comment='视频分发身份0达人,1店长,2服务商,3分公司')
    level_id = Column(Integer, server_default=text("'0'"), comment='用户等级 默认是0粉丝,1会员,2核心会员')
    create_nmu = Column(Integer, server_default=text("'0'"), comment='本次生成总数')
    act_user_id = Column(Integer, server_default=text("'0'"), comment='激活用户id')
    act_user_phone = Column(String(40), comment='激活用户电话')
    act_user_name = Column(String(40), comment='激活指定用户昵称')
    act_time = Column(TIMESTAMP, comment='激活时间')
    is_act = Column(TINYINT, server_default=text("'0'"), comment='是否被激活,0未激活,1已激活')
    act_code = Column(String(100), comment='激活码')
    batch_code = Column(String(100), comment='创建批次码')


class TVideoRechargeLog(Base):
    __tablename__ = 't_video_recharge_log'
    __table_args__ = {'comment': '用户账户视频生成条数变动记录表'}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, comment='激活用户id')
    user_nick = Column(String(45), comment='激活用户昵称')
    phone = Column(VARCHAR(45), comment='激活用户联系方式')
    change = Column(Integer, nullable=False, server_default=text("'0'"), comment='变动条数')
    balance = Column(Integer, nullable=False, comment='剩余条数')
    type = Column(VARCHAR(20), comment='类型')
    description = Column(VARCHAR(100), comment='详细描述')
    create_time = Column(TIMESTAMP, comment='创建时间')
    operator_id = Column(Integer, comment='操作员ID')
    out_trade_no = Column(String(64))
    good_id = Column(VARCHAR(100), comment='收益商品id')
    good_title = Column(Text, comment='收益商品标题名称')
    good_num = Column(VARCHAR(100), comment='收益商品数量')
    recharge_id = Column(Integer, comment='充值礼包ID')
    owner_id = Column(Integer, nullable=False, comment='码主用户id')
    owner_nick = Column(String(45), comment='码主用户昵称')
    owner_phone = Column(VARCHAR(45), comment='码主用户联系方式')


class TVideoTask(Base):
    __tablename__ = 't_video_task'
    __table_args__ = {'comment': '分发视频任务表'}

    id = Column(Integer, primary_key=True, comment='标识id')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    title = Column(String(255), comment='任务标题')
    describe = Column(Text, comment='任务描述,任务要求')
    top = Column(Integer, server_default=text("'0'"), comment='任务领取上限')
    big = Column(Integer, server_default=text("'0'"), comment='单号最大领取量')
    received = Column(Integer, server_default=text("'0'"), comment='已领取量')
    money = Column(Integer, server_default=text("'0'"), comment='获得任务金额')
    coin = Column(Integer, server_default=text("'0'"), comment='获得任务购物券')
    shoper_id = Column(Integer, server_default=text("'0'"), comment='所属商家id')
    shoper_name = Column(String(255), comment='分发商名称')
    shoper_phone = Column(String(40), comment='分发商电话')
    stat = Column(TINYINT, server_default=text("'0'"), comment='0未开启,1进行中,2已结束')
    style = Column(Text, comment='参考图样地址七牛oss,逗号分割多个图样地址')
    verfy = Column(String(40), comment='平台名称抖音,小红书,视频号,快手,朋友圈')
    run_time = Column(TIMESTAMP, comment='开始时间')
    expired_time = Column(TIMESTAMP, comment='结束时间')
    is_auto = Column(TINYINT, server_default=text("'0'"), comment='是否自动处理状态,0自动,1手动')
    cover = Column(String(500), comment='封面图')
    local_path = Column(String(500), comment='素材在本地地址')
    update_time = Column(TIMESTAMP, comment='更新时间')
    type_id = Column(Integer, server_default=text("'0'"), comment='所属类型id类型,0图片1视频2音频')
    show_money = Column(Integer, server_default=text("'0'"), comment='显示售价')
    prop_one = Column(Float(5), server_default=text("'0.0000'"), comment='佣金分成比值')
    des_sp = Column(Text, comment='视频文案')
    des_sp_link = Column(Text, comment='视频文案链接')
    des_kou = Column(Text, comment='口播文案')
    audit = Column(TINYINT, server_default=text("'0'"), comment='0未审核,1通过审核,2未通过')
    audit_time = Column(TIMESTAMP, comment='审核时间')
    audit_adm = Column(Integer, server_default=text("'0'"), comment='审核管理人id')
    audit_info = Column(String(255), comment='审核备注100个汉字以内')
    finish_id = Column(Integer, server_default=text("'0'"), comment='成品视频素材id')
    synth_id = Column(Integer, server_default=text("'0'"), comment='合成视频素材id')
    day_top = Column(Integer, server_default=text("'0'"), comment='用户每日任务领取上限')
    video_num = Column(Integer, server_default=text("'0'"), comment='视频领取数量')
    pic_num = Column(Integer, server_default=text("'0'"), comment='图片领取数量')
    music_num = Column(Integer, server_default=text("'0'"), comment='音频领取数量')
    class_id = Column(Integer, server_default=text("'0'"), comment='所属分类')
    rem_money = Column(Integer, server_default=text("'0'"), comment='推荐人金额')
    rem_mid_money = Column(Integer, server_default=text("'0'"), comment='间推人金额')
    rem_team = Column(Integer, server_default=text("'0'"), comment='推荐团长金额')
    rem_mid_team = Column(Integer, server_default=text("'0'"), comment='间推团长金额')
    live_mid_uid = Column(Integer, server_default=text("'0'"), comment='居间人id')
    live_mid_money = Column(Integer, server_default=text("'0'"), comment='居间人收益')


class TVideoTaskMaterial(Base):
    __tablename__ = 't_video_task_material'
    __table_args__ = {'comment': '视频任务素材表'}

    id = Column(Integer, primary_key=True, comment='标识id')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    task_id = Column(Integer, server_default=text("'0'"), comment='参与任务id')
    path = Column(Text, comment='素材七牛地址')
    m_type = Column(TINYINT, server_default=text("'0'"), comment='素材类型,0图片1视频2音频')
    update_time = Column(TIMESTAMP, comment='截图更新时间')
    is_del = Column(TINYINT, server_default=text("'0'"), comment='是否删除,0正常1删除')
    ma_name = Column(String(100), comment='素材名称')
    ma_info = Column(String(255), comment='备注信息')
    bag_id = Column(Integer, server_default=text("'0'"), comment='素材包id')
    is_download = Column(TINYINT, server_default=text("'0'"), comment='是否下载,0正常1已下载')
    down_time = Column(TIMESTAMP, comment='下载更新时间')
    user_id = Column(Integer, server_default=text("'0'"), comment='领取用户id')


class TVideoTaskMaterialBag(Base):
    __tablename__ = 't_video_task_material_bag'
    __table_args__ = {'comment': '视频任务素材包表'}

    id = Column(Integer, primary_key=True, comment='标识id')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    task_id = Column(Integer, server_default=text("'0'"), comment='参与任务id')
    update_time = Column(TIMESTAMP, comment='截图更新时间')
    is_del = Column(TINYINT, server_default=text("'0'"), comment='是否删除,0正常1删除')
    bag_name = Column(String(255), comment='素材包名称')


class TVideoTaskReceive(Base):
    __tablename__ = 't_video_task_receive'
    __table_args__ = {'comment': '领取视频任务表'}

    id = Column(Integer, primary_key=True, comment='标识id')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    task_id = Column(Integer, server_default=text("'0'"), comment='参与任务id')
    shoper_id = Column(Integer, server_default=text("'0'"), comment='所属商家id')
    shoper_name = Column(String(255), comment='分发商名称')
    shoper_phone = Column(String(40), comment='分发商电话')
    user_id = Column(Integer, server_default=text("'0'"), comment='用户id')
    user_name = Column(String(45), comment='昵称')
    user_phone = Column(String(45), comment='联系方式')
    title = Column(String(255), comment='任务标题')
    up_pic = Column(Text, comment='任务上传截图')
    audit_comment = Column(Text, comment='审核评论内容')
    audit_status = Column(TINYINT, server_default=text("'0'"), comment='状态,0领取,1待审核,2审核通过,3审核未通过')
    update_time = Column(TIMESTAMP, comment='截图更新时间')
    audit_time = Column(TIMESTAMP, comment='管理审核时间')
    bag_id = Column(Integer, server_default=text("'0'"), comment='素材包id')
    audit_adm = Column(Integer, server_default=text("'0'"), comment='审核管理人id')
    audit_info = Column(String(255), comment='审核备注100个汉字以内')
    mater_id = Column(Integer, server_default=text("'0'"), comment='领取素材id')
    mater_path = Column(String(500), comment='领取素材地址')
    get_time = Column(TIMESTAMP, comment='领取时间')
    money_status = Column(TINYINT, server_default=text("'0'"), comment='状态,0待分润,1已分润')


class TVideoTaskType(Base):
    __tablename__ = 't_video_task_type'
    __table_args__ = {'comment': '分发视频任务分类表'}

    id = Column(Integer, primary_key=True, comment='标识id')
    register_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    title = Column(String(255), comment='类型标题')
    describe = Column(Text, comment='类型描述')
    cover = Column(String(500), comment='封面图')


class TVideoConfig(Base):
    __tablename__ = 'video_config'
    __table_args__ = {'comment': '视频相关模块管理端配置表'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    config_key = Column(VARCHAR(50), nullable=False, comment='配置键')
    config_value = Column(Text, comment='配置值')
    module = Column(VARCHAR(30), nullable=False, comment='所属模块: video_parse / ai_image / video_to_prompt')
    description = Column(VARCHAR(200), comment='配置说明')
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')
