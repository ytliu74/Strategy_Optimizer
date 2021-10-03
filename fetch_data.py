import time
import os
import baostock as bs
import pandas as pd

if not os.path.exists('./data'):
    os.mkdir('./data')

lg = bs.login()

fields = "date, high, low, open, close, volume"
start_date = '2005-01-01'
end_date = '2021-09-01'


code = pd.read_csv("stocks.csv")
code_list = code['code'].tolist()

time_start = time.time()

for code in code_list:
    rs = bs.query_history_k_data(
        code, fields=fields, start_date=start_date, end_date=end_date)
    print(f'Collecting {code}')
    print('query_history_k_data_plus respond error_code:'+rs.error_code)
    print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)
    data_list = []
    while (rs.error_code == '0') & rs.next():
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    result.to_csv(f'./data/{code}.csv', index=False)

duration = round(time.time() - time_start, 2)
print(f'Finish collecting in {duration} seconds')

bs.logout()
