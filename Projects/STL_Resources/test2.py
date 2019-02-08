import matplotlib.pyplot as plt

table = [4.19, 3.41, 2.78, 2.37, 1.8, 1.47, 1.09, 0.99, 1.05]
indices = [i for i in range(len(table))]

ratios = [table[i] / table[i + 1] for i in range(len(table) - 1)]
indices2 = indices[:-1]

plt.plot(indices, table, "r", indices2, ratios, "b")
plt.show()

