import numpy as np

"""
class Wort
- getBinary(zelle)
- parse(str) --> Wort 
 	- würde String einlesen und checken, ob Word, Befehl, 
 	Klartext oder Ganzzahl & entsprechendes Objekt erzeugen

class Befehl(Wort)
- isAddition()
- getAddons()

class Klartext(Wort)
- getBinary

class Ganzzahl(Wort)

Binärzahl als Liste [0,1,0,0,1...] mit len = 38
"""


class Wort:
    def __init__(self, zelle, strWort):
        self.zelle = zelle
        self.strWort = strWort

    def parse(self):
        pass

    def getBinary(self):
        pass


class Befehl(Wort):
    def __init__(self, zelle, strWort):
        super().__init__(zelle, strWort)

    def isAddition(self):
        pass

    def getAddons(self):
        pass


class Klartext(Wort):
    def __init__(self, zelle, strWort):
        super().__init__(zelle, strWort)

    def getBinary(self):
        pass


class Ganzzahl(Wort):
    def __init__(self, zelle, strWort):
        super().__init__(zelle, strWort)

    def getBinary(self):
        pass


