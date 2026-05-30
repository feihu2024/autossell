from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from fastapi.exceptions import HTTPException


class CreateAddress(BaseModel):
    user_id: Optional[int] = Field(title='外键')
    province: Optional[str] = Field(title='省')
    city: Optional[str] = Field(title='市')
    area: Optional[str] = Field(title='区')
    street: Optional[str] = Field(title='街道')
    description: Optional[str] = Field(title='详细地址')
    consignee: Optional[str] = Field(title='收货人姓名')
    phone: Optional[str] = Field(title='收货人电话')
    default_val: Optional[int] = Field(title='1:默认  0:非默认')

        
class SAddress(CreateAddress):
    id: int

    class Config:
        orm_mode = True

class Address(CreateAddress):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResAddress(BaseModel):
    data: List[SAddress]
    total: int
    
class CreateAdmin(BaseModel):
    username: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    level_id: Optional[int]
    password: Optional[str]
    id_card: Optional[str]
    gender: Optional[str]
    register_time: Optional[datetime] = Field(title='创建时间')
    last_active_time: Optional[datetime]
    status: Optional[str]
    business_id: Optional[int] = Field(title='商家ID_busiess_content')
    admin_id: Optional[int] = Field(title='所属商家管理id')
    user_pic: Optional[str] = Field(title='头像url')
    user_info: Optional[str] = Field(title='用户备注')

        
class SAdmin(CreateAdmin):
    id: int

    class Config:
        orm_mode = True

class Admin(CreateAdmin):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResAdmin(BaseModel):
    data: List[SAdmin]
    total: int
    
class CreateAutobody(BaseModel):
    register_time: Optional[datetime] = Field(title='创建时间')
    type_id: Optional[int] = Field(title='所属智能体分类id')
    at_name: Optional[str] = Field(title='智能体名称')
    describe: Optional[str] = Field(title='智能体描述')
    cover: Optional[str] = Field(title='智能体封面图')
    at_id: Optional[str] = Field(title='智能体ID')
    order_id: Optional[int] = Field(title='优先级排序')
    stat: Optional[int] = Field(title='状态,0正常1关闭')
    update_time: Optional[datetime] = Field(title='更新时间')
    preview_video: Optional[str] = Field(title='智能体封面图')
    auto_tag: Optional[str] = Field(title='智能体标签')
    del_stat: Optional[int] = Field(title='删除,0正常1删除')

        
class SAutobody(CreateAutobody):
    id: int = Field(title='标识id')

    class Config:
        orm_mode = True

class Autobody(CreateAutobody):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResAutobody(BaseModel):
    data: List[SAutobody]
    total: int
    
class CreateAutobodyFile(BaseModel):
    register_time: Optional[datetime] = Field(title='创建时间')
    autobody_id: Optional[int] = Field(title='所属智能体id')
    title: Optional[str] = Field(title='文件名称')
    describe: Optional[str] = Field(title='文件描述')
    url: Optional[str] = Field(title='文件地址')

        
class SAutobodyFile(CreateAutobodyFile):
    id: int = Field(title='标识id')

    class Config:
        orm_mode = True

class AutobodyFile(CreateAutobodyFile):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResAutobodyFile(BaseModel):
    data: List[SAutobodyFile]
    total: int
    
class CreateAutobodyType(BaseModel):
    register_time: Optional[datetime] = Field(title='创建时间')
    title: Optional[str] = Field(title='类型标题')
    describe: Optional[str] = Field(title='类型描述')
    cover: Optional[str] = Field(title='封面图')

        
class SAutobodyType(CreateAutobodyType):
    id: int = Field(title='标识id')

    class Config:
        orm_mode = True

class AutobodyType(CreateAutobodyType):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResAutobodyType(BaseModel):
    data: List[SAutobodyType]
    total: int
    
class CreateBagCagegory(BaseModel):
    pc_name: Optional[str] = Field(title='批次名称')
    pc_num: Optional[int] = Field(title='批次数量')
    register_time: Optional[datetime] = Field(title='创建时间')
    endtime: Optional[datetime] = Field(title='结束时间')
    bag_id: Optional[int] = Field(title='礼包id')

        
class SBagCagegory(CreateBagCagegory):
    id: int = Field(title='标识id')

    class Config:
        orm_mode = True

class BagCagegory(CreateBagCagegory):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResBagCagegory(BaseModel):
    data: List[SBagCagegory]
    total: int
    
class CreateBagPas(BaseModel):
    pass_num: Optional[str] = Field(title='加密编号(十六进制)')
    pc_name: Optional[str] = Field(title='批次名称')
    pc_num: Optional[int] = Field(title='批次数量')
    pc_id: Optional[int] = Field(title='批次id(不可重复)')
    stat: Optional[int] = Field(title='是否激活,默认0未激活1已激活2过期未用')
    register_time: Optional[datetime] = Field(title='创建时间')
    startime: Optional[datetime] = Field(title='激活时间')
    user_id: Optional[int] = Field(title='激活会员id')
    endtime: Optional[datetime] = Field(title='结束时间')
    cate_id: Optional[int] = Field(title='批次分类id')

        
class SBagPas(CreateBagPas):
    id: int = Field(title='标识id')

    class Config:
        orm_mode = True

class BagPas(CreateBagPas):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResBagPas(BaseModel):
    data: List[SBagPas]
    total: int
    
class CreateBalance(BaseModel):
    user_id: Optional[int] = Field(title='外键')
    change: Optional[int] = Field(title='变动金额')
    balance: Optional[int] = Field(title='余额')
    type: Optional[str] = Field(title='类型')
    description: Optional[str] = Field(title='详细描述')
    create_time: Optional[datetime] = Field(title='创建时间')
    user_withdraw_id: Optional[int]
    operator_id: Optional[int] = Field(title='操作员ID')
    out_trade_no: Optional[str]
    good_id: Optional[str] = Field(title='收益商品id')
    good_title: Optional[str] = Field(title='收益商品标题名称')
    good_num: Optional[str] = Field(title='收益商品数量')
    titlelog: Optional[str] = Field(title='标题记录')
    user_nick: Optional[str] = Field(title='用户昵称')
    phone: Optional[str] = Field(title='联系方式')
    register_time: Optional[datetime] = Field(title='注册时间')

        
class SBalance(CreateBalance):
    id: int

    class Config:
        orm_mode = True

class Balance(CreateBalance):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResBalance(BaseModel):
    data: List[SBalance]
    total: int
    
class CreateBalanceGive(BaseModel):
    user_ids: Optional[str] = Field(title='分配用户，逗号分隔的用户id')
    coin: Optional[int] = Field(title='分配积分总额')
    balance: Optional[int] = Field(title='分配余额总额')
    type: Optional[int] = Field(title='类型，1为余额，2为积分')
    description: Optional[str] = Field(title='分配明细')
    create_time: Optional[datetime] = Field(title='创建时间')
    operator_id: Optional[int] = Field(title='操作员ID')
    sucess_num: Optional[int] = Field(title='分配成功数量')
    give_txt: Optional[str] = Field(title='打款备注信息')

        
class SBalanceGive(CreateBalanceGive):
    id: int

    class Config:
        orm_mode = True

class BalanceGive(CreateBalanceGive):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResBalanceGive(BaseModel):
    data: List[SBalanceGive]
    total: int
    
class CreateBanner(BaseModel):
    image: Optional[str] = Field(title='图片url')
    title: Optional[str] = Field(title='主标题')
    subtitle: Optional[str] = Field(title='视频地址')
    width: Optional[int] = Field(title='图片宽度')
    height: Optional[int] = Field(title='图片高度')
    create_time: Optional[datetime] = Field(title='创建时间')
    description: Optional[str] = Field(title='详情')
    good_id: Optional[int] = Field(title='商品id')
    ban_label: Optional[str] = Field(title='标签')
    type_id: Optional[int] = Field(title='0:banner   1:直通车')
    good_spec_id: Optional[int]
    ba_stat: Optional[int] = Field(title='小程序端展示状态,默认0正常展示')
    video: Optional[str] = Field(title='视频url')
    is_video: Optional[int] = Field(title='是否展示视频0:使用imag图片地址1:使用video视频地址')
    class_id: Optional[int] = Field(title='广告分类id')

        
class SBanner(CreateBanner):
    id: int

    class Config:
        orm_mode = True

class Banner(CreateBanner):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResBanner(BaseModel):
    data: List[SBanner]
    total: int
    
class CreateBannerType(BaseModel):
    register_time: Optional[datetime] = Field(title='创建时间')
    title: Optional[str] = Field(title='类型标题')
    describe: Optional[str] = Field(title='类型描述')
    cover: Optional[str] = Field(title='封面图')

        
class SBannerType(CreateBannerType):
    id: int = Field(title='标识id')

    class Config:
        orm_mode = True

class BannerType(CreateBannerType):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResBannerType(BaseModel):
    data: List[SBannerType]
    total: int
    
class CreateBigorderFour(BaseModel):
    layer_id: Optional[int] = Field(title='行号(所在层数)')
    cur_layer_id: Optional[int] = Field(title='当前行号从左到右排序号')
    cur_layer_total: Optional[int] = Field(title='当前行排序总数量')
    parent_id: Optional[int] = Field(title='上级对应序号')
    order_id: Optional[int] = Field(title='大公排id')

        
class SBigorderFour(CreateBigorderFour):
    id: int = Field(title='标识id')

    class Config:
        orm_mode = True

class BigorderFour(CreateBigorderFour):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResBigorderFour(BaseModel):
    data: List[SBigorderFour]
    total: int
    
class CreateBigorderInitbag(BaseModel):
    bag_name: Optional[str] = Field(title='礼包名称')
    register_time: Optional[datetime] = Field(title='创建时间')
    tuan_id: Optional[int] = Field(title='所属团长id')
    price_total: Optional[int] = Field(title='总价格')
    invited_money: Optional[int] = Field(title='直推金额')
    layer_every: Optional[int] = Field(title='每层复购金额')
    layer_num: Optional[int] = Field(title='复购层数（含直推）')
    grant_num: Optional[int] = Field(title='赠予兑换券额度')
    bag_cont: Optional[str] = Field(title='礼包介绍')
    bag_type: Optional[int] = Field(title='礼包类型0正常1大团长复购礼包')
    phone: Optional[str] = Field(title='团长电话')
    bag_pic: Optional[str] = Field(title='图像url')
    fund_one: Optional[int] = Field(title='归集初级资金池额度')
    fund_two: Optional[int] = Field(title='归集高级资金池额度')
    fund_three: Optional[int] = Field(title='归集顶级资金池额度')

        
class SBigorderInitbag(CreateBigorderInitbag):
    id: int = Field(title='主键id')

    class Config:
        orm_mode = True

class BigorderInitbag(CreateBigorderInitbag):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResBigorderInitbag(BaseModel):
    data: List[SBigorderInitbag]
    total: int
    
class CreateBigorderLog(BaseModel):
    register_time: Optional[datetime] = Field(title='创建时间')
    user_id: Optional[int] = Field(title='复购用户id')
    price_total: Optional[int] = Field(title='总价格')
    invited_money: Optional[int] = Field(title='直推金额')
    layer_every: Optional[int] = Field(title='每层复购金额')
    layer_num: Optional[int] = Field(title='复购层数（含直推）')
    grant_num: Optional[int] = Field(title='赠予兑换券额度')
    bag_cont: Optional[str] = Field(title='复购分润结构[{layer:1,user:2,balance:100,order:1}]')

        
class SBigorderLog(CreateBigorderLog):
    id: int = Field(title='主键id')

    class Config:
        orm_mode = True

class BigorderLog(CreateBigorderLog):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResBigorderLog(BaseModel):
    data: List[SBigorderLog]
    total: int
    
class CreateBigorderSet(BaseModel):
    set_name: Optional[str] = Field(title='配置参数关键字名称')
    val_int: Optional[int] = Field(title='数字值')
    val_str: Optional[str] = Field(title='文本值')
    set_cont: Optional[str] = Field(title='配置项介绍')

        
class SBigorderSet(CreateBigorderSet):
    id: int = Field(title='序号id')

    class Config:
        orm_mode = True

class BigorderSet(CreateBigorderSet):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResBigorderSet(BaseModel):
    data: List[SBigorderSet]
    total: int
    
class CreateBigorderThree(BaseModel):
    layer_id: Optional[int] = Field(title='行号(所在层数)')
    cur_layer_id: Optional[int] = Field(title='当前行号从左到右排序号')
    cur_layer_total: Optional[int] = Field(title='当前行排序总数量')
    parent_id: Optional[int] = Field(title='上级对应序号')
    order_id: Optional[int] = Field(title='大公排id')

        
class SBigorderThree(CreateBigorderThree):
    id: int = Field(title='标识id')

    class Config:
        orm_mode = True

class BigorderThree(CreateBigorderThree):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResBigorderThree(BaseModel):
    data: List[SBigorderThree]
    total: int
    
class CreateBigorderTwo(BaseModel):
    layer_id: Optional[int] = Field(title='行号(所在层数)')
    cur_layer_id: Optional[int] = Field(title='当前行号从左到右排序号')
    cur_layer_total: Optional[int] = Field(title='当前行排序总数量')
    parent_id: Optional[int] = Field(title='上级对应序号')
    order_id: Optional[int] = Field(title='大公排id')

        
class SBigorderTwo(CreateBigorderTwo):
    id: int = Field(title='标识id')

    class Config:
        orm_mode = True

class BigorderTwo(CreateBigorderTwo):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResBigorderTwo(BaseModel):
    data: List[SBigorderTwo]
    total: int
    
class CreateBusinessContent(BaseModel):
    register_time: Optional[datetime] = Field(title='创建时间')
    business_code: Optional[str] = Field(title='业务申请编号')
    contact_type: Optional[str] = Field(title='超级管理员类型LEGAL：经营者/法人,SUPER：经办人')
    contact_name: Optional[str] = Field(title='超级管理员姓名')
    contact_id_doc_type: Optional[str] = Field(title='当超级管理员类型是经办人时，请上传超级管理员证件类型')
    contact_license_info: Optional[int] = Field(title='超管license表ID,授权函license_copy_other1')
    contact_openid: Optional[str] = Field(title='该字段选填，若上传为超级管理员签约时，会校验微信号是否与该微信OpenID一致')
    contact_mobile_phone: Optional[str] = Field(title='联系手机')
    contact_email: Optional[str] = Field(title='联系邮箱')
    subject_type: Optional[str] = Field(title='主体类型需与营业执照/登记证书上一致')
    subject_finance_institution: Optional[int] = Field(title='是否是金融机构,0不是(false),1是(true)')
    subject_business_license_info: Optional[int] = Field(title='营业执照license表ID')
    subject_certificate_info: Optional[int] = Field(title='登记证书license表ID')
    subject_certificate_letter_copy: Optional[int] = Field(title='单位证明函照片license表ID')
    subject_finance_institution_info: Optional[int] = Field(title='金融机构许可证信息license表ID')
    subject_identity_info: Optional[int] = Field(title='经营者/法人身份证件license表ID')
    subject_ubo_info_list: Optional[str] = Field(title='最终受益人信息列表(UBO),license表ID：1,2,3')
    business_merchant_shortname: Optional[str] = Field(title='商户简称')
    business_service_phone: Optional[str] = Field(title='客服电话')
    business_sales_scenes_type: Optional[str] = Field(title='经营场景类型如:SALES_SCENES_STORE,SALES_SCENES_MP')
    sales_biz_store_info: Optional[int] = Field(title='线下场所场景license表ID')
    sales_mp_info: Optional[int] = Field(title='公众号场景license表ID')
    sales_mini_program_info: Optional[int] = Field(title='小程序场景license表ID')
    sales_app_info: Optional[int] = Field(title='App场景license表ID')
    sales_web_info: Optional[int] = Field(title='互联网网站场景license表ID')
    sales_wework_info: Optional[int] = Field(title='企业微信场景license表ID')
    settlement_id: Optional[str] = Field(title='入驻结算规则ID')
    settlement_qualification_type: Optional[str] = Field(title='所属行业')
    settlement_qualifications: Optional[int] = Field(title='特殊资质图片license表ID')
    settlement_activities_id: Optional[str] = Field(title='优惠费率活动ID')
    settlement_activities_rate: Optional[str] = Field(title='优惠费率活动值')
    settlement_debit_activities_rate: Optional[str] = Field(title='非信用卡活动费率值')
    settlement_credit_activities_rate: Optional[str] = Field(title='信用卡活动费率值')
    settlement_activities_additions: Optional[int] = Field(title='优惠费率活动补充材料license表ID')
    bank_account_type: Optional[str] = Field(title='账户类型')
    bank_account_name: Optional[str] = Field(title='开户名称')
    bank_account_bank: Optional[str] = Field(title='开户银行')
    bank_address_code: Optional[str] = Field(title='开户银行省市编码')
    bank_branch_id: Optional[str] = Field(title='开户银行联行号')
    bank_name: Optional[str] = Field(title='开户银行全称（含支行）')
    bank_account_number: Optional[str] = Field(title='银行账号')
    addition_msg: Optional[str] = Field(title='补充说明')
    addition_info: Optional[int] = Field(title='补充材料license表ID')
    audit_stat: Optional[int] = Field(title='状态,0未提交,1提交成功,2提交失败,3审核成功,4审核失败')
    subject_ubo_id_owner: Optional[int] = Field(title='法人是否是收益人')

        
