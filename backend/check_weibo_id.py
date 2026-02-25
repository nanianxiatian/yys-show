"""
检查微博ID转换
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def mid_to_url(mid):
    """将mid转换为URL格式的ID"""
    charset = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    url = ""
    mid = int(mid)
    while mid > 0:
        url = charset[mid % 62] + url
        mid //= 62
    return url

def url_to_mid(url):
    """将URL格式的ID转换为mid"""
    charset = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    mid = 0
    for char in url:
        mid = mid * 62 + charset.index(char)
    return str(mid)

# 检查目标微博ID
target_url_id = "QtaCga9AD"
converted_mid = url_to_mid(target_url_id)
print(f"目标微博 URL ID: {target_url_id}")
print(f"转换为 MID: {converted_mid}")

# 检查数据库中的ID
db_mid = "5269545574203740"  # 第5轮的ID
converted_url = mid_to_url(db_mid)
print(f"\n数据库中的 MID: {db_mid}")
print(f"转换为 URL ID: {converted_url}")

# 检查是否匹配
if converted_mid == db_mid:
    print("\n✓ 匹配！目标微博就是数据库中的第5轮")
else:
    print("\n✗ 不匹配")
    print(f"  目标微博MID: {converted_mid}")
    print(f"  数据库第5轮MID: {db_mid}")
