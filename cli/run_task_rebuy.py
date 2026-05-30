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
from dao import d_bigorder

def main():
    # d_task.run_task_auto_stat()
    # d_task.run_taskuser_auto_retract()
    # d_task.init_bigorder_two()
    d_bigorder.san_rebuy_list()

if __name__ == '__main__':
    main()