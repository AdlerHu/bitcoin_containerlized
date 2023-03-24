'''
Draw the last 30 days prediction and real price chart
'''
from utils.config import connect_db
import pyecharts.options as opts
from pyecharts.charts import Line
import pandas as pd
from datetime import datetime


def get_all_data(db_connection):
    sql_str = 'SELECT date, prediction FROM prediction;'
    raw_data = pd.read_sql_query(sql_str, db_connection)
    date_list = list(raw_data['date'])
    prediction_list = list(raw_data['prediction'])

    sql_str = 'SELECT real_price FROM result;'
    raw_data = pd.read_sql_query(sql_str, db_connection)
    
    return date_list, prediction_list, list(raw_data['real_price'])


def generate_all_chart(connection):
    date_list, prediction_list, real_list = get_all_data(connection)
    (
        Line()
        .add_xaxis(xaxis_data=date_list)
        .add_yaxis(
            series_name="Prediction",
            y_axis=prediction_list,
            label_opts=opts.LabelOpts(is_show=False),
        )
        .add_yaxis(
            series_name="Real",
            y_axis=real_list,
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Bitcoin Prediction"),
            datazoom_opts=opts.DataZoomOpts(type_="slider", range_start=95, range_end=100),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        )
        .render("templates/bitcoin_all_predict.html")
    )


def get_30_days_data(connection):
    sql_str = 'SELECT * FROM result where DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= date(date);'
    raw_data = pd.read_sql_query(sql_str, connection)
    return list(raw_data['date']), list(raw_data['prediction']), list(raw_data['real_price'])


def generate_30_days_chart(connection):
    date_list, prediction_list, real_list = get_30_days_data(connection)
    (
        Line()
        .add_xaxis(xaxis_data=date_list)
        .add_yaxis(
            series_name="Prediction",
            y_axis=prediction_list,
            label_opts=opts.LabelOpts(is_show=False),
        )
        .add_yaxis(
            series_name="Real",
            y_axis=real_list,
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Bitcoin Prediction"),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        )
       .render("templates/bitcoin_30_predict.html")
    )


def main():
    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M')
    connection, cursor = connect_db()
    generate_30_days_chart(connection)
    generate_all_chart(connection)

    print(f'{now}: Chart Done')
    cursor.close()
    connection.close()


if __name__ == '__main__':
    main()