class SBusinessContent(CreateBusinessContent):
    id: int = Field(title='标识id')

    class Config:
        orm_mode = True

class BusinessContent(CreateBusinessContent):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResBusinessContent(BaseModel):
    data: List[SBusinessContent]
    total: int
    
class CreateBusinessLicense(BaseModel):
    register_time: Optional[datetime] = Field(title='创建时间')
    business_id: Optional[int] = Field(title='特约主表id')
    lic_name: Optional[str] = Field(title='证件名称，如：营业执照')
    lic_type: Optional[str] = Field(title='证件类型:contact超管,license营业,certificate登记证书,finance金融许可,card经营者,other其他,ubo受益人,biz线下场景,mp公众号mini小程序,app,web网站场景wework企业微信')
    lic_type_name: Optional[str] = Field(title='证件类型名称')
    lic_number: Optional[str] = Field(title='证件号码')
    lic_copy: Optional[str] = Field(title='证件正面照片')
    lic_copy_wx: Optional[str] = Field(title='证件正面微信MediaID')
    lic_copy_back: Optional[str] = Field(title='证件反面照片')
    lic_copy_back_wx: Optional[str] = Field(title='证件反面微信MediaID')
    lic_copy_other1: Optional[str] = Field(title='附加照片1')
    lic_copy_other1_wx: Optional[str] = Field(title='附加照片1微信MediaID')
    lic_copy_other2: Optional[str] = Field(title='附加照片2')
    lic_copy_other2_wx: Optional[str] = Field(title='附加照片2微信MediaID')
    lic_copy_array: Optional[str] = Field(title='多张照片pic1,pic2')
    lic_copy_array_wx: Optional[str] = Field(title='多张照片微信MediaID')
    lic_period_begin: Optional[datetime] = Field(title='证件有效期开始时间')
    lic_period_end: Optional[datetime] = Field(title='证件有效期结束时间')
    lic_person1: Optional[str] = Field(title='证件上的名称1,如公司名称,省份证姓名')
    lic_person2: Optional[str] = Field(title='证件上的名称2,如法人姓名')
    lic_address: Optional[str] = Field(title='证件地址')
    lic_person_video: Optional[str] = Field(title='视频材料')
    lic_person_video_wx: Optional[str] = Field(title='视频材料微信MediaID')
    lic_period_end_long: Optional[int] = Field(title='证件是否长期有效')

        
class SBusinessLicense(CreateBusinessLicense):
    id: int = Field(title='标识id')

    class Config:
        orm_mode = True

class BusinessLicense(CreateBusinessLicense):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResBusinessLicense(BaseModel):
    data: List[SBusinessLicense]
    total: int
    
class CreateCart(BaseModel):
    user_id: Optional[int] = Field(title='用户编号')
    good_id: Optional[int] = Field(title='商品编号')
    amount: Optional[int] = Field(title='购买数量')
    creat_time: Optional[datetime] = Field(title='创建时间')
    good_spec_id: Optional[int]
    good_option_id: Optional[int] = Field(title='商品选项id')
    good_option_name: Optional[str] = Field(title='选项名称')
    zdyspec: Optional[str] = Field(title='用户所选自定义规格')

        
class SCart(CreateCart):
    id: int

    class Config:
        orm_mode = True

class Cart(CreateCart):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResCart(BaseModel):
    data: List[SCart]
    total: int
    
class CreateCategory(BaseModel):
    cname: Optional[str] = Field(title='分类名称')
    parent_category_id: Optional[int] = Field(title='上级分类id，默认0为顶级分类')

        
class SCategory(CreateCategory):
    id: int

    class Config:
        orm_mode = True

class Category(CreateCategory):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResCategory(BaseModel):
    data: List[SCategory]
    total: int
    
class CreateCity(BaseModel):
    cname: Optional[str]
    parid: Optional[int] = Field(title='上级地区id，默认0为顶级地区')
    status: Optional[int] = Field(title='地区状态')

        
class SCity(CreateCity):
    id: int

    class Config:
        orm_mode = True

class City(CreateCity):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResCity(BaseModel):
    data: List[SCity]
    total: int
    
class CreateCoin(BaseModel):
    user_id: Optional[int] = Field(title='外键')
    change: Optional[int] = Field(title='变动')
    coin: Optional[int] = Field(title='积分')
    type: Optional[str] = Field(title='类型')
    description: Optional[str] = Field(title='详细')
    create_time: Optional[datetime] = Field(title='创建时间')
    out_trade_no: Optional[str]
    user_nick: Optional[str] = Field(title='用户昵称')
    phone: Optional[str] = Field(title='联系方式')
    register_time: Optional[datetime] = Field(title='注册时间')

        
class SCoin(CreateCoin):
    id: int

    class Config:
        orm_mode = True

class Coin(CreateCoin):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResCoin(BaseModel):
    data: List[SCoin]
    total: int
    
class CreateCombo(BaseModel):
    good_id: Optional[int]
    title: Optional[str]
    amount: Optional[int]
    price: Optional[int]

        
class SCombo(CreateCombo):
    id: int

    class Config:
        orm_mode = True

class Combo(CreateCombo):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResCombo(BaseModel):
    data: List[SCombo]
    total: int
    
class CreateComment(BaseModel):
    user_id: Optional[int] = Field(title='会员id')
    create_time: Optional[datetime] = Field(title='创建时间')
    phone: Optional[str] = Field(title='联系方式')
    content: Optional[str] = Field(title='留言内容')
    status: Optional[int] = Field(title='留言处理状态 ')

        
class SComment(CreateComment):
    id: int

    class Config:
        orm_mode = True

class Comment(CreateComment):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResComment(BaseModel):
    data: List[SComment]
    total: int
    
class CreateCouponTag(BaseModel):
    status: Optional[int] = Field(title='标签状态：0为正常，-1为删除')
    tname: Optional[str] = Field(title='标签名称')
    register_time: Optional[datetime] = Field(title='标签创建时间')
    pro_id: Optional[int] = Field(title='所属行业id，t_store_profession表id')
    operator_id: Optional[int] = Field(title='操作员ID')

        
class SCouponTag(CreateCouponTag):
    id: int

    class Config:
        orm_mode = True

class CouponTag(CreateCouponTag):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResCouponTag(BaseModel):
    data: List[SCouponTag]
    total: int
    
class CreateDeliveryRule(BaseModel):
    good_id: Optional[int] = Field(title='商品id')
    spec_id: Optional[int] = Field(title='规格id')
    province: Optional[str] = Field(title='省')
    city: Optional[str] = Field(title='市')
    area: Optional[str] = Field(title='区')
    is_reachable: Optional[int] = Field(title='是否可抵达    0：不可抵达     1：可抵达')
    delivery_fee: Optional[int] = Field(title='邮寄费用')

        
class SDeliveryRule(CreateDeliveryRule):
    id: int

    class Config:
        orm_mode = True

class DeliveryRule(CreateDeliveryRule):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResDeliveryRule(BaseModel):
    data: List[SDeliveryRule]
    total: int
    
class CreateExportFile(BaseModel):
    user_id: Optional[int] = Field(title='用户id')
    export_url: Optional[str] = Field(title='文件生成地址')
    type: Optional[str] = Field(title='类型')
    description: Optional[str] = Field(title='详细描述')
    create_time: Optional[datetime] = Field(title='创建时间')

        
class SExportFile(CreateExportFile):
    id: int

    class Config:
        orm_mode = True

class ExportFile(CreateExportFile):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResExportFile(BaseModel):
    data: List[SExportFile]
    total: int
    
class CreateFlashOrder(BaseModel):
    package_id: Optional[int] = Field(title='包id')
    status: Optional[int] = Field(title='状态   0：未付款    1：已付款    2：未发货    3：已发货    4：已签收     5：退货申请    6：退货中    7：已退货    8：取消交易')
    create_time: Optional[datetime] = Field(title='下单时间')
    paid_time: Optional[datetime] = Field(title='付款时间')
    user_id: Optional[int] = Field(title='用户id')
    number: Optional[int] = Field(title='商品数量')
    flash_price: Optional[int] = Field(title='秒杀单价')
    flash_cost: Optional[int] = Field(title='秒杀成本')
    out_trade_no: Optional[str]
    paid_amount: Optional[int] = Field(title='支付金额')
    paid_balance: Optional[int] = Field(title='余额支付金额')
    single_status: Optional[int] = Field(title='是否单份代卖')
    sold: Optional[int] = Field(title='已售出商品数量')
    whole_status: Optional[int] = Field(title='是否整份代码,暂时废弃,统一启用single_status字段判断')
    spec_id: Optional[int] = Field(title='规格id')
    put_on_time: Optional[datetime] = Field(title='上架时间,计算收益时使用')
    detail: Optional[str] = Field(title='订单备注,+=更新')
    is_assign_income: Optional[int] = Field(title='是否分配收益')
    complete_time: Optional[datetime] = Field(title='订单完结时间')
    return_sold: Optional[int] = Field(title='已提货数量')

        
class SFlashOrder(CreateFlashOrder):
    id: int

    class Config:
        orm_mode = True

class FlashOrder(CreateFlashOrder):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResFlashOrder(BaseModel):
    data: List[SFlashOrder]
    total: int
    
class CreateFlashOrderReturn(BaseModel):
    user_id: Optional[int] = Field(title='用户id')
    income_days: Optional[int] = Field(title='剩余秒杀退货收益天数')
    latest_time: Optional[datetime] = Field(title='最近一次退货时间')
    latest_income_user: Optional[int] = Field(title='最近一次退货收益')
    latest_income_layer: Optional[int] = Field(title='最近一次退货层级收益')
    latest_income_toper: Optional[int] = Field(title='最近一次退货见点收益')
    latest_income_groupsir: Optional[int] = Field(title='最近一次退货团长收益')

        
class SFlashOrderReturn(CreateFlashOrderReturn):
    id: int = Field(title='主键id')

    class Config:
        orm_mode = True

class FlashOrderReturn(CreateFlashOrderReturn):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResFlashOrderReturn(BaseModel):
    data: List[SFlashOrderReturn]
    total: int
    
class CreatePackageOrderStatus(BaseModel):
    title: Optional[str]

        
class SPackageOrderStatus(CreatePackageOrderStatus):
    id: int

    class Config:
        orm_mode = True

class PackageOrderStatus(CreatePackageOrderStatus):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResPackageOrderStatus(BaseModel):
    data: List[SPackageOrderStatus]
    total: int
    
class CreateFund(BaseModel):
    zhouqi: Optional[int] = Field(title='属期数字(年+月202401)')
    good_id: Optional[int] = Field(title='商品id')
    order_id: Optional[int] = Field(title='订单id')
    balance: Optional[int] = Field(title='金额')
    register_time: Optional[datetime] = Field(title='创建时间')
    fenpei_time: Optional[datetime] = Field(title='分配时间')
    status: Optional[int] = Field(title='状态(0未分配，1已分配)')

        
class SFund(CreateFund):
    id: int = Field(title='标识id编号')

    class Config:
        orm_mode = True

class Fund(CreateFund):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResFund(BaseModel):
    data: List[SFund]
    total: int
    
class CreateFundFplog(BaseModel):
    zhouqi: Optional[int] = Field(title='属期数字(年+月202401)')
    balance_fen: Optional[int] = Field(title='分红金额')
    balance_total: Optional[int] = Field(title='总金额')
    balance: Optional[int] = Field(title='余额')
    user_id: Optional[int] = Field(title='合伙人id')
    user_phone: Optional[str] = Field(title='电话')
    register_time: Optional[datetime] = Field(title='创建时间')
    user_name: Optional[str] = Field(title='合伙人昵称')
    prom: Optional[int] = Field(title='分红比例除以100')
    user_id_fen: Optional[str] = Field(title='分红时计数的合伙人ID1,2,3')

        
class SFundFplog(CreateFundFplog):
    id: int = Field(title='标识id编号')

    class Config:
        orm_mode = True

class FundFplog(CreateFundFplog):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResFundFplog(BaseModel):
    data: List[SFundFplog]
    total: int
    
class CreateFundPartner(BaseModel):
    zhouqi: Optional[int] = Field(title='属期数字(年+月202401)')
    user_id: Optional[int] = Field(title='合伙人会员id')
    register_time: Optional[datetime] = Field(title='创建时间')
    parent_id: Optional[int] = Field(title='上级合伙人id')

        
class SFundPartner(CreateFundPartner):
    id: int = Field(title='标识id编号')

    class Config:
        orm_mode = True

class FundPartner(CreateFundPartner):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResFundPartner(BaseModel):
    data: List[SFundPartner]
    total: int
    
class CreateFundPond(BaseModel):
    date_num: Optional[str] = Field(title='期id(初级one20250818,高级two20250818,顶级three20250818)')
    stat: Optional[int] = Field(title='是否结算,默认0待结算1已结算')
    balance: Optional[int] = Field(title='金额')
    run_balance: Optional[int] = Field(title='执行金额')
    register_time: Optional[datetime] = Field(title='创建时间')
    end_time: Optional[datetime] = Field(title='截止时间')
    run_time: Optional[datetime] = Field(title='执行时间')
    users: Optional[str] = Field(title='当前达标人(逗号分开的会员id)')
    detail: Optional[str] = Field(title='备注')
    ftype: Optional[int] = Field(title='资金类型:0初级1高级2顶级')
    users_time: Optional[datetime] = Field(title='会员归集时间')

        
class SFundPond(CreateFundPond):
    id: int = Field(title='序号id')

    class Config:
        orm_mode = True

class FundPond(CreateFundPond):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResFundPond(BaseModel):
    data: List[SFundPond]
    total: int
    
class CreateFundPondLog(BaseModel):
    add_balance: Optional[int] = Field(title='增加金额')
    all_balance: Optional[int] = Field(title='资金余额')
    register_time: Optional[datetime] = Field(title='创建时间')
    source_id: Optional[int] = Field(title='来源商品id')
    source_cont: Optional[str] = Field(title='来源备注')

        
class SFundPondLog(CreateFundPondLog):
    id: int = Field(title='序号id')

    class Config:
        orm_mode = True

class FundPondLog(CreateFundPondLog):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResFundPondLog(BaseModel):
    data: List[SFundPondLog]
    total: int
    
class CreateFundRunLog(BaseModel):
    register_time: Optional[datetime] = Field(title='创建时间')
    user_id: Optional[int] = Field(title='用户id')
    user_phone: Optional[str] = Field(title='用户电话')
    weight: Optional[int] = Field(title='当前权重')
    run_balance: Optional[int] = Field(title='执行金额')
    stat: Optional[int] = Field(title='是否成功,默认0成功1失败')

        
class SFundRunLog(CreateFundRunLog):
    id: int = Field(title='序号id')

    class Config:
        orm_mode = True

class FundRunLog(CreateFundRunLog):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResFundRunLog(BaseModel):
    data: List[SFundRunLog]
    total: int
    
class CreateFundWeightLog(BaseModel):
    register_time: Optional[datetime] = Field(title='创建时间')
    user_id: Optional[int] = Field(title='推荐人用户id')
    user_phone: Optional[str] = Field(title='用户电话')
    weight: Optional[int] = Field(title='增加权重')
    all_balance: Optional[int] = Field(title='权重余额')
    add_rec: Optional[int] = Field(title='增加推荐有效人数')
    all_rec: Optional[int] = Field(title='总推荐有效人数')
    source_id: Optional[int] = Field(title='权重来源会员,购买礼包的会员')

        
class SFundWeightLog(CreateFundWeightLog):
    id: int = Field(title='序号id')

    class Config:
        orm_mode = True

class FundWeightLog(CreateFundWeightLog):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResFundWeightLog(BaseModel):
    data: List[SFundWeightLog]
    total: int
    
class CreateFundZqlog(BaseModel):
    zhouqi: Optional[int] = Field(title='属期id')
    balance: Optional[int] = Field(title='分配金额')
    register_time: Optional[datetime] = Field(title='创建时间')
    fenpei_num: Optional[int] = Field(title='分配人数')
    status: Optional[int] = Field(title='分配成功0分配失败1')
    fenpei_users: Optional[str] = Field(title='备注')
    user_id: Optional[int] = Field(title='获奖用户id')
    balance_pro: Optional[float] = Field(title='分配百分比')

        
class SFundZqlog(CreateFundZqlog):
    id: int = Field(title='标识id编号')

    class Config:
        orm_mode = True

class FundZqlog(CreateFundZqlog):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResFundZqlog(BaseModel):
    data: List[SFundZqlog]
    total: int
    
