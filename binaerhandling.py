# https://python-baudot.readthedocs.io/en/latest/reference.html#baudot.codecs.BaudotCodec
from baudot import encode_str, codecs, handlers
from io import StringIO


# Repräsentation von Zahlen
# Repräsentation von Buchstaben
# Repräsentation von Befehlen

# alles 38 bits (38-stellige Binärzahlen)

# jede Speicherzelle hat 38 Dualstellen: eine Zahl, einen Befehl oder 7 Klartextzeichen

## 00 negative Zahl
## 11 positive Zahl
## 01 Buchstaben
## 10 Befehle

def encode(input:str):
    # Zahl: '-124'
    # Befehl: 'E1586' 
    # Wort: 'Wort'
    pass

def decode(input:list):
    pass

input_str = ' '
with StringIO() as output_buffer:
    writer = handlers.TapeWriter(output_buffer)
    encode_str(input_str, codecs.ITA2_STANDARD, writer)
    print(output_buffer.getvalue())


"""▶ Speicher: 38-stellige Binärzahlen (= 1 ‚Wort‘)
▶ Trommelspeicher: 8192 Speicherzellen für je 1 Wort (= 38.9 kB) 
▶ Mittlere Zugriffszeit: 5 msec
▶ 256 mit je 32 Sektoren = 8192 = 213
▶ Schnellspeicher: 14 Zellen (Z22R: 25) „Ohne Zugriffszeit“ ▶ Adressen 0–31: Schnellspeicheradressen; 4: Akkumulator"""

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


# Repräsentation von Daten
# 1. und 2. Bit: Type
# 3. Bit 0 oder 1? Umschalter zwischen Zahlen und Buchstaben?
# 7 Zeichen a 5 bits
