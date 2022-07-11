import numpy as np
import re
# https://python-baudot.readthedocs.io/en/latest/reference.html#baudot.codecs.BaudotCodec
from baudot import encode_str, decode_to_str, codecs, handlers
from io import StringIO


def parse(input):
    """
    Prüfen, um welchen Untertyp es sich handelt und ein Objekt des entsprechenden Typs erstellen
    :param strWort: Wort als String
    :return: Objekt des jeweiligen Typs
    """
    obj = None
    if type(input) == str:
        input.strip()
        wort = input
        # check empty string -- and store as 0
        if wort == "":
          obj = Ganzzahl(0)
        # check Strichzahl
        elif wort[-1] == '\'':
            obj = Ganzzahl(input[0:-1])
        elif wort == '0':
            obj = Ganzzahl(input)
        # check Klartext (lexikalisches Wort)
        elif not bool(re.search(r'\d', wort)) and wort != 'D':
            obj = Klartext(input)
        # check Befehl
        elif (bool(re.search(r'\d', wort)) and bool(re.search('[A-Z]', wort))) or wort == 'D':
            obj = Befehl(input)
        # sonst fehlerhafter Input
        # NR: Vielleicht auch int akzeptieren und in Ganzzahl überführen?
        else:
            raise Exception(f"Objekttyp für Input {wort} konnte nicht identifiziert werden. \n Bitte Input überprüfen.")
    elif type(input) == int:
        obj = Ganzzahl(str(input))
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
        return _parseKlartext(binary)


def _parseGanzzahl(binary):
    if binary[2] == 0:
        number = int(''.join(map(str, binary[3:])), 2)
    elif binary[2] == 1:
        number = -int(''.join(map(str, binary[3:])), 2)

    else:
        raise Exception(f"{binary} is not valid.")

    return parse(str(number) + '\'')


def _parseBefehl(binary):
    # Überprüfung, ob die Binärzahl alle notwendigen Stellen hat
    if len(binary) != 38:
        raise Exception(f"{binary} is not valid.")

    # Initialisierung aller Befehle als Vokabular + Sonderfall-Speicherzelle für B-Befehl
    voc = ['PP', 'P', 'QQ', 'Q', 'Y', 'C', 'N', 'LL', 'R', 'U', 'A', 'S', 'F', 'K', 'H', 'Z', 'G', 'V']
    spec = [1900, 1950, 1990, 1993, 1996]
    # Initialisierung des Befehls-String
    operation = str()
    # Überprüfung, ob es sich um einen E-Befehl handelt
    # hierbei müssen Stellen 11,12 und 14 = 0 sein
    if all(v == 0 for v in binary[11:13]) and (binary[14] == 0):
        for i, b in enumerate(binary[2:10]):
            if b != 0:
                operation += str(voc[i])
        operation += 'E'
        for i, b in enumerate(binary[13:20]):
            if b != 0:
                operation += str(voc[13 + i])
    # alle anderen Befehle können einfach aneinander gekettet werden
    else:
        for i, b in enumerate(binary[2:20]):
            if b != 0:
                operation += str(voc[i])

    # Schnell- und Trommelspeicher werden aus Binärzahl dekodiert
    schnellspeicher = int(''.join(map(str, binary[20:25])), 2)
    trommelspeicher = int(''.join(map(str, binary[25:])), 2)

    # Auflösung von Sonderfällen I, L, B, T und D
    if operation.__contains__('UA') or operation.__eq__('UA'):
        operation = operation.replace('UA', 'I')
    if operation.__contains__('LLR') or operation.__eq__('LLR'):
        operation = operation.replace('LLR', 'L')
    if operation.__contains__('NA') or operation.__eq__('NA'):
        operation = operation.replace('NA', 'B')
    if operation.__contains__('NU') or operation.__eq__('NU'):
        operation = operation.replace('NU', 'T')
    if (operation.__contains__('F') or operation.__eq__('F')) and trommelspeicher == 644:
        operation = operation.replace('F', 'D')
        schnellspeicher = 0
        trommelspeicher = 0

    # Zusammenfügen der Befehls- und Speicherstrings
    # Schnell- und Trommelspeicher
    if trommelspeicher >= 32 and schnellspeicher < 32:
        # Schnellspeicher ist 0
        if schnellspeicher == 0:
            # Sonderfall Befehl B<s>+<t>
            if operation.__contains__('B'):
                # workaround: Unterschied zwischen Binärzahl von 'B1900' und 'B0+1900' noch nicht klar
                # die hier überprüften Speicherzellen kommen nur in Zusammenhang mit 'B0+' vor
                if spec.__contains__(trommelspeicher):
                    return parse(operation + str(schnellspeicher) + '+' + str(trommelspeicher))
                # alle anderen werden einfach an den Befehl dran gehängt
                else:
                    return parse(operation + str(trommelspeicher))
            # andernfalls wird nur Trommelspeicher angegeben
            # interne Darstellung, wenn Schnellspeicher nicht genutzt wird: <Befehl>0+<t>
            # extern abkürzbar mit: <Befehl><t>
            else:
                return parse(operation + str(trommelspeicher))
        # wenn Schnellspeicher != 0 ist, dann werden beide Speicherstellen mit einem + verbunden
        else:
            return parse(operation + str(schnellspeicher) + '+' + str(trommelspeicher))

    # wenn nur der Schnellspeicher genutzt wird, ist die Stelle K = 1
    # in externer Darstellung wird das K aber nicht angezeigt
    # z.B. AK0 -> A0
    if operation.__contains__('K'):
        return parse(operation.replace('K', '') + str(schnellspeicher))

    # Sonderfall D: nur Befehl wird ausgegeben
    if operation.__contains__('D'):
        return parse(operation)