class CreateGood(BaseModel):
    name: Optional[str] = Field(title='产品名称')
    is_flash_sale: Optional[int] = Field(title='是否参加秒杀')
    category_id: Optional[int] = Field(title='大类别ID   关联t_category表')
    type: Optional[int] = Field(title='0:普通商品 1:报单商品')
    num_sale: Optional[int] = Field(title='销量')
    image_url: Optional[str] = Field(title='主图片url')
    priority: Optional[int] = Field(title='优先级  越小越好')
    add_coin: Optional[int] = Field(title='购买后给予多少积分')
    model_id: Optional[int] = Field(title='所属团长id')
    expired_time: Optional[datetime] = Field(title='过期时间')
    parent_good_id: Optional[int] = Field(title='如果是套餐产品，这个是父商品id')
    title: Optional[str] = Field(title='主标题        如糖醋鱼的标题是美食')
    subtitle: Optional[str] = Field(title='副标题')
    stock_cordon: Optional[int] = Field(title='库存警戒线')
    status: Optional[int] = Field(title='0: 下架   1: 上架 ')
    details: Optional[str] = Field(title='商品详情描述')
    supplier_id: Optional[int] = Field(title='供应商id')
    share_ratio: Optional[int] = Field(title='分成比例')
    create_time: Optional[datetime] = Field(title='添加时间')
    last_update_time: Optional[datetime] = Field(title='最后修改时间')
    saleable: Optional[int] = Field(title='0：下架  1：上架')
    click_count: Optional[int] = Field(title='点击量')
    transmit_count: Optional[int] = Field(title='转发量')
    coinable: Optional[int] = Field(title='0:不可以使用优惠券1:可使用')
    price_line: Optional[int] = Field(title='商品划价线')
    introducer_id: Optional[int] = Field(title='介绍人id')
    sell_high: Optional[int] = Field(title='最高售价')
    sell_low: Optional[int] = Field(title='最低售价')
    cost_high: Optional[int] = Field(title='最高成本')
    cost_low: Optional[int] = Field(title='最低成本')
    display: Optional[int] = Field(title='显示位置          1:顶部       0:底部')
    coinable_number: Optional[int] = Field(title='优惠券可用额度')
    is_package: Optional[int]
    fake_owner_name: Optional[str] = Field(title='临时数据   负责人名称')
    fake_owner_phone: Optional[str] = Field(title='临时数据   负责人电话')
    unavailable_date: Optional[str] = Field(title='不可用时间')
    available_time: Optional[str]
    usage_rule: Optional[str]
    refund_rule: Optional[str]
    order_expired_time: Optional[datetime] = Field(title='订单过期时间，用户下单后这个日期会被复制code_expired_time，后期修改不影响已下单过期时间')
    cover_url: Optional[str] = Field(title='封面图片url')
    video_url: Optional[str] = Field(title='视频url')
    is_wholesale: Optional[int] = Field(title='是不是成为批发商商品，0为默认普通产品，1为批发商产品')
    zdyspec: Optional[str] = Field(title='自定义规格')
    sale_type: Optional[int] = Field(title='商品经营类型，0自营，1商家产品')
    admin_id: Optional[int] = Field(title='所属商家管理id')
    admin_audit: Optional[int] = Field(title='商家商品审核状态0未审核1审核通过2未通过')
    admin_info: Optional[str] = Field(title='审核说明')
    video_level: Optional[int] = Field(title='视频分发身份0达人,1店长,2服务商,3分公司')
    video_num: Optional[int] = Field(title='获取合成视频条数')
    is_video: Optional[int] = Field(title='是否视频分发礼包产品,设置为1')
    live_mid_uid: Optional[int] = Field(title='居间人id')
    live_mid_money: Optional[int] = Field(title='居间人收益')

        
class SGood(CreateGood):
    id: int

    class Config:
        orm_mode = True

class Good(CreateGood):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResGood(BaseModel):
    data: List[SGood]
    total: int
    
class CreateGoodCategory(BaseModel):
    title: Optional[str] = Field(title='小类别名称   比如火锅、烧烤')
    general_id: Optional[int] = Field(title='大类id     关联t_category表')

        
class SGoodCategory(CreateGoodCategory):
    id: int

    class Config:
        orm_mode = True

class GoodCategory(CreateGoodCategory):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResGoodCategory(BaseModel):
    data: List[SGoodCategory]
    total: int
    
class CreateGoodImage(BaseModel):
    image: Optional[str] = Field(title='商品图片url')
    good_id: Optional[int] = Field(title='商品id')

        
class SGoodImage(CreateGoodImage):
    id: int

    class Config:
        orm_mode = True

class GoodImage(CreateGoodImage):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResGoodImage(BaseModel):
    data: List[SGoodImage]
    total: int
    
class CreateGoodIntroducer(BaseModel):
    name: Optional[str] = Field(title='介绍人名称')
    phone: Optional[str] = Field(title='介绍人电话')
    address: Optional[str] = Field(title='介绍人住址')
    id_card: Optional[str] = Field(title='介绍人身份证')

        
class SGoodIntroducer(CreateGoodIntroducer):
    id: int

    class Config:
        orm_mode = True

class GoodIntroducer(CreateGoodIntroducer):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResGoodIntroducer(BaseModel):
    data: List[SGoodIntroducer]
    total: int
    
class CreateGoodModel(BaseModel):
    model: Optional[str]

        
class SGoodModel(CreateGoodModel):
    id: int

    class Config:
        orm_mode = True

class GoodModel(CreateGoodModel):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResGoodModel(BaseModel):
    data: List[SGoodModel]
    total: int
    
class CreateGoodOption(BaseModel):
    good_id: Optional[int] = Field(title='商品id')
    good_spec_id: Optional[int] = Field(title='商品规格ID')
    opt_name: Optional[str] = Field(title='选项名称')
    create_time: Optional[datetime] = Field(title='创建时间')
    status: Optional[int] = Field(title='0为正常状态，-1是删除')
    operator_id: Optional[int] = Field(title='操作员ID')

        
class SGoodOption(CreateGoodOption):
    id: int

    class Config:
        orm_mode = True

class GoodOption(CreateGoodOption):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResGoodOption(BaseModel):
    data: List[SGoodOption]
    total: int
    
class CreateGoodPackage(BaseModel):
    number: Optional[str] = Field(title='商品份数')
    price: Optional[str] = Field(title='单价')
    title: Optional[str] = Field(title='商品标题')
    create_time: Optional[datetime] = Field(title='创建时间')
    good_id: Optional[int] = Field(title='商品id')

        
class SGoodPackage(CreateGoodPackage):
    id: int

    class Config:
        orm_mode = True

class GoodPackage(CreateGoodPackage):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResGoodPackage(BaseModel):
    data: List[SGoodPackage]
    total: int
    
class CreateGoodPerson(BaseModel):
    good_id: Optional[int] = Field(title='商品编号')
    person_id: Optional[int] = Field(title='人数id')

        
class SGoodPerson(CreateGoodPerson):
    id: int

    class Config:
        orm_mode = True

class GoodPerson(CreateGoodPerson):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResGoodPerson(BaseModel):
    data: List[SGoodPerson]
    total: int
    
class CreateGoodPersonState(BaseModel):
    title: Optional[str] = Field(title='使用人数')

        
class SGoodPersonState(CreateGoodPersonState):
    id: int

    class Config:
        orm_mode = True

class GoodPersonState(CreateGoodPersonState):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResGoodPersonState(BaseModel):
    data: List[SGoodPersonState]
    total: int
    
class CreateGoodPriority(BaseModel):
    title: Optional[str]

        
class SGoodPriority(CreateGoodPriority):
    id: int

    class Config:
        orm_mode = True

class GoodPriority(CreateGoodPriority):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResGoodPriority(BaseModel):
    data: List[SGoodPriority]
    total: int
    
class CreateGoodRule(BaseModel):
    good_id: Optional[int] = Field(title='商品id')
    create_time: Optional[datetime] = Field(title='创建时间')
    validate_day: Optional[str] = Field(title='有效期    例如： 2023.04.19   至  2024.04.19')
    unuseful_day: Optional[str] = Field(title='不可用日期     例如： 2023.05.01 至 2024.05.07')
    useful_time: Optional[str] = Field(title='可用时间      例如：24小时可用       14:00-20:00可用等')
    use_rule: Optional[str] = Field(title='使用规则')
    return_rule: Optional[str] = Field(title='退货规则')
    room: Optional[int] = Field(title='0:不可使用包间     1：可使用包间')
    title: Optional[str]
    value: Optional[str]

        
class SGoodRule(CreateGoodRule):
    id: int

    class Config:
        orm_mode = True

class GoodRule(CreateGoodRule):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResGoodRule(BaseModel):
    data: List[SGoodRule]
    total: int
    
class CreateGoodSpec(BaseModel):
    good_id: Optional[int] = Field(title='商品id')
    price: Optional[int] = Field(title='售价')
    cost: Optional[int] = Field(title='成本')
    value: Optional[str] = Field(title='规格的值    例如：糖醋里脊的甜口、酸口')
    stock: Optional[int] = Field(title='库存')
    price_line: Optional[int] = Field(title='划价线')
    image: Optional[str] = Field(title='图片url')
    is_sub_good: Optional[int]
    num_sale: Optional[int] = Field(title='销量')
    parent_fee: Optional[int] = Field(title='分层奖，上一级的奖励')
    top_fee: Optional[int] = Field(title='见点奖，第一高级会员分成')
    recommender_fee: Optional[int] = Field(title='售出奖，推荐人的奖励')
    supplier_fee: Optional[int] = Field(title='供货收益')
    lower_num_people: Optional[int] = Field(title='人数下限')
    upper_num_people: Optional[int] = Field(title='人数上限')
    room: Optional[str] = Field(title='包间')
    post: Optional[str]
    status: Optional[int] = Field(title='0: 下架   1: 上架 ')
    share_fee: Optional[int] = Field(title='分享商品收益')
    is_default: Optional[int] = Field(title='是否默认规格')
    spec_num: Optional[str] = Field(title='商品规格编号')
    profit: Optional[int] = Field(title='产品利润')
    eqlevel_fee: Optional[int] = Field(title='平级奖 直推关系下见点收益的推荐人收益')
    wholesale_fee: Optional[int] = Field(title='批发商返利')
    wholesale_price: Optional[int] = Field(title='批发价')
    purchase_price: Optional[int] = Field(title='进价')
    freight_txt: Optional[int] = Field(title='运费')
    taxation_txt: Optional[int] = Field(title='税费')
    recommender2_fee: Optional[int] = Field(title='额外的推荐人奖励')
    kg_num: Optional[int] = Field(title='商品克重（克）')
    is_pifa: Optional[int] = Field(title='是否批发商品,默认0,1为是')
    is_single: Optional[int] = Field(title='是否单份代卖,默认0单份,1为整份')
    pifa_num: Optional[int] = Field(title='单份批发商品数量')
    unitprice_diff: Optional[int] = Field(title='单份批发商品差价')
    random_fee: Optional[int] = Field(title='给批发商的随机分润')
    tuan_uid: Optional[int] = Field(title='团长分润id')
    retuan_uid: Optional[int] = Field(title='上级团长分润id')
    tuan_fee: Optional[int] = Field(title='团长分润')
    retuan_fee: Optional[int] = Field(title='上级团长分润')

        
class SGoodSpec(CreateGoodSpec):
    id: int

    class Config:
        orm_mode = True

class GoodSpec(CreateGoodSpec):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResGoodSpec(BaseModel):
    data: List[SGoodSpec]
    total: int
    
class CreateGoodSpecCombo(BaseModel):
    good_spec_id: Optional[int]
    value: Optional[str]
    price: Optional[int]
    amount: Optional[str] = Field(title='数量')

        
class SGoodSpecCombo(CreateGoodSpecCombo):
    id: int

    class Config:
        orm_mode = True

class GoodSpecCombo(CreateGoodSpecCombo):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResGoodSpecCombo(BaseModel):
    data: List[SGoodSpecCombo]
    total: int
    
class CreateGoodSpecDetail(BaseModel):
    good_spec_id: Optional[int]
    detail: Optional[str]

        
class SGoodSpecDetail(CreateGoodSpecDetail):
    id: int

    class Config:
        orm_mode = True

class GoodSpecDetail(CreateGoodSpecDetail):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResGoodSpecDetail(BaseModel):
    data: List[SGoodSpecDetail]
    total: int
    
class CreateGoodSpecImage(BaseModel):
    spec_id: Optional[int] = Field(title='规格id')
    image: Optional[str] = Field(title='图片url')

        
class SGoodSpecImage(CreateGoodSpecImage):
    id: int

    class Config:
        orm_mode = True

class GoodSpecImage(CreateGoodSpecImage):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResGoodSpecImage(BaseModel):
    data: List[SGoodSpecImage]
    total: int
    
class CreateGoodStore(BaseModel):
    good_id: Optional[int]
    store_id: Optional[int]

        
class SGoodStore(CreateGoodStore):
    id: int

    class Config:
        orm_mode = True

class GoodStore(CreateGoodStore):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResGoodStore(BaseModel):
    data: List[SGoodStore]
    total: int
    
class CreateGoodText(BaseModel):
    good_id: Optional[int] = Field(title='商品id')
    description: Optional[str] = Field(title='图文详情   图片和文字放在一起')
    create_time: Optional[datetime] = Field(title='创建时间')

        
class SGoodText(CreateGoodText):
    id: int

    class Config:
        orm_mode = True

class GoodText(CreateGoodText):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResGoodText(BaseModel):
    data: List[SGoodText]
    total: int
    
class CreateGoodType(BaseModel):
    type: Optional[str]

        
class SGoodType(CreateGoodType):
    id: int

    class Config:
        orm_mode = True

class GoodType(CreateGoodType):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResGoodType(BaseModel):
    data: List[SGoodType]
    total: int
    
class CreateGroupsir(BaseModel):
    user_id: Optional[int] = Field(title='关联t_user表id')
    parent_id: Optional[int] = Field(title='0:表示团长，非0表示下级成员')
    register_time: Optional[datetime] = Field(title='成团时间和入团')
    status: Optional[int] = Field(title='0: 启用   1: 暂停  -1：出团或解散')
    is_empower: Optional[int] = Field(title='0: 未授权   1:已授权（可以使用所有商品秒杀包）')
    notes: Optional[str] = Field(title='团员备注')

        
class SGroupsir(CreateGroupsir):
    id: int = Field(title='团长id')

    class Config:
        orm_mode = True

class Groupsir(CreateGroupsir):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResGroupsir(BaseModel):
    data: List[SGroupsir]
    total: int
    
class CreateGroupsirlog(BaseModel):
    register_time: Optional[datetime] = Field(title='创建时间')
    user_id: Optional[int] = Field(title='变动账号id')
    groupsir_id: Optional[int] = Field(title='团长id')
    admin_id: Optional[int] = Field(title='操作员id')
    logtype: Optional[str] = Field(title='变动类型：入团、出团、建团、消团')

        
class SGroupsirlog(CreateGroupsirlog):
    id: int

    class Config:
        orm_mode = True

class Groupsirlog(CreateGroupsirlog):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResGroupsirlog(BaseModel):
    data: List[SGroupsirlog]
    total: int
    
class CreateLevel(BaseModel):
    title: Optional[str]

        
class SLevel(CreateLevel):
    id: int

    class Config:
        orm_mode = True

class Level(CreateLevel):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResLevel(BaseModel):
    data: List[SLevel]
    total: int
    
class CreateLockBalance(BaseModel):
    user_id: Optional[int] = Field(title='外键')
    change: Optional[int] = Field(title='变动')
    lock_balance: Optional[int] = Field(title='锁定金额')
    type: Optional[str] = Field(title='类型')
    description: Optional[str] = Field(title='描述')
    create_time: Optional[datetime] = Field(title='创建时间')
    out_trade_no: Optional[str]

        
class SLockBalance(CreateLockBalance):
    id: int

    class Config:
        orm_mode = True

class LockBalance(CreateLockBalance):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResLockBalance(BaseModel):
    data: List[SLockBalance]
    total: int
    
class CreateModel(BaseModel):
    product_id: Optional[int]

        
class SModel(CreateModel):
    id: int

    class Config:
        orm_mode = True

class Model(CreateModel):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResModel(BaseModel):
    data: List[SModel]
    total: int
    
class CreateNotice(BaseModel):
    user_ids: Optional[str] = Field(title='通知用户，逗号分隔的用户id;值为all则表示所有用户')
    type: Optional[str] = Field(title='类别：系统通知、收益通知')
    title: Optional[str] = Field(title='标题')
    description: Optional[str] = Field(title='通知内容')
    register_time: Optional[datetime] = Field(title='通知时间')
    status: Optional[int] = Field(title='0: 正常  -1: 删除')

        
class SNotice(CreateNotice):
    id: int

    class Config:
        orm_mode = True

class Notice(CreateNotice):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResNotice(BaseModel):
    data: List[SNotice]
    total: int
    
