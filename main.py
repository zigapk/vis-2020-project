import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('data/export.csv')

x = df['difficulty']
y = df['rating']

# k, n = np.polyfit(x, y, 1)

plt.scatter(x, y)
# plt.plot(x, k * x + n, 'red')
plt.xlabel('Povprečen uspeh reševanja')
plt.ylabel('ELO rating')
plt.show()

cor = np.corrcoef(x, y)[0][1]
print(cor)
