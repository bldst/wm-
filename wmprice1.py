import csv
import logging
import requests

# 配置日志
logging.basicConfig(
    filename='运行日志1.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def fetch_sell_orders(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 抛出HTTP错误
        return response.json()
    except requests.RequestException as e:
        logging.error(f"异常： {url}: {e}")
        return None


def extract_and_filter_orders(orders_json):
    if orders_json is None:
        return []
    orders_data = orders_json['payload']['orders']
    # 筛选订单
    filtered_orders = [order for order in orders_data if
                       order['order_type'] == 'sell' and order['user']['status'] in ['ingame', 'online']]
    # 排序订单
    sorted_orders = sorted(filtered_orders, key=lambda x: x['platinum'])
    # 取前三条记录的价格
    top_prices = [str(order['platinum']) for order in sorted_orders[:3]]
    return top_prices


def save_prices_to_csv(url_name, zh_name, prices):
    try:
        with open('price1.csv', mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([url_name, zh_name] + prices)
        logging.info("写入完成")
    except IOError as e:
        print(f"Error writing to CSV: {e}")


def process_item(url_name, zh_name):
    url = f'https://api.warframe.market/v1/items/{url_name}/orders'
    orders_json = fetch_sell_orders(url)
    if orders_json:
        prices = extract_and_filter_orders(orders_json)
        save_prices_to_csv(url_name, zh_name, prices)
        # for price in prices:
        #     print(price)


def read_items_from_csv(file_path):
    items = []
    count = 0
    try:
        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                count += 1
                if count > 20000:
                    break
                items.append([row['url_name'], row['zh_name']])
    except FileNotFoundError:
        logging.error(f" {file_path} 不存在.")
    except Exception as e:
        logging.error(f"读取时候出错: {e}")
    return items


if __name__ == "__main__":


    for x in range(1, 7):
        items_file_path = f'./file/item{x}.csv'
        print(f"打开第{x}个文件")
        items = read_items_from_csv(items_file_path)
        print(items)
        print(items_file_path)

        for item in items:
            print("开始查询:" + item[1])
            logging.info(f"开始查询: {item[1]}")
            process_item(*item)
