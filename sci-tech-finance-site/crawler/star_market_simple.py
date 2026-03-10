#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
科创板数据爬虫 - 简化版
适合快速上手和测试

功能:
1. 使用 AKShare 获取科创板实时数据
2. 存储到 SQLite 数据库
3. 导出 JSON 文件
"""

import json
import sqlite3
from datetime import datetime
import akshare as ak
import pandas as pd


def create_database():
    """创建数据库和表"""
    conn = sqlite3.connect('star_market.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS star_market_companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_code TEXT UNIQUE NOT NULL,
            stock_name TEXT NOT NULL,
            industry TEXT,
            market_cap REAL,
            listing_date TEXT,
            price REAL,
            change_pct REAL,
            volume REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ 数据库初始化完成")


def fetch_star_market_data():
    """获取科创板数据"""
    print("🚀 正在获取科创板数据...")
    
    try:
        # 使用 AKShare 获取科创板实时行情
        df = ak.stock_zh_kcb_spot_em()
        print(f"✅ 成功获取 {len(df)} 条数据")
        return df
    except Exception as e:
        print(f"❌ 获取数据失败: {e}")
        return None


def fetch_listing_dates():
    """获取上市日期信息"""
    print("📅 正在获取上市日期信息...")
    
    try:
        # 获取科创板IPO列表
        df = ak.stock_zh_kcb_report_em()
        
        # 创建股票代码到上市日期的映射
        listing_map = {}
        for _, row in df.iterrows():
            code = str(row.get('股票代码', '')).strip()
            date = str(row.get('上市日期', '')).strip()
            if code and date:
                listing_map[code] = date
        
        print(f"✅ 获取到 {len(listing_map)} 条上市日期")
        return listing_map
    except Exception as e:
        print(f"⚠️  获取上市日期失败: {e}")
        return {}


def process_data(df, listing_map):
    """处理数据"""
    companies = []
    
    for _, row in df.iterrows():
        try:
            stock_code = str(row.get('代码', '')).strip()
            
            company = {
                'stock_code': stock_code,
                'stock_name': str(row.get('名称', '')).strip(),
                'industry': str(row.get('所属行业', '')).strip() if pd.notna(row.get('所属行业')) else None,
                'market_cap': round(float(row.get('总市值', 0)) / 100000000, 2) if pd.notna(row.get('总市值')) else None,  # 转换为亿元
                'price': round(float(row.get('最新价', 0)), 2) if pd.notna(row.get('最新价')) else None,
                'change_pct': round(float(row.get('涨跌幅', 0)), 2) if pd.notna(row.get('涨跌幅')) else None,
                'volume': round(float(row.get('成交量', 0)) / 10000, 2) if pd.notna(row.get('成交量')) else None,  # 转换为万股
                'listing_date': listing_map.get(stock_code, None)
            }
            
            companies.append(company)
        except Exception as e:
            print(f"⚠️  解析数据失败: {e}")
            continue
    
    return companies


def save_to_database(companies):
    """保存到数据库"""
    conn = sqlite3.connect('star_market.db')
    cursor = conn.cursor()
    
    success_count = 0
    
    for company in companies:
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO star_market_companies 
                (stock_code, stock_name, industry, market_cap, listing_date, price, change_pct, volume, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                company['stock_code'],
                company['stock_name'],
                company['industry'],
                company['market_cap'],
                company['listing_date'],
                company['price'],
                company['change_pct'],
                company['volume'],
                datetime.now()
            ))
            success_count += 1
        except Exception as e:
            print(f"❌ 保存失败 {company['stock_code']}: {e}")
    
    conn.commit()
    conn.close()
    
    print(f"✅ 成功保存 {success_count}/{len(companies)} 条数据到数据库")
    return success_count


def export_to_json(companies, filename='star_market_data.json'):
    """导出到 JSON"""
    export_data = {
        'export_time': datetime.now().isoformat(),
        'total_count': len(companies),
        'data_source': '上海证券交易所科创板',
        'data': companies
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 数据已导出到: {filename}")


def export_to_csv(companies, filename='star_market_data.csv'):
    """导出到 CSV"""
    df = pd.DataFrame(companies)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"✅ 数据已导出到: {filename}")


def print_statistics():
    """打印统计信息"""
    conn = sqlite3.connect('star_market.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM star_market_companies')
    total = cursor.fetchone()[0]
    
    cursor.execute('SELECT AVG(market_cap) FROM star_market_companies WHERE market_cap IS NOT NULL')
    avg_cap = cursor.fetchone()[0]
    
    cursor.execute('''
        SELECT industry, COUNT(*) as count 
        FROM star_market_companies 
        WHERE industry IS NOT NULL 
        GROUP BY industry 
        ORDER BY count DESC 
        LIMIT 5
    ''')
    top_industries = cursor.fetchall()
    
    conn.close()
    
    print("\n" + "=" * 50)
    print("📊 数据统计")
    print("=" * 50)
    print(f"总公司数: {total}")
    print(f"平均市值: {avg_cap:.2f} 亿元")
    print("\n🏭 前5大行业:")
    for industry, count in top_industries:
        print(f"  {industry}: {count} 家")
    print("=" * 50)


def main():
    """主函数"""
    print("=" * 50)
    print("🚀 科创板数据爬虫启动")
    print("=" * 50)
    
    # 1. 创建数据库
    create_database()
    
    # 2. 获取数据
    df = fetch_star_market_data()
    if df is None:
        print("❌ 任务失败")
        return
    
    # 3. 获取上市日期
    listing_map = fetch_listing_dates()
    
    # 4. 处理数据
    companies = process_data(df, listing_map)
    print(f"📦 成功处理 {len(companies)} 条数据")
    
    # 5. 保存到数据库
    save_to_database(companies)
    
    # 6. 导出文件
    export_to_json(companies)
    export_to_csv(companies)
    
    # 7. 打印统计
    print_statistics()
    
    print("\n✅ 任务完成!")


if __name__ == "__main__":
    main()
