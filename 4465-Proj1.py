import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
import math
import sympy as sym
import random
from sympy import exp

pop = 1000
M0 = 50000000
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

    savings = None
    cogs = None

    pref = None
    min = None

    def __init__(self, cogs, savings, M):
        self.cogs = cogs
        self.savings = savings
        self.prices(M)

    def prices(self, M):
        self.pref = random.randint(20, 60) * self.cogs
        self.min = self.pref * 0.8

    # float(1 + ((M - M0) / M0))


class Buyer:

    purchaseGoal = 500  # Goal

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
            seller.savings += seller.pref - seller.cogs
            self.purchaseGoal -= 1

            # self.pref += seller.pref * 0.01
            # seller.min = seller.pref * 0.8
            # self.pref -= self.pref * 0.01

            return [seller.pref, self.pref, self.max, seller.pref, seller.min]

        if seller.min > self.max:
            # print("Not Sold")
            # seller.pref -= seller.pref * 0.01
            # self.pref += self.pref * 0.01
            # self.max = self.pref * 1.2

            return [-1, self.pref, self.max, seller.pref, seller.min]

        # print("Sold after Negotiating")
        self.spend -= (seller.pref + self.pref) / 2
        seller.savings += ((seller.pref + self.pref) / 2) - seller.cogs
        self.purchaseGoal -= 1
        return [
            (seller.pref + self.pref) / 2,
            self.pref,
            self.max,
            seller.pref,
            seller.min,
        ]

    def determineFuture(self, seller):
        if self.purchaseGoal == 0:
            self.viableSellers.clear()
        elif self.spend < seller.min or self.max < seller.min:
            self.viableSellers.remove(seller)


def Model(pop, M, consumption, savings, buyerGoal):

    NumSellers = int(pop * 0.04)
    NumBuyers = int(pop * 0.96)

    consumptionsUnadjusted = [random.gauss(40000, 10000) for x in range(NumBuyers)]
    consumptions = [
        (i / sum(consumptionsUnadjusted)) * consumption for i in consumptionsUnadjusted
    ]

    savingsUnadjusted = [random.gauss(6000, 2000) for x in range(pop)]
    savings = [(i / sum(savingsUnadjusted)) * savings for i in savingsUnadjusted]

    allBuyers = []
    allSellers = []

    for i in range(NumSellers):
        allSellers.append(
            Seller((sum(consumptions) / len(consumptions)) * 0.02, savings[i], int(M))
        )

    for i in range(NumBuyers):
        allBuyers.append(Buyer(allSellers[:], consumptions[i], savings[i + NumSellers]))

    Buyers = allBuyers[:]
    Sellers = allSellers[:]

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

    totalSavings = 0

    for x in allBuyers:
        totalSavings += x.savings

    for x in allSellers:
        totalSavings += x.savings

    def interestRate():

        stillWant = 0

        for x in allBuyers:
            if x.purchaseGoal != 0:
                stillWant += x.purchaseGoal

        moneyDemand = int(M) + (stillWant) * (
            sum(Transactions) / (len(Transactions) if len(Transactions) > 0 else 1)
        )

        # print("Money Demanded: " + str(moneyDemand))

        r = sym.Symbol("r")
        y = sym.solve(
            sym.Eq(moneyDemand, int(totalSavings) + (0.1 / 500) * M0 * (buyerGoal / r)),
            r,
        )

        if len(y) == 0:
            y.append(0)

        return [y[0], moneyDemand]

    return [Transactions, TransactionInfo, interestRate(), totalSavings]


first = []

for i in range(len(C1)):
    save = Model(pop, mt1[i], C1[i], Savings1[i], 500)
    first.append(
        [
            (sum(save[0]) / (len(save[0]) if len(save[0]) > 0 else 1)),
            (len(save[0])),
            save[2][0],
            mt1[i],
            save[3],
            save[2][1],
        ]
    )

# print(first)

"""
normalTransactions = save[0]
supplyMinA = [x[4] for x in save[1]]
supplyPrefA = [x[3] for x in save[1]]
buyerMaxA = [x[2] for x in save[1]]
buyerPrefA = [x[1] for x in save[1]]
"""

second = []

for i in range(len(C2)):
    save = Model(pop, mt2[i], C2[i], Savings2[i], 500)
    second.append(
        [
            (sum(save[0]) / (len(save[0]) if len(save[0]) > 0 else 1)),
            (len(save[0])),
            save[2][0],
            mt1[i],
            save[3],
            save[2][1],
        ]
    )

# print(second)

"""
inflationTransactions = save[0]
supplyMinB = [x[4] for x in save[1]]
supplyPrefB = [x[3] for x in save[1]]
buyerMaxB = [x[2] for x in save[1]]
buyerPrefB = [x[1] for x in save[1]]
"""

third = []

for i in range(len(C3)):
    save = Model(pop, mt3[i], C3[i], Savings3[i], 500)
    third.append(
        [
            (sum(save[0]) / (len(save[0]) if len(save[0]) > 0 else 1)),
            (len(save[0])),
            save[2][0],
            mt1[i],
            save[3],
            save[2][1],
        ]
    )

# print(third)

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
time = [x for x in range(0, len(first))]

plt.figure(3)
plt.plot(time, [x[0] for x in second], label="10% Growth")
plt.plot(time, [x[0] for x in first], label="0% Growth")
plt.plot(time, [x[0] for x in third], label="-10% Growth")

for x in range(len(time)):
    plt.annotate(first[x][1], (time[x], first[x][0]))
    plt.annotate(second[x][1], (time[x], second[x][0]))
    plt.annotate(third[x][1], (time[x], third[x][0]))

plt.xlabel("Time Period (Years)")
plt.ylabel("Equilibrium Price")
plt.legend()
plt.annotate(
    "(Markers Represent # of Transactions)", xy=(0.45, 0.9), xycoords="axes fraction"
)
plt.title(
    "Equilibrium Prices and Number of Tansactions of Various Money Supply Growth Rates Over Time"
)
plt.show()

# previous method: x[2]          savings/moneydemand: x[4] / x[5]
plt.figure(4)
plt.plot(time, [x[4] / x[3] for x in second], label="10% Growth")
plt.plot(time, [x[4] / x[3] for x in first], label="0% Growth")
plt.plot(time, [x[4] / x[3] for x in third], label="-10% Growth")
plt.xlabel("Time Period (Years)")
plt.ylabel("Interest Rate")
plt.legend()
plt.title("Equilibrium Interest Rates of Various Money Supply Growth Rates Over Time")
plt.show()


plt.figure(5)
plt.plot(time, [(x[0] * x[1]) / x[3] for x in second], label="10% Growth")
plt.plot(time, [(x[0] * x[1]) / x[3] for x in first], label="0% Growth")
plt.plot(time, [(x[0] * x[1]) / x[3] for x in third], label="-10% Growth")
plt.xlabel("Time Period (Years)")
plt.ylabel("Velocity")
plt.legend()
plt.title("Velocity of Money of Various Money Supply Growth Rates Over Time")
plt.show()

plt.figure(6)
plt.plot(time, [x[4] for x in second], label="10% Growth")
plt.plot(time, [x[4] for x in first], label="0% Growth")
plt.plot(time, [x[4] for x in third], label="-10% Growth")
plt.xlabel("Time Period (Years)")
plt.ylabel("Savings")
plt.legend()
plt.title("Savings of Various Money Supply Growth Rates Over Time")
plt.show()