def _parseKlartext(binary):
    # von Binärdarstellung als Liste mit 0 und 1 zu String Wort
    bin_word = binary
    # Liste aus 0 und 1 als baudot Tape darstellen
    tape = _binaryToTape(bin_word)
    with StringIO(tape) as code_stream:
        reader = handlers.TapeReader(code_stream)
        decoded = decode_to_str(reader, codecs.ITA2_STANDARD)
    return decoded


def _binaryToTape(bin_word):
    # Binärliste zu baudot tape Repräsentation umwandeln
    # Umschalttaste checken (für korrekte Darstellung von Punkt)
    if bin_word[2] == 0:
        tape_encoded = '***.**\n'
    else:
        tape_encoded = '** .**\n'
    # Erste drei Stellen abschneiden
    bin_word = bin_word[3:]
    # Über Slices von je 5 bits iterieren und baudot tape enkodieren
    for i in range(0,len(bin_word),5):
        bin_char = bin_word[i:i+5]
        # Nicht enkodieren wenn in den 5 bits alle 0 sind --> Wort zu Ende
        if all(x == 0 for x in bin_char):
            break
        # line breaks einfügen, die für Tape Enkodierung notwendig sind
        # Punkte einfügen, die für Tape Enkodierung notwendig sind
        for j in range(len(bin_char)):
            if j == 3:
                tape_encoded += '.'
            if bin_char[j] == 0:
                tape_encoded += ' '
            elif bin_char[j] == 1:
                tape_encoded += '*'
            else:
                raise Exception(f"Binärwort {bin_word} enthält Elemente, die nicht 0 oder 1 sind")
        tape_encoded += '\n'
    return(tape_encoded)

