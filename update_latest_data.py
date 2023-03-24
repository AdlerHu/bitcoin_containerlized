from datetime import datetime
from utils.config import connect_db


# 更新歷史資料表
def update_historical_data(cursor):
    # 這個 SQL 語句會將 bitcoin 有而 historical_data 沒有的日期、比特幣價格
    # 插入歷史資料表
    sql_str = f'''
        INSERT INTO historical_data (date, bitcoin_price)
        SELECT b.date, b.price FROM bitcoin as b WHERE ( 
        SELECT COUNT(1) FROM historical_data as h WHERE b.date = h.date) = 0;    
    '''
    try:
        cursor.execute(sql_str)
    except Exception as err:
        print(err.args)

    # 如果某一個日期有比特幣交易資料而沒有黃金或石油資料，就補上最近的一筆黃金或石油的資料
    sql_str = f'''
        UPDATE historical_data as h
            SET
            h.gold_price = (
                SELECT 	price
                FROM	gold
                WHERE	date <= h.date
                ORDER BY date DESC LIMIT 1
            ), 
            h.oil_price = (
                SELECT 	price
                FROM	oil
                WHERE	date <= h.date
                ORDER BY date DESC LIMIT 1
            ),
            h.future_date = date_add(h.date, INTERVAL 7 DAY);
    '''
    try:
        cursor.execute(sql_str)
    except Exception as err:
        print(err.args)


def main():
    connection, cursor = connect_db()
    update_historical_data(cursor)

    now = datetime.utcnow().strftime('%Y-%m-%d %H-%M')
    cursor.close()
    print(f'{now}: Update Done')
    connection.close()


if __name__ == '__main__':
    main()
