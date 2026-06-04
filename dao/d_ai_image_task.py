import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from model.schema import TAiImageTask
from common.db import engine

logger = logging.getLogger(__name__)
Session = sessionmaker(bind=engine)


def create_image_task(userid: str, task_id: str) -> TAiImageTask:
    """
    创建图片生成任务记录，qiniu_url 默认为'生成中'
    """
    sess = Session()
    try:
        record = TAiImageTask(userid=userid, task_id=task_id, qiniu_url='生成中')
        sess.add(record)
        sess.commit()
        sess.refresh(record)
        logger.info(f"创建图片任务记录: userid={userid}, task_id={task_id}")
        return record
    except Exception as e:
        sess.rollback()
        logger.error(f"创建图片任务记录失败: {e}")
        raise
    finally:
        sess.close()


def get_pending_tasks_by_userid(userid: str) -> list:
    """
    查询某用户下 qiniu_url='生成中' 的待处理任务列表
    返回字典列表，避免 session 关闭后 ORM 对象属性过期
    """
    sess = Session()
    try:
        records = sess.query(TAiImageTask).filter(
            TAiImageTask.userid == userid,
            TAiImageTask.qiniu_url == '生成中'
        ).all()
        return [{"task_id": r.task_id, "qiniu_url": r.qiniu_url} for r in records]
    finally:
        sess.close()


def update_task_qiniu_url(task_id: str, qiniu_url: str) -> bool:
    """
    根据 task_id 更新对应记录的 qiniu_url
    """
    sess = Session()
    try:
        record = sess.query(TAiImageTask).filter(TAiImageTask.task_id == task_id).first()
        if not record:
            logger.warning(f"更新任务qiniu_url失败: task_id={task_id} 不存在")
            return False
        record.qiniu_url = qiniu_url
        sess.commit()
        logger.info(f"更新任务qiniu_url: task_id={task_id}, qiniu_url={qiniu_url[:50]}...")
        return True
    except Exception as e:
        sess.rollback()
        logger.error(f"更新任务qiniu_url异常: {e}")
        return False
    finally:
        sess.close()


def get_all_tasks_by_userid(userid: str) -> list:
    """
    查询某用户下所有任务记录，返回 task_id 和 qiniu_url 列表
    """
    sess = Session()
    try:
        records = sess.query(TAiImageTask).filter(
            TAiImageTask.userid == userid
        ).order_by(TAiImageTask.id.asc()).all()
        return [{"task_id": r.task_id, "qiniu_url": r.qiniu_url} for r in records]
    finally:
        sess.close()
