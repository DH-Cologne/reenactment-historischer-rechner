import re
from word import Word

class Befehl(Word):
    re = re.compile(r"^(C|L|LL|N|PPQQ|PP|QQ|Y)*([ASIDBET]+)(\d+)(\+(\d+))?([TE])?$")

    def __init__(self, befehl):
        self.befehl = befehl
        m = self.re.match(self.befehl)
        if m:
            self.modifiers = m.group(1)
            self.commands = m.group(2)
            self.address  = int(m.group(3))
            if m.group(5):
                self.address2 = int(m.group(5))
            else:
                self.address2 = None
            self.postmodifiers = m.group(6)
        else: 
            self.modifiers = None
            self.commands = None
            self.address = None
            self.address2 = None
            self.postmodifiers = None

    def __repr__(self):
        s = ""
        if self.modifiers:
            s += self.modifiers
        s += self.commands
        s += str(self.address)
        if self.address2:
            s += "+"
            s += str(self.address2)
        if self.postmodifiers:
            s += self.postmodifiers
        return s


    def getCommands(self):
        return self.commands

    def isBandbefehl(self):
        return self.commands == "T" and self.postmodifiers == "T" or self.commands == "E" and self.postmodifiers == "E"
    
    def __bool__(self):
        return self.commands != None and self.address != None

if __name__ == '__main__':
    b = Befehl("A1000")
    print(b)
    print(b.isBandbefehl())
    b = Befehl("B0+1000")
    print(b)
    print(b.isBandbefehl())
    b = Befehl("T1700T")
    print(b)
    print(b.isBandbefehl())
    