from common import Dao
from model.mall import m_account
from model.schema import TUserAccount, TUserBank, TCoin, TBalance, TUser, TUserWithdraw, TLockBalance, TTranAccount, TRoomgold, TRoomContributelog, TFundPond
import time, datetime, math
from sqlalchemy import or_
from dao import d_db, d_user
from model.m_schema import CreateRoomgold
from common.global_define import room_config, balance_type

def create_account(item: m_account.TUserAccount):
    with Dao() as db:
        db.add(item)
        db.commit()
        db.refresh(item)
    return item


def delete_account_by_id(account_id: int):
    with Dao() as db:
        db.query(TUserAccount).where(TUserAccount.id == account_id).delete()
        db.commit()


def update_account_by_id(account_id: int, item: dict):
    with Dao() as db:
        if item.get("id"):
            item.pop("id")
        db.query(TUserAccount).where(TUserAccount.id == account_id).update(item)
        db.commit()

def update_account_balance(user_id: int, balance: int):
    with Dao() as db:
        db.query(TUserAccount).where(TUserAccount.user_id == user_id).update({"balance": balance, "update_time":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())})
        db.commit()

def update_account_coin(user_id: int, coin: int):
    with Dao() as db:
        db.query(TUserAccount).where(TUserAccount.user_id == user_id).update({"coin": coin, "update_time":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())})
        db.commit()

def get_account_info(user_id:int = 0):
    with Dao() as db:
        return db.query(TUserAccount).filter(TUserAccount.user_id == user_id).first()

def get_account_info_add(user_id:int = 0):
    if user_id is None:
        user_id = 0
    with Dao() as db:
        account_info = db.query(TUserAccount).filter(TUserAccount.user_id == user_id).first()
        if not account_info and user_id > 0:
            account_info = create_account(TUserAccount(
                user_id = user_id,
                balance = 0,
                lock_balance = 0,
                coin = 0,
                create_time = datetime.datetime.now()
            ))
        return account_info

def get_acount_list(user_id:int):
    with Dao() as db:
        #q = db.query(TUserAccount)
        #t_acount_list = q.where(TUserAccount.user_id == user_id).all()
        q = db.query(TUserBank)
        t_acount_list = q.where(TUserBank.user_id == user_id).all()
        return t_acount_list

def get_coin_balance_list(user_id:int):
    with Dao() as db:
        q = db.query(TUserAccount)
        t_acount_list = q.where(TUserAccount.user_id == user_id).all()
        return t_acount_list

def get_coin_balance(user_id:int):
    with Dao() as db:
        return db.query(TUserAccount).where(TUserAccount.user_id == user_id).first()

def update_bank(account_id: int, item: dict):
    with Dao() as db:
        if item.get("id"):
            item.pop("id")
        db.query(TUserBank).where(TUserBank.id == account_id).update(item)
        db.commit()

def insert_coin(items: m_account.CoinModel):
    add_instance = TCoin(
        user_id=items.user_id,
        change=items.change,
        coin=items.coin,
        type=items.type,
        create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        description=items.description,
        out_trade_no=items.out_trade_no
    )
    with Dao() as db:
        db.add(add_instance)
        db.commit()

def insert_bank(items: m_account.BalanceModel):
    add_instance = TBalance(
        user_id=items.user_id,
        change=items.change,
        balance=items.balance,
        type="manager",
        create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    )
    with Dao() as db:
        db.add(add_instance)
        db.commit()

def add_balance(items: m_account.BalanceModel):
    add_instance = TBalance(
        user_id=items.user_id,
        change=items.change,
        balance=items.balance,
        type=items.type,
        create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        good_id=items.good_id,
        good_title=items.good_title,
        good_num=items.good_num,
        out_trade_no=items.out_trade_no

    )
    with Dao() as db:
        db.add(add_instance)
        db.commit()

def add_lock_balance(items: m_account.LockBalanceModel):
    add_instance = TLockBalance(
        user_id=items.user_id,
        change=items.change,
        lock_balance=items.lock_balance,
        type=items.type,
        create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        out_trade_no=items.out_trade_no
    )
    with Dao() as db:
        db.add(add_instance)
        db.commit()

