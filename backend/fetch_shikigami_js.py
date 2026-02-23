"""
从阴阳师官网JS文件中提取式神数据
"""
import requests
import re
import json

def fetch_shikigami_from_js():
    """从官网JS文件中提取式神数据"""
    
    # 可能的JS文件路径
    js_urls = [
        "https://yys.res.netease.com/pc/zt/20161108171335/js/index.js",
        "https://yys.res.netease.com/pc/zt/20161108171335/js/shishen.js",
        "https://yys.res.netease.com/pc/gw/20160929201016/js/common.js",
        "https://yys.163.com/shishen/js/index.js",
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0