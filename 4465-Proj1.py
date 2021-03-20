import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
import math
import sympy as sym
import random
from sympy import exp

pop = 50
M0 = 50000
C = 0.9
S = 0.1

# Function that returns dm/dt
def model(M, t, mu):
    dmdt = M * mu
    return dmdt


t = np.arange(1, 13, 1)

# Solve ODEs
mu = 0.0
mt1 = odeint(model, M0, t, args=(mu,)).round(2)
mu = 0.1
mt2 = odeint(model, M0, t, args=(mu,)).round(2)
mu = -0.1
mt3 = odeint(model, M0, t, args=(mu,)).round(2)

# Total Income
Y1 = mt1 / pop
Y2 = mt2 / pop
Y3 = mt3 / pop

## This is the Income used for consumption
C1 = [int(Y * C) for Y in Y1]
C2 = [int(Y * C) for Y in Y2]
C3 = [int(Y * C) for Y in Y3]

Savings = 0.1
Savings1 = Y1 * Savings
Savings2 = Y2 * Savings
Savings3 = Y3 * Savings


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
        self.pref = random.randint(20, 60) * 0.01 * self.income
        self.min = self.pref * 0.8


class Buyer:

    savings = 0

    pref = None
    max = None

    spend = 0
    viableSellers = list()

    def __init__(self, sellers, consumption, savings):
        self.viableSellers = sellers
        self.savings = savings
        self.spend = consumption
        self.prices()

    def prices(self):
        self.pref = random.randint(0, 40) * 0.01 * self.spend
        self.max = self.pref * 1.2

    def negotiateWith(self, seller):

        if self.spend < self.max:
            self.pref = self.spend
            self.max = self.spend

        if seller.pref <= self.pref:
            # print("Easily Sold")
            self.spend -= seller.pref
            # seller.pref += seller.pref * .01
            # self.pref -= self.pref * .01
            return [seller.pref, self.pref, self.max, seller.pref, seller.min]

        if seller.min > self.max:
            # print("Not Sold")
            # seller.pref -= seller.pref * .01
            # self.pref += self.pref * .01
            return [-1, self.pref, self.max, seller.pref, seller.min]

        # print("Sold after Negotiating")
        self.spend -= (seller.pref + self.pref) / 2
        return [
            (seller.pref + self.pref) / 2,
            self.pref,
            self.max,
            seller.pref,
            seller.min,
        ]

    def determineFuture(self, seller):
        if self.spend < seller.min or self.max < seller.min:
            self.viableSellers.remove(seller)


def Model(pop, M, consumption, savings):

    NumSellers = int(pop / 2)
    NumBuyers = int(pop / 2)

    consumptionsUnadjusted = [random.gauss(40000, 10000) for x in range(pop)]
    consumptions = [
        (i / sum(consumptionsUnadjusted)) * consumption for i in consumptionsUnadjusted
    ]

    savingsUnadjusted = [random.gauss(6000, 2000) for x in range(pop)]
    savings = [(i / sum(savingsUnadjusted)) * savings for i in savingsUnadjusted]

    Buyers = []
    Sellers = []

    for i in range(NumSellers):
        Sellers.append(Seller(consumptions[i], savings[i]))

    for i in range(NumBuyers):
        Buyers.append(
            Buyer(Sellers[:], consumptions[i + NumSellers], savings[i + NumSellers])
        )

    TransactionInfo = []
    # print("\n")

    while len(Buyers) != 0:
        index = 0
        for buyer in Buyers:

            seller = random.choice(buyer.viableSellers)
            """
            print("Buyer  " + str(id(Buyers[index])) + " (preference $" + str(round(Buyers[index].pref, 2))  + 
                                                                ", max $" + str(round(Buyers[index].max))  +
                ")\nSeller " +   str(id(seller))   + " (preference $" + str(round(seller.pref, 2))         + 
                                                                ", min $" + str(round(seller.min))    + ")")
            """
            TransactionInfo.append(Buyers[index].negotiateWith(seller))

            # print("Transaction: $" + str(round(TransactionInfo[index][0], 2)))

            buyer.determineFuture(seller)

            if buyer.spend <= 0:
                # print("removed (no funds) " + str(id(buyer)))
                Buyers.remove(buyer)
            elif not buyer.viableSellers:
                # print("removed (funds insufficient for any seller) " + str(id(buyer)))
                Buyers.remove(buyer)

            # print("\n")

            index += 1

    Transactions = [round(x[0], 2) for x in TransactionInfo if x[0] != -1]

    """
    print("\nTransaction Log: " + str(Transactions))
    print("Number of transactions: " + str(len(Transactions)))
    print("Total money flow: $" + str(round(sum(Transactions), 2)))
    print(
        "Avg transaction amount: $"
        + str(
            round(
                sum(Transactions) / (len(Transactions) if len(Transactions) > 0 else 1)
            )
        )
        + "\n\n"
    )
    """

    return [Transactions, TransactionInfo]


