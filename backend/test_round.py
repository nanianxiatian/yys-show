#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from spider import GuessParser
from datetime import datetime

# 测试不同时间对应的轮次
test_times = [
    (2026, 2, 22, 10, 30),   # 10:30 -> 第1轮
    (2026, 2, 22, 11, 45),   # 11:45 -> 第1轮
    (2026, 2, 22, 12, 0),    # 12:00 -> 第2轮
    (2026, 2, 22, 12, 44),   # 12:44 -> 第2轮 (徐清林的微博)
    (2026, 2, 22, 13, 30),   # 13:30 -> 第2轮
    (2026, 2, 22, 14, 0),    # 14:00 -> 第3轮
    (2026, 2, 22, 15, 59),   # 15:59 -> 第3轮
    (2026, 2, 22, 16, 0),    # 16:00 -> 第4轮
    (2026, 2, 22, 18, 0),    # 18:00 -> 第5轮
    (2026, 2, 22, 20, 0),    # 20:00 -> 第6轮
    (2026, 2, 22, 22, 0),    # 22:00 -> 第7轮
    (2026, 2, 22, 23, 59),   # 23:59 -> 第7轮
    (2026, 2, 22, 9, 0),     # 09:00 -> None (不在竞猜时间)
]

print("=" * 60)
print("测试轮次计算")
print("=" * 60)

for year, month, day, hour, minute in test_times:
    publish_time = datetime(year, month, day, hour, minute)
    round_num = GuessParser.parse_guess_round(publish_time)
    print(f"{hour:02d}:{minute:02d} -> 第{round_num}轮")

print("\n" + "=" * 60)
