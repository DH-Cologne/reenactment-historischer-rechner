import wort


class Memory:
    """
    Z22 Intern-Code.pdf S. 2
    Schnellspeicherzelle 0: Alles null
    Schnellspeicherzelle 1: liefert "1" in der obersten Stelle (VZ bzw. Befehlskennzeichenstelle)
    Schnellspeicherzelle 2: Vorzeichentestregister, sonst wie Speicher 6 bis 15 (Test bezieht sich nur auf die
    oberste Dualstelle)
    Schnellspeicherzelle 3: Testspeicherzelle für die unterste Stelle. Er kann mit dem Akkumulator zu gemeinsamen
    Verschiebngen verkkolpelt werden. Einleitung einer 1'in der untersten Stelle bei H.
    Schnellspeicherzelle 4: Akkumulator
    Schnellspeicherzelle 5: Rückkehradressenregister
    6- 15
    16: Die Speicherzelle 16 ist mit Zelle 5 identisch, kann unter der Adresse 16 aber nur gelesen werden.
    """

    def __init__(self):
        self.memory = {}
        # TODO: Akkumulator auch mir 'a' in dict? Extra Zugriff auf Akkumulator?
        self.memory.update({0: wort.parse('0\'')})
        self.memory.update({4: wort.parse('0\'')})
        self.memory.update({'b': wort.parse('0\'')})
        self.memory.update({'c': wort.parse('0\'')})

    def set(self, zelle, word):
        """ Saves word as object of class Wort in given cell """

        # if string parse string to object of class Wort
        if type(word) == str:
            if zelle in list(self.memory.keys()):
                self.memory[zelle] = wort.parse(word)
            else:
                self.memory.update({zelle: wort.parse(word)})
        # elif object of class Wort safe object
        elif type(word) == wort.Wort:
            if zelle in list(self.memory.keys()):
                self.memory[zelle] = word
            else:
                self.memory.update({zelle: word})
        # else raise Exception
        else:
            raise Exception(f"Type {type(word)} of {word} can not be processed in memory.")

    def get(self, zelle, binary=False):
        """ Returns content of given cell """

        # TODO: binary = True? noch notwendig?
        # if cell not in memory return 0
        if zelle not in list(self.memory.keys()):
            return wort.parse('0\'')
        else:
            return self.memory[zelle]

    def getAll(self) -> dict:
        """ Returns current state of memory

        :return: dict """
        return self.memory


if __name__ == '__main__':
    speicher = Memory()
    print(speicher.get(8))
    print(speicher.get(4))
    print(speicher.get(0))

    print(speicher.get(10))
    speicher.set(4, "Akkumulator")
    speicher.set(12, 5)
    speicher.set(12, [2, 3, 4, 5, 6, 9])
