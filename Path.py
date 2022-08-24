import json

import jdatetime
import requests

from LogTrain import LogTrain
from globalVariable import Sex


def sex_switch(sex: Sex):
    if Sex.MAN == sex:
        return "Man"
    elif Sex.WOMAN == sex:
        return "Woman"
    elif Sex.BOTH == sex:
        return "Both"
    else:
        raise "sex isn in Sex Enum"


def sex_enum_to_int(sex: Sex) -> int:
    if Sex.MAN == sex:
        return 1
    elif Sex.WOMAN == sex:
        return 2
    elif Sex.BOTH == sex:
        return 3
    else:
        raise "sex isn in Sex Enum"


def j_to_g(date: str, spliter='/') -> str:
    splitDate: list[str] = date.split(spliter)
    return str(jdatetime.date(day=int(splitDate[2]), month=int(splitDate[1]), year=int(splitDate[0])).togregorian())


def get_query(beginning: str, ending: str, date: str) -> str:
    query: str = ""
    query += "from=" + beginning + '&'
    query += "to=" + ending + '&'
    query += "date=" + j_to_g(date) + '&'
    query += "adultCount=" + "1" + '&'
    query += "childCount=" + "0" + '&'
    query += "infantCount=" + "0" + '&'
    query += "exclusive=" + "false" + '&'
    query += "availableStatus=" + "Both"
    return query


class Path:
    __train: dict = {}
    __listOfTrain: list = []

    def is_free(self, beginning: str, ending: str, date: str, sex: Sex, listTrainId: list[int | str]) -> bool:
        query = get_query(beginning, ending, date)
        response = requests.get("https://train.atighgasht.com/TrainService/api/GetAvailable/v2?" + query).text
        self.__get_list_of_train(json.loads(response), sex)
        return self.__set_train(listTrainId)

    def __get_list_of_train(self, data, sex: Sex) -> None:
        if not 'Trains' in data:
            return
        trains = data['Trains']
        LogTrain().write(trains)
        for train in trains:
            capacity: int = 0
            for b in train['Prices']:
                if b['SellType'] == sex_enum_to_int(sex):
                    for c in b['Classes']:
                        capacity += c['Capacity']
                    break

            if not capacity == 0:
                self.__listOfTrain.append(train)

    def __set_train(self, listTrainId: list[int | str]) -> bool:
        if len(self.__listOfTrain) == 0:
            return False

        for Id in listTrainId:
            if Id == 0:
                return True
            for train in self.__listOfTrain:
                if str(Id) == str(train['TrainNumber']):
                    self.__train = train
                    return True

        return False