class CreateOrder(BaseModel):
    good_id: Optional[int] = Field(title='商品id')
    paider_id: Optional[int] = Field(title='付款人id')
    sale_price: Optional[int] = Field(title='售价      记录客户购买时的商品价格（因为价格可能变动）')
    cost_price: Optional[int] = Field(title='成本       记录客户购买时的商品成本（因为成本可能变动）')
    create_time: Optional[datetime] = Field(title='创建时间    与支付时间有本质区别')
    paid_time: Optional[datetime] = Field(title='支付时间')
    status_id: Optional[int] = Field(title='状态id:0待付款、1待发货、2待收货、3已完成')
    number: Optional[int] = Field(title='商品数量')
    consignee_address: Optional[str] = Field(title='收货人地址')
    consignee_phone: Optional[str] = Field(title='收货人联系电话')
    store_id: Optional[int] = Field(title='店铺id')
    paid_amount: Optional[int] = Field(title='实际第三方支付的金额     用于标记除客户账户以外支付的金额（比如微信、银行卡)')
    delivery_fee: Optional[int] = Field(title='运费金额')
    spec_id: Optional[int] = Field(title='规格编号')
    paid_coin: Optional[int] = Field(title='实际支付的优惠券用于标记客户账户内支付的优惠券')
    delivery_track_code: Optional[str] = Field(title='第三方物流单号  比如顺丰的单号')
    paid_channel_id: Optional[int] = Field(title='第三方支付渠道    比如微信支付  银行卡支付等')
    consignee_name: Optional[str] = Field(title='收货人名称')
    delivery_time: Optional[datetime] = Field(title='发货时间')
    good_name: Optional[str] = Field(title='商品名称    记录客户购买时的商品名称（因为名称可能变动）')
    paid_track_code: Optional[str] = Field(title='第三方支付流水号    比如微信支付提供的支付编码')
    paider_name: Optional[str] = Field(title='付款人姓名')
    paider_phone: Optional[str] = Field(title='付款人电话')
    paider_address: Optional[str] = Field(title='付款人地址')
    supplier_id: Optional[int] = Field(title='商家id')
    paid_balance: Optional[int] = Field(title='实际支付的余额         用于标记客户账户内支付的余额')
    paid_lock_balance: Optional[int] = Field(title='实际支付的锁定额        用于标记客户账户内支付的锁定额')
    delivery_company: Optional[str] = Field(title='第三方物流公司   比如圆通、顺丰等')
    complete_time: Optional[datetime] = Field(title='订单完结时间')
    use_balance: Optional[int] = Field(title='是否使用余额')
    use_coin: Optional[int] = Field(title='是否使用积分')
    consignee_province: Optional[str]
    consignee_description: Optional[str]
    consignee_city: Optional[str]
    consignee_area: Optional[str]
    consignee_street: Optional[str]
    out_trade_no: Optional[str] = Field(title='商户单号')
    code: Optional[str] = Field(title='虚拟消费券的code')
    code_expired_time: Optional[datetime] = Field(title='虚拟消费券的过期时间')
    is_display: Optional[int] = Field(title='是否可以展示')
    recommender_id: Optional[int] = Field(title='推荐人Id')
    detail: Optional[str] = Field(title='订单备注,+=更新')
    is_assign_income: Optional[int] = Field(title='是否分配收益')
    parent_uid: Optional[int] = Field(title='层级收益人id')
    top_uid: Optional[int] = Field(title='顶级收益人id')
    invited_uid: Optional[int] = Field(title='直推收益人id')
    supplier_uid: Optional[int] = Field(title='供货介绍收益人id')
    good_option_id: Optional[int] = Field(title='商品选项id')
    good_option_name: Optional[str] = Field(title='选项名称')
    user_detail: Optional[str] = Field(title='用户下单信息备注')
    zdyspec: Optional[str] = Field(title='用户所选自定义规格')
    wholesale_id: Optional[int] = Field(title='成为批发商类型的id')
    tuan_uid: Optional[int] = Field(title='团长分润id')
    zdyspec_good: Optional[str] = Field(title='选规格后商品规格')
    zdyspec_good_index: Optional[str] = Field(title='用户所选自定义规格库存')
    isfirst: Optional[int] = Field(title='是否首单礼包订单,默认0非首单礼包订单')
    detail_tut: Optional[str] = Field(title='订单教程备注')
    is_video: Optional[int] = Field(title='是否视频分发礼包产品订单,设置为1')
    act_uid: Optional[int] = Field(title='激活收益人id卡密所属人')
    invited_two_uid: Optional[int] = Field(title='间推收益人id')
    share_invited_uid: Optional[int] = Field(title='分享推荐收益人id')
    share_invited_two_uid: Optional[int] = Field(title='分享间推收益人id')
    retuan_uid: Optional[int] = Field(title='间推团长分润id')
    is_user_price: Optional[int] = Field(title='是否会员价订单,默认0为售价')
    live_mid_uid: Optional[int] = Field(title='居间人id')
    live_mid_money: Optional[int] = Field(title='居间人收益')
    ad_id: Optional[int] = Field(title='来源广告id')
    sh_agent_id: Optional[int] = Field(title='市代id')

        
class SOrder(CreateOrder):
    id: int = Field(title='订单id')

    class Config:
        orm_mode = True

class Order(CreateOrder):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResOrder(BaseModel):
    data: List[SOrder]
    total: int
    
class CreateOrderBatch(BaseModel):
    create_time: Optional[datetime]

        
class SOrderBatch(CreateOrderBatch):
    id: int

    class Config:
        orm_mode = True

class OrderBatch(CreateOrderBatch):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResOrderBatch(BaseModel):
    data: List[SOrderBatch]
    total: int
    
class CreateOrderCheck(BaseModel):
    order_id: Optional[int] = Field(title='订单id')
    check_num: Optional[int] = Field(title='核销数量')
    check_time: Optional[datetime] = Field(title='核销时间')
    worker_id: Optional[int] = Field(title='核销人id，对应店铺的人员')
    check_amount: Optional[int] = Field(title='核销金额')

        
class SOrderCheck(CreateOrderCheck):
    id: int

    class Config:
        orm_mode = True

class OrderCheck(CreateOrderCheck):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResOrderCheck(BaseModel):
    data: List[SOrderCheck]
    total: int
    
class CreateOrderReturn(BaseModel):
    returner_name: Optional[str] = Field(title='退款人姓名   对应订单表的付款人')
    returner_phone: Optional[str] = Field(title='退款人电话   对应订单表的付款人')
    returner_address: Optional[str] = Field(title='退款人地址   对应订单表的付款人')
    delivery_fee: Optional[int] = Field(title='退货运费')
    return_amount: Optional[int] = Field(title='第三方支付退款额度    比如退还微信10元')
    return_submit_time: Optional[datetime] = Field(title='退货申请时间')
    return_reason: Optional[str] = Field(title='退货原因')
    order_id: Optional[int] = Field(title='订单编号     关联订单表')
    good_id: Optional[int] = Field(title='商品id')
    return_num: Optional[int] = Field(title='退货商品数量')
    store_id: Optional[int] = Field(title='店铺id')
    return_delivery_track_code: Optional[str] = Field(title='第三方退货物流单号')
    status_id: Optional[int] = Field(title='状态id     对应退款协商中、未处理、已退货')
    consignee_name: Optional[str] = Field(title='收货人姓名')
    consignee_phone: Optional[str] = Field(title='收货人电话')
    consignee_address: Optional[str] = Field(title='收货人地址')
    return_balance: Optional[int] = Field(title='客户账户余额退还额度')
    return_lock_balance: Optional[int] = Field(title='客户账户锁定额退还额度')
    return_coin: Optional[int] = Field(title='客户账户积分退还额度')
    return_delivery_company: Optional[str] = Field(title='第三方物流公司')
    return_paid_track_code: Optional[str] = Field(title='第三方退款流水号')

        
class SOrderReturn(CreateOrderReturn):
    id: int = Field(title='退货编号')

    class Config:
        orm_mode = True

class OrderReturn(CreateOrderReturn):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResOrderReturn(BaseModel):
    data: List[SOrderReturn]
    total: int
    
class CreateOrderReturnState(BaseModel):
    state: Optional[str] = Field(title='退换货状态')

        
class SOrderReturnState(CreateOrderReturnState):
    id: int

    class Config:
        orm_mode = True

class OrderReturnState(CreateOrderReturnState):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResOrderReturnState(BaseModel):
    data: List[SOrderReturnState]
    total: int
    
class CreateOrderReturnType(BaseModel):
    type: Optional[str] = Field(title='类型')

        
class SOrderReturnType(CreateOrderReturnType):
    id: int

    class Config:
        orm_mode = True

class OrderReturnType(CreateOrderReturnType):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResOrderReturnType(BaseModel):
    data: List[SOrderReturnType]
    total: int
    
class CreateOrderSource(BaseModel):
    order_id: Optional[int] = Field(title='订单id')
    source_id: Optional[int] = Field(title='订单来源，来再t_flash_order.id，如果是空或者-1表示平台')
    amount: Optional[int] = Field(title='商品数量')
    create_time: Optional[datetime] = Field(title='创建时间')
    order_user_id: Optional[int] = Field(title='订单购买用户id')
    package_user_id: Optional[int] = Field(title='秒杀包用户id')

        
class SOrderSource(CreateOrderSource):
    id: int

    class Config:
        orm_mode = True

class OrderSource(CreateOrderSource):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResOrderSource(BaseModel):
    data: List[SOrderSource]
    total: int
    
class CreateOrderState(BaseModel):
    state: Optional[str] = Field(title='订单状态')
    belong: Optional[str] = Field(title='所属订单类别   比如发货  退货')

        
class SOrderState(CreateOrderState):
    id: int

    class Config:
        orm_mode = True

class OrderState(CreateOrderState):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResOrderState(BaseModel):
    data: List[SOrderState]
    total: int
    
class CreatePackage(BaseModel):
    good_id: Optional[int] = Field(title='产品id')
    amount: Optional[int] = Field(title='份数;the number of good in one amount一个包包含的产品的数量')
    flash_sale_price: Optional[int] = Field(title='秒杀价格;in cent,秒杀价格')
    num: Optional[int] = Field(title='包个数;一共有多少个包')
    stock: Optional[int] = Field(title='剩余包数量')
    seller_id: Optional[int] = Field(title='发布商品的卖家，如果id为空或者0，则为官方卖家')
    spec_id: Optional[int] = Field(title='规格id')
    share_fee: Optional[int] = Field(title='让利金额')
    status: Optional[int] = Field(title='状态：-1删除, 默认0/null正常')
    devide_cost: Optional[int] = Field(title='分润成本，商品规格分润之 和')

        
class SPackage(CreatePackage):
    id: int

    class Config:
        orm_mode = True

class Package(CreatePackage):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResPackage(BaseModel):
    data: List[SPackage]
    total: int
    
class CreatePackageExpress(BaseModel):
    flash_order_id: Optional[int]
    status: Optional[int] = Field(title='1: 申请中  2:  已发货  3: 拒绝发货退款  4：已签收  5:未使用  6:已使用')
    address_id: Optional[int] = Field(title='邮寄地址id')
    amount: Optional[int] = Field(title='邮寄数量')
    express_num: Optional[str] = Field(title='物流号')
    apply_time: Optional[datetime] = Field(title='申请发货时间')
    delivery_time: Optional[datetime] = Field(title='发货时间')
    complete_time: Optional[datetime] = Field(title='签收或完成时间')
    detail: Optional[str] = Field(title='订单备注,+=更新')

        
class SPackageExpress(CreatePackageExpress):
    id: int

    class Config:
        orm_mode = True

class PackageExpress(CreatePackageExpress):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResPackageExpress(BaseModel):
    data: List[SPackageExpress]
    total: int
    
class CreatePackageExpressStatus(BaseModel):
    title: Optional[str]

        
class SPackageExpressStatus(CreatePackageExpressStatus):
    id: int

    class Config:
        orm_mode = True

class PackageExpressStatus(CreatePackageExpressStatus):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResPackageExpressStatus(BaseModel):
    data: List[SPackageExpressStatus]
    total: int
    
class CreatePackageTime(BaseModel):
    start_time: Optional[int] = Field(title='开始时间;9*3600表示9:00')
    end_time: Optional[int] = Field(title='结束时间;以秒为单位')

        
class SPackageTime(CreatePackageTime):
    id: int

    class Config:
        orm_mode = True

class PackageTime(CreatePackageTime):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResPackageTime(BaseModel):
    data: List[SPackageTime]
    total: int
    
class CreatePackageTimePair(BaseModel):
    package_id: Optional[int]
    package_time_id: Optional[int]
    status: Optional[int] = Field(title='状态; 0: 未激活, 1: 激活')
    package_num: Optional[int] = Field(title='此时段秒杀包库存')

        
class SPackageTimePair(CreatePackageTimePair):
    id: int

    class Config:
        orm_mode = True

class PackageTimePair(CreatePackageTimePair):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResPackageTimePair(BaseModel):
    data: List[SPackageTimePair]
    total: int
    
class CreatePayChannel(BaseModel):
    type: Optional[str] = Field(title='支付方式')

        
class SPayChannel(CreatePayChannel):
    id: int

    class Config:
        orm_mode = True

class PayChannel(CreatePayChannel):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResPayChannel(BaseModel):
    data: List[SPayChannel]
    total: int
    
class CreatePlatformLaw(BaseModel):
    create_time: Optional[datetime] = Field(title='创建时间')
    admin_id: Optional[int] = Field(title='操作员id')
    law: Optional[str] = Field(title='法律文本 用户协议')
    privacy: Optional[str] = Field(title='法律文本 用户协议')
    purchase: Optional[str] = Field(title='法律文本 用户协议')
    flash_law: Optional[str] = Field(title='法律文本 用户协议')
    withdraw_law: Optional[str] = Field(title='法律文本 用户协议')

        
class SPlatformLaw(CreatePlatformLaw):
    id: int

    class Config:
        orm_mode = True

class PlatformLaw(CreatePlatformLaw):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResPlatformLaw(BaseModel):
    data: List[SPlatformLaw]
    total: int
    
class CreatePlatformNotice(BaseModel):
    title: Optional[str] = Field(title='通知内容')
    create_time: Optional[datetime] = Field(title='创建时间')
    admin_id: Optional[int] = Field(title='添加人id    对应哪个管理员')

        
class SPlatformNotice(CreatePlatformNotice):
    id: int

    class Config:
        orm_mode = True

class PlatformNotice(CreatePlatformNotice):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResPlatformNotice(BaseModel):
    data: List[SPlatformNotice]
    total: int
    
class CreatePoster(BaseModel):
    user_id: Optional[int] = Field(title='用户id')
    poster_url: Optional[str] = Field(title='海报文件地址')
    status: Optional[str] = Field(title='状态')
    description: Optional[str] = Field(title='描述')
    create_time: Optional[datetime] = Field(title='创建时间')

        
class SPoster(CreatePoster):
    id: int

    class Config:
        orm_mode = True

class Poster(CreatePoster):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResPoster(BaseModel):
    data: List[SPoster]
    total: int
    
class CreatePrize(BaseModel):
    user_id: Optional[int] = Field(title='会员id')
    create_time: Optional[datetime] = Field(title='创建时间')
    status: Optional[int] = Field(title='奖励值')

        
class SPrize(CreatePrize):
    id: int

    class Config:
        orm_mode = True

class Prize(CreatePrize):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResPrize(BaseModel):
    data: List[SPrize]
    total: int
    
class CreateRandompro(BaseModel):
    register_time: Optional[datetime] = Field(title='创建时间')
    pro_oneid: Optional[int] = Field(title='收益人id')
    pro_twoid: Optional[int] = Field(title='分成人id')
    pro_price: Optional[int] = Field(title='分成价格')
    pro_num: Optional[float] = Field(title='分成比例')
    pro_balance: Optional[int] = Field(title='分成获得额')
    order_id: Optional[int] = Field(title='订单id')
    out_trade_no: Optional[str] = Field(title='商户单号')
    details: Optional[str] = Field(title='备注字段')

        
class SRandompro(CreateRandompro):
    id: int

    class Config:
        orm_mode = True

class Randompro(CreateRandompro):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResRandompro(BaseModel):
    data: List[SRandompro]
    total: int
    
class CreateRoomContributelog(BaseModel):
    room_id: Optional[int] = Field(title='房间id')
    contribute_val: Optional[int] = Field(title='贡献值额度')
    user_id: Optional[int] = Field(title='受益人id')
    source_id: Optional[int] = Field(title='来源人id')
    register_time: Optional[datetime] = Field(title='创建时间')

        
class SRoomContributelog(CreateRoomContributelog):
    id: int = Field(title='标识id编号')

    class Config:
        orm_mode = True

class RoomContributelog(CreateRoomContributelog):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResRoomContributelog(BaseModel):
    data: List[SRoomContributelog]
    total: int
    
