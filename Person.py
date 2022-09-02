from globalVariable import Sex


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


class Person:
    __firstName: str = ""
    __lastName: str = ""
    __ID: str = ""
    __day: int = 0
    __month: int = 0
    __year: int = 0
    __sex: Sex = Sex.BOTH
    __set = False

    def set(self, firstName: str, lastName: str, ID: str | int, berthDay: str, sex: int):
        self.__set_first_name(firstName)
        self.__set_last_name(lastName)
        self.__set_ID(ID)
        self.__set_berth_day(berthDay)
        self.__set_sex(sex)

    def set_on_dict(self, data: dict):
        if not data['firstName']:
            raise "not correct data"
        if not data['lastName']:
            raise "not correct data"
        if not data['berthDay']['year']:
            raise "not correct data"
        if not data['berthDay']['month']:
            raise "not correct data"
        if not data['berthDay']['day']:
            raise "not correct data"
        if not data['sex']:
            raise "not correct data"

        self.__set_first_name(data['firstName'])
        self.__set_last_name(data['lastName'])
        self.__set_ID(data['ID'])
        self.__set_berth_day(
            str(data['berthDay']['year']) + "/" + str(data['berthDay']['month']) + "/" + str(data['berthDay']['day'])
        )
        self.__set_sex(data['sex'])

    def __set_sex(self, sex: int):
        self.__sex = int_to_sex_enum(sex)

    def __set_berth_day(self, date: str) -> None:
        dateSpirited = date.split('/')
        if int(dateSpirited[0]) <= 1300:
            raise "not correct data"
        if not int(dateSpirited[1]) in range(1, 12):
            raise "not correct data"
        if not int(dateSpirited[2]) in range(1, 31):
            raise "not correct data"
        self.__day = int(dateSpirited[2])
        self.__month = int(dateSpirited[1])
        self.__year = int(dateSpirited[0])

    def __set_first_name(self, firstName: str) -> None:
        if len(firstName) == 0:
            raise "not correct data"
        self.__firstName = firstName

    def __set_last_name(self, lastName: str) -> None:
        if len(lastName) == 0:
            raise "not correct data"
        self.__lastName = lastName

    def __set_ID(self, ID: str | int) -> None:
        if type(ID) is str:
            if not len(ID) == 10:
                raise "not correct data"
            for char in ID:
                if not ord(char) in range(ord("0"), ord("9")):
                    raise "not correct data"
            self.__ID = ID
        else:
            if not 10e10 < ID < 10e11:
                raise "not correct data"
            self.__ID = str(ID)

    def get_dict(self) -> dict:
        # if not self.__set:
        #     raise "don't set person"
        return {
            'firstName': self.__firstName,
            'lastName': self.__lastName,
            'ID': self.__ID,
            'berthDay': {
                'day': self.__day,
                'month': self.__month,
                'year': self.__year
            },
            'sex': sex_enum_to_int(self.__sex)
        }

    def get_first_name(self):
        # if not self.__set:
        #     raise "don't set person"
        return self.__firstName

    def get_last_name(self):
        # if not self.__set:
        #     raise "don't set person"
        return self.__lastName

    def get_ID(self):
        # if not self.__set:
        #     raise "don't set person"
        return self.__ID

    def get_day(self):
        # if not self.__set:
        #     raise "don't set person"
        return self.__day

    def get_month(self):
        # if not self.__set:
        #     raise "don't set person"
        return self.__month

    def get_year(self):
        # if not self.__set:
        #     raise "don't set person"
        return self.__year

    def get_sex(self) -> Sex:
        # if not self.__set:
        #     raise "don't set person"
        return self.__sex
