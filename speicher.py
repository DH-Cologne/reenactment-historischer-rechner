import binaerhandling
import numpy as np

# Frage: Trommelspeicher mit 8192 speicherzellen für je 1 Wort: Notwendig für unsere Implementierung, die obere Grenze festzulegen?
# Schnellspeicher: 0-31 (0 immer Nullen, 4 = Akkumulator)

# Frage: Optional: Verwendung von zwei Zellen für eine Zahl (doppelte Länge!)??

### Z22 Intern-Code.pdf S. 2

# Schnellspeicherzelle 0: Alles null
# Schnellspeicherzelle 1: liefert "1" in der obersten Stelle (VZ bzw. Befehlskennzeichenstelle)
# Schnellspeicherzelle 2: Vorzeichentestregister, sonst wie Speicher 6 bis 15 (Test bezieht sich nur auf die oberste Dualstelle)
# Schnellspeicherzelle 3: Testspeicherzelle für die unterste Stelle. Er kann mit dem Akkumulator zu gemeinsamen Verschiebngen verkkolpelt werden. Einleitung einer 1'in der untersten Stelle bei H.
# Schnellspeicherzelle 4: Akkumulator
# Schnellspeicherzelle 5: Rückkehradressenregister
# 6- 15
# 16: Die Speicherzelle 16 ist mit Zelle 5 identisch, kann unter der Adresse 16 aber nur gelesen werden.

# erste beide bits

class Speicher(): 
    speicher = {}
    zero = {'0':np.zeros(38, dtype=np.int8)}
    akkumulator = {'4':np.zeros(38, dtype=np.int8)}


    def schreibe(self, zelle, wert):
        binaerhandling.encode(wert)
        pass
    def lese(self, zelle):
        pass
    
    def __init__(self):
        pass