class CreateRoomgold(BaseModel):
    level: Optional[int] = Field(title='房间级别')
    register_time: Optional[datetime] = Field(title='注册时间')
    start_time: Optional[datetime] = Field(title='开始时间')
    end_time: Optional[datetime] = Field(title='结束时间')
    status_val: Optional[int] = Field(title='房间状态0:默认  1:进行中 2已结束')
    balance: Optional[int] = Field(title='奖金金额')
    partner_id: Optional[int] = Field(title='分裂时记录上级房间id')
    position_one: Optional[int] = Field(title='位置1')
    contribute_one: Optional[int] = Field(title='位置1的贡献值')
    position_two: Optional[int] = Field(title='位置2')
    contribute_two: Optional[int] = Field(title='位置2的贡献值')
    position_three: Optional[int] = Field(title='位置3')
    contribute_three: Optional[int] = Field(title='位置3的贡献值')
    position_four: Optional[int] = Field(title='位置4')
    contribute_four: Optional[int] = Field(title='位置4的贡献值')
    position_five: Optional[int] = Field(title='位置5')
    contribute_five: Optional[int] = Field(title='位置5的贡献值')
    position_six: Optional[int] = Field(title='位置6')
    contribute_six: Optional[int] = Field(title='位置6的贡献值')
    position_seven: Optional[int] = Field(title='位置7')
    contribute_seven: Optional[int] = Field(title='位置7的贡献值')
    position_one_time: Optional[datetime] = Field(title='位置一加入时间')
    position_two_time: Optional[datetime] = Field(title='位置二加入时间')
    position_three_time: Optional[datetime] = Field(title='位置三加入时间')
    position_four_time: Optional[datetime] = Field(title='位置四加入时间')
    position_five_time: Optional[datetime] = Field(title='位置五加入时间')
    position_six_time: Optional[datetime] = Field(title='位置六加入时间')
    position_seven_time: Optional[datetime] = Field(title='位置七加入时间')

        
class SRoomgold(CreateRoomgold):
    id: int

    class Config:
        orm_mode = True

class Roomgold(CreateRoomgold):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResRoomgold(BaseModel):
    data: List[SRoomgold]
    total: int
    
class CreateSdGuest(BaseModel):
    user_id: Optional[int] = Field(title='小程序会员id')
    topic_id: Optional[int] = Field(title='主题id')
    user_name: Optional[str] = Field(title='顾客姓名')
    register_time: Optional[datetime] = Field(title='创建时间')
    phone: Optional[str] = Field(title='电话')
    user_num: Optional[int] = Field(title='报名人数')
    price: Optional[int] = Field(title='每人单价')
    total: Optional[int] = Field(title='报名总额')
    status: Optional[int] = Field(title='报名状态,0下单未支付,1下单已支付,2报名成功')
    short_var1: Optional[str] = Field(title='短文1')
    short_var2: Optional[str] = Field(title='短文2')
    short_var3: Optional[str] = Field(title='短文3')
    short_var4: Optional[str] = Field(title='短文4')
    short_var5: Optional[str] = Field(title='短文5')
    short_var6: Optional[str] = Field(title='短文6')
    short_var7: Optional[str] = Field(title='短文7')
    short_var8: Optional[str] = Field(title='短文8')
    short_var9: Optional[str] = Field(title='短文9')

        
class SSdGuest(CreateSdGuest):
    id: int

    class Config:
        orm_mode = True

class SdGuest(CreateSdGuest):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResSdGuest(BaseModel):
    data: List[SSdGuest]
    total: int
    
class CreateSdTopic(BaseModel):
    tp_name: Optional[str] = Field(title='报名主题名称')
    register_time: Optional[datetime] = Field(title='创建时间')
    cover_url: Optional[str] = Field(title='封面图片url')
    reg_num: Optional[int] = Field(title='报名人数')
    details: Optional[str] = Field(title='主题详情描述')
    reg_field: Optional[str] = Field(title='报名字段')
    reg_status: Optional[int] = Field(title='是否收费,0免费,1收费')
    price: Optional[int] = Field(title='收费金额（每人）')
    status: Optional[int] = Field(title='产品状态,0正常,1禁用')

        
class SSdTopic(CreateSdTopic):
    id: int

    class Config:
        orm_mode = True

class SdTopic(CreateSdTopic):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResSdTopic(BaseModel):
    data: List[SSdTopic]
    total: int
    
class CreateSetting(BaseModel):
    recommend_num: Optional[int] = Field(title='定义推荐系升级人数')
    flash_order_income: Optional[float] = Field(title='定义秒杀产品24小时停留收益比千分之')
    tuan_order_income: Optional[float] = Field(title='定义团长秒杀产品收益比（千分之）')
    flash_order_max: Optional[int] = Field(title='秒杀用户持单量限制(未完成出售订单)')
    flash_order_money_max: Optional[int] = Field(title='秒杀用户持单总金额限制(未完成出售订单)')
    flash_order_active_user: Optional[int] = Field(title='秒杀并支付多少单，普通会员晋升活跃会员')
    consume_money_active_user: Optional[int] = Field(title='完成商品订单达到指定额度，普通会员晋升活跃会员')
    many_high_user: Optional[int] = Field(title='直推多少个活跃会员，晋升高级会员')
    many_top_user: Optional[int] = Field(title='直推多少个高级会员，晋升顶级会员')
    flash_order_income_retio: Optional[float] = Field(title='秒杀人退货收益比（千分之）')
    flash_order_income_layer: Optional[float] = Field(title='秒杀人退货层级收益比（百分之）')
    flash_order_income_toper: Optional[float] = Field(title='秒杀人退货顶级收益比(百分比)')
    flash_order_income_groupsir: Optional[float] = Field(title='秒杀人退货团长收益比(百分比)')
    flash_order_owner_times: Optional[int] = Field(title='秒杀包持有人退货时间限制（小时）')
    parent_user_limit: Optional[int] = Field(title='推广人升级顶级时，留给原上级的人数')
    flash_order_income_subsidy: Optional[int] = Field(title='团队补贴,秒杀的退款收益， 给直接推荐人 的一份')
    random_proportion: Optional[float] = Field(title='定义批发商随机分成比例益比（百分之）')
    random_max: Optional[int] = Field(title='定义批发商随机分成最大分配次数')
    random_low: Optional[int] = Field(title='定义批发商随机分成最小分配次数')
    ws1_proportion: Optional[float] = Field(title='wholesale1批发商随机分成比例益比（百分之）')
    ws2_proportion: Optional[float] = Field(title='wholesale2批发商随机分成比例益比（百分之）')
    ws3_proportion: Optional[float] = Field(title='wholesale3批发商随机分成比例益比（百分之）')

        
class SSetting(CreateSetting):
    id: int = Field(title='标识id，修改时从1开始对应recommend_num之后的字段')

    class Config:
        orm_mode = True

class Setting(CreateSetting):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResSetting(BaseModel):
    data: List[SSetting]
    total: int
    
class CreateShConsumption(BaseModel):
    register_time: Optional[datetime] = Field(title='创建时间')
    pro_name: Optional[str] = Field(title='消费产品名称')
    balance: Optional[int] = Field(title='消费金额')
    shop_id: Optional[int] = Field(title='店铺id')
    pinpai_id: Optional[int] = Field(title='品牌id')
    manager_id: Optional[int] = Field(title='操作员id')
    user_id: Optional[int] = Field(title='消费会员id')
    shareuser_id: Optional[int] = Field(title='分成会员id')
    shareuser_balance: Optional[int] = Field(title='分成会员获得金额')
    pro_id: Optional[int] = Field(title='消费产品ID')
    user_phone: Optional[str] = Field(title='消费者电话')
    user_name: Optional[str] = Field(title='消费者姓名')
    lbalance: Optional[int] = Field(title='余额')
    lgivefee: Optional[int] = Field(title='增额')
    lgivebalance: Optional[int] = Field(title='已分配额')
    lgivetarget: Optional[int] = Field(title='可分配额')
    cons_type: Optional[int] = Field(title='消费类型,0储值消费,1第三方消费')

        
class SShConsumption(CreateShConsumption):
    id: int

    class Config:
        orm_mode = True

class ShConsumption(CreateShConsumption):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResShConsumption(BaseModel):
    data: List[SShConsumption]
    total: int
    
class CreateShCzyushe(BaseModel):
    register_time: Optional[datetime] = Field(title='创建时间')
    yushe_name: Optional[str] = Field(title='产品名称')
    balance: Optional[int] = Field(title='余额')
    givefee: Optional[int] = Field(title='增额')
    givetarget: Optional[int] = Field(title='可分配额')
    shop_id: Optional[int] = Field(title='店铺id')
    pinpai_id: Optional[int] = Field(title='品牌id')
    status: Optional[int] = Field(title='产品状态,0正常,1禁用')

        
class SShCzyushe(CreateShCzyushe):
    id: int

    class Config:
        orm_mode = True

class ShCzyushe(CreateShCzyushe):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResShCzyushe(BaseModel):
    data: List[SShCzyushe]
    total: int
    
class CreateShProduct(BaseModel):
    register_time: Optional[datetime] = Field(title='创建时间')
    pro_name: Optional[str] = Field(title='产品名称')
    price: Optional[int] = Field(title='产品价格（单位分）')
    shop_id: Optional[int] = Field(title='店铺id')
    pinpai_id: Optional[int] = Field(title='品牌id')
    status: Optional[int] = Field(title='产品状态,0正常,1禁用')

        
class SShProduct(CreateShProduct):
    id: int

    class Config:
        orm_mode = True

class ShProduct(CreateShProduct):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResShProduct(BaseModel):
    data: List[SShProduct]
    total: int
    
class CreateShRose(BaseModel):
    register_time: Optional[datetime] = Field(title='创建时间')
    shop_id: Optional[int] = Field(title='店铺id')
    pinpai_id: Optional[int] = Field(title='品牌id')
    rose_name: Optional[str] = Field(title='角色名称')
    status: Optional[int] = Field(title='商家状态,0正常,1禁用')

        
class SShRose(CreateShRose):
    id: int

    class Config:
        orm_mode = True

class ShRose(CreateShRose):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResShRose(BaseModel):
    data: List[SShRose]
    total: int
    
class CreateShShop(BaseModel):
    register_time: Optional[datetime] = Field(title='创建时间')
    shop_name: Optional[str] = Field(title='品牌/店铺名称')
    phone: Optional[str] = Field(title='电话')
    user_name: Optional[str] = Field(title='用户名')
    user_pass: Optional[str] = Field(title='密码')
    province: Optional[str] = Field(title='省份')
    city: Optional[str] = Field(title='城市')
    area: Optional[str] = Field(title='区域')
    street: Optional[str] = Field(title='街道')
    address: Optional[str] = Field(title='详细地址')
    status: Optional[int] = Field(title='商家状态,0正常,1注销')
    type: Optional[int] = Field(title='商家类型;   0: 品牌  1:商家')
    parent_id: Optional[int] = Field(title='上级品牌id')
    shop_id: Optional[int] = Field(title='用户所属店铺id')
    rose_id: Optional[int] = Field(title='角色id')
    latitude: Optional[float] = Field(title='纬度地区')
    longitude: Optional[float] = Field(title='经度地区')

        
class SShShop(CreateShShop):
    id: int

    class Config:
        orm_mode = True

class ShShop(CreateShShop):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResShShop(BaseModel):
    data: List[SShShop]
    total: int
    
class CreateShUser(BaseModel):
    register_time: Optional[datetime] = Field(title='创建时间')
    shop_id: Optional[int] = Field(title='店铺id')
    pinpai_id: Optional[int] = Field(title='品牌id')
    user_name: Optional[str] = Field(title='用户名称')
    user_nicheng: Optional[str] = Field(title='用户昵姓名')
    phone: Optional[str] = Field(title='电话')
    balance: Optional[int] = Field(title='余额')
    givefee: Optional[int] = Field(title='增额')
    givebalance: Optional[int] = Field(title='已分配额')
    givetarget: Optional[int] = Field(title='可分配额')
    recommenda: Optional[int] = Field(title='平台推荐人')
    recommendb: Optional[int] = Field(title='转发推荐人')
    user_level: Optional[int] = Field(title='用户级别')
    status: Optional[int] = Field(title='商家状态,0正常,1禁用')

        
class SShUser(CreateShUser):
    id: int

    class Config:
        orm_mode = True

class ShUser(CreateShUser):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResShUser(BaseModel):
    data: List[SShUser]
    total: int
    
class CreateShUserlevel(BaseModel):
    register_time: Optional[datetime] = Field(title='创建时间')
    level_name: Optional[str] = Field(title='级别名称')
    propo: Optional[int] = Field(title='消费分成比例（百分比）')
    shop_id: Optional[int] = Field(title='店铺id')
    pinpai_id: Optional[int] = Field(title='品牌id')
    status: Optional[int] = Field(title='级别状态,0正常,1默认')

        
class SShUserlevel(CreateShUserlevel):
    id: int

    class Config:
        orm_mode = True

class ShUserlevel(CreateShUserlevel):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResShUserlevel(BaseModel):
    data: List[SShUserlevel]
    total: int
    
class CreateShoperorderfee(BaseModel):
    register_time: Optional[datetime] = Field(title='创建时间')
    good_id: Optional[int] = Field(title='商品d')
    order_id: Optional[int] = Field(title='订单id')
    user_id: Optional[int] = Field(title='排队批发商id')
    fee_num: Optional[int] = Field(title='剩余分润次数')
    fee_time: Optional[datetime] = Field(title='最近一次分润时间')
    gtype: Optional[int] = Field(title='商品分类,0表示未定义,1联营会员2仓库主3巨省会员')
    fee_count: Optional[int] = Field(title='总分润次数')

        
class SShoperorderfee(CreateShoperorderfee):
    id: int = Field(title='标识id')

    class Config:
        orm_mode = True

class Shoperorderfee(CreateShoperorderfee):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResShoperorderfee(BaseModel):
    data: List[SShoperorderfee]
    total: int
    
class CreateStore(BaseModel):
    name: Optional[str] = Field(title='店铺名称')
    phone: Optional[str] = Field(title='电话')
    province: Optional[str] = Field(title='省份')
    city: Optional[str] = Field(title='城市')
    area: Optional[str] = Field(title='区域')
    street: Optional[str] = Field(title='街道')
    address: Optional[str] = Field(title='详细地址')
    status: Optional[int] = Field(title='店铺状态')
    owner: Optional[str] = Field(title='店铺负责人')
    recommender_id: Optional[int] = Field(title='推荐人id   对应某个用户')
    register_time: Optional[datetime] = Field(title='注册时间')
    type: Optional[int] = Field(title='店铺类型：0为企业，1为个体')
    expired_time: Optional[datetime] = Field(title='合同到期时间')
    open_time: Optional[int] = Field(title='开始营业时间   9*3600表示9:00')
    close_time: Optional[int] = Field(title='结束营业时间   9*3600表示9:00，以秒为单位')
    image: Optional[str] = Field(title='商家门头图片')
    owner_id: Optional[int] = Field(title='负责人id')
    supplier_id: Optional[int] = Field(title='商家id')
    company_name: Optional[str] = Field(title='公司名称')
    reject_reason: Optional[str] = Field(title='驳回原因')
    reject_time: Optional[datetime] = Field(title='驳回时间')
    reject_admin_id: Optional[int] = Field(title='管理员id   记录是谁驳回的')
    is_default: Optional[int] = Field(title='默认店铺')
    commit_way: Optional[int] = Field(title='提交方式:0,营业执照; 1身份证')
    social_credit_code: Optional[str] = Field(title='统一社会信用代码')
    transactor_id: Optional[int] = Field(title='办理人ID')
    recommend_id: Optional[int] = Field(title='推荐人ID')
    parent_id: Optional[int] = Field(title='上一级店铺ID')
    latitude: Optional[float] = Field(title='纬度地区')
    longitude: Optional[float] = Field(title='经度地区')
    profession_id: Optional[int] = Field(title='店铺行业ID')
    business_area_id: Optional[int] = Field(title='商圈ID')
    refine_steps: Optional[int] = Field(title='完善步骤：1、2、3、4......')
    consume_aver: Optional[int] = Field(title='人均消费')
    usable_room: Optional[int] = Field(title='包间是否可用，默认0,可用为1')

        
class SStore(CreateStore):
    id: int

    class Config:
        orm_mode = True

class Store(CreateStore):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResStore(BaseModel):
    data: List[SStore]
    total: int
    
class CreateStoreAmount(BaseModel):
    type: Optional[int] = Field(title='变动类型')
    change: Optional[int] = Field(title='资金变动额      +10    -5')
    amount: Optional[int] = Field(title='资金总额')
    create_time: Optional[datetime] = Field(title='创建时间')
    store_id: Optional[int] = Field(title='店铺id')

        
class SStoreAmount(CreateStoreAmount):
    id: int

    class Config:
        orm_mode = True

class StoreAmount(CreateStoreAmount):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResStoreAmount(BaseModel):
    data: List[SStoreAmount]
    total: int
    
class CreateStoreBusinessArea(BaseModel):
    city_id: Optional[int] = Field(title='地区ID，t_city表Id')
    area_name: Optional[str] = Field(title='商圈名称')
    latitude: Optional[float] = Field(title='纬度地区')
    longitude: Optional[float] = Field(title='经度地区')
    area_radius: Optional[int] = Field(title='半径，CM')
    register_time: Optional[datetime] = Field(title='创建时间')
    operator_id: Optional[int] = Field(title='操作员ID')

        
class SStoreBusinessArea(CreateStoreBusinessArea):
    id: int

    class Config:
        orm_mode = True

class StoreBusinessArea(CreateStoreBusinessArea):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResStoreBusinessArea(BaseModel):
    data: List[SStoreBusinessArea]
    total: int
    
class CreateStoreChangeType(BaseModel):
    type: Optional[str] = Field(title='资金变动类型')

        
class SStoreChangeType(CreateStoreChangeType):
    id: int

    class Config:
        orm_mode = True

class StoreChangeType(CreateStoreChangeType):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResStoreChangeType(BaseModel):
    data: List[SStoreChangeType]
    total: int
    
