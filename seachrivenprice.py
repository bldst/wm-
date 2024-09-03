import csv
import json
import logging

import requests

# 配置日志
logging.basicConfig(
    filename='运行日志1.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def get_riven_orders(url_wepon):
    try:
        RivenOrders = requests.get(
            url=f'https://api.warframe.market/v1/auctions/search?type=riven&weapon_url_name={url_wepon}&sort_by=price_asc')
        return RivenOrders.json()
    except requests.RequestException as e:
        logging.error(f"异常： {url_wepon}: {e}")
        return None

#按照在线，最低价排序
def extract_and_filter_orders(orders_json):
    if orders_json is None:
        return []
    orders = orders_json['payload']['auctions']
    online_orders = []
    #剔除不在线的用户订单
    for order in orders:
        if order['owner']['status'] == 'offline':
            continue
        online_orders.append(order)
    return online_orders


def process_item(item_name, online_orders):
    prices = []
    for order in online_orders[:5]:
        prices.append(order['buyout_price'])
    savetop5orders(order['item']['weapon_url_name'], item_name, prices)


def savetop5orders(url_wepon, item_name, prices):
    with open('rivenprice.csv', mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([url_wepon, item_name] + prices)


if __name__ == "__main__":
    count = 0
    with open('WM紫卡表.json','r',encoding='utf-8') as f:
        file = json.load(f)
    for items in file['payload']['items']:
        count += 1
        if count > 1500:
            break
        rivejson=get_riven_orders(items['url_name'])
        print("开始查询:"+items['item_name'])
        res = extract_and_filter_orders(rivejson)
        process_item(items['item_name'], res)
        print("写入完成")