import numpy as np
import re
# https://python-baudot.readthedocs.io/en/latest/reference.html#baudot.codecs.BaudotCodec
from baudot import encode_str, codecs, handlers
from io import StringIO

"""
Notizen aus Stunde am 03.05.2022
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


Repräsentation von Daten
1. und 2. Bit: Type
3. Bit 0 oder 1? Umschalter zwischen Zahlen und Buchstaben?
7 Zeichen a 5 bits

Zahl: '-124'
Befehl: 'E1586'
Wort: 'Wort'

Repräsentation von Zahlen
Repräsentation von Buchstaben
Repräsentation von Befehlen

alles 38 bits (38-stellige Binärzahlen)

jede Speicherzelle hat 38 Dualstellen: eine Zahl, einen Befehl oder 7 Klartextzeichen

00 negative Zahl
11 positive Zahl
01 Buchstaben
10 Befehle
"""


class Wort:
    def __init__(self, zelle, strWort):
        self.zelle = zelle
        self.strWort = strWort.strip()

    def parse(self):
        """
        Prüfen, um welchen Untertyp es sich handelt und ein Objekt des entsprechenden Typs erstellen
        :return: Objekt des jeweiligen Typs
        """
        obj = None
        wort = self.strWort
        # check Strichzahl
        if wort[-1] == '\'':
            obj = Ganzzahl(self.zelle, self.strWort[0:-1])
        # check Klartext (lexikalisches Wort)
        elif not bool(re.search(r'\d', wort)) and wort != 'D':
            obj = Klartext(self.zelle, self.strWort)
        # check Befehl
        elif (bool(re.search(r'\d', wort)) and bool(re.search('[A-Z]', wort))) or wort == 'D':
            obj = Befehl(self.zelle, self.strWort)
        # sonst fehlerhafter Input
        else:
            print('Objekttyp konnte nicht identifiziert werden')
            print('Inputstring checken')
        return obj

    def getBinary(self):
        # nur in Unterklassen implementieren?
        pass


class Befehl(Wort):

    # benötigen wir den Schnellspeicher?

    def __init__(self, zelle, strWort):
        super().__init__(zelle, strWort)

    def isAddition(self):
        pass

    def getAddons(self):
        pass

    def getBinary(self):
        pass


class Klartext(Wort):

    def __init__(self, zelle, strWort):
        super().__init__(zelle, strWort)

    def getBinary(self):
        # Buchstaben beginnen mit [0,1] (Typ)
        # Frage: Umschalten relevant für uns?
        # Frage: Wie Leerzeichen sinnvoll einsetzen? Wenn Wort weniger als 7 Zeichen, dass Rest mit Leerzeichen auffüllen?

        print(self.strWort)
        if len(self.strWort) > 7:
            raise Exception(f"Klartext {self.strWort} is out of bound.")

        with StringIO() as output_buffer:
            writer = handlers.TapeWriter(output_buffer)
            encode_str(self.strWort, codecs.ITA2_STANDARD, writer)
            output = output_buffer.getvalue()

        print(output)
        print(type(output))
        print(output.split("\n")[1:])

        pass


class Ganzzahl(Wort):
    def __init__(self, zelle, strWort):
        super().__init__(zelle, strWort)

    def getBinary(self):

        # does not include handling of float humbers
        float_rep = float(self.strWort)
        if abs(float_rep) > (2**35) - 1:
            raise Exception(f"Strichzahl {float_rep} is out of bound.")

        bin_number = list(bin(int(self.strWort)).split("b")[1].strip(" "))

        while len(bin_number) < 35:
            bin_number.insert(0, 0)

        if float_rep > 0:
            if float_rep % 1 == 0.0:
                bin_number.insert(0, 0)
            else:
                bin_number.insert(0, 1)
            bin_number.insert(0, 0)
            bin_number.insert(0, 0)

        if float_rep < 0:
            if float_rep % 1 == 0.0:
                bin_number.insert(0, 1)
            else:
                bin_number.insert(0, 0)
            bin_number.insert(0, 1)
            bin_number.insert(0, 1)

        bin_number = [int(item) for item in bin_number]

        return bin_number


if __name__ == '__main__':
    w1 = Wort(1, 'EZ0+1E')
    w2 = Wort(2, 'A0')
    w3 = Wort(3, 'D')
    w4 = Wort(4, 'SCHLOS ')
    w5 = Wort(5, '2\'')
    print('Typ von String {} ist {}'.format(w1.strWort, type(w1.parse())))
    print('Typ von String {} ist {}'.format(w2.strWort, type(w2.parse())))
    print('Typ von String {} ist {}'.format(w3.strWort, type(w3.parse())))
    print('Typ von String {} ist {}'.format(w4.strWort, type(w4.parse())))
    print('Typ von String {} ist {}'.format(w5.strWort, type(w5.parse())))

    print(w5.parse().getBinary())
    print(w4.parse().getBinary())
