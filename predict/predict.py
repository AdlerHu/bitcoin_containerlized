'''
predict from lastest data, insert into prediction table
'''
from numpy import array
import pandas as pd
from keras.models import load_model
from datetime import datetime
from utils.config import connect_db


# insert the prediction table
def insert_prediction(cursor, date, prediction):
    sql_str = f'''INSERT INTO prediction (date, prediction) VALUES (\'{date}\', {prediction});'''
    try:
        cursor.execute(sql_str)
    except Exception as err:
        print(f'{date}: {err.args}')


# predict from saved model
def predict(model, predict_data_list):
    n_steps = 1
    n_features = 3

    # demonstrate prediction    
    x_input = array(predict_data_list)
    x_input = x_input.reshape((1, n_steps, n_features))
    yhat = model.predict(x_input, verbose=0)
    
    answer = yhat.flatten().tolist()
    ans = ''.join(str(x) for x in answer)
    return ans


def get_unpredicted_data(connection):
    sql_str = '''SELECT h.future_date, h.bitcoin_price, h.gold_price, h.oil_price 
        FROM historical_data as h 
        WHERE ( SELECT COUNT(1) FROM prediction as p WHERE h.future_date = p.date) = 0;'''
    data_row = pd.read_sql_query(sql_str, connection)    
    return data_row


def main():
    connection, cursor = connect_db()
    model = load_model('model/7th_days.h5')
    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M')

    data_row = get_unpredicted_data(connection)

    date_list = list(data_row['future_date'])
    bitcoin_list = list(data_row['bitcoin_price'])
    gold_list = list(data_row['gold_price'])
    oil_list = list(data_row['oil_price'])

    for i in range(len(date_list)):
        predict_data_list = [bitcoin_list[i], gold_list[i], oil_list[i]]
        prediction = predict(model=model, predict_data_list=predict_data_list)
        insert_prediction(cursor=cursor, date=date_list[i], prediction=prediction)

    cursor.close()
    print(f'{now}: Predict Done')
    connection.close()


if __name__ == '__main__':
    main()