#增加会员优惠券
def add_grant_num(user_id:int, grant_num:int = 0, bagid:int = 0, bag_num:int = 1, out_trade_no:str = '', bag_name:str = ''):
    account_info = get_account_info(user_id)
    if account_info:
        total_grant_num = account_info.coin + grant_num
        with Dao() as db:
            db.query(TUserAccount).where(TUserAccount.user_id == user_id).update({"coin": total_grant_num})
            db.commit()

        description_str = str(bagid) + bag_name
        coin_record = TCoin(
            change=grant_num,
            user_id=user_id,
            coin=total_grant_num,
            create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            out_trade_no=out_trade_no,
            description=description_str,
            type=balance_type[10]
        )
        insert_coin(coin_record)


def get_user_withdraw(withdraw_id:int):
    with Dao() as db:
        res = db.query(TUserWithdraw, TUser, TUserAccount) \
            .outerjoin(TUser, TUserWithdraw.user_id == TUser.id) \
            .outerjoin(TUserAccount, TUserWithdraw.user_id == TUserAccount.user_id) \
            .filter(TUserWithdraw.id == withdraw_id).first()
        return res

def update_user_withdraw_status(withdraw_id:int, user_withdraw_status_id:int):
    with Dao() as db:
        db.query(TUserWithdraw).where(TUserWithdraw.id == withdraw_id).update({"user_withdraw_status_id": user_withdraw_status_id})
        db.commit()

def update_user_withdraw_balance(withdraw_id:int, fee_balance:int, deduct_balance:int):
    with Dao() as db:
        db.query(TUserWithdraw).where(TUserWithdraw.id == withdraw_id).update({"fee_balance": fee_balance, "deduct_balance": deduct_balance})
        db.commit()

def update_user_withdraw_balance_pic(withdraw_id:int, moneypic:str):
    with Dao() as db:
        db.query(TUserWithdraw).where(TUserWithdraw.id == withdraw_id).update({"money_pic": moneypic})
        db.commit()

def add_tran_log(user_ou:int, user_out_phone:str, user_out_name:str, user_out_balance:int, user_get:int, user_get_phone:str, user_get_name:str, user_get_balance:int, balance:int):
    add_instance = TTranAccount(
        user_out=user_ou,
        user_out_phone=user_out_phone,
        user_out_name=user_out_name,
        user_out_balance=user_out_balance,
        user_get=user_get,
        user_get_phone=user_get_phone,
        user_get_name=user_get_name,
        user_get_balance=user_get_balance,
        balance=balance
    )
    with Dao() as db:
        db.add(add_instance)
        db.commit()

#############################会员房间处理功能################################################################
def getuser_rooms(user_id: int, is_ing:int = 0):
    with Dao() as db:
        q = db.query(TRoomgold)
        if is_ing:
            t_list = q.filter(or_(TRoomgold.position_one == user_id, TRoomgold.position_two == user_id,TRoomgold.position_three == user_id, \
                                  TRoomgold.position_four == user_id, TRoomgold.position_five == user_id,TRoomgold.position_six == user_id, \
                                  TRoomgold.position_seven == user_id)).order_by(TRoomgold.id.desc()).all()
        else:
            # 进行中房间
            t_list = q.filter(or_(TRoomgold.position_one == user_id, TRoomgold.position_two == user_id,TRoomgold.position_three == user_id, \
                                  TRoomgold.position_four == user_id, TRoomgold.position_five == user_id,TRoomgold.position_six == user_id, \
                                  TRoomgold.position_seven == user_id)).filter(TRoomgold.status_val == 1).order_by(TRoomgold.id.desc()).first()
        return t_list

