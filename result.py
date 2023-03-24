'''
insert verifiable prediction to result table
'''
from datetime import datetime
from utils.config import connect_db


# insert verifiable prediction to result table
def insert_result_table(cursor):
    sql_str = '''INSERT INTO result (date, prediction, real_price)
                SELECT 	r.date, p.prediction, r.bitcoin_price
                FROM prediction as p
                JOIN 
                (SELECT h.date, h.bitcoin_price 
                FROM historical_data as h  
                WHERE ( SELECT COUNT(1) FROM result as res WHERE h.date = res.date) = 0) as r
                ON p.date = r.date;'''
    try:
        cursor.execute(sql_str)
    except Exception as err:
        print(err.args)


def main():
    connection, cursor = connect_db()
    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M')
    insert_result_table(cursor=cursor)

    print(f'{now}: Insert Result Done')
    cursor.close()
    connection.close()


if __name__ == '__main__':
    main()
