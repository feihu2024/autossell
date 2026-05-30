from pydantic import BaseModel, Field

from typing import List, Optional, Literal

class PackageTimePairUpdate(BaseModel):
    package_id: int = Field(..., title='秒杀包id')
    package_time_id: int = Field(..., title='秒杀包时间id')
    status: Literal[0, 1] = Field(..., title='秒杀包时间对状态; 0或者null: 未开始, 1: 进行中')
    package_num: int = Field(..., title='此时段秒杀包库存')