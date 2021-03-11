import random


numPeople = 10
NumBuyers = int(.5 * numPeople)
NumSellers = int(.5 * numPeople)

M = 1000000
V = 2.5
P = 2.5
Q = 1000000

assert M * V == P * Q, "False equality."



class Seller:

    income = None

    pref = None
    min = None

    def __init__(self, income):
        self.income = income
        self.prices()
        

    def prices(self):
        self.pref = random.randint(20,60)
        self.min = self.pref - 10
    


class Buyer:

    income = None

    pref = None
    max = None

    def __init__(self, income):
        self.income = income
        self.prices()
        

    def prices(self):
        self.pref = random.randint(0,40)
        self.max = self.pref + 10

    def negotiateWith(self, seller):

        if (seller.pref <= self.pref):
            print("Easily Sold")
            return

        if (seller.min > self.max):
            print("Not Sold")
            return

        print("Sold after Negotiating")


#Needs to add up to total money supply
incomes = [random.randint(30000,120000) for x in range(numPeople)]

# Other Info that we will pass to the agents



Buyers = []
Sellers = []

for i in range(NumBuyers):
    Buyers.append(Buyer(incomes[i]))

for i in range(NumSellers):
    Sellers.append(Seller(incomes[i+NumBuyers]))



for i in range(NumBuyers):
    for j in range(NumSellers):
        Buyers[i].negotiateWith(Sellers[j])
