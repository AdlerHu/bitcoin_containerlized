'''
Get Historical bitcoin、gold、oil price from Yahoo Finance
'''
import requests
import pandas as pd
from datetime import datetime
import time
import pytz 
from utils.config import connect_db


# 得到起始日、終止日的 2 個 list
def get_period():
    years = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
    quarters = ['Q1', 'Q2', 'Q3', 'Q4']
    start_date_list = []
    end_date_list = []

    for year in years:
        for quarter in quarters:
            if quarter == 'Q1':
                start_date = f'{year}-01-01'
                end_date = f'{year}-03-31'
            elif quarter == 'Q2':
                start_date = f'{year}-04-01'
                end_date = f'{year}-06-30'
            elif quarter == 'Q3':
                start_date = f'{year}-07-01'
                end_date = f'{year}-09-30'
            else:
                start_date = f'{year}-10-01'
                end_date = f'{year}-12-31'
            start_date_list.append(start_date)
            end_date_list.append(end_date)
    return start_date_list, end_date_list


# 定義 UTC 時區
utc = pytz.UTC

# 將日期字符串轉換為 UTC timestamp
def date_str_to_timpstamp(date_str):
    # 使用 UTC 時區將日期字符串轉換為 datetime 對象
    date = datetime.strptime(date_str, '%Y-%m-%d').replace(tzinfo=utc)

    # 將 datetime 對象轉換為 UTC timestamp
    timestamp = int(date.timestamp())
    return str(timestamp)


# insert bitcoin、gold、oil historical price to each table
def insert_target_table(cursor, raw_data, table):
    date_list = raw_data['Date']
    price_list = raw_data['Close*']

    for i in range(len(date_list) -1):
        date_str = datetime.strptime(date_list[i], '%b %d, %Y').strftime('%Y-%m-%d')
        sql_str = f'INSERT INTO {table} (date, price) VALUES (\"{date_str}\", {price_list[i]});'

        try:
            cursor.execute(sql_str)
        except Exception as err:
            print(f'{table} - {date_str} - {price_list[i]}')    


# from yahoo finance api get historical raw data
def crawler(url, cursor, table):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/80.0.3987.132 Safari/537.36'}
    ss = requests.session()
    res = ss.get(url, headers=headers)

    raw_data = pd.read_html(res.text)[0]
    insert_target_table(cursor=cursor, raw_data=raw_data, table=table)


def main():
    # data of 3 months at once
    connection, cursor = connect_db()
    start_date_list, end_date_list = get_period()
    now = datetime.now().strftime('%Y-%m-%d %H:%m')

    # 'target-name': ['url-code', 'table-name']
    target_dict = {'Bitcoin':['BTC-USD','bitcoin'],
                   'Gold':['GC%3DF','gold'],
                   'Oil':['BZ%3DF','oil'] 
    }
    
    for key in target_dict.keys():
        code = target_dict[key][0]
        table = target_dict[key][1]

        for i in range(len(start_date_list)):
            start_date_str = date_str_to_timpstamp(start_date_list[i])
            end_date_str = date_str_to_timpstamp(end_date_list[i])

            url = 'https://finance.yahoo.com/quote/' + code + '/history?period1=' + start_date_str \
                    + '&period2=' + end_date_str + '&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true'

            crawler(url=url, cursor=cursor, table=table)
            time.sleep(2)

    cursor.close()
    connection.close()
    print(f'{now} done')


if __name__ == '__main__':
    main()