class CreateStoreContract(BaseModel):
    contract: Optional[str] = Field(title='合同照片')
    store_id: Optional[int] = Field(title='商家编号')
    create_time: Optional[datetime] = Field(title='创建时间')
    expired_time: Optional[datetime] = Field(title='到期时间')

        
class SStoreContract(CreateStoreContract):
    id: int

    class Config:
        orm_mode = True

class StoreContract(CreateStoreContract):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResStoreContract(BaseModel):
    data: List[SStoreContract]
    total: int
    
class CreateStoreIncome(BaseModel):
    income_add: Optional[int] = Field(title='收入增加额')
    income_total: Optional[int] = Field(title='商家总收入')
    create_time: Optional[datetime] = Field(title='创建时间')
    store_id: Optional[int] = Field(title='商家id')

        
class SStoreIncome(CreateStoreIncome):
    id: int

    class Config:
        orm_mode = True

class StoreIncome(CreateStoreIncome):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResStoreIncome(BaseModel):
    data: List[SStoreIncome]
    total: int
    
class CreateStoreLicense(BaseModel):
    license: Optional[str] = Field(title='营业执照文本')
    store_id: Optional[int] = Field(title='商家id')
    create_time: Optional[datetime] = Field(title='更新时间')
    license_type: Optional[str] = Field(title='商家证件类型：营业执照,税务登记证,组织机构代码证,质量认证,卫生认证')
    status: Optional[int] = Field(title='默认0，-1为删除')

        
class SStoreLicense(CreateStoreLicense):
    id: int

    class Config:
        orm_mode = True

class StoreLicense(CreateStoreLicense):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResStoreLicense(BaseModel):
    data: List[SStoreLicense]
    total: int
    
class CreateStoreMembership(BaseModel):
    store_id: Optional[int] = Field(title='商家id')
    user_id: Optional[int] = Field(title='用户id')
    status: Optional[str]
    create_time: Optional[datetime]
    expired_time: Optional[datetime] = Field(title='过期时间')

        
class SStoreMembership(CreateStoreMembership):
    id: int

    class Config:
        orm_mode = True

class StoreMembership(CreateStoreMembership):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResStoreMembership(BaseModel):
    data: List[SStoreMembership]
    total: int
    
class CreateStoreOwner(BaseModel):
    name: Optional[str] = Field(title='负责人姓名')
    phone: Optional[str] = Field(title='电话')
    password: Optional[str] = Field(title='密码（哈希值）')
    id_card: Optional[str] = Field(title='身份证号')
    front_image: Optional[str] = Field(title='身份证正面照')
    back_image: Optional[str] = Field(title='身份证背面照')
    create_time: Optional[datetime] = Field(title='创建时间')
    user_role: Optional[int] = Field(title='商铺管理角色：0负责人，1财务，2收银员，3辅员，4其他')
    parent_id: Optional[int] = Field(title='隶属关系：0顶级，大于0为上一级id')
    open_id: Optional[str] = Field(title='微信openID')
    union_id: Optional[str] = Field(title='微信unionID')
    status: Optional[int] = Field(title='商铺账户状态：0正常，-1删除')
    remark: Optional[str] = Field(title='账户备注')
    login_code: Optional[str] = Field(title='用户登录code')
    login_time: Optional[datetime] = Field(title='会员登录时间')
    store_id: Optional[int] = Field(title='店铺ID')

        
class SStoreOwner(CreateStoreOwner):
    id: int

    class Config:
        orm_mode = True

class StoreOwner(CreateStoreOwner):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResStoreOwner(BaseModel):
    data: List[SStoreOwner]
    total: int
    
class CreateStoreProfession(BaseModel):
    pname: Optional[str] = Field(title='行业名称')
    coupon_add_path: Optional[str] = Field(title='创建此行业卡券时的跳转路径')
    coupon_fix_path: Optional[str] = Field(title='修改此行业卡券时的跳转路径')
    parent_id: Optional[int] = Field(title='上级ID，默认是0表示顶级')
    register_time: Optional[datetime] = Field(title='店铺创建时间')
    operator_id: Optional[int] = Field(title='操作员ID')
    pro_other: Optional[str] = Field(title='行业相关备注')

        
class SStoreProfession(CreateStoreProfession):
    id: int

    class Config:
        orm_mode = True

class StoreProfession(CreateStoreProfession):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResStoreProfession(BaseModel):
    data: List[SStoreProfession]
    total: int
    
class CreateStoreState(BaseModel):
    status: Optional[str] = Field(title='商家类型')

        
class SStoreState(CreateStoreState):
    id: int

    class Config:
        orm_mode = True

class StoreState(CreateStoreState):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResStoreState(BaseModel):
    data: List[SStoreState]
    total: int
    
class CreateStoreTag(BaseModel):
    store_id: Optional[int] = Field(title='商家ID')
    tag_id: Optional[int] = Field(title='标签ID')
    register_time: Optional[datetime] = Field(title='标签关系创建时间')
    operator_id: Optional[int] = Field(title='操作员ID')

        
class SStoreTag(CreateStoreTag):
    id: int

    class Config:
        orm_mode = True

class StoreTag(CreateStoreTag):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResStoreTag(BaseModel):
    data: List[SStoreTag]
    total: int
    
class CreateStoreTransactor(BaseModel):
    type: Optional[int] = Field(title='办理人类型：0法人办理、1代理人办理')
    tname: Optional[str] = Field(title='办理人姓名')
    certificate_type: Optional[int] = Field(title='证件类型：0法人证件、1个人身份证证件')
    certificate_num: Optional[str] = Field(title='证件号码')
    license1: Optional[str] = Field(title='证件照地址1')
    license2: Optional[str] = Field(title='证件照地址2')
    license3: Optional[str] = Field(title='证件照地址3')
    license4: Optional[str] = Field(title='证件照地址4')
    certificate_phone: Optional[str] = Field(title='电话')
    register_time: Optional[datetime] = Field(title='注册时间')
    operator_id: Optional[int] = Field(title='操作员ID')
    store_id: Optional[int] = Field(title='店铺ID')

        
class SStoreTransactor(CreateStoreTransactor):
    id: int

    class Config:
        orm_mode = True

class StoreTransactor(CreateStoreTransactor):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResStoreTransactor(BaseModel):
    data: List[SStoreTransactor]
    total: int
    
class CreateSupplier(BaseModel):
    name: Optional[str] = Field(title='商家名称')
    phone: Optional[str] = Field(title='电话')
    province: Optional[str] = Field(title='省份')
    city: Optional[str] = Field(title='城市')
    area: Optional[str] = Field(title='区域')
    street: Optional[str] = Field(title='街道')
    address: Optional[str] = Field(title='详细地址')
    status: Optional[int] = Field(title='商家状态')
    owner: Optional[str] = Field(title='商家负责人')
    recommender_id: Optional[int] = Field(title='推荐人id   对应某个用户')
    register_time: Optional[datetime] = Field(title='注册时间')
    type: Optional[int] = Field(title='商家类型;   0: 商家  1:供应商')
    expired_time: Optional[datetime] = Field(title='合同到期时间')
    open_time: Optional[int] = Field(title='开始营业时间   9*3600表示9:00')
    close_time: Optional[int] = Field(title='结束营业时间   9*3600表示9:00，以秒为单位')
    image: Optional[str] = Field(title='商家门头图片')
    owner_id: Optional[int] = Field(title='负责人id')
    category: Optional[int] = Field(title='供应商类型  2：供应商   1：商家')
    balance: Optional[int] = Field(title='余额；以分为单位')
    reject_reason: Optional[str] = Field(title='驳回原因')
    reject_admin_id: Optional[int] = Field(title='管理员id   记录是谁审批的')
    reject_time: Optional[datetime] = Field(title='驳回时间')
    company_name: Optional[str] = Field(title='公司名称')
    license1: Optional[str] = Field(title='营业执照证件地址')
    license2: Optional[str] = Field(title='证件地址2')
    license3: Optional[str] = Field(title='证件地址3')
    license4: Optional[str] = Field(title='备注文本')

        
class SSupplier(CreateSupplier):
    id: int

    class Config:
        orm_mode = True

class Supplier(CreateSupplier):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResSupplier(BaseModel):
    data: List[SSupplier]
    total: int
    
class CreateSupplierAmount(BaseModel):
    type: Optional[int] = Field(title='变动类型')
    change: Optional[int] = Field(title='资金变动额      +10    -5')
    amount: Optional[int] = Field(title='资金总额')
    create_time: Optional[datetime] = Field(title='创建时间')
    supplier_id: Optional[int] = Field(title='商家id')
    order_id: Optional[int] = Field(title='订单id')
    description: Optional[str] = Field(title='描述')

        
class SSupplierAmount(CreateSupplierAmount):
    id: int

    class Config:
        orm_mode = True

class SupplierAmount(CreateSupplierAmount):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResSupplierAmount(BaseModel):
    data: List[SSupplierAmount]
    total: int
    
class CreateSupplierChangeType(BaseModel):
    type: Optional[str] = Field(title='资金变动类型')

        
class SSupplierChangeType(CreateSupplierChangeType):
    id: int

    class Config:
        orm_mode = True

class SupplierChangeType(CreateSupplierChangeType):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResSupplierChangeType(BaseModel):
    data: List[SSupplierChangeType]
    total: int
    
class CreateSupplierIncome(BaseModel):
    supplier_id: Optional[int] = Field(title='外键,供应商id')
    change: Optional[int] = Field(title='变动金额')
    balance: Optional[int] = Field(title='余额')
    type: Optional[str] = Field(title='类型')
    description: Optional[str] = Field(title='详细描述')
    create_time: Optional[datetime] = Field(title='创建时间')
    user_withdraw_id: Optional[int]
    operator_id: Optional[int] = Field(title='操作员ID')
    out_trade_no: Optional[str]

        
class SSupplierIncome(CreateSupplierIncome):
    id: int

    class Config:
        orm_mode = True

class SupplierIncome(CreateSupplierIncome):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResSupplierIncome(BaseModel):
    data: List[SSupplierIncome]
    total: int
    
class CreateSupplierLicense(BaseModel):
    license: Optional[str] = Field(title='营业执照文本')
    supplier_id: Optional[int] = Field(title='商家id')
    create_time: Optional[datetime] = Field(title='更新时间')

        
class SSupplierLicense(CreateSupplierLicense):
    id: int

    class Config:
        orm_mode = True

class SupplierLicense(CreateSupplierLicense):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResSupplierLicense(BaseModel):
    data: List[SSupplierLicense]
    total: int
    
class CreateSupplierMembership(BaseModel):
    supplier_id: Optional[int] = Field(title='商家id')
    user_id: Optional[int] = Field(title='用户id')
    status: Optional[str]
    create_time: Optional[datetime]
    expired_time: Optional[datetime] = Field(title='过期时间')

        
class SSupplierMembership(CreateSupplierMembership):
    id: int

    class Config:
        orm_mode = True

class SupplierMembership(CreateSupplierMembership):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResSupplierMembership(BaseModel):
    data: List[SSupplierMembership]
    total: int
    
class CreateSupplierOwner(BaseModel):
    name: Optional[str] = Field(title='负责人姓名')
    phone: Optional[str] = Field(title='电话')
    password: Optional[str] = Field(title='密码（哈希值）')
    id_card: Optional[str] = Field(title='身份证号')
    front_image: Optional[str] = Field(title='身份证正面照')
    back_image: Optional[str] = Field(title='身份证背面照')
    open_id: Optional[str]
    union_id: Optional[str]
    level_id: Optional[int] = Field(title='角色id    0：负责人     1：财务人员      2：核销人员')

        
class SSupplierOwner(CreateSupplierOwner):
    id: int

    class Config:
        orm_mode = True

class SupplierOwner(CreateSupplierOwner):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResSupplierOwner(BaseModel):
    data: List[SSupplierOwner]
    total: int
    
class CreateSupplierState(BaseModel):
    status: Optional[str] = Field(title='商家类型')

        
class SSupplierState(CreateSupplierState):
    id: int

    class Config:
        orm_mode = True

class SupplierState(CreateSupplierState):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResSupplierState(BaseModel):
    data: List[SSupplierState]
    total: int
    
class CreateSupplierType(BaseModel):
    type_: Optional[str] = Field(title='类型')

        
class SSupplierType(CreateSupplierType):
    id: int

    class Config:
        orm_mode = True

class SupplierType(CreateSupplierType):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResSupplierType(BaseModel):
    data: List[SSupplierType]
    total: int
    
class CreateTask(BaseModel):
    register_time: Optional[datetime] = Field(title='创建时间')
    title: Optional[str] = Field(title='任务标题')
    describe: Optional[str] = Field(title='任务描述')
    top: Optional[int] = Field(title='任务上限')
    big: Optional[int] = Field(title='单号最大领取量')
    received: Optional[int] = Field(title='已领取量')
    stat: Optional[int] = Field(title='0未开启,1进行中,2打开中,3已结束')
    style: Optional[str] = Field(title='图样地址七牛oss,逗号分割多个图样地址')
    verfy: Optional[str] = Field(title='任务完成后打卡证明格式,逗号分割打卡平台名称')
    run_time: Optional[datetime] = Field(title='进行中时间')
    clock_time: Optional[datetime] = Field(title='打卡时间')
    expired_time: Optional[datetime] = Field(title='结束时间')
    down: Optional[int] = Field(title='素材下载次数')
    upload: Optional[int] = Field(title='素材上传数量')
    ctype: Optional[int] = Field(title='任务分类,0表示视频类,1表示图文类')
    islink: Optional[int] = Field(title='是否开启链接上传,0否,1是')
    start_time: Optional[datetime] = Field(title='开始时间')
    verfy_num: Optional[int] = Field(title='打卡项数目')
    is_auto: Optional[int] = Field(title='是否自动处理状态,0自动,1手动')
    cover: Optional[str] = Field(title='封面图')

        
class STask(CreateTask):
    id: int = Field(title='标识id')

    class Config:
        orm_mode = True

class Task(CreateTask):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResTask(BaseModel):
    data: List[STask]
    total: int
    
class CreateTaskclockup(BaseModel):
    register_time: Optional[datetime] = Field(title='创建时间')
    task_id: Optional[int] = Field(title='参与任务id')
    tuser_id: Optional[int] = Field(title='素材id')
    topic_id: Optional[int] = Field(title='话题id')
    user_id: Optional[int] = Field(title='参与会员id')
    manage_id: Optional[int] = Field(title='审核人id')
    ctype: Optional[int] = Field(title='任务分类,0表示视频截图类,1表示图文类')
    content: Optional[str] = Field(title='截图地址或图文内容')
    verfy_name: Optional[str] = Field(title='平台名称')
    status: Optional[int] = Field(title='状态,0未审核,1合格,2不合格')
    stat_time: Optional[datetime] = Field(title='审核时间')
    stat_count: Optional[int] = Field(title='统计浏览次数')
    user_acc: Optional[str] = Field(title='打卡平台账号')

        
class STaskclockup(CreateTaskclockup):
    id: int = Field(title='标识id')

    class Config:
        orm_mode = True

class Taskclockup(CreateTaskclockup):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResTaskclockup(BaseModel):
    data: List[STaskclockup]
    total: int
    
class CreateTasktopic(BaseModel):
    register_time: Optional[datetime] = Field(title='创建时间')
    task_id: Optional[int] = Field(title='参与任务id')
    topic_name: Optional[str] = Field(title='任务话题内容')
    topic_comment: Optional[str] = Field(title='任务评论内容')
    status: Optional[int] = Field(title='状态,0正常')
    ts_num: Optional[int] = Field(title='素材数量')

        
class STasktopic(CreateTasktopic):
    id: int = Field(title='标识id')

    class Config:
        orm_mode = True

class Tasktopic(CreateTasktopic):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResTasktopic(BaseModel):
    data: List[STasktopic]
    total: int
    
class CreateTaskuser(BaseModel):
    register_time: Optional[datetime] = Field(title='素材上传时间')
    user_time: Optional[datetime] = Field(title='会员领取时间')
    task_url: Optional[str] = Field(title='七牛oss素材地址')
    task_id: Optional[int] = Field(title='参与任务id')
    user_id: Optional[int] = Field(title='参与会员id,0表示未领取')
    phone: Optional[str] = Field(title='联系方式')
    address: Optional[str] = Field(title='地址')
    upload: Optional[int] = Field(title='打卡上传数量')
    down: Optional[int] = Field(title='素材下载次数')
    verfy_upload: Optional[str] = Field(title='打卡证明格式{key:url}|{}')
    topic_id: Optional[int] = Field(title='所属话题id')
    link_stat: Optional[int] = Field(title='链接审核状态,0未操作,1链接未审核,2链接已审核')
    pic_stat: Optional[int] = Field(title='截图审核状态,0未打卡,1未审核,2已审核,')
    nopass: Optional[str] = Field(title='不合格原因选项')
    nopass_txt: Optional[str] = Field(title='不合格原因文本')
    filename: Optional[str] = Field(title='生成token的文件名称')
    status: Optional[int] = Field(title='状态,0正常,-1删除')
    recovery: Optional[int] = Field(title='回收次数')

        
