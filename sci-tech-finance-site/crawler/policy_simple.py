#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
国务院政策爬虫 - 简化版
适合快速上手和测试

功能:
1. 爬取国务院政策文件
2. 自动去重
3. 保存到 SQLite
4. 导出 JSON
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
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}


def init_database():
    """初始化数据库"""
    conn = sqlite3.connect('policies.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS policies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            publish_date TEXT,
            source TEXT,
            summary TEXT,
            url TEXT UNIQUE NOT NULL,
            url_hash TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 创建索引
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_url_hash ON policies(url_hash)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_date ON policies(publish_date)')
    
    conn.commit()
    conn.close()
    print("✅ 数据库初始化完成")


def is_exists(url):
    """检查URL是否已存在"""
    conn = sqlite3.connect('policies.db')
    cursor = conn.cursor()
    
    url_hash = hashlib.md5(url.encode()).hexdigest()
    cursor.execute('SELECT 1 FROM policies WHERE url_hash = ?', (url_hash,))
    exists = cursor.fetchone() is not None
    
    conn.close()
    return exists


def save_policy(title, url, date=None, source=None, summary=None):
    """保存政策到数据库"""
    conn = sqlite3.connect('policies.db')
    cursor = conn.cursor()
    
    url_hash = hashlib.md5(url.encode()).hexdigest()
    
    try:
        cursor.execute('''
            INSERT OR IGNORE INTO policies (title, publish_date, source, summary, url, url_hash)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, date, source, summary, url, url_hash))
        
        conn.commit()
        inserted = cursor.rowcount > 0
        conn.close()
        return inserted
        
    except Exception as e:
        print(f"❌ 保存失败: {e}")
        conn.close()
        return False


def fetch_policies(page=0):
    """获取政策列表"""
    url = 'http://sousuo.gov.cn/column/30412/0.htm'
    params = {'page': page}
    
    try:
        print(f"🚀 正在获取第 {page + 1} 页...")
        response = requests.get(url, params=params, headers=HEADERS, timeout=30)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            print(f"❌ HTTP {response.status_code}")
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        policies = []
        
        # 查找政策列表（根据政府网实际结构调整）
        items = soup.select('.list li') or soup.select('.result li')
        
        for item in items:
            try:
                link = item.find('a')
                if not link:
                    continue
                
                title = link.get_text(strip=True)
                href = link.get('href', '')
                
                if not title or not href:
                    continue
                
                # 处理URL
                if href.startswith('http'):
                    full_url = href
                else:
                    full_url = urljoin('https://www.gov.cn', href)
                
                # 提取日期
                date_text = item.get_text()
                date_match = re.search(r'(\d{4})-(\d{2})-(\d{2})', date_text)
                publish_date = date_match.group(0) if date_match else None
                
                policies.append({
                    'title': title,
                    'url': full_url,
                    'date': publish_date
                })
                
            except Exception as e:
                print(f"⚠️ 解析失败: {e}")
                continue
        
        print(f"✅ 获取到 {len(policies)} 条政策")
        return policies
        
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return []


def main():
    """主函数"""
    print("=" * 60)
    print("🏛️  国务院政策爬虫启动")
    print("=" * 60)
    
    # 1. 初始化数据库
    init_database()
    
    # 2. 爬取数据
    total_new = 0
    total_skip = 0
    
    for page in range(3):  # 爬取前3页
        policies = fetch_policies(page)
        
        for policy in policies:
            if is_exists(policy['url']):
                total_skip += 1
                print(f"⏭️  跳过(已存在): {policy['title'][:40]}...")
            else:
                if save_policy(
                    title=policy['title'],
                    url=policy['url'],
                    date=policy['date']
                ):
                    total_new += 1
                    print(f"✅ 新增: {policy['title'][:40]}...")
        
        time.sleep(1)  # 礼貌延迟
    
    # 3. 导出数据
    conn = sqlite3.connect('policies.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM policies ORDER BY publish_date DESC')
    rows = cursor.fetchall()
    
    policies_data = [dict(row) for row in rows]
    
    with open('policies.json', 'w', encoding='utf-8') as f:
        json.dump({
            'export_time': datetime.now().isoformat(),
            'total': len(policies_data),
            'data': policies_data
        }, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已导出到 policies.json (共 {len(policies_data)} 条)")
    
    # 4. 统计
    print("\n" + "=" * 60)
    print("📊 统计信息")
    print("=" * 60)
    print(f"新增: {total_new} 条")
    print(f"跳过: {total_skip} 条")
    print(f"数据库总数: {len(policies_data)} 条")
    print("=" * 60)
    
    conn.close()


if __name__ == "__main__":
    main()
