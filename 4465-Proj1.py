import random

class Seller:
    def __init__(self, money, pref, min):
        self.money = money
        self.pref = pref
        self.min = min
    

class Buyer:
    def __init__(self, money, pref, max):
        self.money = money
        self.pref = pref
        self.max = max

    
numPeople = 10

money = [random.randint(40000,100000) for x in range(numPeople)]

buyerPref = [random.randint(0,40) for x in range(numPeople/2)]
buyerMax = [x+10 for x in buyerPref]

sellerPref = [random.randint(20,60) for x in range(numPeople/2)]
sellerMin = [x-10 for x in sellerPref]


for i in range(numPeople):
    Buyer(money[i], buyerPref[i], buyerMax[i])
    Seller(money[i], sellerPref[i], sellerMin[i])
    