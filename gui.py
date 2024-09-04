import json
import tkinter as tk
from datetime import datetime, timedelta
from tkinter import ttk

import requests

# 定义全局变量items 保存WM紫卡表中的items
global_items = {}
global_count_orders=15

class AutoCompleteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("自动补全输入框")
        self.root.geometry("600x400")

        # 预定义的候选词汇列表
        self.candidates = self.get_weponname()

        # 创建一个框架来容纳输入框和提交按钮
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(pady=5)

        # 输入框
        self.entry = ttk.Entry(self.input_frame, width=15)
        self.entry.pack(side=tk.LEFT, padx=5)
        self.entry.bind('<KeyRelease>', self.find_matches)

        # 提交按钮
        self.submit_button = tk.Button(self.input_frame, text="提交", command=self.on_submit)
        self.submit_button.pack(side=tk.RIGHT)

        # 列表框用于显示候选词汇
        self.listbox = tk.Listbox(self.root, width=15, height=3)
        self.listbox.pack(pady=5)
        self.listbox.bind('<<ListboxSelect>>', self.select_candidate)

        # 创建一个文本框来显示输出
        self.output_text = tk.Text(self.root, height=15)
        self.output_text.pack(pady=10)

    def find_matches(self, event):
        current_text = self.entry.get().strip().lower()
        matches = [word for word in self.candidates if word.lower().startswith(current_text)]

        # 清除旧的候选选项
        self.listbox.delete(0, tk.END)

        # 添加新的候选选项
        for match in matches:
            self.listbox.insert(tk.END, match)

    def select_candidate(self, event):
        selected = self.listbox.get(self.listbox.curselection())
        self.entry.delete(0, tk.END)
        self.entry.insert(0, selected)

    def on_submit(self):
        input_text = self.entry.get()
        self.entry.delete(0, tk.END)
        #获得武器url_name
        weapon_url = self.get_url_name(input_text)
        #获取所有订单
        orders = self.get_riven_price_(weapon_url)
        filter_orders = self.extract_and_filter_orders(orders)
        for f in filter_orders:
            print(f)
        print(len(filter_orders))
        self.output_text.insert(tk.END, f'你查找的是: {weapon_url}\n')

    #获取候选框提示词
    def get_weponname(self):
        candidates = []
        global global_items  # 声明我们将要修改的是全局变量
        with open('WM紫卡表.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            global_items = data['payload']['items']
        for names in global_items:
            candidates.append(names['item_name'])
        return candidates

    def get_url_name(self, weapon_name):
        for item in global_items:
            if weapon_name == item['item_name']:
                return item['url_name']
        return '没有找到'

    #查找价格
    def get_riven_price_(self, weapon_url):
        try:
            RivenOrders = requests.get(
                url=f'https://api.warframe.market/v1/auctions/search?type=riven&weapon_url_name={weapon_url}&sort_by=price_asc')
            return RivenOrders.json()
        except requests.RequestException as e:

            return None

    # 对订单主要信息提取(只保留一个月内的前15个售卖订单)
    def extract_and_filter_orders(self,orders_json):
        if orders_json is None:
            return []
        orders = orders_json['payload']['auctions']
        # 获取当前日期时间
        now = datetime.now()
        # 计算一个月前的日期
        one_month_ago = now - timedelta(days=30)
        #保存符合条件的订单列表
        filter_orders_res=[]
        #计数器只保留15项订单
        count=1
        global global_count_orders
        # 提取一个月内的售卖订单
        for order in orders:
            #如果是拍卖订单直接跳过
            if order['starting_price']!=order['buyout_price']:
                continue
            create_time= datetime.fromisoformat(order['created'].replace("T", " ").replace("+00:00", ""))
            #如果订单在一个月内，就保存该订单
            if one_month_ago<=create_time:
                filter_orders_res.append(order)

            #订单保留数量
            if count>global_count_orders:
                break
            count+=1
        return filter_orders_res

    #分析订单，提取重要项目
    # def analysis_orders(self,orders):


if __name__ == "__main__":
    root = tk.Tk()
    app = AutoCompleteApp(root)
    root.mainloop()
