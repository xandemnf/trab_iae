class Pokedex:
    def __init__(self):
        self.__local = []
        self.__national = []
        self.__national_activated = False

    def get_local_seen(self):
        return self.get_local_caught() +  self.__local.count(1)

    def get_local_caught(self):
        return self.__local.count(2)

    def get_national_seen(self):
        return self.get_national_caught() + self.__national.count(1)

    def get_national_caught(self):
        return self.__national.count(2)



