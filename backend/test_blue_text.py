#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试蓝字解析修复
"""
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from bs4 import BeautifulSoup
import re

def old_clean_html(html_text):
    """旧的清理方法（有问题）"""
    if not html_text:
        return ''
    
    # 移除HTML标签 - 这会删除标签内的内容
    text = re.sub(r'<[^>]+>', '', html_text)
    text = text.replace('&quot;', '"')
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&nbsp;', ' ')
    
    return text.strip()

def new_clean_html(html_text):
    """新的清理方法（修复后）"""
    if not html_text:
        return ''
    
    # 使用BeautifulSoup解析HTML，保留标签内的文本
    soup = BeautifulSoup(html_text, 'html.parser')
    text = soup.get_text()
    
    text = text.replace('&quot;', '"')
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&nbsp;', ' ')
    
    return text.strip()

# 测试用例 - 模拟微博蓝字内容
test_cases = [
    # 测试用例1: 蓝字标签
    '<span class="s-color-blue">蓝</span>方必胜，压蓝',
    
    # 测试用例2: 红字标签
    '<span class="s-color-red">红</span>方必胜，压红',
    
    # 测试用例3: 混合内容
    '对弈竞猜第1轮：<span class="s-color-blue">蓝</span>方，我压蓝',
    
    # 测试用例4: 多个蓝字
    '<span class="s-color-blue">蓝蓝</span>方，压蓝',
    
    # 测试用例5: 普通内容
    '对弈竞猜，左边必胜，压左',
    
    # 测试用例6: 带链接的蓝字
    '<a href="xxx"><span class="s-color-blue">蓝</span></a>方',
]

print("=" * 80)
print("测试蓝字解析修复")
print("=" * 80)

for i, test_html in enumerate(test_cases, 1):
    old_result = old_clean_html(test_html)
    new_result = new_clean_html(test_html)
    
    print(f"\n测试用例 {i}:")
    print(f"  原始HTML: {test_html}")
    print(f"  旧方法结果: {old_result}")
    print(f"  新方法结果: {new_result}")
    
    # 检查是否包含"蓝"字
    has_blue_old = '蓝' in old_result
    has_blue_new = '蓝' in new_result
    
    if has_blue_old != has_blue_new:
        print(f"  ⚠️  差异: 旧方法{'包含' if has_blue_old else '不包含'}'蓝'字，新方法{'包含' if has_blue_new else '不包含'}'蓝'字")
    else:
        print(f"  ✅ 结果一致")

print("\n" + "=" * 80)
print("测试完成")
print("=" * 80)
