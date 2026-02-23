"""
检查运行中的应用
"""
import http.client

conn = http.client.HTTPConnection("127.0.0.1", 5000)

# 测试GET请求
conn.request("GET", "/api/shikigami-manager")
response = conn.getresponse()
print(f'GET /api/shikigami-manager: {response.status}')
print(response.read().decode()[:200])

conn.close()
