from datetime import datetime, timedelta

data = [
    {"created": "2024-08-20T15:06:25.000+00:00"},
    {"created": "2024-07-20T15:06:25.000+00:00"},
    {"created": "2024-08-08T15:06:25.000+00:00"}
]
# 获取当前日期时间
now = datetime.now()
# 计算一个月前的日期
one_month_ago = now - timedelta(days=30)
dt = datetime.fromisoformat(data[2]['created'].replace("T", " ").replace("+00:00", ""))

print(one_month_ago<dt)