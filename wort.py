import numpy as np
import re
# https://python-baudot.readthedocs.io/en/latest/reference.html#baudot.codecs.BaudotCodec
from baudot import encode_str, codecs, handlers
from io import StringIO


def parse(strWort):
    """
    Prüfen, um welchen Untertyp es sich handelt und ein Objekt des entsprechenden Typs erstellen
    :param strWort: Wort als String
    :return: Objekt des jeweiligen Typs
    """
    strWort.strip()
    obj = None
    wort = strWort
    # check Strichzahl
    if wort[-1] == '\'':
        obj = Ganzzahl(strWort[0:-1])
    elif wort == '0':
        obj = Ganzzahl(strWort)
    # check Klartext (lexikalisches Wort)
    elif not bool(re.search(r'\d', wort)) and wort != 'D':
        obj = Klartext(strWort)
    # check Befehl
    elif (bool(re.search(r'\d', wort)) and bool(re.search('[A-Z]', wort))) or wort == 'D':
        obj = Befehl(strWort)
    # sonst fehlerhafter Input
    # NR: Vielleicht auch int akzeptieren und in Ganzzahl überführen? 
    else:
        raise Exception(f"Objekttyp für Input {wort} konnte nicht identifiziert werden. \n Bitte Input überprüfen.")
    return obj


def parseBinary(binary):
    """
    Prüfen, um welchen Untertyp es sich handelt und ein Objekt des entsprechenden Typs erstellen
    :param binary: Wort als Binärrepräsentation
    :return: Objekt des jeweiligen Typs
    """

    if binary[0] == binary[1]:
        return _parseGanzzahl(binary)

    elif binary[0] == 1:
        return _parseBefehl(binary)

    elif binary[0] == 0:
        return _parseWort(binary)


def _parseGanzzahl(binary):
    if binary[2] == 0:
        number = int(''.join(map(str, binary[3:])), 2)
    elif binary[2] == 1:
        number = -int(''.join(map(str, binary[3:])), 2)

    else:
        raise Exception(f"{binary} is not valid.")

    return parse(str(number) + '\'')


def _parseBefehl(binary):
    if len(binary) != 38:
        raise Exception(f"{binary} is not valid.")

    voc = ['PP', 'P', 'QQ', 'Q', 'Y', 'C', 'N', 'LL', 'R', 'U', 'A', 'S', 'F', 'K', 'H', 'Z', 'G', 'V']
    operation = str()
    if (binary[11:12] == 0) & (binary[14] == 0):
        for i, b in enumerate(binary[2:10]):
            operation += str(voc[i])
        operation += 'E'
        for i, b in enumerate(binary[13:19]):
            operation += str(voc[i])
    else:
        for i, b in enumerate(binary[2:19]):
            if b != 0:
                operation += str(voc[i])

    schnellspeicher = int(''.join(map(str, binary[20:24])), 2)
    trommelspeicher = int(''.join(map(str, binary[25:])), 2)

    if operation.__contains__('UA'):
        operation = operation.replace('UA', 'I')
    if operation.__contains__('LLR'):
        operation = operation.replace('LLR', 'L')
    if operation.__contains__('NA'):
        operation = operation.replace('NA', 'B')
    if operation.__contains__('NU'):
        operation = operation.replace('NU', 'T')
    if operation.__contains__('F') & trommelspeicher == 644:
        operation = operation.replace('F', 'D')

    # TODO return noch nicht richtig
    # Problem: Was passiert, wenn der Schnellspeicher eigentlich im Befehl nicht vorkommt?
    # Es wird immer 0 zurückgegeben
    if trommelspeicher > 32 & schnellspeicher <= 32:
        return parse(operation + str(schnellspeicher) + '+' + str(trommelspeicher))

    if (trommelspeicher < 32 | trommelspeicher == 0) & schnellspeicher <= 32:
        return parse(operation + str(schnellspeicher))

    if trommelspeicher > 32 & schnellspeicher > 32:
        return parse(operation + str(trommelspeicher))


def _parseWort(binary):
    pass


