import jdatetime


def j_to_g(date: str, spliter='/') -> str:
    splitDate: list[str] = date.split(spliter)
    return str(jdatetime.date(day=int(splitDate[2]), month=int(splitDate[1]), year=int(splitDate[0])).togregorian())


def int_to_month_of_number(data: int) -> str:
    if data < 10:
        return "0" + str(data)
    else:
        return str(data)