class Wort:
    def __init__(self, strWort: str):
        self.strWort = strWort

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

        # trennen von Operations- + Adressteil
        match = re.match(r"([a-z]+)(\d+)?([+]\d+)?([a-z]+)?", befehl, re.I)
        if match:
            items = match.groups()
            items = [i for i in items if i is not None]

            # Zusammenfügen der einzelnen Teile zu einer Binärzahl
            binary += self.encode(items)

        return binary

    def encode(self, items: list) -> list:
        """
        Übegeordnete Funktion zur Umwandlung des Operations- und Speicherteils der Binärzahl
        Deckt besondere Fälle ab
        :param items: Liste mit aufgetrennten String-Befehl
        :return: Binärzahl des Befehls
        """
        operations = [i for i in items if i.isalpha()]
        adressen = [i for i in items if i.isnumeric() | i.__contains__('+')]

        # Umwandlung in Binärzahl
        operation = self._encodeOperation(operations)
        # wenn die Operation == D ist, dann wird die Speicherzelle auf 644 gesetzt
        if operations.__contains__('D'):
            b = format(644, 'b')
            speicher = ([0] * 5) + (([0] * (13 - len(b))) + (list(map(int, list(b)))))
        # in allen anderen Fällen wird der String in eine Binärzahl umgewandelt
        else:
            speicher = self._encodeAddress(adressen)
        # wenn nur eine Schnellspeicheradresse angegeben ist, dann wird K = 1 gesetzt
        if all(v == 0 for v in speicher[5:]):
            operation[13] = 1

        return operation + speicher

    def _encodeOperation(self, operation_list: list) -> list:
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
                operation[10] = 1
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
            if o.__contains__('I'):
                operation[9] = 1
                operation[10] = 1

        return operation

    def _encodeAddress(self, address_list: list) -> list:
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
            if a >= 32:
                # Umwandlung in Binärzahl
                binary = format(a, 'b')
                # Trommelspeicher hat insgesamt 13 Stellen. Die, die nicht für die Binärzahl gebraucht werden,
                # werden mit 0 gefüllt
                trommelspeicher = [0] * (13 - len(binary))
                trommelspeicher += list(map(int, list(binary)))
            # Schnellspeicher
            elif a < 32:
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
        baudot_wort = self._baudotEncode(wort)
        # Entsprechende Bits auf 1 setzen
        for i in range(len(baudot_wort)):
            if baudot_wort[i] == '*':
                binary[i + 3] = 1
        return list(binary)

    def _baudotEncode(self, wort: str) -> str:
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
    
    
    def __int__(self) -> int:
        """
        This allows using int() on a Ganzzahl object
        """
        return self.getInt()
        
    def toBefehl(self):
        pass


if __name__ == '__main__':
    w1 = parse('PPQQE1850')
    w2 = parse('A0')
    w3 = parse('D')
    w4 = parse('SCHLOS')
    w5 = parse('2\'')
    w6 = parse('B0+1900')
    w7 = parse('B1900')
    w8 = parse('0')
    w9 = parse('7\'')
    w10 = parse('-7\'')
    w11 = parse('CA1')
    w12 = parse('1\'')
    w13 = parse('1\'')
    w14 = parse('I1')


    print('Typ von String {} ist {}'.format(w1.strWort, type(w1)))
    print('Typ von String {} ist {}'.format(w2.strWort, type(w2)))
    print('Typ von String {} ist {}'.format(w3.strWort, type(w3)))
    print('Typ von String {} ist {}'.format(w4.strWort, type(w4)))
    print('Typ von String {} ist {}'.format(w5.strWort, type(w5)))
    print('Typ von String {} ist {}'.format(w6.strWort, type(w6)))
    print('Typ von String {} ist {}'.format(w7.strWort, type(w7)))
    print('Typ von String {} ist {}'.format(w8.strWort, type(w8)))
    print('Typ von String {} ist {}'.format(w12.strWort, type(w12)))
    print('Typ von String {} ist {}'.format(w13.strWort, type(w13)))
    print('Typ von String {} ist {}'.format(w14.strWort, type(w14)))

    print(w1.getBinary())
    print(parseBinary(w1.getBinary()))

    print(w2.getBinary())
    print(parseBinary(w2.getBinary()))


    print(w4.getBinary())
    print(w5.getBinary())
    print(w6.getBinary())
    print(parseBinary(w6.getBinary()))

    print(w7.getBinary())
    print(parseBinary(w7.getBinary()))
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

    print(w11.getBinary())
    print(parseBinary(w11.getBinary()))

    print(w12.getBinary())
    print(parseBinary(w12.getBinary()))

    print(w13.getBinary())
    print(parseBinary(w13.getBinary()))

    print(w14.getBinary())
    print(parseBinary(w14.getBinary()))

    print(w3.getBinary())
    print(parseBinary(w3.getBinary()))

    # # checken, ob _parseKlartext binär --> String funktioniert
    # w4 = parse('ALT')
    # bin_w4 = w4.getBinary()
    # print(bin_w4)
    # tape = _binaryToTape(bin_w4)
    # decodedWort = _parseKlartext(bin_w4)
    # print(decodedWort)
    # # Okay, dass Leerzeichen bei Dekodierung mit ausgegeben wird?
    #
    # wort = 'ALT '
    # with StringIO() as output_buffer:
    #     writer = handlers.TapeWriter(output_buffer)
    #     encode_str(wort, codecs.ITA2_STANDARD, writer)
    #     output = output_buffer.getvalue()
    #
    # # Gegencheck: Tape Output von _binaryToTape == Decoding Output von baudot Bibliothek?
    # print(tape.replace('\n', '/'))
    # print(output.replace('\n', '/'))
    # print(tape == output)
