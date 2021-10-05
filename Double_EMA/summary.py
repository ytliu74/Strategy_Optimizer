import os
import pandas as pd
import matplotlib.pyplot as plt

list_path = os.path.abspath('.\\Double_EMA\\best_double_ema')

best_list = os.listdir(list_path)

slow_emas = list()
fast_emas = list()

for best_ma in best_list:
    csv_path = os.path.join(list_path, best_ma)

    df = pd.read_csv(csv_path)

    # select best top 3
    for i in range(1):
        s = df.loc[i]['ema_slow']
        f = df.loc[i]['ema_fast']

        slow_emas.append(s)
        fast_emas.append(f)

plt.scatter(slow_emas, fast_emas, s=10, marker='o')
plt.xlabel('ma_slow')
plt.ylabel('ma_fast')
plt.savefig('.\\Double_EMA\\summary.png', format='png')
plt.show()
