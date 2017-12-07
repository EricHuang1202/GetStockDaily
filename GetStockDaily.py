# -*- coding: utf-8 -*-
import os
import re
import time
import logging
import requests
from datetime import datetime, timedelta
import pymysql

def main():

    if not os.path.isdir('log'):
        os.makedirs('log')
    logging.basicConfig(filename='log/error.log',
        level=logging.ERROR,
        format='%(asctime)s\t[%(levelname)s]\t%(message)s',
        datefmt='%Y/%m/%d %H:%M:%S')

    today = datetime.today()

    tradeDate = '{0}{1:02d}{2:02d}'.format(today.year, today.month, today.day)

    url = 'http://www.twse.com.tw/exchangeReport/MI_INDEX'

    query_params = {
        'date': tradeDate,
        'response': 'json',
        'type': 'ALL',
        '_': str(round(time.time() * 1000) - 500)
    }

    page = requests.get(url, params=query_params)
    if not page.ok:
        logging.error("get Taiwan TSE {} trade data error".format(tradeDate))
        return

    db = pymysql.connect("localhost", "user", "user1234", "StockCrawler", use_unicode=True, charset="utf8")
    cursor = db.cursor()

    content = page.json()
    for data in content['data5']:
        sign = '-' if data[9].find('green') > 0 else ''
        row = clean([
            tradeDate,  # 日期
            data[2],  # 成交股數
            data[4],  # 成交金額
            data[5],  # 開盤價
            data[6],  # 最高價
            data[7],  # 最低價
            data[8],  # 收盤價
            sign + data[10],  # 漲跌價差
            data[3],  # 成交筆數
        ])

        stockId = data[0].strip()

        try:
            sql = "INSERT INTO DailyData(StockId, TradeDate, Volume, Turnover, \
                           Opening, Highest, Lowest, Closing, QuoteChange, TransNum) \
                           VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                  (stockId, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
            cursor.execute(sql)
            db.commit()
            print(stockId, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])

        except Exception as e:
            print(e)
            logging.error(
                "insert DailyData error → StockId:" + stockId + ", RowData:" + str(row) + ", error msg:" + str(e))
            db.rollback()

def clean(row):
    for index, content in enumerate(row):
        row[index] = re.sub(",", "", content.strip())
    return row


if __name__ == '__main__':
    main()
