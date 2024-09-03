import logging
import pandas as pd

# 配置日志
logging.basicConfig(
    filename='运行日志1.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

try:
    # 读取第一个 CSV 文件
    df1 = pd.read_csv('price1.csv')

    # 读取第二个 CSV 文件
    df2 = pd.read_csv('price2.csv')

    # 合并两个 DataFrame
    merged_df = pd.concat([df1, df2], ignore_index=True)

    # 将合并后的 DataFrame 写入新的 CSV 文件
    merged_df.to_csv('Price.csv', index=False)

    # 记录日志信息
    logging.info('Files successfully merged into merged_file.csv')
except Exception as e:
    # 记录异常信息到日志文件
    logging.error(f'An error occurred: {e}')
    print(f"An error occurred: {e}")