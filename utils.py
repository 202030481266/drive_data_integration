from datetime import datetime


def str_to_datetime(time_string=None):
    """把字符串转换成日期的对象"""
    if time_string is None:
        return None
    return datetime.strptime(time_string, '%Y-%m-%d')


def save_no_none(data):
    """去除data里面所有空值的项， data可以为列表或者字典"""
    if isinstance(data, list):
        return [x for x in data if x]
    res = {}
    for key, value in data.items():
        if value:
            res[key] = value
    return res


def check_date(year, month, day):
    """
    检查时间合不合法
    :param year: 年
    :param month: 月
    :param day: 日
    :return: 是否合法
    """
    year = int(year)
    month = int(month)
    day = int(day)
    if year > 2022 or year < 1:
        return False
    if month < 1 or month > 12:
        return False
    if day < 1 or day > 31:
        return False
    # 检查是否为闰年
    if ((year % 4 == 0) and (year % 100 != 0)) or year % 400 == 0:
        if day > 29 and month == 2:
            return False
    else:
        if day > 28 and month == 2:
            return False
    return True