class STaskuser(CreateTaskuser):
    id: int = Field(title='标识id')

    class Config:
        orm_mode = True

class Taskuser(CreateTaskuser):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResTaskuser(BaseModel):
    data: List[STaskuser]
    total: int
    
class CreateTranAccount(BaseModel):
    user_out: Optional[int] = Field(title='转让人id')
    user_out_phone: Optional[str] = Field(title='转让人电话')
    user_out_name: Optional[str] = Field(title='转让人姓名')
    user_out_balance: Optional[int] = Field(title='转让人余额')
    user_get: Optional[int] = Field(title='收钱人id')
    register_time: Optional[datetime] = Field(title='创建时间')
    user_get_phone: Optional[str] = Field(title='收钱人电话')
    user_get_name: Optional[str] = Field(title='收钱人姓名')
    user_get_balance: Optional[int] = Field(title='收钱人余额')
    balance: Optional[int] = Field(title='金额')

        
class STranAccount(CreateTranAccount):
    id: int = Field(title='标识id编号')

    class Config:
        orm_mode = True

class TranAccount(CreateTranAccount):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResTranAccount(BaseModel):
    data: List[STranAccount]
    total: int
    
class CreateTsrecoverylog(BaseModel):
    register_time: Optional[datetime] = Field(title='回收时间')
    user_id: Optional[int] = Field(title='会员账号id')
    ts_id: Optional[int] = Field(title='回收素材id')
    task_id: Optional[int] = Field(title='回收素材任务id')
    phone: Optional[str] = Field(title='会员联系方式')
    address: Optional[str] = Field(title='地址')
    logtype: Optional[str] = Field(title='自动回收、手动回收')

        
class STsrecoverylog(CreateTsrecoverylog):
    id: int

    class Config:
        orm_mode = True

class Tsrecoverylog(CreateTsrecoverylog):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResTsrecoverylog(BaseModel):
    data: List[STsrecoverylog]
    total: int
    
class CreateUser(BaseModel):
    username: Optional[str] = Field(title='用户名')
    email: Optional[str] = Field(title='邮箱')
    open_id: Optional[str] = Field(title='openID from wechat channel')
    union_id: Optional[str] = Field(title='unionID from tecent')
    password: Optional[str] = Field(title='密码（哈希值）')
    nickname: Optional[str] = Field(title='昵称')
    phone: Optional[str] = Field(title='联系方式')
    id_card: Optional[str] = Field(title='身份证')
    level_id: Optional[int] = Field(title='用户等级 默认是0粉丝,1会员,2核心会员')
    status: Optional[int] = Field(title='0: 已实名   1: 未实名,被is_agree替代')
    register_time: Optional[datetime] = Field(title='注册时间')
    avatar: Optional[str] = Field(title='头像url')
    invited_user_id: Optional[int] = Field(title='邀请人id')
    coin: Optional[int] = Field(title='积分')
    gender: Optional[int] = Field(title='0:  男  1:  女')
    last_active_time: Optional[datetime] = Field(title='最近登录时间')
    name: Optional[str] = Field(title='用户名')
    is_agree: Optional[int] = Field(title='是否已经校验')
    parent_id: Optional[int] = Field(title='父级用户')
    parent_id_history: Optional[str] = Field(title='曾经的上级(ID之间逗号分隔)')
    level_one_time: Optional[datetime] = Field(title='升级he合伙人会员时间')
    level_two_time: Optional[datetime] = Field(title='升级老板会员时间')
    level_three_time: Optional[datetime] = Field(title='升级大老板会员时间')
    level_top_time: Optional[datetime] = Field(title='升级推广顶级时间')
    wholesale_id: Optional[int] = Field(title='身份0普通1小团长2大团长')
    wholesale_amount: Optional[int] = Field(title='批发商品累计消费额')
    paidui: Optional[int] = Field(title='排队分次数')
    tuan_id: Optional[int] = Field(title='所属团id,0表示未入团人员,>0表示所属团长id')
    tran_pass: Optional[str] = Field(title='转账密码')
    invited_code: Optional[str] = Field(title='邀请码')
    bigorder_id: Optional[int] = Field(title='公排id')
    layer_id: Optional[int] = Field(title='行号(所在层数)')
    cur_layer_id: Optional[int] = Field(title='当前行号从左到右排序号')
    cur_layer_total: Optional[int] = Field(title='当前行排序总数量')
    bigorder_parent_id: Optional[int] = Field(title='上级对应序号')
    entrust_status: Optional[int] = Field(title='委托状态0未接受1临时托管中2永久托管')
    light_status: Optional[int] = Field(title='熄灯状态0正常1熄灯')
    voucher_total: Optional[int] = Field(title='商品购买券数量')
    endorders_total: Optional[int] = Field(title='完成订单数量')
    doubule_id: Optional[int] = Field(title='是否分身大于0为分身id')
    entrust_startime: Optional[datetime] = Field(title='开启托管时间')
    entrust_endtime: Optional[datetime] = Field(title='结束托管时间')
    pai_buydui: Optional[int] = Field(title='排队复购次数')
    bagorder_num: Optional[int] = Field(title='礼包购买数')
    weight_num: Optional[int] = Field(title='权重指数')
    fund_weight_num: Optional[int] = Field(title='分红权重指数')
    video_level: Optional[int] = Field(title='视频任务分发级别,1达人,2店长3,服务商,4分公司 ')
    is_tuan: Optional[int] = Field(title='视频团长和身份id')
    ercode: Optional[str] = Field(title='个人二维码')
    sh_agent: Optional[int] = Field(title='市代身份 ')
    sh_agent_id: Optional[int] = Field(title='市代id')

        
class SUser(CreateUser):
    id: int = Field(title='标识id')

    class Config:
        orm_mode = True

class User(CreateUser):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResUser(BaseModel):
    data: List[SUser]
    total: int
    
class CreateUser250810(BaseModel):
    username: Optional[str] = Field(title='用户名')
    email: Optional[str] = Field(title='邮箱')
    open_id: Optional[str] = Field(title='openID from wechat channel')
    union_id: Optional[str] = Field(title='unionID from tecent')
    password: Optional[str] = Field(title='密码（哈希值）')
    nickname: Optional[str] = Field(title='昵称')
    phone: Optional[str] = Field(title='联系方式')
    id_card: Optional[str] = Field(title='身份证')
    level_id: Optional[int] = Field(title='用户等级 默认是0粉丝,1会员,2核心会员')
    status: Optional[int] = Field(title='0: 已实名   1: 未实名,被is_agree替代')
    register_time: Optional[datetime] = Field(title='注册时间')
    avatar: Optional[str] = Field(title='头像url')
    invited_user_id: Optional[int] = Field(title='邀请人id')
    coin: Optional[int] = Field(title='积分')
    gender: Optional[int] = Field(title='0:  男  1:  女')
    last_active_time: Optional[datetime] = Field(title='最近登录时间')
    name: Optional[str] = Field(title='用户名')
    is_agree: Optional[int] = Field(title='是否已经校验')
    parent_id: Optional[int] = Field(title='父级用户')
    parent_id_history: Optional[str] = Field(title='曾经的上级(ID之间逗号分隔)')
    level_one_time: Optional[datetime] = Field(title='升级he合伙人会员时间')
    level_two_time: Optional[datetime] = Field(title='升级老板会员时间')
    level_three_time: Optional[datetime] = Field(title='升级大老板会员时间')
    level_top_time: Optional[datetime] = Field(title='升级推广顶级时间')
    wholesale_id: Optional[int] = Field(title='身份0普通1小团长2大团长')
    wholesale_amount: Optional[int] = Field(title='批发商品累计消费额')
    paidui: Optional[int] = Field(title='排队分次数')
    tuan_id: Optional[int] = Field(title='所属团id,0表示未入团人员,>0表示所属团长id')
    tran_pass: Optional[str] = Field(title='转账密码')
    invited_code: Optional[str] = Field(title='邀请码')
    bigorder_id: Optional[int] = Field(title='公排id')
    layer_id: Optional[int] = Field(title='行号(所在层数)')
    cur_layer_id: Optional[int] = Field(title='当前行号从左到右排序号')
    cur_layer_total: Optional[int] = Field(title='当前行排序总数量')
    bigorder_parent_id: Optional[int] = Field(title='上级对应序号')
    entrust_status: Optional[int] = Field(title='委托状态0未接受1临时托管中2永久托管')
    light_status: Optional[int] = Field(title='熄灯状态0正常1熄灯')
    voucher_total: Optional[int] = Field(title='商品购买券数量')
    endorders_total: Optional[int] = Field(title='完成订单数量')
    doubule_id: Optional[int] = Field(title='是否分身大于0为分身id')
    entrust_startime: Optional[datetime] = Field(title='开启托管时间')
    entrust_endtime: Optional[datetime] = Field(title='结束托管时间')
    pai_buydui: Optional[int] = Field(title='排队复购次数')
    bagorder_num: Optional[int] = Field(title='礼包购买数')

        
class SUser250810(CreateUser250810):
    id: int = Field(title='标识id')

    class Config:
        orm_mode = True

class User250810(CreateUser250810):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResUser250810(BaseModel):
    data: List[SUser250810]
    total: int
    
class CreateUserAccount(BaseModel):
    user_id: Optional[int] = Field(title='用户id')
    balance: Optional[int] = Field(title='余额')
    lock_balance: Optional[int] = Field(title='推荐金额')
    coin: Optional[int] = Field(title='优惠券额度')
    description: Optional[str] = Field(title='详细描述')
    create_time: Optional[datetime] = Field(title='记录生成时间')
    freeze_balance: Optional[int] = Field(title='冻结额 单位：分')
    update_time: Optional[datetime]
    forecast_one: Optional[int] = Field(title='初级资金池分润预测值')
    forecast_two: Optional[int] = Field(title='高级资金池分润预测值')
    forecast_three: Optional[int] = Field(title='顶级资金池分润预测值')
    prop_one: Optional[float] = Field(title='初级资金池分润预测比值')
    prop_two: Optional[float] = Field(title='高级资金池分润预测比值')
    prop_three: Optional[float] = Field(title='顶级资金池分润预测比值')
    nvideo: Optional[int] = Field(title='用户剩余视频条数')

        
class SUserAccount(CreateUserAccount):
    id: int = Field(title='账户id')

    class Config:
        orm_mode = True

class UserAccount(CreateUserAccount):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResUserAccount(BaseModel):
    data: List[SUserAccount]
    total: int
    
class CreateUserAd(BaseModel):
    create_time: Optional[datetime] = Field(title='创建时间')
    user_id: Optional[int] = Field(title='用户id')
    user_name: Optional[str] = Field(title='用户昵称')
    user_phone: Optional[str] = Field(title='用户电话')
    qr_code_user: Optional[str] = Field(title='用户微信')
    qr_code_enterprise: Optional[str] = Field(title='企业微信')
    adbrand_id: Optional[int] = Field(title='广告品牌id')
    is_del: Optional[int] = Field(title='是否删除,0正常,1删除')
    del_brand: Optional[int] = Field(title='项目是否删除,1删除')

        
class SUserAd(CreateUserAd):
    id: int

    class Config:
        orm_mode = True

class UserAd(CreateUserAd):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResUserAd(BaseModel):
    data: List[SUserAd]
    total: int
    
class CreateUserAdUinfo(BaseModel):
    create_time: Optional[datetime] = Field(title='创建时间')
    user_id: Optional[int] = Field(title='用户id')
    user_name: Optional[str] = Field(title='用户昵称')
    user_phone: Optional[str] = Field(title='用户电话')
    qr_code_user: Optional[str] = Field(title='用户微信')
    qr_code_enterprise: Optional[str] = Field(title='企业微信')
    is_del: Optional[int] = Field(title='是否删除,0正常,1删除')

        
class SUserAdUinfo(CreateUserAdUinfo):
    id: int

    class Config:
        orm_mode = True

class UserAdUinfo(CreateUserAdUinfo):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResUserAdUinfo(BaseModel):
    data: List[SUserAdUinfo]
    total: int
    
class CreateUserAdbrand(BaseModel):
    create_time: Optional[datetime] = Field(title='创建时间')
    title: Optional[str] = Field(title='广告品牌标题')
    ad_id: Optional[int] = Field(title='Banner图片id')
    describe: Optional[str] = Field(title='详情描述 (富文本)')
    qr_code: Optional[str] = Field(title='企业微信二维码')
    qual_pic: Optional[str] = Field(title='营业执照、许可证等资质图片（最多4张)')
    video: Optional[str] = Field(title='品牌宣传视频，支持mp4格式 ')
    good_id: Optional[str] = Field(title='绑定商品ID')
    poster_share: Optional[str] = Field(title='品牌宣传视频，支持mp4格式 ')
    is_del: Optional[int] = Field(title='是否删除,0正常,1删除')
    share_title: Optional[str] = Field(title='分享标题')
    share_pic: Optional[str] = Field(title='分享海报图')
    is_default: Optional[int] = Field(title='项目是否默认,1默认')
    information: Optional[str] = Field(title='资料介绍')
    customer_case: Optional[str] = Field(title='客户案例')
    is_show_good: Optional[int] = Field(title='是否展示商品介绍，默认0显示，1为隐藏')

        
class SUserAdbrand(CreateUserAdbrand):
    id: int

    class Config:
        orm_mode = True

class UserAdbrand(CreateUserAdbrand):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResUserAdbrand(BaseModel):
    data: List[SUserAdbrand]
    total: int
    
class CreateUserAdbrandFile(BaseModel):
    create_time: Optional[datetime] = Field(title='创建时间')
    adbrand_id: Optional[int] = Field(title='广告模板id')
    file_name: Optional[str] = Field(title='文件名称')
    file_size: Optional[int] = Field(title='文件大小KB')
    file_url: Optional[str] = Field(title='文件地址')
    file_type: Optional[str] = Field(title='文件类型pdf,doc,xls')
    is_del: Optional[int] = Field(title='是否删除,0正常,1删除')
    menu_id: Optional[int] = Field(title='项目菜单id')

        
class SUserAdbrandFile(CreateUserAdbrandFile):
    id: int

    class Config:
        orm_mode = True

class UserAdbrandFile(CreateUserAdbrandFile):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResUserAdbrandFile(BaseModel):
    data: List[SUserAdbrandFile]
    total: int
    
class CreateUserAdbrandMenu(BaseModel):
    create_time: Optional[datetime] = Field(title='创建时间')
    adbrand_id: Optional[int] = Field(title='广告模板id')
    m_name: Optional[str] = Field(title='导航名称')
    pic_url: Optional[str] = Field(title='模块主图')
    m_title: Optional[str] = Field(title='模块标题')
    m_type: Optional[int] = Field(title='类型0表示内容型,1表示文件列表型')
    text_one: Optional[str] = Field(title='图文简介')
    text_two: Optional[str] = Field(title='富文本内容')
    is_del: Optional[int] = Field(title='是否删除,0正常,1删除')
    is_hide: Optional[int] = Field(title='是否隐藏,0正常,1隐藏')

        
class SUserAdbrandMenu(CreateUserAdbrandMenu):
    id: int

    class Config:
        orm_mode = True

class UserAdbrandMenu(CreateUserAdbrandMenu):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResUserAdbrandMenu(BaseModel):
    data: List[SUserAdbrandMenu]
    total: int
    
class CreateUserBank(BaseModel):
    bank_name: Optional[str] = Field(title='开户行')
    username: Optional[str] = Field(title='户主姓名')
    id_card: Optional[str] = Field(title='银行卡号')
    user_id: Optional[int] = Field(title='用户id')
    phone: Optional[str] = Field(title='户主电话')
    bank_address: Optional[str] = Field(title='开户行地址')
    is_default: Optional[int]

        
class SUserBank(CreateUserBank):
    id: int

    class Config:
        orm_mode = True

class UserBank(CreateUserBank):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResUserBank(BaseModel):
    data: List[SUserBank]
    total: int
    
class CreateUserFav(BaseModel):
    user_id: Optional[int]
    good_id: Optional[int]
    create_time: Optional[datetime]
    spec_id: Optional[int] = Field(title='规格id')

        
class SUserFav(CreateUserFav):
    id: int

    class Config:
        orm_mode = True

class UserFav(CreateUserFav):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResUserFav(BaseModel):
    data: List[SUserFav]
    total: int
    
class CreateUserLevel(BaseModel):
    title: Optional[str]

        
class SUserLevel(CreateUserLevel):
    id: int

    class Config:
        orm_mode = True

class UserLevel(CreateUserLevel):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResUserLevel(BaseModel):
    data: List[SUserLevel]
    total: int
    
class CreateUserPaymentHistory(BaseModel):
    fee: Optional[int]
    create_time: Optional[datetime]
    description: Optional[str]

        
class SUserPaymentHistory(CreateUserPaymentHistory):
    id: int

    class Config:
        orm_mode = True

class UserPaymentHistory(CreateUserPaymentHistory):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResUserPaymentHistory(BaseModel):
    data: List[SUserPaymentHistory]
    total: int
    
