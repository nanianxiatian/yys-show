#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from spider import GuessParser

# 测试用例
test_cases = [
    "今天天气比较好，天比较蓝，那就继续蓝。输的话评论区抽一个小可爱送花合战。",
    "红方胜",
    "蓝方胜",
    "左边",
    "右边",
]

print("详细调试：\n")

for content in test_cases:
    print(f"原文: {content}")
    
    # 测试红蓝转换
    converted = GuessParser._convert_colors(content)
    print(f"转换后: {converted}")
    
    # 测试匹配
    import re
    left_patterns = [r'左[边侧]?', r'红[色方]?', r'左边赢', r'红方赢']
    right_patterns = [r'右[边侧]?', r'蓝[色方]?', r'右边赢', r'蓝方赢']
    
    for pattern in left_patterns:
        matches = re.findall(pattern, converted, re.IGNORECASE)
        if matches:
            print(f"  左匹配: {pattern} -> {matches}")
    
    for pattern in right_patterns:
        matches = re.findall(pattern, converted, re.IGNORECASE)
        if matches:
            print(f"  右匹配: {pattern} -> {matches}")
    
    result = GuessParser.parse_prediction(content)
    print(f"结果: {result}")
    print()
