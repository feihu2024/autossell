import datetime
import pytz


def now_timestamp_tz() -> float:
    # 创建时区对象
    timezone = pytz.timezone('Asia/Shanghai')

    # 获取当前时间
    now = datetime.datetime.now(tz=timezone)

    return now.timestamp() + now.tzinfo._utcoffset.seconds


if __name__ == '__main__':
    print(now_timestamp_tz() % (3600*24)/3600)


