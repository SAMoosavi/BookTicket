from jdatetime import date


def jalali_to_gregorian(date_str: str, separator: str = '/') -> str:
    year, month, day = map(int, date_str.split(separator))
    if year < 100:
        year += 1300
    return str(date(year=year, month=month, day=day).togregorian())
