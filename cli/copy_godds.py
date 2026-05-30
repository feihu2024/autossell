import datetime,time,sys,math
from pathlib import Path
from sqlalchemy import or_
root_dir = Path(__file__).parents[1]
model_dir = root_dir / 'model'
#print(root_dir)
# print(model_dir)
sys.path.append(str(root_dir))

from common import Dao, global_define
#from common.global_define import *
from model import schema, m_schema

from dao import d_user_account, d_account, d_user, d_package, d_order, d_groupsir, d_settings, d_supplier_account, d_supplier_income
from model.mall import m_account
from typing import Optional
from dao import d_db


def get_goods(good_ids: list):
    re_data = {"total":0, "data":[]}
    with Dao() as db:
        good_list = db.query(schema.TGood).filter(schema.TGood.id.in_(good_ids))

        re_data['total'] = good_list.count()
        re_data['data'] = good_list.all()
    return re_data

def copy_good_images(old_good_id: int, new_good_id:int):
    print(f"复制商品数据图片：old_good_id：{old_good_id}；new_good_id：{new_good_id}")
    with Dao() as db:
        good_list = db.query(schema.TGoodImage).filter(schema.TGoodImage.good_id == old_good_id)
        for data in good_list.all():
            print(f"复制ID:{data.id}")
            create_item : m_schema.CreateGoodImage = m_schema.CreateGoodImage(
                image = data.image,
                good_id  = new_good_id
            )
            re_val = d_db.insert_good_image(create_item)
            print(f"good_image新ID:{re_val.id}")

def copy_good_texts(old_good_id: int, new_good_id:int):
    print(f"复制商品文本数据：old_good_id：{old_good_id}；new_good_id：{new_good_id}")
    with Dao() as db:
        good_list = db.query(schema.TGoodText).filter(schema.TGoodText.good_id == old_good_id)
        for data in good_list.all():
            print(f"复制ID:{data.id}")
            create_item : m_schema.CreateGoodText = m_schema.CreateGoodText(
                good_id = new_good_id,
                description = data.description
            )
            re_val = d_db.insert_good_text(create_item)
            print(f"good_text新ID:{re_val.id}")

def copy_specs(good_id: int, new_good_id:int):
    print(f"复制商品规格：good_id：{good_id}")
    with Dao() as db:
        good_list = db.query(schema.TGoodSpec).filter(schema.TGoodSpec.good_id == good_id)
        for data in good_list.all():
            print(f"复制ID:{data.id}")
            create_item : m_schema.CreateGoodSpec = m_schema.CreateGoodSpec(
                good_id = new_good_id,
                price = data.price,
                cost = data.cost,
                value = data.value,
                stock = data.stock,
                price_line = data.price_line,
                image = data.image,
                is_sub_good = data.is_sub_good,
                num_sale = data.num_sale,
                parent_fee = data.parent_fee,
                top_fee = data.top_fee,
                recommender_fee = data.recommender_fee,
                supplier_fee = data.supplier_fee,
                lower_num_people = data.lower_num_people,
                upper_num_people = data.upper_num_people,
                room = data.room,
                post = data.post,
                status = data.status,
                share_fee = data.share_fee,
                is_default = data.is_default,
                spec_num = data.spec_num,
                profit = data.profit,
                eqlevel_fee = data.eqlevel_fee,
                wholesale_fee = data.wholesale_fee,
                wholesale_price = data.wholesale_price
            )
            re_val = d_db.insert_good_spec(create_item)
            print(f"good_spec新ID:{re_val.id}")
            #复制规格combos数据
            copy_spec_combos(data.id, re_val.id)
            # 复制规格detail数据
            copy_spec_detail(data.id, re_val.id)
            # 复制规格image数据
            copy_spec_image(data.id, re_val.id)

def copy_spec_combos(old_spec_id: int, new_spec_id:int):
    print(f"复制商品规格数据good_spec_combo：old_spec_id：{old_spec_id}；new_spec_id：{new_spec_id}")
    with Dao() as db:
        good_list = db.query(schema.TGoodSpecCombo).filter(schema.TGoodSpecCombo.good_spec_id == old_spec_id)
        for data in good_list.all():
            print(f"复制ID:{data.id}")
            create_item : m_schema.CreateGoodSpecCombo = m_schema.CreateGoodSpecCombo(
                good_spec_id = new_spec_id,
                value = data.value,
                price = data.price,
                amount = data.amount
            )
            re_val = d_db.insert_good_spec_combo(create_item)
            print(f"good_spec_combo新ID:{re_val.id}")