class CreateUserPhoneCode(BaseModel):
    user_id: Optional[int]
    code: Optional[str] = Field(title='6位验证码')
    expired_time: Optional[int] = Field(title='按秒计算')
    send_time: Optional[datetime] = Field(title='短信发送时间')
    employee_id: Optional[int]
    store_owner_id: Optional[int] = Field(title='店主管id')
    worker_id: Optional[int] = Field(title='普通员工id')
    phone: Optional[str] = Field(title='电话号码')

        
class SUserPhoneCode(CreateUserPhoneCode):
    id: int

    class Config:
        orm_mode = True

class UserPhoneCode(CreateUserPhoneCode):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResUserPhoneCode(BaseModel):
    data: List[SUserPhoneCode]
    total: int
    
class CreateUserWithdraw(BaseModel):
    amount: Optional[int] = Field(title='提现金额，单位分')
    user_withdraw_status_id: Optional[int] = Field(title='状态0待审批1已经提现2已经驳回')
    create_time: Optional[datetime] = Field(title='申请时间')
    update_time: Optional[datetime] = Field(title='更新时间')
    user_id: Optional[int]
    type_id: Optional[int] = Field(title='提现类型')
    user_bank_id: Optional[str] = Field(title='当类型为银行卡时，该字段指向银行卡号，或支付宝账号')
    operator_id: Optional[int]
    fee_type: Optional[int] = Field(title='扣费类型')
    fee_pro: Optional[float] = Field(title='扣费比例')
    out_batch_no: Optional[str] = Field(title=' 商户系统内部的商家批次单号，要求此参数只能由数字、大小写字母组成，在商户系统内部唯一')
    batch_name: Optional[str] = Field(title='该笔批量转账的名称')
    batch_remark: Optional[str] = Field(title='转账说明，UTF8编码，最多允许32个字符')
    out_detail_no: Optional[str] = Field(title=' 商户系统内部区分转账批次单下不同转账明细单的唯一标识，要求此参数只能由数字、大小写字母组成')
    user_name: Optional[str] = Field(title=' 姓名')
    user_phone: Optional[str] = Field(title=' 电话')
    fee_balance: Optional[int] = Field(title='实际提现金额')
    deduct_balance: Optional[int] = Field(title='扣除或返锁定额金额')
    money_pic: Optional[str] = Field(title='截图回传')
    user_bank_other: Optional[str] = Field(title='关于账号其他备注信息')
    surp_balance: Optional[int] = Field(title='剩余余额')
    surp_local_balance: Optional[int] = Field(title='剩余推荐余额')

        
class SUserWithdraw(CreateUserWithdraw):
    id: int

    class Config:
        orm_mode = True

class UserWithdraw(CreateUserWithdraw):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResUserWithdraw(BaseModel):
    data: List[SUserWithdraw]
    total: int
    
class CreateUserWithdrawStatus(BaseModel):
    title: Optional[str]

        
class SUserWithdrawStatus(CreateUserWithdrawStatus):
    id: int

    class Config:
        orm_mode = True

class UserWithdrawStatus(CreateUserWithdrawStatus):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResUserWithdrawStatus(BaseModel):
    data: List[SUserWithdrawStatus]
    total: int
    
class CreateUserWithdrawType(BaseModel):
    title: Optional[str] = Field(title='标注')

        
class SUserWithdrawType(CreateUserWithdrawType):
    id: int

    class Config:
        orm_mode = True

class UserWithdrawType(CreateUserWithdrawType):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResUserWithdrawType(BaseModel):
    data: List[SUserWithdrawType]
    total: int
    
class CreateVideoArticle(BaseModel):
    type_id: Optional[int] = Field(title='文章分类id')
    description: Optional[str] = Field(title='详细描述')
    create_time: Optional[datetime] = Field(title='创建时间')
    operator_id: Optional[int] = Field(title='操作员ID')
    cover: Optional[str] = Field(title='封面图')
    cover_video: Optional[str] = Field(title='封面视频')
    is_del: Optional[int] = Field(title='是否删除,0正常,1删除')
    title: Optional[str] = Field(title='文章标题')
    title_tit: Optional[str] = Field(title='文章副标题')
    auther: Optional[str] = Field(title='作者')
    proc_id: Optional[int] = Field(title='礼包id')
    pic_id: Optional[int] = Field(title='0图片1视频')
    avatar: Optional[str] = Field(title='头像url')
    share_word: Optional[str] = Field(title='分享钩子语')
    share_label: Optional[str] = Field(title='分享标签，按逗号分割')
    share_title: Optional[str] = Field(title='微信分享标题')
    share_pic: Optional[str] = Field(title='分享卡片图')
    is_draft: Optional[int] = Field(title='是否是草稿,0正常,1是')
    video_level: Optional[int] = Field(title='默认0表示普通,1达人,2店长3,服务商,4分公司')
    order_id: Optional[int] = Field(title='排序id')

        
class SVideoArticle(CreateVideoArticle):
    id: int

    class Config:
        orm_mode = True

class VideoArticle(CreateVideoArticle):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResVideoArticle(BaseModel):
    data: List[SVideoArticle]
    total: int
    
class CreateVideoArticleList(BaseModel):
    type_id: Optional[int] = Field(title='文章内容类型,0可复制文本,1编辑器,2视频')
    article_id: Optional[int] = Field(title='所属video_article文章id')
    create_time: Optional[datetime] = Field(title='创建时间')
    operator_id: Optional[int] = Field(title='操作员ID')
    content: Optional[str] = Field(title='文章模块内容')
    is_del: Optional[int] = Field(title='是否删除,0正常,1删除')

        
class SVideoArticleList(CreateVideoArticleList):
    id: int

    class Config:
        orm_mode = True

class VideoArticleList(CreateVideoArticleList):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResVideoArticleList(BaseModel):
    data: List[SVideoArticleList]
    total: int
    
class CreateVideoArticleType(BaseModel):
    register_time: Optional[datetime] = Field(title='创建时间')
    title: Optional[str] = Field(title='类型标题')
    describe: Optional[str] = Field(title='类型描述')
    cover: Optional[str] = Field(title='封面图')

        
class SVideoArticleType(CreateVideoArticleType):
    id: int = Field(title='标识id')

    class Config:
        orm_mode = True

class VideoArticleType(CreateVideoArticleType):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResVideoArticleType(BaseModel):
    data: List[SVideoArticleType]
    total: int
    
class CreateVideoContent(BaseModel):
    register_time: Optional[datetime] = Field(title='创建时间')
    content_name: Optional[str] = Field(title='视频名称')
    content_url: Optional[str] = Field(title='视频播放URL（https开头完整路径）')
    group_id: Optional[int] = Field(title='所属分组id，t_video_group表id')

        
class SVideoContent(CreateVideoContent):
    id: int

    class Config:
        orm_mode = True

class VideoContent(CreateVideoContent):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResVideoContent(BaseModel):
    data: List[SVideoContent]
    total: int
    
class CreateVideoGroup(BaseModel):
    register_time: Optional[datetime] = Field(title='创建时间')
    group_name: Optional[str] = Field(title='分组名称')

        
class SVideoGroup(CreateVideoGroup):
    id: int

    class Config:
        orm_mode = True

class VideoGroup(CreateVideoGroup):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResVideoGroup(BaseModel):
    data: List[SVideoGroup]
    total: int
    
class CreateVideoRecharge(BaseModel):
    register_time: Optional[datetime] = Field(title='创建时间')
    good_id: Optional[int] = Field(title='礼包商品id')
    good_name: Optional[str] = Field(title='礼包名称')
    admin_name: Optional[str] = Field(title='操作员名字')
    user_id: Optional[int] = Field(title='指定用户id')
    user_phone: Optional[str] = Field(title='指定用户电话')
    user_name: Optional[str] = Field(title='指定指定用户昵称')
    video_level: Optional[int] = Field(title='视频分发身份0达人,1店长,2服务商,3分公司')
    level_id: Optional[int] = Field(title='用户等级 默认是0粉丝,1会员,2核心会员')
    create_nmu: Optional[int] = Field(title='本次生成总数')
    act_user_id: Optional[int] = Field(title='激活用户id')
    act_user_phone: Optional[str] = Field(title='激活用户电话')
    act_user_name: Optional[str] = Field(title='激活指定用户昵称')
    act_time: Optional[datetime] = Field(title='激活时间')
    is_act: Optional[int] = Field(title='是否被激活,0未激活,1已激活')
    act_code: Optional[str] = Field(title='激活码')
    batch_code: Optional[str] = Field(title='创建批次码')

        
class SVideoRecharge(CreateVideoRecharge):
    id: int = Field(title='标识id')

    class Config:
        orm_mode = True

class VideoRecharge(CreateVideoRecharge):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResVideoRecharge(BaseModel):
    data: List[SVideoRecharge]
    total: int
    
class CreateVideoRechargeLog(BaseModel):
    user_id: Optional[int] = Field(title='激活用户id')
    user_nick: Optional[str] = Field(title='激活用户昵称')
    phone: Optional[str] = Field(title='激活用户联系方式')
    change: Optional[int] = Field(title='变动条数')
    balance: Optional[int] = Field(title='剩余条数')
    type: Optional[str] = Field(title='类型')
    description: Optional[str] = Field(title='详细描述')
    create_time: Optional[datetime] = Field(title='创建时间')
    operator_id: Optional[int] = Field(title='操作员ID')
    out_trade_no: Optional[str]
    good_id: Optional[str] = Field(title='收益商品id')
    good_title: Optional[str] = Field(title='收益商品标题名称')
    good_num: Optional[str] = Field(title='收益商品数量')
    recharge_id: Optional[int] = Field(title='充值礼包ID')
    owner_id: Optional[int] = Field(title='码主用户id')
    owner_nick: Optional[str] = Field(title='码主用户昵称')
    owner_phone: Optional[str] = Field(title='码主用户联系方式')

        
class SVideoRechargeLog(CreateVideoRechargeLog):
    id: int

    class Config:
        orm_mode = True

class VideoRechargeLog(CreateVideoRechargeLog):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResVideoRechargeLog(BaseModel):
    data: List[SVideoRechargeLog]
    total: int
    
class CreateVideoTask(BaseModel):
    register_time: Optional[datetime] = Field(title='创建时间')
    title: Optional[str] = Field(title='任务标题')
    describe: Optional[str] = Field(title='任务描述,任务要求')
    top: Optional[int] = Field(title='任务领取上限')
    big: Optional[int] = Field(title='单号最大领取量')
    received: Optional[int] = Field(title='已领取量')
    money: Optional[int] = Field(title='获得任务金额')
    coin: Optional[int] = Field(title='获得任务购物券')
    shoper_id: Optional[int] = Field(title='所属商家id')
    shoper_name: Optional[str] = Field(title='分发商名称')
    shoper_phone: Optional[str] = Field(title='分发商电话')
    stat: Optional[int] = Field(title='0未开启,1进行中,2已结束')
    style: Optional[str] = Field(title='参考图样地址七牛oss,逗号分割多个图样地址')
    verfy: Optional[str] = Field(title='平台名称抖音,小红书,视频号,快手,朋友圈')
    run_time: Optional[datetime] = Field(title='开始时间')
    expired_time: Optional[datetime] = Field(title='结束时间')
    is_auto: Optional[int] = Field(title='是否自动处理状态,0自动,1手动')
    cover: Optional[str] = Field(title='封面图')
    local_path: Optional[str] = Field(title='素材在本地地址')
    update_time: Optional[datetime] = Field(title='更新时间')
    type_id: Optional[int] = Field(title='所属类型id类型,0图片1视频2音频')
    show_money: Optional[int] = Field(title='显示售价')
    prop_one: Optional[float] = Field(title='佣金分成比值')
    des_sp: Optional[str] = Field(title='视频文案')
    des_sp_link: Optional[str] = Field(title='视频文案链接')
    des_kou: Optional[str] = Field(title='口播文案')
    audit: Optional[int] = Field(title='0未审核,1通过审核,2未通过')
    audit_time: Optional[datetime] = Field(title='审核时间')
    audit_adm: Optional[int] = Field(title='审核管理人id')
    audit_info: Optional[str] = Field(title='审核备注100个汉字以内')
    finish_id: Optional[int] = Field(title='成品视频素材id')
    synth_id: Optional[int] = Field(title='合成视频素材id')
    day_top: Optional[int] = Field(title='用户每日任务领取上限')
    video_num: Optional[int] = Field(title='视频领取数量')
    pic_num: Optional[int] = Field(title='图片领取数量')
    music_num: Optional[int] = Field(title='音频领取数量')
    class_id: Optional[int] = Field(title='所属分类')
    rem_money: Optional[int] = Field(title='推荐人金额')
    rem_mid_money: Optional[int] = Field(title='间推人金额')
    rem_team: Optional[int] = Field(title='推荐团长金额')
    rem_mid_team: Optional[int] = Field(title='间推团长金额')
    live_mid_uid: Optional[int] = Field(title='居间人id')
    live_mid_money: Optional[int] = Field(title='居间人收益')

        
class SVideoTask(CreateVideoTask):
    id: int = Field(title='标识id')

    class Config:
        orm_mode = True

class VideoTask(CreateVideoTask):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResVideoTask(BaseModel):
    data: List[SVideoTask]
    total: int
    
class CreateVideoTaskMaterial(BaseModel):
    register_time: Optional[datetime] = Field(title='创建时间')
    task_id: Optional[int] = Field(title='参与任务id')
    path: Optional[str] = Field(title='素材七牛地址')
    m_type: Optional[int] = Field(title='素材类型,0图片1视频2音频')
    update_time: Optional[datetime] = Field(title='截图更新时间')
    is_del: Optional[int] = Field(title='是否删除,0正常1删除')
    ma_name: Optional[str] = Field(title='素材名称')
    ma_info: Optional[str] = Field(title='备注信息')
    bag_id: Optional[int] = Field(title='素材包id')
    is_download: Optional[int] = Field(title='是否下载,0正常1已下载')
    down_time: Optional[datetime] = Field(title='下载更新时间')
    user_id: Optional[int] = Field(title='领取用户id')

        
class SVideoTaskMaterial(CreateVideoTaskMaterial):
    id: int = Field(title='标识id')

    class Config:
        orm_mode = True

class VideoTaskMaterial(CreateVideoTaskMaterial):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResVideoTaskMaterial(BaseModel):
    data: List[SVideoTaskMaterial]
    total: int
    
class CreateVideoTaskMaterialBag(BaseModel):
    register_time: Optional[datetime] = Field(title='创建时间')
    task_id: Optional[int] = Field(title='参与任务id')
    update_time: Optional[datetime] = Field(title='截图更新时间')
    is_del: Optional[int] = Field(title='是否删除,0正常1删除')
    bag_name: Optional[str] = Field(title='素材包名称')

        
class SVideoTaskMaterialBag(CreateVideoTaskMaterialBag):
    id: int = Field(title='标识id')

    class Config:
        orm_mode = True

class VideoTaskMaterialBag(CreateVideoTaskMaterialBag):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResVideoTaskMaterialBag(BaseModel):
    data: List[SVideoTaskMaterialBag]
    total: int
    
class CreateVideoTaskReceive(BaseModel):
    register_time: Optional[datetime] = Field(title='创建时间')
    task_id: Optional[int] = Field(title='参与任务id')
    shoper_id: Optional[int] = Field(title='所属商家id')
    shoper_name: Optional[str] = Field(title='分发商名称')
    shoper_phone: Optional[str] = Field(title='分发商电话')
    user_id: Optional[int] = Field(title='用户id')
    user_name: Optional[str] = Field(title='昵称')
    user_phone: Optional[str] = Field(title='联系方式')
    title: Optional[str] = Field(title='任务标题')
    up_pic: Optional[str] = Field(title='任务上传截图')
    audit_comment: Optional[str] = Field(title='审核评论内容')
    audit_status: Optional[int] = Field(title='状态,0领取,1待审核,2审核通过,3审核未通过')
    update_time: Optional[datetime] = Field(title='截图更新时间')
    audit_time: Optional[datetime] = Field(title='管理审核时间')
    bag_id: Optional[int] = Field(title='素材包id')
    audit_adm: Optional[int] = Field(title='审核管理人id')
    audit_info: Optional[str] = Field(title='审核备注100个汉字以内')
    mater_id: Optional[int] = Field(title='领取素材id')
    mater_path: Optional[str] = Field(title='领取素材地址')
    get_time: Optional[datetime] = Field(title='领取时间')
    money_status: Optional[int] = Field(title='状态,0待分润,1已分润')

        
class SVideoTaskReceive(CreateVideoTaskReceive):
    id: int = Field(title='标识id')

    class Config:
        orm_mode = True

class VideoTaskReceive(CreateVideoTaskReceive):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResVideoTaskReceive(BaseModel):
    data: List[SVideoTaskReceive]
    total: int
    
class CreateVideoTaskType(BaseModel):
    register_time: Optional[datetime] = Field(title='创建时间')
    title: Optional[str] = Field(title='类型标题')
    describe: Optional[str] = Field(title='类型描述')
    cover: Optional[str] = Field(title='封面图')

        
class SVideoTaskType(CreateVideoTaskType):
    id: int = Field(title='标识id')

    class Config:
        orm_mode = True

class VideoTaskType(CreateVideoTaskType):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterResVideoTaskType(BaseModel):
    data: List[SVideoTaskType]
    total: int
    