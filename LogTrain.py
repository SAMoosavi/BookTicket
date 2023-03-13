class LogTrain:
    __PATH = "storage/train.csv"

    def write(self, trains):
        with open(self.__PATH, 'a') as file:
            for train in trains:
                base_str = [
                    str(train['TrainNumber']),
                    train['FromName'],
                    train['ToName'],
                    train['DepartureTime'],
                    train['ArrivalTime'],
                    train['ProviderName'],
                    train['CorporationName'],
                    train['Weekday'],
                    train['DateString'],
                ]
                for sell_type in train['Prices']:
                    sell_type_str = str(sell_type['SellType'])
                    for wagon_type in sell_type['Classes']:
                        wagon_type_str = [
                            sell_type_str,
                            wagon_type['WagonName'],
                            str(wagon_type['Capacity']),
                            str(wagon_type['Price']),
                            str(wagon_type['Capacity'] > 0)
                        ]
                        result = ','.join(base_str + wagon_type_str) + '\n'
                        file.write(result)
