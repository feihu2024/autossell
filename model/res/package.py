from typing import List, Optional

from pydantic import BaseModel, Field
from model.m_schema import SPackage, SPackageTime, SGood, SGoodSpec, SPackageTimePair


class PackageTimePairData(BaseModel):
    package: Optional[SPackage] = Field(..., title='秒杀包')
    package_time_pair: Optional[SPackageTimePair] = Field(..., title='秒杀包时间对')
    package_time: Optional[SPackageTime] = Field(..., tilte='秒杀包时间')
    good: Optional[SGood] = Field(..., title='商品')
    good_spec: Optional[SGoodSpec] = Field(..., title='商品规格')


class PackageTimePairRes(BaseModel):
    data: List[PackageTimePairData] = Field(..., title='秒杀包时间对列表')
    total: int = Field(..., title='总数')


class PackageData(BaseModel):
    package: Optional[SPackage] = Field(..., title='秒杀包')
    good: Optional[SGood] = Field(..., title='商品')
    good_spec: Optional[SGoodSpec] = Field(..., title='商品规格')

class PackageRes(BaseModel):
    data: List[PackageData] = Field(..., title='秒杀包列表')
    total: int = Field(..., title='总数')