class Wort:
    def __init__(self, strWort: str):
        self.strWort = strWort.strip()

    def __repr__(self):
        return self.strWort


class Befehl(Wort):

    def __init__(self, strWort: str):
        super().__init__(strWort)
        self.isArithmetic = False
        self.isJumpOrCall = False
        self.isCondition = False
        self.isStop = False
        self.isShift = False
        self.isReadOrSave = False

    def getBinary(self) -> list:
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
            operations = [i for i in items if i.isalpha()]

            # Umwandlung in Binärzahl
            operation = self.encode_operation(operations)
            # wenn die Operation == D ist, dann wird die Speicherzelle auf 644 gesetzt
            if operations.__contains__('D'):
                b = format(644, 'b')
                speicher = ([0] * 5) + (([0] * (13 - len(b))) + (list(map(int, list(b)))))
            # in allen anderen Fällen wird der String in eine Binärzahl umgewandelt
            else:
                speicher = self.encode_address([i for i in items if i.isnumeric() | i.__contains__('+')])

        # Zusammenfügen der einzelnen Teile zu einer Binärzahl
        binary += operation + speicher
        return binary

    def encode_operation(self, operation_list: list) -> list:
        """
        String Befehl wird zu 18-stelliger Binärzahl umgewandelt.
        :param operation_list Liste mit allen genannten Operationen einer Speicherzelle
        :return: operation als Binärzahl
        """
        # Rückgabe-Liste: wird mit 0 und 1 an entsprechenden Stellen gefüllt
        operation = [0] * 18
        for o in operation_list:
            # Überprüfung der einzelnen Befehle
            if o.__contains__('P'):
                counter = o.count('P')
                if (counter % 2) == 0:
                    operation[0] = 1
                else:
                    operation[1] = 1
                self.isCondition = True
            if o.__contains__('Q'):
                counter = o.count('Q')
                if (counter % 2) == 0:
                    operation[2] = 1
                else:
                    operation[3] = 1
                self.isCondition = True
            if o.__contains__('Y'):
                operation[4] = 1
                self.isCondition = True
            if o.__contains__('C'):
                operation[5] = 1
                self.isCondition = True
            if o.__contains__('N'):
                operation[6] = 1
                self.isShift = True
            if o.__contains__('L'):
                counter = o.count('L')
                if (counter % 2) == 0:
                    operation[7] = 1
                else:
                    operation[7] = 1
                    operation[8] = 1
                self.isShift = True
            if o.__contains__('R'):
                operation[8] = 1
                self.isShift = True
            if o.__contains__('U'):
                operation[9] = 1
                self.isArithmetic = True
            if o.__contains__('A'):
                operation[10] = 1
                self.isArithmetic = True
            if o.__contains__('S'):
                operation[11] = 1
                self.isArithmetic = True
            if o.__contains__('F'):
                operation[12] = 1
                self.isJumpOrCall = True
            if o.__contains__('K'):
                operation[13] = 1
                self.isCondition = True
            if o.__contains__('H'):
                operation[14] = 1
                self.isCondition = True
            if o.__contains__('Z'):
                operation[15] = 1
                self.isStop = True
            if o.__contains__('G'):
                operation[16] = 1
                self.isCondition = True
            if o.__contains__('V'):
                operation[17] = 1
                self.isCondition = True
            if o.__contains__('D'):
                operation[12] = 1
                # NR: Reicht das? D müsste doch zu F644 werden, 
                # d.h. hier müsste auch eine Speicheradresse definiert werden.
            if o.__contains__('B'):
                operation[6] = 1
                operation[10] = 1
                self.isReadOrSave = True
            if o.__contains__('T'):
                operation[6] = 1
                operation[9] = 1
                self.isReadOrSave = True
            if o.__contains__('E'):
                self.isJumpOrCall = True
                operation[9] = 0
                operation[10] = 0

        return operation

    def encode_address(self, address_list: list) -> list:
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
    def __init__(self, strWort: str):
        super().__init__(strWort)
        if len(strWort) > 6:
            raise Exception(f"Wort {strWort} überschreitet die maximale Länge von 6 Zeichen")

    def getBinary(self) -> list:
        """
        Binärzahl aus String erstellen
        :return: 38-stellige Binärzahl als Liste
        """
        wort = self.strWort
        # Vektor initialisieren, Klartext Typ beginnt mit [0, 1]
        binary = np.zeros(38, dtype=int)
        binary[1] = 1
        # Umschalter Bit ändern nur bei Punkt
        if wort == '.':
            binary[2] = 1
        # 1 Leerzeichen anhängen
        wort += ' '
        # baudot encodieren des Wortes
        baudot_wort = self._baudot_encode(wort)
        # Entsprechende Bits auf 1 setzen
        for i in range(len(baudot_wort)):
            if baudot_wort[i] == '*':
                binary[i + 3] = 1
        return list(binary)

    def _baudot_encode(self, wort: str) -> str:
        """
        String Wort als Baudot Code encodieren
        :param wort: Input Wort als String
        :return: baudot-encodiertes Wort als Zeichenkette aus * und . für 1 und 0
        """
        with StringIO() as output_buffer:
            writer = handlers.TapeWriter(output_buffer)
            encode_str(wort, codecs.ITA2_STANDARD, writer)
            output = output_buffer.getvalue()
        baudot_string = output.replace('.', '').replace('\n', '').replace(' ', '.')
        # Automatisch hinzugefügtes Anfangszeichen abschneiden
        baudot_string = baudot_string[5:]
        return baudot_string


