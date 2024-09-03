import csv
import os

def split_csv(input_file, output_dir, chunk_size=200):
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 读取原始 CSV 文件
    with open(input_file, 'r', newline='', encoding='gbk') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # 读取表头
        chunk = []
        chunk_count = 1

        for row in reader:
            chunk.append(row)
            if len(chunk) == chunk_size:
                # 写入当前 chunk 到新文件
                output_file = os.path.join(output_dir, f'item{chunk_count}.csv')
                with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
                    writer = csv.writer(outfile)
                    writer.writerow(header)  # 写入表头
                    writer.writerows(chunk)
                chunk = []
                chunk_count += 1

        # 写入剩余的行
        if chunk:
            output_file = os.path.join(output_dir, f'item{chunk_count}.csv')
            with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
                writer = csv.writer(outfile)
                writer.writerow(header)  # 写入表头
                writer.writerows(chunk)

# 使用示例
input_file = 'items.csv'  # 原始 CSV 文件路径
output_dir = 'file'  # 输出目录

split_csv(input_file, output_dir)