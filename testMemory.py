import unittest

import memory as m
import wort


class MemoryTest(unittest.TestCase):
    # Überprüfung des Values im Speicher, diese werden als Wort-Objekte abgespeichert
    def testMemory(self):
        speicher = m.Memory()
        self.assertIsInstance(speicher.memory, dict)
        for key, value in speicher.memory.items():
            self.assertIsInstance(value, wort.Wort)

    # Überprüfung der get- und set-Methode
    def testGetterSetter(self):
        # es ist möglich, Strings oder Wort-Objekte abzuspeichern, Rückgabewert ist immer ein Wort-Objekt
        speicher = m.Memory()
        speicher.set(12, "SCHLOS")
        self.assertIsInstance(speicher.get(12), wort.Wort)
        speicher.set(13, "5'")
        self.assertIsInstance(speicher.get(12), wort.Wort)
        speicher.set(14, 'B0+1900')
        self.assertIsInstance(speicher.get(12), wort.Wort)
        speicher.set(15, 'E1720E')
        self.assertIsInstance(speicher.get(12), wort.Wort)
        # Begrenzung der Strings auf 6 Zeichen + andere Datentypen funktionieren nicht
        with self.assertRaises(Exception):
            speicher.set(4, "Akkumulator")
            speicher.set(12, 5)
            speicher.set(12, [2, 3, 4, 5, 6, 9])

    # Überprüfung der getAll-Methode
    def testGetAll(self):
        speicher = m.Memory()
        self.assertIsInstance(speicher.getAll(), dict)

    # Überprüfung der Befehls-Klasse + Methoden
    def testBefehlGetBinary(self):
        list_example = [0] * 38
        w1 = wort.parse('PPQQE1850')
        self.assertEqual(
            [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0,
             1, 0], w1.getBinary())
        self.assertEqual(len(list_example), len(w1.getBinary()))
        w2 = wort.parse('A0')
        self.assertEqual(
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0], w2.getBinary())
        self.assertEqual(len(list_example), len(w2.getBinary()))
        w3 = wort.parse('D')
        self.assertEqual(
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1,
             0, 0], w3.getBinary())
        self.assertEqual(len(list_example), len(w3.getBinary()))
        w4 = wort.parse('B0+1900')
        self.assertEqual(
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1,
             0, 0], w4.getBinary())
        self.assertEqual(len(list_example), len(w4.getBinary()))

    def testBefehlParseBinary(self):
        pass
        # TODO


if __name__ == '__main__':
    unittest.main()
