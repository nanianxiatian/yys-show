import pymysql

# 连接MySQL（不指定数据库）
conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='yys20260217'
)

try:
    with conn.cursor() as cursor:
        # 创建数据库
        cursor.execute("CREATE DATABASE IF NOT EXISTS yys_guess CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print("数据库 yys_guess 创建成功")
finally:
    conn.close()
