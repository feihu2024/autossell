# coding: utf-8
from datetime import datetime
from pydantic import BaseModel, Field
from sqlalchemy import Column, DECIMAL, Float, Integer, String, TIMESTAMP, Text, text
from sqlalchemy.ext.declarative import declarative_base
from typing import Optional
from sqlalchemy.dialects.mysql import LONGTEXT, MEDIUMTEXT, TINYINT, VARCHAR

Base = declarative_base()
metadata = Base.metadata

class SaveSucai(BaseModel):
    task_id: Optional[int] = Field(title='参与任务id', default=0)
    sucai_id: Optional[int] = Field(title='创建过token的返回id', default=0)
    topic_id: Optional[int] = Field(title='所属话题id', default=0)
    task_url: Optional[str] = Field(title='七牛oss素材地址', default=None)

class SaveReason(BaseModel):
    task_id: Optional[int] = Field(title='参与任务id', default=0)
    sucai_id: Optional[int] = Field(title='素材id', default=0)
    link_stat: Optional[int] = Field(title='链接审核状态,0未操作,1链接未审核,2链接已审核', default=0)
    nopass: Optional[str] = Field(title='不合格原因选项', default=None)
    nopass_txt: Optional[str] = Field(title='不合格原因文本', default=None)

class SaveTopic(BaseModel):
    task_id: Optional[int] = Field(title='参与任务id', default=0)
    tp_id: Optional[int] = Field(title='话题id', default=0)
    topic_name: Optional[str] = Field(title='任务话题内容', default=None)
    topic_comment: Optional[str] = Field(title='任务评论内容', default=None)


class CreateTask(BaseModel):
    title: Optional[str] = Field(title='任务标题')
    describe: Optional[str] = Field(title='任务描述')
    top: Optional[int] = Field(title='任务上限')
    big: Optional[int] = Field(title='单号最大领取量')
    style: Optional[str] = Field(title='图样地址七牛oss,逗号分割多个图样地址')
    run_time: Optional[datetime] = Field(title='进行中时间')
    clock_time: Optional[datetime] = Field(title='打卡时间')
    expired_time: Optional[datetime] = Field(title='结束时间')
    ctype: Optional[int] = Field(title='任务分类,0表示视频类,1表示图文类')
    islink: Optional[int] = Field(title='是否开启链接上传,0否,1是')
    start_time: Optional[datetime] = Field(title='开始时间')
    is_auto: Optional[int] = Field(title='是否自动处理状态,0自动,1手动')
    cover: Optional[str] = Field(title='封面图')

class STask(CreateTask):
    id: int = Field(title='标识id')

    class Config:
        orm_mode = True

#用户打卡表
class UserTaskclockup(BaseModel):
    id: Optional[int] = Field(title='标识id，修改时传递', default=0)
    task_id: Optional[int] = Field(title='参与任务id')
    sucai_id: Optional[int] = Field(title='素材id')
    topic_id: Optional[int] = Field(title='话题id')
    user_id: Optional[int] = Field(title='参与会员id')
    ctype: Optional[int] = Field(title='任务分类,0表示视频截图类,1表示图文类')
    content: Optional[str] = Field(title='截图地址或图文内容')
    verfy_name: Optional[str] = Field(title='平台名称')
    stat_count: Optional[int] = Field(title='流量，统计浏览次数', default=0)
    user_acc: Optional[str] = Field(title='打卡平台账号', default=None)

class GetTaskuser(BaseModel):
    # id = Column(Integer, primary_key=True, comment='标识id')
    task_id: Optional[int] = Field(title='参与任务id')
    # sucai_id = Column(Integer, comment='素材id')
    topic_id: Optional[int] = Field(title='话题id')
    user_id: Optional[int] = Field(title='参与会员id')
    # user_time = Optional[datetime] = Field(title='领取时间')
    phone: Optional[str] = Field(title='联系方式')
    address: Optional[str] = Field(title='地址')

class GroupSir(BaseModel):
    user_id: Optional[int] = Field(title='用户id')
    group_id: Optional[int] = Field(title='团长id', default=0)
    is_group: Optional[int] = Field(title='是否设置为团长：0表示普通人员，1表示团长', default=0)
    phone: Optional[str] = Field(title='联系方式')
    username: Optional[str] = Field(title='团长名')
    email: Optional[str] = Field(title='邮箱')

class ShengDai(BaseModel):
    user_id: Optional[int] = Field(title='用户id')
    level_shengdai: Optional[int] = Field(title='省代值', default=0)
