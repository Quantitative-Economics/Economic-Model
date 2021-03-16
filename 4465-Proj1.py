import random


numPeople = 26
NumBuyers = int(.5 * numPeople)
NumSellers = int(.5 * numPeople)
s = .5                             # % of money supply in savings

M = 1000
V = 2.5
P = 2.5
Q = 1000

assert M * V == P * Q, "False equality."



class Seller:
    
    income = None
    savings = None

    pref = None
    min = None

    def __init__(self, income, savings):
        self.income = income
        self.savings = savings
        self.prices()
        

    def prices(self):
        self.pref = random.randint(20, 60) * .01 *self.income
        self.min = self.pref * .8
    


class Buyer:

    income = None
    savings = None

    pref = None
    max = None

    satisfied = 0
    notVisited = list()

    def __init__(self, sellers, income, savings):
        self.notVisited = sellers
        self.income = income
        self.savings = savings
        self.prices()
        

    def prices(self):
        self.pref = random.randint(0, 40) * .01 * self.income
        self.max = self.pref * 1.2

    def negotiateWith(self, seller):

        if (seller.pref <= self.pref):
            print("Easily Sold")
            self.satisfied = 1
            return seller.pref

        if (seller.min > self.max):
            print("Not Sold")
            return -1

        print("Sold after Negotiating")
        self.satisfied = 1
        return (seller.pref + self.pref)/2


#add up to total money supply
incomesUnadjusted = [random.gauss(40000, 10000) for x in range(numPeople)]
incomes = [(i/sum(incomesUnadjusted))*(1-s)*M for i in incomesUnadjusted]

savingsUnadjusted = [random.gauss(6000, 2000) for x in range(numPeople)]
savings = [(i/sum(savingsUnadjusted))*s*M for i in savingsUnadjusted]


# Other Info that we will pass to the agents



Buyers = []
Sellers = []

for i in range(NumSellers):
    Sellers.append(Seller(incomes[i], savings[i]))

for i in range(NumBuyers):
    Buyers.append(Buyer(Sellers[:], incomes[i+NumSellers], savings[i+NumSellers]))

Transactions = []
print("\n")

while len(Buyers) != 0:
    index = 0
    for buyer in Buyers:

        seller = random.choice(buyer.notVisited)

        print("Buyer  " + str(id(Buyers[index])) + " (preference $" + str(round(Buyers[index].pref, 2))  + 
                                                              ", max $" + str(round(Buyers[index].max))  +
              ")\nSeller " +   str(id(seller))   + " (preference $" + str(round(seller.pref, 2))         + 
                                                              ", min $" + str(round(seller.min))    + ")")
        
        Transactions.append(Buyers[index].negotiateWith(seller))

        print("Transaction: $" + str(round(Transactions[index], 2)))

        buyer.notVisited.remove(seller)

        if buyer.satisfied == 1:
            print("removed satisfied " + str(id(buyer)))
            Buyers.remove(buyer)

        if not buyer.notVisited:
            print("removed unsatisfied " + str(id(buyer)))
            Buyers.remove(buyer)

        print("\n")

        index += 1

Transactions = [round(x, 2) for x in Transactions if x != -1]

print("Transaction Log: " + str(Transactions))
print("Number of transactions: " + str(len(Transactions)))
print("Total money flow: $" + str(round(sum(Transactions), 2)))
print("Avg transaction amount: $" + str(round(sum(Transactions)/(len(Transactions) if len(Transactions) > 0 else 1))))
