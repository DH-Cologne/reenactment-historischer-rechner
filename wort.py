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
    def __init__(self, strWort):
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
            obj = Ganzzahl(self.strWort[0:-1])
        # check Klartext (lexikalisches Wort)
        elif not bool(re.search(r'\d', wort)) and wort != 'D':
            obj = Klartext(self.strWort)
        # check Befehl
        elif (bool(re.search(r'\d', wort)) and bool(re.search('[A-Z]', wort))) or wort == 'D':
            obj = Befehl(self.strWort)
        # sonst fehlerhafter Input
        else:
            print('Objekttyp konnte nicht identifiziert werden')
            print('Inputstring checken')
        return obj


class Befehl(Wort):

    def __init__(self, strWort):
        super().__init__(strWort)
        self.isArithmetic = False
        self.isJumpOrCall = False
        self.isCondition = False
        self.isStop = False
        self.isShift = False

    def getAddons(self):
        # Was ist hiermit gemeint?
        pass

    def getBinary(self):
        """
        Umwandlung eines Befehls als String in eine Binärzahl.
        :return: Befehl als Binärzahl
        """
        # Befehl wird aus String erstellt (Operation + Adresse)
        befehl = self.strWort

        # Befehle beginnen mit [1,0]
        binary = [1, 0]

        # Initialisierung von Binärzahl-Sequenzen, die dann mit Inhalt gefüllt werden
        operation = list
        speicher = list

        # trennen von Operations- + Adressteil
        match = re.match(r"([a-z]+)(\d+)?([+]\d+)?([a-z]+)?", befehl, re.I)
        if match:
            items = match.groups()
            items = [i for i in items if i is not None]

            # Umwandlung in Binärzahl
            operation = self.encode_operation([i for i in items if i.isalpha()])
            speicher = self.encode_address([i for i in items if i.isnumeric() | i.__contains__('+')])

        # Zusammenfügen der einzelnen Teile zu einer Binärzahl
        binary += operation + speicher
        return binary

    def encode_operation(self, operation_list):
        """
        String Befehl wird zu 18-stelliger Binärzahl umgewandelt.
        :param operation_list Liste mit allen genannten Operationen einer Speicherzelle
        :return: operation als Binärzahl
        """
        # Rückgabe-Liste: wird mit 0 und 1 an entsprechenden Stellen gefüllt
        operation = [0] * 18
        for o in operation_list:
            # Überprüfung der einzelnen Befehle
            if o.__contains__('PP'):
                operation[1] = 1
                self.isCondition = True
            if o.__contains__('P'):
                operation[2] = 1
                self.isCondition = True
            if o.__contains__('QQ'):
                operation[3] = 1
                self.isCondition = True
            if o.__contains__('Q'):
                operation[4] = 1
                self.isCondition = True
            if o.__contains__('Y'):
                operation[5] = 1
                self.isCondition = True
            if o.__contains__('C'):
                operation[6] = 1
                self.isCondition = True
            if o.__contains__('N'):
                operation[7] = 1
                self.isShift = True
            if o.__contains__('LL'):
                operation[8] = 1
                self.isShift = True
            if o.__contains__('R'):
                operation[9] = 1
                self.isShift = True
            if o.__contains__('U'):
                operation[10] = 1
                self.isArithmetic = True
            if o.__contains__('A'):
                operation[11] = 1
                self.isArithmetic = True
            if o.__contains__('S'):
                operation[12] = 1
                self.isArithmetic = True
            if o.__contains__('F'):
                operation[13] = 1
                self.isJumpOrCall = True
            if o.__contains__('K'):
                operation[14] = 1
                self.isCondition = True
            if o.__contains__('H'):
                operation[15] = 1
                self.isCondition = True
            if o.__contains__('Z'):
                operation[16] = 1
                self.isStop = True
            if o.__contains__('G'):
                operation[17] = 1
                self.isCondition = True
            if o.__contains__('V'):
                operation[18] = 1
                self.isCondition = True

        return operation

    def encode_address(self, address_list):
        """
           String Speicheradresse wird zu 18-stelliger Binärzahl umgewandelt.
           Unterteilung des Schnell- (5-stellig) und Trommelspeichers (13-stellig).
           :param address_list Liste mit allen genannten Speicherzellen
           :return: adresse als Binärzahl
           """
        # Initialisierung der Speicher, die mit Inhalt gefüllt werden
        schnellspeicher = list()
        trommelspeicher = list()

        for a in address_list:
            # wenn mehrere Speicherzellen angegeben sind, wird die zweite mit '+' angegeben
            # damit die Speicherzelle als Integer weiterverarbeitet werden kann, wird das '+' entfernt
            if a.__contains__('+'):
                a.replace('+', '')
            # Umwandlung des Strings in einen Integer
            a = int(a)
            # Trommelspeicher
            if a > 32:
                # Umwandlung in Binärzahl
                binary = format(a, 'b')
                # Trommelspeicher hat insgesamt 13 Stellen. Die, die nicht für die Binärzahl gebraucht werden,
                # werden mit 0 gefüllt
                trommelspeicher = [0] * (13 - len(binary))
                trommelspeicher += list(map(int, list(binary)))
            # Schnellspeicher
            elif a <= 32:
                # Umwandlung in Binärzahl
                binary = format(a, 'b')
                # Schnellspeicher hat insgesamt 5 Stellen. Die, die nicht für die Binärzahl gebraucht werden,
                # werden mit 0 gefüllt
                schnellspeicher = [0] * (5 - len(binary))
                schnellspeicher += list(map(int, list(binary)))

        # falls einer der Speicher leer ist, wird dieser mit 0 gefüllt
        if not trommelspeicher:
            trommelspeicher = [0] * 13
        if not schnellspeicher:
            schnellspeicher = [0] * 5

        # Zusammenfügen zu einer Binärzahl
        adresse = schnellspeicher + trommelspeicher
        return adresse