#加入房间
def join_roomgold(room_id:int, user_id:int):
    room_rs = d_db.get_roomgold(room_id)
    update_js = {}
    re_position = 0
    if room_rs:
        is_end = False
        if room_rs.position_two <= 0:
            update_js['position_two'] = user_id
            update_js['position_two_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            re_position = 2
        elif room_rs.position_three <=0:
            update_js['position_three'] = user_id
            update_js['position_three_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            re_position = 3
        elif room_rs.position_four <= 0:
            update_js['position_four'] = user_id
            update_js['position_four_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            re_position = 4
        elif room_rs.position_five <= 0:
            update_js['position_five'] = user_id
            update_js['position_five_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            re_position = 5
        elif room_rs.position_six <= 0:
            update_js['position_six'] = user_id
            update_js['position_six_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            re_position = 6
        elif room_rs.position_seven <= 0:
            update_js['position_seven'] = user_id
            update_js['position_seven_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            re_position = 7
            is_end = True
        with Dao() as db:
            db.query(TRoomgold).where(TRoomgold.id == room_id).update(update_js)
            db.commit()
        # d_db.update_roomgold(room_rs)
        if is_end:
            #分裂房间
            achieve_room_user(room_id)
    return re_position

#分红、分裂房间
def achieve_room_user(room_id:int):
    room_info = d_db.get_roomgold(room_id)
    if room_info:
        if room_info.status_val == 1:
            #修改房间状态
            update_room_status(room_id, 2)
            invited_balance = round(room_info.balance * room_config['room_bouns'] / 100)
            # user_balance = room_info.balance - invited_balance
            user_balance = room_info.balance
            income_users = []
            # arr = [[2, 1], [1, 2], [0, 3], [0, 4], [1, 5], [2, 6], [2, 7]]
            # sorted_arr = sorted(arr, key=lambda x: x[0])
            # [[0, 3], [0, 4], [1, 2], [1, 5], [2, 1], [2, 6], [2, 7]]
            # arr = sorted(arr, key=lambda x: (x[0], -x[1])) 第一列升序，第二列降序
            # [[0, 4], [0, 3], [1, 5], [1, 2], [2, 7], [2, 6], [2, 1]]
            # sorted_arr[-1]       --------------   sorted_arr[-7]
            users_arr = [[room_info.contribute_one, room_info.position_one],[room_info.contribute_two, room_info.position_two],\
                         [room_info.contribute_three, room_info.position_three],[room_info.contribute_four, room_info.position_four],\
                         [room_info.contribute_five, room_info.position_five],[room_info.contribute_six, room_info.position_six],\
                         [room_info.contribute_seven, room_info.position_seven]]
            # users_arr = sorted(users_arr, key=lambda x: x[0])
            users_arr = sorted(users_arr, key=lambda x: (x[0], -x[1]))
            #房间谁 贡献值高给谁。贡献值一样的情况下 。按照位置。 从上到下 从左到右判定
            #后面的逻辑是 谁拿了分红 谁去推荐人所在的房间。
            #对剩下这6个，两个贡献值最高的，然后各占领一个房间的最高位。然后剩下那俩就按照这个一高一低，然后一左一右这种分配就行了。
            # 团队一：users_arr[-2],users_arr[-7], users_arr[-5]
            d_user.update_user_parent(users_arr[-2][1])
            d_user.update_user_parent(users_arr[-7][1], users_arr[-2][1])
            d_user.update_user_parent(users_arr[-5][1], users_arr[-2][1])
            room_new = create_roomgold(users_arr[-2][1], room_info.id)
            if users_arr[-2][0] > 0:
                update_contribute_to_room(room_new.id, users_arr[-2][1], users_arr[-2][0])
            position_id = join_roomgold(room_new.id, users_arr[-7][1])
            if users_arr[-7][0] > 0:
                update_contribute_to_room(room_new.id, users_arr[-7][1], users_arr[-7][0], position_id)
            position_id = join_roomgold(room_new.id, users_arr[-5][1])
            if users_arr[-5][0] > 0:
                update_contribute_to_room(room_new.id, users_arr[-5][1], users_arr[-5][0], position_id)

            # 团队二：users_arr[-3],users_arr[-6], users_arr[-4]
            d_user.update_user_parent(users_arr[-3][1])
            d_user.update_user_parent(users_arr[-6][1], users_arr[-3][1])
            d_user.update_user_parent(users_arr[-4][1], users_arr[-3][1])
            room_new = create_roomgold(users_arr[-3][1], room_info.id)
            if users_arr[-3][0] > 0:
                update_contribute_to_room(room_new.id, users_arr[-3][1], users_arr[-3][0])
            position_id = join_roomgold(room_new.id, users_arr[-6][1])
            if users_arr[-6][0] > 0:
                update_contribute_to_room(room_new.id, users_arr[-6][1], users_arr[-6][0], position_id)
            position_id = join_roomgold(room_new.id, users_arr[-4][1])
            if users_arr[-4][0] > 0:
                update_contribute_to_room(room_new.id, users_arr[-4][1], users_arr[-4][0], position_id)

            #分红，并处理分红人进入房间
            u_info = d_user.get_user_by_id(users_arr[-1][1])
            if u_info:
                income_users.append(u_info.id)
                u_account = get_account_info_add(u_info.id)
                total_balance = user_balance + u_account.balance
                update_account_balance(u_info.id, total_balance)
                add_instance = TBalance(
                    user_id=u_info.id,
                    change=user_balance,
                    balance=total_balance,
                    type=balance_type[2],
                    create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    good_id=room_info.id
                    # good_title=f"房间{room_info.id}",
                    # good_num=items.good_num,
                    # out_trade_no=items.out_trade_no

                )
                with Dao() as db:
                    db.add(add_instance)
                    db.commit()
                #推荐人收益
                invited_info = d_user.get_user_by_id(u_info.invited_user_id)
                if invited_info:
                    income_users.append(invited_info.id)
                    u_account = get_account_info_add(invited_info.id)
                    total_balance = invited_balance + u_account.balance
                    update_account_balance(invited_info.id, total_balance)
                    add_instance = TBalance(
                        user_id=invited_info.id,
                        change=invited_balance,
                        balance=total_balance,
                        type=balance_type[7],
                        create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                        good_id=room_info.id
                        # good_title=f"房间{room_info.id}",
                        # good_num=items.good_num,
                        # out_trade_no=items.out_trade_no

                    )
                    with Dao() as db:
                        db.add(add_instance)
                        db.commit()
                    #加入推荐人房间，并给推荐人增加1个贡献值
                    invited_room = getuser_rooms(u_info.invited_user_id)
                    if invited_room:
                        #增加推人贡献值
                        update_contribute(u_info.id, room_config['contribute'])
                        # 创建或加入房间
                        # order_roomgold(user_id)
                        join_roomgold(invited_room.id, u_info.id)
                else:
                    #创建新房间
                    create_roomgold(u_info.id, room_info.id)



#更新房间状态
def update_room_status(room_id:int, status_id:int):
    with Dao() as db:
        db.query(TRoomgold).where(TRoomgold.id == room_id).update({"status_val": status_id})
        db.commit()

#创建房间
def create_roomgold(user_id:int, parent_room_id:int = 0):
    insert_res = d_db.insert_roomgold(CreateRoomgold(
        level=1,
        start_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        status_val=1,
        balance=room_config['room_balance'],
        partner_id=parent_room_id,
        position_one=user_id,
        position_one_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    ))
    return insert_res

def order_roomgold(user_id:int):
    user_info = d_user.get_user_by_id(user_id)
    if user_info:
        # if user_info.invited_user_id:  #有推荐人，下级用户操作
        if user_info.parent_id:  #有上级，下级用户操作
            user_room = getuser_rooms(user_info.parent_id)
            if user_room:
                join_roomgold(user_room.id, user_id)
        else:
            create_roomgold(user_id)

#增加贡献值
def update_contribute(user_id: int, con_num: int):
    user_info = d_user.get_user_by_id(user_id)
    cont_user_id = user_id
    if user_info.invited_user_id > 0:
        cont_user_id = user_info.invited_user_id
    room_info = getuser_rooms(cont_user_id)
    if room_info:
        no_use = True
        #给自己增加贡献值
        for i in range(1, 8):
            if i == 1:
                if room_info.position_one == cont_user_id:
                    if room_info.contribute_one < room_config['max_contribute']:
                        update_contribute_to_room(room_info.id, user_id, con_num, 1)
                        no_use = False
            elif i == 2 and no_use:
                if room_info.position_two == cont_user_id:
                    if room_info.contribute_two < room_config['max_contribute']:
                        update_contribute_to_room(room_info.id, user_id, con_num, 2)
                        no_use = False
            elif i == 3 and no_use:
                if room_info.position_three == cont_user_id:
                    if room_info.contribute_three < room_config['max_contribute']:
                        update_contribute_to_room(room_info.id, user_id, con_num, 3)
                        no_use = False
            elif i == 4 and no_use:
                if room_info.position_four == cont_user_id:
                    if room_info.contribute_four < room_config['max_contribute']:
                        update_contribute_to_room(room_info.id, user_id, con_num, 4)
                        no_use = False
            elif i == 5 and no_use:
                if room_info.position_five == cont_user_id:
                    if room_info.contribute_five < room_config['max_contribute']:
                        update_contribute_to_room(room_info.id, user_id, con_num, 5)
                        no_use = False
            elif i == 6 and no_use:
                if room_info.position_six == cont_user_id:
                    if room_info.contribute_six < room_config['max_contribute']:
                        update_contribute_to_room(room_info.id, user_id, con_num, 6)
                        no_use = False
            elif i == 7 and no_use:
                if room_info.position_two == cont_user_id:
                    if room_info.contribute_two < room_config['max_contribute']:
                        update_contribute_to_room(room_info.id, user_id, con_num, 7)
                        no_use = False
        #当自己贡献值满，给团队人贡献值
        if no_use:
            invited_li = d_user.get_invited_user_ids(cont_user_id)
            for uid in invited_li:
                room_info = getuser_rooms(uid)
                if room_info and no_use:
                    for i in range(1, 8):
                        if room_info.position_one == uid and no_use:
                            if room_info.contribute_one < room_config['max_contribute']:
                                update_contribute_to_room(room_info.id, user_id, con_num, 1)
                                no_use = False
                                break
                        elif room_info.position_two == uid and no_use:
                            if room_info.contribute_two < room_config['max_contribute']:
                                update_contribute_to_room(room_info.id, user_id, con_num, 2)
                                no_use = False
                                break
                        elif room_info.position_three == uid and no_use:
                            if room_info.contribute_three < room_config['max_contribute']:
                                update_contribute_to_room(room_info.id, user_id, con_num, 3)
                                no_use = False
                                break
                        elif room_info.position_four == uid and no_use:
                            if room_info.contribute_four < room_config['max_contribute']:
                                update_contribute_to_room(room_info.id, user_id, con_num, 4)
                                no_use = False
                                break
                        elif room_info.position_five == uid and no_use:
                            if room_info.contribute_five < room_config['max_contribute']:
                                update_contribute_to_room(room_info.id, user_id, con_num, 5)
                                no_use = False
                                break
                        elif room_info.position_six == uid and no_use:
                            if room_info.contribute_six < room_config['max_contribute']:
                                update_contribute_to_room(room_info.id, user_id, con_num, 6)
                                no_use = False
                                break
                        elif room_info.position_seven == uid and no_use:
                            if room_info.contribute_seven < room_config['max_contribute']:
                                update_contribute_to_room(room_info.id, user_id, con_num, 7)
                                no_use = False
                                break

def update_contribute_to_room(room_id:int, user_id:int, contribute_num:int, position_num:int = 1):
    room_info = d_db.get_roomgold(room_id)
    if room_info:
        update_contribute_json = {}
        with Dao() as db:
            if position_num == 1:
                update_contribute_json['contribute_one'] = contribute_num + room_info.contribute_one
                insert_room_contributelog(room_id, contribute_num, room_info.position_one, user_id)
            elif position_num == 2:
                update_contribute_json['contribute_two'] = contribute_num + room_info.contribute_two
                insert_room_contributelog(room_id, contribute_num, room_info.position_two, user_id)
            elif position_num == 3:
                update_contribute_json['contribute_three'] = contribute_num + room_info.contribute_three
                insert_room_contributelog(room_id, contribute_num, room_info.position_three, user_id)
            elif position_num == 4:
                update_contribute_json['contribute_four'] = contribute_num + room_info.contribute_four
                insert_room_contributelog(room_id, contribute_num, room_info.position_four, user_id)
            elif position_num == 5:
                update_contribute_json['contribute_five'] = contribute_num + room_info.contribute_five
                insert_room_contributelog(room_id, contribute_num, room_info.position_five, user_id)
            elif position_num == 6:
                update_contribute_json['contribute_six'] = contribute_num + room_info.contribute_six
                insert_room_contributelog(room_id, contribute_num, room_info.position_six, user_id)
            elif position_num == 7:
                update_contribute_json['contribute_seven'] = contribute_num + room_info.contribute_seven
                insert_room_contributelog(room_id, contribute_num, room_info.position_seven, user_id)
            db.query(TRoomgold).where(TRoomgold.id == room_id).update(update_contribute_json)
            db.commit()

def insert_room_contributelog(room_id:int, contribute_val:int, user_id:int, source_id:int):
    with Dao() as db:
        # 添加
        db.add(TRoomContributelog(
            room_id=room_id,
            contribute_val=contribute_val,
            user_id=user_id,
            source_id=source_id
        ))
        db.commit()

#获取用户分红次数
def get_room_fenhong_count(user_id:int):
    num = 0
    with Dao() as db:
        num = db.query(TBalance).filter(TBalance.user_id == user_id).filter(TBalance.type == balance_type[2]).count()
    return num

def get_user_fund_first(level_id:int = 1):
    if level_id == 1:
        with Dao() as db:
            return db.query(TFundPond).filter(TFundPond.ftype == 0).filter(TFundPond.stat == 0).first()
    elif level_id == 2:
        with Dao() as db:
            return db.query(TFundPond).filter(TFundPond.ftype == 1).filter(TFundPond.stat == 0).first()
    elif level_id == 3:
        with Dao() as db:
            return db.query(TFundPond).filter(TFundPond.ftype == 2).filter(TFundPond.stat == 0).first()
    else:
        return None

#获取用户对应的资金池信息
def get_user_for_fund(user_id:int):
    uinfo = d_user.get_user_by_id(user_id)
    if uinfo:
        return get_user_fund_first(uinfo.level_id)
    else:
        return None

#视频任务获得金额或购物券
def get_video_task_money_coin(money:int = 0, coin:int = 0, user_id:int = 0):
    if money > 0:
        pass
    if coin > 0:
        pass

def video_balance_change(user_id: int, fee: int, category: str, description: str):
    u_info = d_user.get_user_by_id(user_id)
    if u_info:
        category = '视频任务奖励金'
        u_account = get_account_info_add(u_info.id)
        total_balance = fee + u_account.balance
        update_account_balance(u_info.id, total_balance)
        add_instance = TBalance(change=fee, type=category, description=description, user_id=user_id,\
                             balance=total_balance, user_nick=u_info.nickname, phone=u_info.phone,\
                             create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

        with Dao() as db:
            db.add(add_instance)
            db.commit()

def video_coin_change(user_id: int, fee: int, category: str, description: str):
    u_info = d_user.get_user_by_id(user_id)
    if u_info:
        category = '视频任务奖励券'
        u_account = get_account_info_add(u_info.id)
        total_balance = fee + u_account.coin
        update_account_coin(u_info.id, total_balance)
        add_instance = TCoin(change=fee, type=category, description=description, user_id=user_id, coin=total_balance, \
                             user_nick=u_info.nickname, phone=u_info.phone, create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

        with Dao() as db:
            db.add(add_instance)
            db.commit()