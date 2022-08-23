class Person:
    __firstName: str = ""
    __lastName: str = ""
    __ID: str = ""
    __day: int = 0
    __month: int = 0
    __year: int = 0

    def __int__(self, firstName: str, lastName: str, ID: str | int, berthDay: str):
        self.__set_first_name(firstName)
        self.__set_last_name(lastName)
        self.__set_ID(ID)
        self.__set_berth_day(berthDay)

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
        if len(firstName) is 0:
            raise "not correct data"
        self.__firstName = firstName

    def __set_last_name(self, lastName: str) -> None:
        if len(lastName) is 0:
            raise "not correct data"
        self.__lastName = lastName

    def __set_ID(self, ID: str | int) -> None:
        if type(ID) is str:
            if not len(ID) is 10:
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
        return {
            'firstName': self.__firstName,
            'lastName': self.__lastName,
            'ID': self.__ID,
            'berthDay': {
                'day': self.__day,
                'month': self.__month,
                'year': self.__year
            }
        }