class Ganzzahl(Wort):

    def __init__(self, strWort: str):
        super().__init__(strWort)
        self.float_rep = float(self.strWort)
        if abs(self.float_rep) > (2 ** 35) - 1 or self.float_rep % 1 != 0.0:
            raise Exception(f"Strichzahl {self.float_rep} is out of bound.")

    def getBinary(self) -> list:
        """
        Binärzahl aus String erstellen
        :return: 38-stellige Binärzahl als Liste
        """

        bin_number = list(bin(int(self.strWort)).split("b")[1].strip(" "))

        while len(bin_number) < 35:
            bin_number.insert(0, 0)

        if self.float_rep >= 0:
            bin_number = [0, 0, 0] + bin_number
        if self.float_rep < 0:
            bin_number = [1, 1, 1] + bin_number

        bin_number = [int(item) for item in bin_number]

        return bin_number

    def getInt(self) -> int:
        return int(self.strWort)


if __name__ == '__main__':
    w1 = parse('PPQQE1850')
    w2 = parse('A0')
    w3 = parse('D')
    w4 = parse('SCHLOS')
    w5 = parse('2\'')
    w6 = parse('B0+1900')
    w7 = parse('PQE1850')
    w8 = parse('0')
    w9 = parse('7\'')
    w10 = parse('-7\'')

    print('Typ von String {} ist {}'.format(w1.strWort, type(w1)))
    print('Typ von String {} ist {}'.format(w2.strWort, type(w2)))
    print('Typ von String {} ist {}'.format(w3.strWort, type(w3)))
    print('Typ von String {} ist {}'.format(w4.strWort, type(w4)))
    print('Typ von String {} ist {}'.format(w5.strWort, type(w5)))
    print('Typ von String {} ist {}'.format(w6.strWort, type(w6)))
    print('Typ von String {} ist {}'.format(w7.strWort, type(w7)))
    print('Typ von String {} ist {}'.format(w8.strWort, type(w8)))

    print(w1.getBinary())
    print(w2.getBinary())
    print(parseBinary(w2.getBinary()))

    print(w3.getBinary())
    print(parseBinary(w3.getBinary()))

    print(w4.getBinary())
    print(w5.getBinary())
    print(w6.getBinary())
    print(parseBinary(w6.getBinary()))

    print(w7.getBinary())
    print(w8.getBinary())

    print(w5.getBinary())
    print(parseBinary(w5.getBinary()))

    print(w8.getBinary())
    print(parseBinary(w8.getBinary()))

    print(w9.getBinary())
    print(parseBinary(w9.getBinary()))

    print(w10.getBinary())
    print(parseBinary(w10.getBinary()))
    print(type(parseBinary(w10.getBinary())))
