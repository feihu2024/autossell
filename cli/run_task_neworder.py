import datetime,time,sys,math,json
from pathlib import Path
from sqlalchemy import or_
root_dir = Path(__file__).parents[1]
model_dir = root_dir / 'model'
#print(root_dir)
# print(model_dir)
sys.path.append(str(root_dir))

# from common import Dao, global_define
#from common.global_define import *
from model import schema, m_schema

from dao.task import d_task
from dao import d_bigorder, d_user

def main():
    # 重排大公排，剔除空余排序会员
    # d_bigorder.scan_anddel_bigorders()
    # 重新计算用户级别
    d_user.update_user_level()

if __name__ == '__main__':
    main()