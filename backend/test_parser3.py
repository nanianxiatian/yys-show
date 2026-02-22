#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from spider.parser import GuessParser
import re

# 测试内容
test_content = "对弈竞猜12点场:蓝🤛回笼觉晕过去了，醒来继续i童。目前战绩18胜18负。全红胜率应该是16胜20负。    #对弈竞猜# ​​​"

output = []
output.append("=" * 80)
output.append("测试鸽海成路微博内容:")
output.append(test_content)
output.append("=" * 80)

# 测试预测解析
prediction = GuessParser.parse_prediction(test_content)
output.append(f"\n预测结果: {prediction}")

# 详细调试
output.append("\n" + "=" * 80)
output.append("详细匹配过程:")
output.append("=" * 80)

left_score = 0
right_score = 0

# 第一步：直接表达模式
direct_patterns = {
    'left': [r'我红', r'压红', r'押红', r'选红', r'投红'],
    'right': [r'我蓝', r'压蓝', r'押蓝', r'选蓝', r'投蓝']
}

output.append("\n第一步 - 直接表达匹配:")
for pattern in direct_patterns['left']:
    matches = re.findall(pattern, test_content, re.IGNORECASE)
    if matches:
        output.append(f"  左模式 '{pattern}' 匹配: {matches}")
        left_score += 10
        
for pattern in direct_patterns['right']:
    matches = re.findall(pattern, test_content, re.IGNORECASE)
    if matches:
        output.append(f"  右模式 '{pattern}' 匹配: {matches}")
        right_score += 10

output.append(f"直接表达得分 - 左: {left_score}, 右: {right_score}")

# 第二步：颜色标记模式
color_patterns = {
    'left': [
        r'[:：]\s*红\s*[^\u4e00-\u9fa5]',  # 冒号后接红，后接非中文
        r'[选压押投]红',  # 选红、压红、押红、投红
        r'红[色方]\s*[^\u4e00-\u9fa5]',  # 红色、红方后接非中文
    ],
    'right': [
        r'[:：]\s*蓝\s*[^\u4e00-\u9fa5]',  # 冒号后接蓝，后接非中文
        r'[选压押投]蓝',  # 选蓝、压蓝、押蓝、投蓝
        r'蓝[色方]\s*[^\u4e00-\u9fa5]',  # 蓝色、蓝方后接非中文
    ]
}

output.append("\n第二步 - 颜色标记匹配:")
for pattern in color_patterns['left']:
    matches = re.findall(pattern, test_content, re.IGNORECASE)
    if matches:
        output.append(f"  左模式 '{pattern}' 匹配: {matches}")
        left_score += 5
        
for pattern in color_patterns['right']:
    matches = re.findall(pattern, test_content, re.IGNORECASE)
    if matches:
        output.append(f"  右模式 '{pattern}' 匹配: {matches}")
        right_score += 5

output.append(f"颜色标记后得分 - 左: {left_score}, 右: {right_score}")

# 第三步：其他模式
converted_content = GuessParser._convert_colors(test_content)
output.append(f"\n转换后的内容: {converted_content}")

PREDICTION_PATTERNS = {
    'left': [
        r'左[边侧]?', r'红[色方]?', r'左边赢', r'红方赢',
        r'压左', r'押左', r'选左', r'投左',
        r'左边胜', r'红方胜', r'左胜', r'红胜',
        r'我红', r'压红', r'押红', r'选红', r'投红',
        r'left'
    ],
    'right': [
        r'右[边侧]?', r'蓝[色方]?', r'右边赢', r'蓝方赢',
        r'压右', r'押右', r'选右', r'投右',
        r'右边胜', r'蓝方胜', r'右胜', r'蓝胜',
        r'我蓝', r'压蓝', r'押蓝', r'选蓝', r'投蓝',
        r'right'
    ]
}

exclude_patterns = direct_patterns['left'] + direct_patterns['right'] + \
                  color_patterns['left'] + color_patterns['right']
other_left_patterns = [p for p in PREDICTION_PATTERNS['left'] if p not in exclude_patterns]
other_right_patterns = [p for p in PREDICTION_PATTERNS['right'] if p not in exclude_patterns]

output.append("\n第三步 - 其他模式匹配（在转换后的内容上）:")
for pattern in other_left_patterns:
    matches = re.findall(pattern, converted_content, re.IGNORECASE)
    if matches:
        output.append(f"  左模式 '{pattern}' 匹配: {matches} (次数: {len(matches)})")
        left_score += len(matches)
        
for pattern in other_right_patterns:
    matches = re.findall(pattern, converted_content, re.IGNORECASE)
    if matches:
        output.append(f"  右模式 '{pattern}' 匹配: {matches} (次数: {len(matches)})")
        right_score += len(matches)

output.append(f"\n总得分 - 左: {left_score}, 右: {right_score}")

if left_score > right_score:
    output.append("最终预测结果: left")
elif right_score > left_score:
    output.append("最终预测结果: right")
else:
    output.append("最终预测结果: unknown")

with open(r'f:\trace\work-space\yys-show\backend\test_parser3_output.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print("测试完成，结果已写入 test_parser3_output.txt")
