class Word:
 def __init__(self, value):
  self.value = value

class Befehl(Word):
 pass

class Strichzahl(Word):
 def __int__(self):
  return int(self.value, clbase=2)
 pass

class Klartext(Word):
 pass

def fromBinary(binaryString):
 if binaryString[:2] == "10":
  return Befehl(binaryString)
 elif binaryString[:2] == "01":
  return Klartext(binaryString)
 else:
  return Strichzahl(binaryString)


if __name__=="__main__":
 print(type(fromBinary("10001010101000")))