import trendln
import matplotlib.pyplot as plt
import yfinance as yf

tick = yf.Ticker('600000.SS')  # S&P500
hist = tick.history(period="max", rounding=True)
print(hist.info())

fig = trendln.plot_sup_res_date(
    (hist[-150:].Low, hist[-150:].High), hist[-150:].index, accuracy=2)  # requires pandas
plt.savefig('suppres.png', format='png', dpi=200)
plt.show()
plt.clf()  # clear figure
