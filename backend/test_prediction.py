#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from spider import GuessParser

# 测试用例
test_cases = [
    ("今天天气比较好，天比较蓝，那就继续蓝。输的话评论区抽一个小可爱送花合战。", "right"),
    ("我蓝", "right"),
    ("我红", "left"),
    ("压蓝", "right"),
    ("压红", "left"),
    ("左边赢", "left"),
    ("右边赢", "right"),
    ("红方胜", "left"),
    ("蓝方胜", "right"),
    ("选左", "left"),
    ("选右", "right"),
]

print("测试预测解析规则：\n")

for content, expected in test_cases:
    result = GuessParser.parse_prediction(content)
    status = "✅" if result == expected else "❌"
    print(f"{status} 内容: {content[:30]}...")
    print(f"   预期: {expected}, 实际: {result}")
    print()
