from abc import ABC, abstractmethod


class BookTicket(ABC):
    @abstractmethod
    def login(self, data):
        pass

    @abstractmethod
    def search(self, data):
        pass

    # @abstractmethod
    # def __getTrains(self, ID):
    #     pass
    #
    # @abstractmethod
    # def __minTrain(self):
    #     pass

    @abstractmethod
    def setUsers(self, dataUsers):
        pass

    @abstractmethod
    def buy(self):
        pass
