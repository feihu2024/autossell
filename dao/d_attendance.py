from common import dao
from sqlalchemy.orm import Session
from model.schema import TUser, TAttendance


@dao
def get_attendance_by_id(attendance_id: int,
                         db: Session):
    return db.query(TAttendance).where(TAttendance.id == attendance_id).first()


@dao
def get_attendance_by_username(username: str, db: Session):
    return db.query(TAttendance).where(TUser.username == username).all()
