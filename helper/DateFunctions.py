import jdatetime


def j_to_g(date: str, spliter='/') -> str:
    splitDate: list[str] = date.split(spliter)
    year = int(splitDate[0])
    month = int(splitDate[1])
    day = int(splitDate[2])

    if year < 100:
        year += 1300

    return str(jdatetime.date(day=day, month=month, year=year).togregorian())


def int_to_month_of_number(data: int) -> str:
    if data < 10:
        return "0" + str(data)
    else:
        return str(data)
