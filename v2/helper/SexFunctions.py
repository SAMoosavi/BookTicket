from globalClass.globalVariable import Sex


def sex_enum_to_int(sex: Sex) -> int:
    if Sex.MAN == sex:
        return 1
    elif Sex.WOMAN == sex:
        return 2
    elif Sex.BOTH == sex:
        return 3
    else:
        raise "sex isn in Sex Enum"


def int_to_sex_enum(sex: int) -> Sex:
    if sex == 1:
        return Sex.MAN
    elif sex == 2:
        return Sex.WOMAN
    elif sex == 3:
        return Sex.BOTH
    else:
        raise "sex isn in Sex Enum"


def sex_switch(sex: Sex):
    if Sex.MAN == sex:
        return "Man"
    elif Sex.WOMAN == sex:
        return "Woman"
    elif Sex.BOTH == sex:
        return "Both"
    else:
        raise "sex isn in Sex Enum"
