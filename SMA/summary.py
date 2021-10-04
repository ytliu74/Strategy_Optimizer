import os
import pandas as pd
import matplotlib.pyplot as plt

list_path = os.path.abspath('.\\SMA\\best_ma')

best_list = os.listdir(list_path)

slow_mas = list()
fast_mas = list()

for best_ma in best_list:
    csv_path = os.path.join(list_path, best_ma)

    df = pd.read_csv(csv_path)

    for i in range(3):
        s = df.loc[i]['ma_slow']
        f = df.loc[i]['ma_fast']

        slow_mas.append(s)
        fast_mas.append(f)

plt.scatter(slow_mas, fast_mas, s=10, marker='o')
plt.xlabel('ma_slow')
plt.ylabel('ma_fast')
plt.savefig('.\\SMA\\summary.png', format='png')
plt.show()
