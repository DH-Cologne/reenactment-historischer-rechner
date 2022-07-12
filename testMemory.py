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
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
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

    # Überprüfung der Umwandlung einer Binärzahl in einen Befehls-String
    def testBefehlParseBinary(self):
        w1 = wort.parse('PPQQE1850')
        self.assertEqual(wort.parseBinary(w1.getBinary()).strWort, w1.strWort)
        self.assertIsInstance(wort.parseBinary(w1.getBinary()), wort.Befehl)
        w2 = wort.parse('A0')
        self.assertEqual(wort.parseBinary(w2.getBinary()).strWort, w2.strWort)
        self.assertIsInstance(wort.parseBinary(w2.getBinary()), wort.Befehl)
        w3 = wort.parse('D')
        self.assertEqual(wort.parseBinary(w3.getBinary()).strWort, w3.strWort)
        self.assertIsInstance(wort.parseBinary(w3.getBinary()), wort.Befehl)
        w4 = wort.parse('B0+1900')
        self.assertEqual(wort.parseBinary(w4.getBinary()).strWort, w4.strWort)
        self.assertIsInstance(wort.parseBinary(w4.getBinary()), wort.Befehl)
        w5 = wort.parse('CA1')
        self.assertEqual(wort.parseBinary(w5.getBinary()).strWort, w5.strWort)
        self.assertIsInstance(wort.parseBinary(w5.getBinary()), wort.Befehl)
        w6 = wort.parse('F1000')
        self.assertEqual(wort.parseBinary(w6.getBinary()).strWort, w6.strWort)
        self.assertIsInstance(wort.parseBinary(w6.getBinary()), wort.Befehl)
        w7 = wort.parse('B1730')
        self.assertEqual(wort.parseBinary(w7.getBinary()).strWort, w7.strWort)
        self.assertIsInstance(wort.parseBinary(w7.getBinary()), wort.Befehl)
        w8 = wort.parse('AV0')
        self.assertEqual(wort.parseBinary(w8.getBinary()).strWort, w8.strWort)
        self.assertIsInstance(wort.parseBinary(w8.getBinary()), wort.Befehl)

    # Überprüfung parse() Methode für alle möglichen Inputs
    def testParse(self):
        input1 = '' # empty string --> Ganzzahl 0
        self.assertIsInstance(wort.parse(input1), wort.Ganzzahl)
        input2 = '1\'' # Ganzzahl
        self.assertIsInstance(wort.parse(input2), wort.Ganzzahl)
        input3 = '0' # Ganzzahl
        self.assertIsInstance(wort.parse(input3), wort.Ganzzahl)
        input14 = 1  # Ganzzahl
        self.assertIsInstance(wort.parse(input14), wort.Ganzzahl)
        input4 = '-7\''  # Ganzzahl
        self.assertIsInstance(wort.parse(input4), wort.Ganzzahl)
        input5 = 'SCHLOS' # Klartext
        self.assertIsInstance(wort.parse(input5), wort.Klartext)
        input6 = 'ALT' # Klartext
        self.assertIsInstance(wort.parse(input6), wort.Klartext)
        input7 = '.'  # Klartext
        self.assertIsInstance(wort.parse(input7), wort.Klartext)
        input8 = 'KARTOFFEL' # Klartext (wird abgeschnitten)
        self.assertIsInstance(wort.parse(input8), wort.Klartext)
        input9 = 'B0+1900' # Befehl
        self.assertIsInstance(wort.parse(input9), wort.Befehl)
        input10 = 'D' # Befehl
        self.assertIsInstance(wort.parse(input10), wort.Befehl)
        input11 = 'I1' # Befehl
        self.assertIsInstance(wort.parse(input11), wort.Befehl)
        input12 = '%%%' # parse nicht möglich --> Exception
        self.assertRaises(Exception, wort.parse, input12)
        input13 = 'καλημέρα'  # parse nicht möglich --> Exception
        self.assertRaises(Exception, wort.parse, input13)
        inp = 'CI15'
        bef = wort.parse(inp)
        self.assertIsInstance(bef, wort.Befehl)
        self.assertEqual(str(bef), "CI15")
        self.assertCountEqual(bef.getBinary(), [1,0, 0,0,0,0,0,1,0,0,0,1,1,0,0,1,0,0,0,0, 0,1,1,1,1, 0,0,0,0,0,0,0,0,0,0,0,0,0])

    # parseBinary Methode überprüfen für alle Objekttypen
    def testParseBinary(self):
        bin1 = [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0]
        self.assertIsInstance(wort.parseBinary(bin1), wort.Klartext)
        bin2 = [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0]
        self.assertIsInstance(wort.parseBinary(bin2), wort.Befehl)
        bin3 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        self.assertIsInstance(wort.parseBinary(bin3), wort.Ganzzahl)
        bin4 = [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]
        self.assertIsInstance(wort.parseBinary(bin4), wort.Ganzzahl)
        # Input enthält ungültige Werte
        bin5 = [5, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]
        self.assertRaises(Exception, wort.parseBinary, bin5)
        # Input zu kurz
        bin6 = [1, 1, 1, 0, 0]
        self.assertRaises(Exception, wort.parseBinary, bin6)
        # Input zu lang
        bin7 = [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                1, 1, 1, 1, 0]
        self.assertRaises(Exception, wort.parseBinary, bin7)
        bin8 = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1]
        self.assertEqual(38, len(bin8))
        #befehl = wort.parseBinary(bin8)
        #self.assertIsInstance(befehl, wort.Befehl)
        
        
        binString = [1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.assertEqual(38, len(binString))
        befehl = wort.parseBinary(binString)
        self.assertIsInstance(befehl, wort.Befehl)
        self.assertEqual("LLA0", str(befehl))
        
        binString = [1,0, 0,0,0,0,0,1,0,0,0,1,1,0,0,1,0,0,0,0, 0,1,1,1,1, 0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.assertEqual(38, len(binString))
        befehl = wort.parseBinary(binString)
        self.assertIsInstance(befehl, wort.Befehl)
        self.assertEqual("CI15", str(befehl))
        
        
        
  

    # getBinary Funktion von Klartext Klasse überprüfen
    def testKlartextGetBinary(self):
        w1 = wort.parse('SCHLOS')
        self.assertEqual([0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0,
                          1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0],
                         w1.getBinary())
        w2 = wort.parse('ALT')
        self.assertEqual([0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0,
                          0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         w2.getBinary())
        w3 = wort.parse('.')
        self.assertEqual([0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         w3.getBinary())
        w4 = wort.parse('KARTOFFEL') # wird abgeschnitten
        self.assertEqual([0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0,
                          1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0],
                         w4.getBinary())

    # Binary --> Klartext Funktion überprüfen
    def testParseKlartext(self):
        w1 = wort.parse('SCHLOS')
        self.assertEqual(wort.parseBinary(w1.getBinary()).strWort, w1.strWort)
        self.assertIsInstance(wort.parseBinary(w1.getBinary()), wort.Klartext)
        w2 = wort.parse('ALT')
        self.assertEqual(wort.parseBinary(w2.getBinary()).strWort, w2.strWort)
        self.assertIsInstance(wort.parseBinary(w2.getBinary()), wort.Klartext)
        w3 = wort.parse('.')
        self.assertEqual(wort.parseBinary(w3.getBinary()).strWort, w3.strWort)
        self.assertIsInstance(wort.parseBinary(w3.getBinary()), wort.Klartext)

    def testParseGanzzahl(self):
        w1 = wort.parse('0')
        self.assertEqual(wort.parseBinary(w1.getBinary()).strWort, w1.strWort)
        self.assertIsInstance(wort.parseBinary(w1.getBinary()), wort.Ganzzahl)
        w2 = wort.parse('7\'')
        self.assertEqual(wort.parseBinary(w2.getBinary()).strWort, w2.strWort)
        self.assertIsInstance(wort.parseBinary(w2.getBinary()), wort.Ganzzahl)
        w3 = wort.parse('-7\'')
        self.assertEqual(wort.parseBinary(w3.getBinary()).strWort, w3.strWort)
        self.assertIsInstance(wort.parseBinary(w3.getBinary()), wort.Ganzzahl)
        w4 = wort.parse(0)
        self.assertEqual(wort.parseBinary(w4.getBinary()).strWort, w4.strWort)
        self.assertIsInstance(wort.parseBinary(w4.getBinary()), wort.Ganzzahl)
        w5 = wort.parse(1)
        self.assertEqual(wort.parseBinary(w5.getBinary()).strWort, w5.strWort)
        self.assertIsInstance(wort.parseBinary(w5.getBinary()), wort.Ganzzahl)
        # w6 = wort.parse('1256782340891236\'')
        # self.assertRaises(Exception, wort.Ganzzahl, w6)
        w6 = wort.parse('12567823408\'')
        self.assertRaises(Exception, wort.Ganzzahl, w6)
        w7 = wort.parse('-1256\'')
        self.assertRaises(Exception, wort.Ganzzahl, w7)
        # w8 = wort.parse('1.9\'')
        # self.assertRaises(Exception, wort.Ganzzahl, w8)
        w9 = wort.parse('1.0\'')
        self.assertRaises(Exception, wort.parseBinary, w9)


if __name__ == '__main__':
    unittest.main()
