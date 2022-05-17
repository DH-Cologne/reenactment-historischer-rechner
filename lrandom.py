class LutzRandom:
  def __init__(self):
    self.x = 12345678
  
  def nextnumber(self):
    x1 = ((self.x << 4) + self.x) >> 4
    self.x = x1
    # print("{0:b}".format(x1))
    return (x1 & 15)
  
  
if __name__ == "__main__":
  lr = LutzRandom()
  for i in range(10000):
    print(lr.nextnumber())