
class CFG:
    def __init__(self, number, id, phase, an_equip, unit_measur,  a,b, skew, min, max):
        self.__number = number
        self.__id = id
        self.__phase = phase
        self.__an_equip = an_equip
        self.__unit_measur = unit_measur
        self.__a = a
        self.__b = b
        self.__skew = skew
        self.__min = min
        self.__max = max

    def get_number(self):
        return self.__number

    def get_id(self):
        return self.__id

    def get_phase(self):
        return self.__phase

    def get_an_equip(self):
        return self.__an_equip

    def get_unit_measur(self):
        return self.__unit_measur

    def get_a(self):
        return self.__a

    def get_b(self):
        return self.__b

    def get_skew(self):
        return self.__skew

    def get_min(self):
        return self.__min

    def get_max(self):
        return self.__max

    def __str__(self):
        return str(self.__number)+" "+self.__id+" "+self.__phase+" " \
    ""+self.__an_equip+" "+self.__unit_measur+" "+str(self.__a)+" " \
    ""+str(self.__b)+" "+str(self.__skew)+" "+str(self.__min)+" "+str(self.__max)
