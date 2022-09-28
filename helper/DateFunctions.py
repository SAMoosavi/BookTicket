import jdatetime


def jalali_to_gregorian(date: str, spliter='/') -> str:
    split_date: list[str] = date.split(spliter)
    year = int(split_date[0])
    month = int(split_date[1])
    day = int(split_date[2])

    if year < 100:
        year += 1300

    return str(jdatetime.date(day=day, month=month, year=year).togregorian())
