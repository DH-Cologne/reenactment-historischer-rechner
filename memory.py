import numpy as np
# https://python-baudot.readthedocs.io/en/latest/reference.html#baudot.codecs.BaudotCodec
from baudot import encode_str, codecs, handlers
from io import StringIO


# Frage: Trommelspeicher mit 8192 speicherzellen für je 1 Wort: Notwendig für unsere Implementierung,
# die obere Grenze festzulegen?

class Memory:
    """▶ Speicher: 38-stellige Binärzahlen (= 1 ‚Wort‘)
    ▶ Trommelspeicher: 8192 Speicherzellen für je 1 Wort (= 38.9 kB)
    ▶ Mittlere Zugriffszeit: 5 msec
    ▶ 256 mit je 32 Sektoren = 8192 = 213
    ▶ Schnellspeicher: 14 Zellen (Z22R: 25) „Ohne Zugriffszeit“ ▶ Adressen 0–31: Schnellspeicheradressen;
    4: Akkumulator"""

    """Interne Darstellung als 38-bit-Wort:
    1+2 Bit: Typ
    3. Bit: PP
    4. Bit: P
    5. Bit: QQ
    6. Bit: Q
    7. Bit: Y
    8. Bit: C
    9. Bit: N
    10. Bit: LL
    11. Bit: R
    12. Bit: R
    13. Bit: R
    14. Bit: R
    15. Bit: R
    16. Bit: R
    17. Bit: R
    18. Bit: R
    19. Bit: R
    20. Bit: R
    21.-25. Bit: Schnellspeicher (5 Bit)
    26.-38. Bit: Trommelspeicher (12 Bit)


    Speicherzelle 4: Akkumulator
    """

    # Z22 Intern-Code.pdf S. 2

    # Schnellspeicher: 0-31 (0 immer Nullen, 4 = Akkumulator)

    # Schnellspeicherzelle 0: Alles null
    # Schnellspeicherzelle 1: liefert "1" in der obersten Stelle (VZ bzw. Befehlskennzeichenstelle)
    # Schnellspeicherzelle 2: Vorzeichentestregister, sonst wie Speicher 6 bis 15 (Test bezieht sich nur auf die
    # oberste Dualstelle)
    # Schnellspeicherzelle 3: Testspeicherzelle für die unterste Stelle. Er kann mit dem Akkumulator zu gemeinsamen
    # Verschiebngen verkkolpelt werden. Einleitung einer 1'in der untersten Stelle bei H.
    # Schnellspeicherzelle 4: Akkumulator
    # Schnellspeicherzelle 5: Rückkehradressenregister
    # 6- 15
    # 16: Die Speicherzelle 16 ist mit Zelle 5 identisch, kann unter der Adresse 16 aber nur gelesen werden.

    memory = {}
    zero = {'0': np.zeros(38, dtype=np.int8)}
    akkumulator = {'4': np.zeros(38, dtype=np.int8)}

    def __init__(self):
        """ """
        self.memory = {}
        self.zero = {'0': np.zeros(38, dtype=np.int8)}
        self.akkumulator = {'4': np.zeros(38, dtype=np.int8)}
        pass

    def set(self, zelle, strWort) -> bool:
        """ """
        # wert kann binaerzahl oder string sein
        # binaerhandling.encode(word)
        pass

    def get(self, zelle, binary=False) -> str:
        """ """
        pass

    def getAll(self) -> dict:
        """ """
        pass


def _encode(input: str) -> list:
    # Repräsentation von Daten
    # 1. und 2. Bit: Type
    # 3. Bit 0 oder 1? Umschalter zwischen Zahlen und Buchstaben?
    # 7 Zeichen a 5 bits

    # Zahl: '-124'
    # Befehl: 'E1586'
    # Wort: 'Wort'

    # Repräsentation von Zahlen
    # Repräsentation von Buchstaben
    # Repräsentation von Befehlen

    # alles 38 bits (38-stellige Binärzahlen)

    # jede Speicherzelle hat 38 Dualstellen: eine Zahl, einen Befehl oder 7 Klartextzeichen

    # 00 negative Zahl
    # 11 positive Zahl
    # 01 Buchstaben
    # 10 Befehle

    input_str = ' '
    with StringIO() as output_buffer:
        writer = handlers.TapeWriter(output_buffer)
        encode_str(input_str, codecs.ITA2_STANDARD, writer)
        print(output_buffer.getvalue())
    pass


def _decode(input: list) -> str:
    pass


if __name__ == '__main__':
    pass
