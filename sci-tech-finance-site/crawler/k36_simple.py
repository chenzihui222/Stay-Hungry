#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
36氪融资爬虫 - 简化版
适合快速上手和测试
"""

import json
import hashlib
import sqlite3
import re
import time
from datetime import datetime
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

# 配置
DB_PATH = "funding_data.db"
RSS_URL = "https://36kr.com/feed"


def init_database():
    """初始化数据库"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS funding_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            funding_round TEXT,
            amount REAL,
            amount_text TEXT,
            investors TEXT,
            funding_date TEXT,
            industry TEXT,
            source_url TEXT UNIQUE,
            event_hash TEXT UNIQUE,
            title TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_hash ON funding_events(event_hash)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_date ON funding_events(funding_date)')
    
    conn.commit()
    conn.close()
    print("✅ 数据库初始化完成")


def extract_company_name(title):
    """提取公司名"""
    # 匹配「公司名」或"公司名"
    patterns = [
        r'「([^」]{2,20})」',
        r'"([^"]{2,20})"',
        r'【([^】]{2,20})】',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, title)
        if match:
            return match.group(1).strip()
    
    # 从句首提取
    match = re.search(r'^([^，。；]+?)(?:完成|获|宣布)', title)
    if match:
        return match.group(1).strip()
    
    return None


def extract_funding_round(title):
    """提取融资轮次"""
    rounds = {
        '种子': '种子轮', '天使': '天使轮',
        'pre-a': 'Pre-A轮', 'a轮': 'A轮', 'a+': 'A+轮',
        'b轮': 'B轮', 'b+': 'B+轮', 'c轮': 'C轮',
        'd轮': 'D轮', 'e轮': 'E轮', 'f轮': 'F轮',
        'pre-ipo': 'Pre-IPO', 'ipo': 'IPO', '上市': 'IPO',
        '战略': '战略融资', '并购': '并购'
    }
    
    title_lower = title.lower()
    for keyword, round_name in rounds.items():
        if keyword in title_lower:
            return round_name
    
    return None


def extract_amount(title):
    """提取金额"""
    # 匹配数字+单位
    pattern = r'(\d+(?:\.\d+)?)\s*([万亿千万]?)\s*(?:美元|人民币|元)?'
    match = re.search(pattern, title)
    
    if match:
        num = float(match.group(1))
        unit = match.group(2)
        
        # 转换为元
        multipliers = {'万': 10000, '千': 1000, '百万': 1000000, 
                      '千万': 10000000, '亿': 100000000}
        multiplier = multipliers.get(unit, 1)
        
        return num * multiplier, match.group(0)
    
    return None, None


def extract_investors(title):
    """提取投资机构"""
    investors = []
    known = ['红杉', '高瓴', 'IDG', '腾讯', '阿里', '字节', '美团', 
             '小米', '深创投', '达晨', '软银']
    
    for inv in known:
        if inv in title:
            investors.append(inv)
    
    return investors


def fetch_rss():
    """获取RSS数据"""
    print("🚀 正在获取36氪RSS...")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(RSS_URL, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        news_list = []
        for item in items:
            title = item.title.text if item.title else ""
            
            # 只保留融资相关
            if any(kw in title for kw in ['融资', '获投', '轮', '投资']):
                news_list.append({
                    'title': title,
                    'link': item.link.text if item.link else "",
                    'pub_date': item.pubDate.text if item.pubDate else ""
                })
        
        print(f"✅ 获取到 {len(news_list)} 条融资新闻")
        return news_list
        
    except Exception as e:
        print(f"❌ 获取失败: {e}")
        return []


def save_event(title, link, pub_date):
    """保存融资事件"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 提取信息
    company = extract_company_name(title)
    round_type = extract_funding_round(title)
    amount, amount_text = extract_amount(title)
    investors = extract_investors(title)
    
    if not company:
        conn.close()
        return False
    
    # 生成哈希
    event_hash = hashlib.md5(f"{company}_{pub_date}_{round_type}".encode()).hexdigest()
    
    try:
        cursor.execute('''
            INSERT OR IGNORE INTO funding_events 
            (company_name, funding_round, amount, amount_text, investors, 
             funding_date, source_url, event_hash, title)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            company, round_type, amount, amount_text, 
            json.dumps(investors), pub_date, link, event_hash, title
        ))
        
        conn.commit()
        inserted = cursor.rowcount > 0
        conn.close()
        return inserted
        
    except Exception as e:
        print(f"❌ 保存失败: {e}")
        conn.close()
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("🚀 36氪融资爬虫启动")
    print("=" * 60)
    
    # 初始化数据库
    init_database()
    
    # 获取数据
    news_list = fetch_rss()
    
    # 处理和保存
    total = 0
    new_count = 0
    
    for news in news_list:
        total += 1
        if save_event(news['title'], news['link'], news['pub_date']):
            new_count += 1
            print(f"✅ 新增: {news['title'][:50]}...")
        else:
            print(f"⏭️  跳过: {news['title'][:50]}...")
        
        time.sleep(1)  # 礼貌延迟
    
    # 导出
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM funding_events ORDER BY funding_date DESC')
    rows = cursor.fetchall()
    events = [dict(row) for row in rows]
    conn.close()
    
    with open('funding_data.json', 'w', encoding='utf-8') as f:
        json.dump({
            'export_time': datetime.now().isoformat(),
            'total': len(events),
            'data': events
        }, f, ensure_ascii=False, indent=2)
    
    # 统计
    print("\n" + "=" * 60)
    print("📊 统计信息")
    print("=" * 60)
    print(f"处理: {total} 条")
    print(f"新增: {new_count} 条")
    print(f"数据库总数: {len(events)} 条")
    print(f"导出文件: funding_data.json")
    print("=" * 60)


if __name__ == "__main__":
    main()
