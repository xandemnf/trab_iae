class Item:
    def __init__(self, name):
        self.__name = name
        self.__is_key_item = False
        self.__effect = None
        self.__amount = 0
        self.__price = 0

    def get_buy_price(self):
        return self.__price

    def get_sell_price(self):
        return self.__price // 2

    def is_key_item(self):
        return self.__is_key_item

    def get_amount(self):
        return self.__amount

    def add_amount(self, amount):
        if amount + self.__amount <= 999:
            self.__amount += amount
            return 0
        else:
            old_amount = self.__amount
            self.__amount = 999
            return old_amount + amount - 999

    def reduce_amount(self, amount):
        if self.__is_key_item:
            self.__amount = 0
            return True
        if amount > self.__amount:
            return False
        else:
            self.__amount -= amount
            return True