from datetime import datetime

from sqlalchemy.orm import Session

from model.schema import TBalance, TUserAccount, TLockBalance, TCoin
from dao import d_user


def balance_change(user_id: int, fee: int, category: str, description: str, db: Session):
    account = db.query(TUserAccount).filter(TBalance.user_id == user_id).first()
    if account is None:
        account = TUserAccount(
            user_id=user_id,
            balance=fee,
            lock_balance=0,
            coin=0,
            create_time=datetime.now(),
            update_time=datetime.now())
        db.add(account)
        db.flush()
    else:
        account.balance += fee
        db.flush()
    db.refresh(account)

    t_balance = TBalance(change=fee, type=category, description=description, user_id=user_id, balance=account.balance)
    db.add(t_balance)
    db.flush()
    db.refresh(t_balance)


def lock_balance_change(user_id: int, fee: int, category: str, description: str, db: Session):
    account = db.query(TUserAccount).filter(TBalance.user_id == user_id).first()
    if account is None:
        account = TUserAccount(
            user_id=user_id,
            balance=0,
            lock_balance=fee,
            coin=0,
            create_time=datetime.now(),
            update_time=datetime.now())
        db.add(account)
        db.flush()
    else:
        account.lock_balance += fee
        db.flush()
    db.refresh(account)

    t_lock_balance = TLockBalance(change=fee, type=category, description=description, user_id=user_id,
                                  lock_balance=account.lock_balance)
    db.add(t_lock_balance)
    db.flush()
    db.refresh(t_lock_balance)


def coin_change(user_id: int, fee: int, category: str, description: str, db: Session):
    account = db.query(TUserAccount).filter(TBalance.user_id == user_id).first()
    if account is None:
        account = TUserAccount(
            user_id=user_id,
            balance=0,
            lock_balance=0,
            coin=fee,
            create_time=datetime.now(),
            update_time=datetime.now())
        db.add(account)
        db.flush()
    else:
        account.coin += fee
        db.flush()
    db.refresh(account)

    t_coin = TCoin(change=fee, type=category, description=description, user_id=user_id, coin=account.coin)
    db.add(t_coin)
    db.flush()
    db.refresh(t_coin)
