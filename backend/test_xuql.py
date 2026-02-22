#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from spider import GuessParser

# 徐清林的微博内容
content = "阴阳师手游超话#对弈竞猜##超话创作官# 今天天气比较好，天比较蓝，那就继续蓝。输的话评论区抽一个小可爱送花合战。 ​​​"

print(f"微博内容: {content}")
print()

# 测试是否相关
is_related = GuessParser.is_guess_related(content)
print(f"是否对弈竞猜相关: {is_related}")

# 测试预测解析
prediction = GuessParser.parse_prediction(content)
print(f"预测结果: {prediction}")

# 详细分析
print("\n详细分析:")

# 直接表达匹配
direct_patterns = {
    'left': [r'我红', r'压红', r'押红', r'选红', r'投红'],
    'right': [r'我蓝', r'压蓝', r'押蓝', r'选蓝', r'投蓝']
}

import re
for side, patterns in direct_patterns.items():
    for pattern in patterns:
        if re.search(pattern, content, re.IGNORECASE):
            print(f"  直接匹配: {pattern} -> {side}")

# 红蓝转换
converted = GuessParser._convert_colors(content)
print(f"\n转换后内容: {converted}")

# 检查left/right
if 'left' in converted:
    print(f"  包含 'left' (红)")
if 'right' in converted:
    print(f"  包含 'right' (蓝)")
