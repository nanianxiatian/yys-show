#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试实际爬虫流程 - 检查微博内容解析
"""
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from spider import WeiboCrawler, GuessParser

# 创建爬虫实例（不需要有效cookie来测试解析逻辑）
crawler = WeiboCrawler(cookie='')

# 模拟微博API返回的真实数据结构
mock_weibo_data = {
    'id': '1234567890',
    'text': '<span class="s-color-blue">蓝</span>方必胜，对弈竞猜压蓝',
    'created_at': 'Mon Feb 22 14:30:00 +0800 2026',
    'reposts_count': 10,
    'comments_count': 5,
    'attitudes_count': 20,
    'pic_ids': []
}

print("=" * 80)
print("测试微博数据解析流程")
print("=" * 80)

# 测试 _parse_weibo_item 方法
print("\n1. 测试 _parse_weibo_item 解析:")
parsed = crawler._parse_weibo_item(mock_weibo_data)
if parsed:
    print(f"   微博ID: {parsed['weibo_id']}")
    print(f"   内容: {parsed['content']}")
    print(f"   发布时间: {parsed['publish_time']}")
else:
    print("   解析失败")

# 测试 parse_weibo
print("\n2. 测试 GuessParser.parse_weibo:")
if parsed:
    result = GuessParser.parse_weibo(parsed)
    print(f"   是否相关: {result['is_guess_related']}")
    print(f"   预测结果: {result['guess_prediction']}")
    print(f"   竞猜轮次: {result['guess_round']}")
    print(f"   解析后内容: {result['parsed_content']}")

# 测试各种可能的微博内容格式
print("\n" + "=" * 80)
print("测试各种内容格式的预测解析")
print("=" * 80)

test_contents = [
    # 格式1: 纯文本
    ("对弈竞猜：蓝方必胜，压蓝", "纯文本"),
    
    # 格式2: 带蓝字span
    ("<span class=\"s-color-blue\">蓝</span>方必胜，对弈竞猜压蓝", "蓝字span"),
    
    # 格式3: 带红字span
    ("<span class=\"s-color-red\">红</span>方必胜，对弈竞猜压红", "红字span"),
    
    # 格式4: 只有蓝字，没有其他文字
    ("<span class=\"s-color-blue\">蓝</span>", "只有蓝字"),
    
    # 格式5: 蓝字在句子中间
    ("对弈竞猜第1轮，压<span class=\"s-color-blue\">蓝</span>方", "蓝字在中间"),
    
    # 格式6: 多个蓝字
    ("<span class=\"s-color-blue\">蓝</span>方<span class=\"s-color-blue\">蓝</span>方", "多个蓝字"),
    
    # 格式7: 带话题标签
    ("<a href=\"#\">#对弈竞猜#</a> <span class=\"s-color-blue\">蓝</span>方", "带话题标签"),
    
    # 格式8: 带链接的蓝字
    ("<a href=\"xxx\"><span class=\"s-color-blue\">蓝</span></a>方必胜", "带链接的蓝字"),
]

for content, desc in test_contents:
    # 模拟 _clean_html 处理
    cleaned = crawler._clean_html(content)
    is_related = GuessParser.is_guess_related(cleaned)
    prediction = GuessParser.parse_prediction(cleaned) if is_related else 'unknown'
    
    print(f"\n格式: {desc}")
    print(f"  原始: {content[:50]}...")
    print(f"  清理后: {cleaned[:50]}...")
    print(f"  是否相关: {is_related}")
    print(f"  预测结果: {prediction}")
    
    if '蓝' in content and prediction != 'right':
        print(f"  ⚠️ 警告: 内容包含'蓝'字但预测不是'right'")

print("\n" + "=" * 80)
print("测试完成")
print("=" * 80)
