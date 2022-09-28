class LogTrain:
    __PATH = "storage/train.csv"
    __file = None

    def __init__(self):
        pass

    def __del__(self):
        if self.__file:
            self.__file.close()

    def write(self, trains):
        self.__file = open(self.__PATH, 'a')
        self.__write_on_file(trains)

    def __write_on_file(self, data: list):
        for a in data:
            self.__file.write(self.__train_to_str(a))

    def __train_to_str(self, data: dict) -> str:
        result: str = ""
        base_str: str = ""
        base_str += str(data['TrainNumber']) + ','
        base_str += data['FromName'] + ','
        base_str += data['ToName'] + ','
        base_str += data['DepartureTime'] + ','
        base_str += data['ArrivalTime'] + ','
        base_str += data['ProviderName'] + ','
        base_str += data['CorporationName'] + ','
        base_str += data['Weekday'] + ','
        base_str += data['DateString'] + ','
        for sell_type in data['Prices']:
            sell_type_str: str = str(sell_type['SellType']) + ','
            for wagon_type in sell_type['Classes']:
                wagon_type_str: str = ""
                wagon_type_str += wagon_type['WagonName'] + ','
                wagon_type_str += str(wagon_type['Capacity']) + ','
                wagon_type_str += str(wagon_type['Price']) + ','
                wagon_type_str += "True" if wagon_type['Capacity'] > 0 else "False"
                result += base_str + sell_type_str + wagon_type_str + '\n'
        return result
