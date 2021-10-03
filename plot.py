import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import pandas as pd
import re

ma_fast = list()
ma_slow = list()
end_value = list()

f = open('result.txt', 'r')
for line in f:
    nums = re.findall(r'[1-9]+\.?[0-9]*', line)
    ma_fast.append(int(nums[0]))
    ma_slow.append(int(nums[1]))
    end_value.append(float(nums[2]))

df = pd.DataFrame({
    'ma_fast': ma_fast,
    'ma_slow': ma_slow,
    'end_value': end_value,
})

df = df.sort_values(by='end_value', ascending=False)
print(df.head())


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection="3d")

ax.scatter(ma_slow, ma_fast, end_value, zdir="end_value", s=7)
ax.set(xlabel='ma_slow', ylabel='ma_fast', zlabel='end_value')
# plt.savefig('ma.png', format='png')
plt.show()
