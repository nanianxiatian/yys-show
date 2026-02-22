#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from spider.parser import GuessParser

# 测试内容
test_content = "对弈竞猜12点场:蓝🤛回笼觉晕过去了，醒来继续i童。目前战绩18胜18负。全红胜率应该是16胜20负。    #对弈竞猜# ​​​"

output = []
output.append("=" * 80)
output.append("测试内容:")
output.append(test_content)
output.append("=" * 80)

# 测试是否相关
is_related = GuessParser.is_guess_related(test_content)
output.append(f"\n是否竞猜相关: {is_related}")

# 测试预测解析
prediction = GuessParser.parse_prediction(test_content)
output.append(f"预测结果: {prediction}")

# 详细调试
import re

output.append("\n" + "=" * 80)
output.append("详细调试:")
output.append("=" * 80)

content = test_content
left_score = 0
right_score = 0

# 第一步：先匹配包含"我蓝"、"压蓝"、"我红"、"压红"等直接表达（最高权重）
direct_patterns = {
    'left': [r'我红', r'压红', r'押红', r'选红', r'投红'],
    'right': [r'我蓝', r'压蓝', r'押蓝', r'选蓝', r'投蓝']
}

output.append("\n直接表达匹配:")
for pattern in direct_patterns['left']:
    matches = re.findall(pattern, content, re.IGNORECASE)
    if matches:
        output.append(f"  左模式 '{pattern}' 匹配: {matches}")
        left_score += 10
        
for pattern in direct_patterns['right']:
    matches = re.findall(pattern, content, re.IGNORECASE)
    if matches:
        output.append(f"  右模式 '{pattern}' 匹配: {matches}")
        right_score += 10

output.append(f"直接表达得分 - 左: {left_score}, 右: {right_score}")

# 检查是否包含"蓝"
output.append(f"\n内容中包含'蓝': {'蓝' in content}")
output.append(f"内容中包含'红': {'红' in content}")

# 红蓝转换
converted_content = GuessParser._convert_colors(content)
output.append(f"\n转换后的内容: {converted_content}")

# 检查转换后是否包含left/right
output.append(f"转换后包含'left': {'left' in converted_content}")
output.append(f"转换后包含'right': {'right' in converted_content}")

# 写入文件
with open(r'f:\trace\work-space\yys-show\backend\test_parser_output.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print("测试完成，结果已写入 test_parser_output.txt")
