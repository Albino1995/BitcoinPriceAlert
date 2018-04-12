#!/usr/bin/env python
__author__ = 'Albino'

import requests
import time
from datetime import datetime

BITCOIN_API_URL = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'
IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/{IFTTT-KEY}'
BITCOIN_PRICE_MAX = 10000
BITCOIN_PRICE_MIN = 5000


def get_latest_bitcoin_price():
    """
    获取当前比特币价格
    """
    response = requests.get(BITCOIN_API_URL)
    response_json = response.json()
    print('{}: {}'.format(datetime.now().strftime('%d.%m.%Y %H:%M'), float(response_json[0]['price_usd'])))
    return float(response_json[0]['price_usd'])


def post_ifttt_webhook(event, value):
    """
    触发ifttt的webhooks
    """
    data = {'value1': value}
    ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event)
    requests.post(ifttt_event_url, json=data)


def format_bitcoin_history(bitcoin_history):
    rows = []
    for bitcoin_price in bitcoin_history:
        date = bitcoin_price['date'].strftime('%Y-%m-%d %H:%M')
        price = bitcoin_price['price']
        row = '{}: $<b>{}</b>'.format(date, price)
        rows.append(row)

    return '<br>'.join(rows)


if __name__ == '__main__':
    while True:
        # 保存近24条价格记录
        bitcoin_history = []

        while True:
            price = get_latest_bitcoin_price()
            date = datetime.now()
            bitcoin_history.append({'date': date, 'price': price})
            if price > BITCOIN_PRICE_MAX or price < BITCOIN_PRICE_MIN:
                post_ifttt_webhook('bitcoin_price_emergency', price)

            if len(bitcoin_history) == 24:
                print('send email')
                post_ifttt_webhook('bitcoin_price_update',
                                   format_bitcoin_history(bitcoin_history))
                bitcoin_history = []
            time.sleep(60 * 60)