class Klartext(Wort):
    def __init__(self, strWort):
        super().__init__(strWort)

    def getBinary(self):
        """
        Binärzahl aus String erstellen
        :return: 38-stellige Binärzahl als Liste
        """
        # Buchstaben beginnen mit [0,1] (Typ)
        wort = self.strWort
        # drittes Element 0?
        binary = [0, 1, 0]
        while len(wort) < 7:
            wort += ' '
        print(wort)
        # baudot encodieren des Wortes
        encodedWort = self._baudot_encode(wort)
        binary = binary + encodedWort
        print(binary)
        print(len(binary))
        return binary

    def _baudot_encode(self, wort):
        """
        String Wort als Baudot Code encodieren
        :param wort: Input Wort als String
        :return: baudot-encodiertes Wort
        """
        with StringIO() as output_buffer:
            writer = handlers.TapeWriter(output_buffer)
            encode_str(wort, codecs.ITA2_STANDARD, writer)
            output = output_buffer.getvalue()
        output = output.replace('.', '').replace('*', '1').replace(' ', '0')
        output_list = output.split('\n')[1:-1]
        # reverse strings
        output_list = [x[len(x)::-1] for x in output_list]
        output_list = list(''.join(output_list))
        return output_list


class Ganzzahl(Wort):

    def __init__(self, strWort):
        super().__init__(strWort)
        self.float_rep = float(self.strWort)
        if abs(self.float_rep) > (2 ** 35) - 1 or self.float_rep % 1 != 0.0:
            raise Exception(f"Strichzahl {self.float_rep} is out of bound.")

    def getBinary(self):

        bin_number = list(bin(int(self.strWort)).split("b")[1].strip(" "))

        while len(bin_number) < 35:
            bin_number.insert(0, 0)

        if self.float_rep >= 0:
            bin_number = [0, 0, 0] + bin_number
        if self.float_rep < 0:
            bin_number = [1, 1, 1] + bin_number

        bin_number = [int(item) for item in bin_number]

        return bin_number

    def getInt(self):
        return int(strWort)


if __name__ == '__main__':
    w1 = Wort('EZ0+1E')
    w2 = Wort('A0')
    w3 = Wort('D')
    w4 = Wort('SCHLOS ')
    w5 = Wort('2\'')
    w6 = Wort('B0+1900')
    w7 = Wort('E1720E')

    print('Typ von String {} ist {}'.format(w1.strWort, type(w1.parse())))
    print('Typ von String {} ist {}'.format(w2.strWort, type(w2.parse())))
    print('Typ von String {} ist {}'.format(w3.strWort, type(w3.parse())))
    print('Typ von String {} ist {}'.format(w4.strWort, type(w4.parse())))
    print('Typ von String {} ist {}'.format(w5.strWort, type(w5.parse())))
    print('Typ von String {} ist {}'.format(w6.strWort, type(w6.parse())))

    print(w5.parse().getBinary())
    print(w4.parse().getBinary())
    print(w1.parse().getBinary())
    print(w6.parse().getBinary())
    print(w2.parse().getBinary())
    print(w3.parse().getBinary())
    print(w7.parse().getBinary())
