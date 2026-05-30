import traceback

from config import MYSQL

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{MYSQL.username}:{MYSQL.password}@{MYSQL.host}:{MYSQL.port}/{MYSQL.db}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600
    # echo=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Dao:
    def __enter__(self) -> Session:
        self.sess: Session = SessionLocal()
        return self.sess

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            self.sess.rollback()
            traceback.print_exception(exc_type, exc_value, tb)
        self.sess.close()

