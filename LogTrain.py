class LogTrain:
    __URL = "./Train.csv"
    __file = None

    def __init__(self):
        pass
    # TODO:TEST
    def write(self, trains):
        self.__file = open(self.__URL, 'a')
        self.__writeOnFile(trains)

    def __writeOnFile(self, data: list):
        for a in data:
            self.__file.write(self.__trainToStr(a))

    def __trainToStr(self, data: dict) -> str:
        result: str = ""
        baseStr: str = ""
        baseStr += data['TrainNumber'] + ','
        baseStr += data['FromName'] + ','
        baseStr += data['ToName'] + ','
        baseStr += data['DepartureTime'] + ','
        baseStr += data['ArrivalTime'] + ','
        baseStr += data['ProviderName'] + ','
        baseStr += data['CorporationName'] + ','
        baseStr += data['Weekday'] + ','
        baseStr += data['DateString'] + ','
        for sellType in data['Prices']:
            sellTypeStr: str = sellType['SellType'] + ','
            for wagonType in sellType['Classes']:
                wagonTypeStr: str = ""
                wagonTypeStr += wagonType['WagonName'] + ','
                wagonTypeStr += str(wagonType['Capacity']) + ','
                wagonTypeStr += str(wagonType['Price']) + ','
                wagonTypeStr += "True" if wagonType['Capacity'] > 0 else "False"
                result += baseStr + sellTypeStr + wagonTypeStr + '\n'
        print(result)
        return result