first = []

for i in range(len(C1)):
    save = Model(pop, mt1, C1[i], Savings1[i])
    first.append(round(sum(save[0]) / (len(save[0]) if len(save[0]) > 0 else 1)))

print(first)

"""
normalTransactions = save[0]
supplyMinA = [x[4] for x in save[1]]
supplyPrefA = [x[3] for x in save[1]]
buyerMaxA = [x[2] for x in save[1]]
buyerPrefA = [x[1] for x in save[1]]
"""

second = []

for i in range(len(C2)):
    save = Model(pop, mt2, C2[i], Savings2[i])
    second.append(round(sum(save[0]) / (len(save[0]) if len(save[0]) > 0 else 1)))

print(second)

"""
inflationTransactions = save[0]
supplyMinB = [x[4] for x in save[1]]
supplyPrefB = [x[3] for x in save[1]]
buyerMaxB = [x[2] for x in save[1]]
buyerPrefB = [x[1] for x in save[1]]
"""

third = []

for i in range(len(C3)):
    save = Model(pop, mt3, C3[i], Savings3[i])
    third.append(sum(save[0]) / (len(save[0]) if len(save[0]) > 0 else 1))

print(third)

"""
from scipy.stats import variation
normal = variation(normalTransactions)
inflation = variation(inflationTransactions)


print("\n\n Variation (CV) base money supply: " + str(normal))
print(" Variation (CV) 10x base money supply: " + str(inflation))

normalTransactions.sort()
inflationTransactions.sort()
supplyMinA.sort()
buyerMaxA.sort(reverse=True)
supplyMinB.sort()
buyerMaxB.sort(reverse=True)

plt.figure(1)
plt.plot(
    [x for x in range(1, len(normalTransactions) + 1)],
    normalTransactions,
    label="Base Money Supply",
    linestyle="None",
    marker="o",
)
plt.plot(
    [x for x in range(1, len(inflationTransactions) + 1)],
    inflationTransactions,
    label="10x Base money Supply",
    linestyle="None",
    marker="o",
)
plt.xlabel("Transaction #")
plt.ylabel("Price")
plt.legend()
plt.title("Change in prices and number of transactions due to money supply changes")
plt.show()


plt.figure(2)
plt.plot(
    [x for x in range(1, len(supplyMinA) + 1)], supplyMinA, label="Supplier Min Price"
)
plt.plot([x for x in range(1, len(buyerMaxA) + 1)], buyerMaxA, label="Buyer Max Price")
plt.plot(
    [x for x in range(1, len(supplyMinB) + 1)],
    supplyMinB,
    label="Supplier Min Price (10x Money supply)",
)
plt.plot(
    [x for x in range(1, len(buyerMaxB) + 1)],
    buyerMaxB,
    label="Buyer Max Price (10x Money supply)",
)
plt.xlabel("Transaction Spectrum (Sorted by Price: Demand Desc, Supply Asc)")
plt.ylabel("Price")
plt.legend()
plt.title("Supply and Demand Shifts due to Money Supply Changes")
plt.xticks([])
plt.show()
"""

plt.figure(3)
plt.plot([x for x in range(0, len(first))], first, label="0% Growth")
plt.plot([x for x in range(0, len(second))], second, label="10% Growth")
plt.plot([x for x in range(0, len(third))], third, label="-10% Growth")
plt.xlabel("Time Period")
plt.ylabel("Price")
plt.legend()
plt.title("Equilibrium Prices of Different Money Supply Growth Rates Over Time")
plt.show()
