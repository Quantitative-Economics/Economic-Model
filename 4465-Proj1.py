import random
import matplotlib.pyplot as plt


numPeople = 50
NumBuyers = int(.5 * numPeople)
NumSellers = int(.5 * numPeople)
s = .5                             # % of money supply in savings

M = 10000
V = 2.5
P = 2.5
Q = 10000
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
    savings = 0

    pref = None
    max = None

    spend = 0
    viableSellers = list()

    def __init__(self, sellers, income, savings):
        self.viableSellers = sellers
        self.income = income
        self.savings += savings + income * .1
        self.spend = income * .9
        self.prices()
        

    def prices(self):
        self.pref = random.randint(0, 40) * .01 * self.income
        self.max = self.pref * 1.2

    def negotiateWith(self, seller):

        if (self.spend < self.max):
            self.pref = self.spend
            self.max = self.spend

        if (seller.pref <= self.pref):
            #print("Easily Sold")
            self.spend -= seller.pref
            #seller.pref += seller.pref * .01
            #self.pref -= self.pref * .01
            return seller.pref

        if (seller.min > self.max):
            #print("Not Sold")
            #seller.pref -= seller.pref * .01
            #self.pref += self.pref * .01
            return -1

        #print("Sold after Negotiating")
        self.spend -= (seller.pref + self.pref)/2
        return (seller.pref + self.pref)/2

    def determineFuture(self, seller):
        if  self.spend < seller.min or self.max < seller.min:
            self.viableSellers.remove(seller)


def Model(NumBuyers, NumSellers, M, s):

    numPeople = NumBuyers + NumSellers

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
    #print("\n")

    while len(Buyers) != 0:
        index = 0
        for buyer in Buyers:

            seller = random.choice(buyer.viableSellers)
            '''
            print("Buyer  " + str(id(Buyers[index])) + " (preference $" + str(round(Buyers[index].pref, 2))  + 
                                                                ", max $" + str(round(Buyers[index].max))  +
                ")\nSeller " +   str(id(seller))   + " (preference $" + str(round(seller.pref, 2))         + 
                                                                ", min $" + str(round(seller.min))    + ")")
            '''
            Transactions.append(Buyers[index].negotiateWith(seller))

            #print("Transaction: $" + str(round(Transactions[index], 2)))

            buyer.determineFuture(seller)

            if buyer.spend <= 0:
                #print("removed (no funds) " + str(id(buyer)))
                Buyers.remove(buyer)
            elif not buyer.viableSellers:
                #print("removed (funds insufficient for any seller) " + str(id(buyer)))
                Buyers.remove(buyer)

            #print("\n")

            index += 1

    Transactions = [round(x, 2) for x in Transactions if x != -1]

    print("\nTransaction Log: " + str(Transactions))
    print("Number of transactions: " + str(len(Transactions)))
    print("Total money flow: $" + str(round(sum(Transactions), 2)))
    print("Avg transaction amount: $" + str(round(sum(Transactions)/(len(Transactions) if len(Transactions) > 0 else 1))) + "\n\n")

    return Transactions


normalTransactions = Model(NumBuyers, NumSellers, M, s)

M = 100000     #increase money supply 10x

inflationTransactions = Model(NumBuyers, NumSellers, M, s)

from scipy.stats import variation

normal = variation(normalTransactions)
inflation = variation(inflationTransactions)

print("\n\n Variation (CV) base money supply: " + str(normal))
print(" Variation (CV) 10x base money supply: " + str(inflation))

plt.figure(1)
plt.plot([x for x in range(1, len(normalTransactions)+1)], normalTransactions, label='Base Money Supply', linestyle="None", marker='o')
plt.plot([x for x in range(1, len(inflationTransactions)+1)], inflationTransactions, label='10x Base money Supply', linestyle='None', marker='o')
plt.xlabel('Transaction #')
plt.ylabel('Price')
plt.legend()
plt.title("Change in prices and number of transactions due to money supply changes")
plt.show()