def copy_spec_detail(old_spec_id: int, new_spec_id:int):
    print(f"复制商品规格数据good_spec_detail：old_spec_id：{old_spec_id}；new_spec_id：{new_spec_id}")
    with Dao() as db:
        good_list = db.query(schema.TGoodSpecDetail).filter(schema.TGoodSpecDetail.good_spec_id == old_spec_id)
        for data in good_list.all():
            print(f"复制ID:{data.id}")
            create_item : m_schema.CreateGoodSpecDetail = m_schema.CreateGoodSpecDetail(
                good_spec_id = new_spec_id,
                detail = data.detail
            )
            re_val = d_db.insert_good_spec_detail(create_item)
            print(f"good_spec_detail新ID:{re_val.id}")

def copy_spec_image(old_spec_id: int, new_spec_id:int):
    print(f"复制商品规格数据copy_spec_image：old_spec_id：{old_spec_id}；new_spec_id：{new_spec_id}")
    with Dao() as db:
        good_list = db.query(schema.TGoodSpecImage).filter(schema.TGoodSpecImage.spec_id == old_spec_id)
        for data in good_list.all():
            print(f"复制ID:{data.id}")
            create_item : m_schema.CreateGoodSpecImage = m_schema.CreateGoodSpecImage(
                spec_id= new_spec_id,
                image = data.image
            )
            re_val = d_db.insert_good_spec_image(create_item)
            print(f"good_spec_image新ID:{re_val.id}")

def main():
    now_time = datetime.datetime.now()
    gid_list = [833, 834, 812, 725, 803, 779, 765, 776, 750, 735, 739, 726, 728, 715, 714, 705, 633, 546]
    #gid_list = [616, 618, 619]
    new_gid_list = []

    print(f"{now_time} - 复制任务启动")
    goods_list = get_goods(gid_list)

    count_rows = goods_list['total']
    print(f"复制：{count_rows} 条，商品数据")
    for t_good in goods_list['data']:
        create_item : m_schema.CreateGood = m_schema.CreateGood(
            name = t_good.name,
            is_flash_sale  = t_good.is_flash_sale,
            category_id = t_good.category_id,
            type = t_good.type,
            num_sale = t_good.num_sale,
            image_url = t_good.image_url,
            priority = t_good.priority,
            add_coin = t_good.add_coin,
            model_id = t_good.model_id,
            expired_time = t_good.expired_time,
            parent_good_id = t_good.parent_good_id,
            title = t_good.title,
            subtitle = t_good.subtitle,
            stock_cordon = t_good.stock_cordon,
            status = t_good.status,
            details = t_good.details,
            supplier_id = t_good.supplier_id,
            share_ratio = t_good.share_ratio,
            #create_time = t_good.
            #last_update_time = t_good.last_update_time
            saleable = t_good.saleable,
            click_count = t_good.click_count,
            transmit_count = t_good.transmit_count,
            coinable = t_good.coinable,
            price_line = t_good.price_line,
            introducer_id = t_good.introducer_id,
            sell_high = t_good.sell_high,
            sell_low = t_good.sell_low,
            cost_high = t_good.cost_high,
            cost_low = t_good.cost_low,
            display = t_good.display,
            coinable_number =t_good.coinable_number,
            is_package = t_good.is_package,
            fake_owner_name = t_good.fake_owner_name,
            fake_owner_phone = t_good.fake_owner_phone,
            unavailable_date = t_good.unavailable_date,
            available_time = t_good.available_time,
            usage_rule = t_good.usage_rule,
            refund_rule = t_good.refund_rule,
            order_expired_time = t_good.order_expired_time,
            cover_url = t_good.cover_url,
            video_url = t_good.video_url,
            is_wholesale = 1
        )
        print(f"insert：{t_good.id} ")
        #print(dict(create_item))
        re_val = d_db.insert_good(create_item)
        insert_good_id = re_val.id
        new_gid_list.append(insert_good_id)
        print(f"insert good id：{insert_good_id} ")
        #复制good_image
        copy_good_images(t_good.id, insert_good_id)
        #复制good_text
        copy_good_texts(t_good.id, insert_good_id)
        #复制规格
        copy_specs(t_good.id, insert_good_id)

        print(f"=============================return insert good id：{insert_good_id} 规格/规格combo/规格detail/规格image/商品image/商品text===============================")
    new_gid_list_str = str(new_gid_list)
    print(f"新产品ID：{new_gid_list_str}")
    print(f"复制任务执行完毕")


if __name__ == '__main__':
    main()