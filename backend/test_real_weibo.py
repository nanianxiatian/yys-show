#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试真实微博数据解析
"""
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup

# 模拟微博API返回的真实数据格式（包含蓝字）
real_weibo_html_examples = [
    # 示例1: 简单的蓝字span
    '<span class="s-color-blue">蓝</span>方',
    
    # 示例2: 带style的蓝字
    '<span style="color:#4B7EFF">蓝</span>方',
    
    # 示例3: 微博常见的蓝字格式（带topic链接）
    '<a href="//s.weibo.com/weibo?q=%23%E5%AF%B9%E5%BC%88%E7%AB%9E%E7%8C%9C%23" data-hide="">#对弈竞猜#</a>第1轮：<span class="s-color-blue">蓝</span>方必胜',
    
    # 示例4: 嵌套标签
    '<span class="s-color-blue"><span class="s-color-blue">蓝</span></span>方',
    
    # 示例5: 带class的复杂格式
    '<span class="s-color-blue s-fc-blue">蓝</span>方压蓝',
    
    # 示例6: 微博实际返回的格式（可能包含更多属性）
    '<span class=\"s-color-blue\" style=\"color: rgb(75, 126, 255);\">蓝</span>方',
]

def old_clean_html(html_text):
    """旧的清理方法"""
    if not html_text:
        return ''
    text = re.sub(r'<[^>]+>', '', html_text)
    text = text.replace('&quot;', '"')
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&nbsp;', ' ')
    return text.strip()

def new_clean_html(html_text):
    """新的清理方法"""
    if not html_text:
        return ''
    soup = BeautifulSoup(html_text, 'html.parser')
    text = soup.get_text()
    text = text.replace('&quot;', '"')
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&nbsp;', ' ')
    return text.strip()

print("=" * 80)
print("测试真实微博HTML格式解析")
print("=" * 80)

for i, html in enumerate(real_weibo_html_examples, 1):
    old_result = old_clean_html(html)
    new_result = new_clean_html(html)
    
    print(f"\n测试用例 {i}:")
    print(f"  原始HTML: {html[:80]}...")
    print(f"  旧方法结果: {old_result}")
    print(f"  新方法结果: {new_result}")
    
    # 检查是否包含"蓝"字
    has_blue_old = '蓝' in old_result
    has_blue_new = '蓝' in new_result
    
    if has_blue_old != has_blue_new:
        print(f"  ⚠️  差异: 旧方法{'包含' if has_blue_old else '不包含'}'蓝'字，新方法{'包含' if has_blue_new else '不包含'}'蓝'字")
    elif not has_blue_new:
        print(f"  ❌ 警告: 两种方法都无法提取'蓝'字")
    else:
        print(f"  ✅ 正常")

# 测试预测解析
print("\n" + "=" * 80)
print("测试预测解析")
print("=" * 80)

from spider import GuessParser

test_contents = [
    "对弈竞猜第1轮：<span class=\"s-color-blue\">蓝</span>方，压蓝",
    "对弈竞猜：蓝方必胜，我压蓝",
    "#对弈竞猜# 第2轮 <span style=\"color:#4B7EFF\">蓝</span>方",
    "对弈竞猜第3轮：红方必胜",
    "对弈竞猜：左边",
]

for content in test_contents:
    is_related = GuessParser.is_guess_related(content)
    prediction = GuessParser.parse_prediction(content)
    
    print(f"\n内容: {content}")
    print(f"  是否相关: {is_related}")
    print(f"  预测结果: {prediction}")
