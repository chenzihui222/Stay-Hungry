#!/usr/bin/env python3
"""
科创板数据抓取模块
- 抓取科创板上市公司列表
- 抓取IPO数据
- 抓取市场行情数据
使用akshare库获取上交所数据
"""

import os
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 项目根目录
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / 'data' / 'raw' / 'star_market'

# 确保目录存在
DATA_DIR.mkdir(parents=True, exist_ok=True)


class StarMarketScraper:
    """科创板数据抓取器"""
    
    def __init__(self):
        self.today = datetime.now().strftime('%Y-%m-%d')
        logger.info(f"初始化科创板数据抓取器 - {self.today}")
    
    def get_stock_list(self):
        """获取科创板股票列表"""
        try:
            logger.info("开始抓取科创板股票列表...")
            
            # 使用akshare获取科创板数据
            import akshare as ak
            df = ak.stock_kcg_board_em()
            
            # 数据清洗
            df = df.rename(columns={
                '代码': 'code',
                '名称': 'name',
                '最新价': 'price',
                '涨跌幅': 'change_pct',
                '总市值': 'market_cap',
                '市盈率': 'pe_ratio',
                '所属行业': 'industry',
                '上市日期': 'listing_date'
            })
            
            # 保存数据
            output_file = DATA_DIR / f'stock_list_{self.today}.csv'
            df.to_csv(output_file, index=False, encoding='utf-8-sig')
            logger.info(f"股票列表已保存: {output_file}")
            logger.info(f"共抓取 {len(df)} 只股票")
            
            return df
            
        except Exception as e:
            logger.error(f"抓取股票列表失败: {e}")
            return None
    
    def get_ipo_data(self, years=3):
        """获取科创板IPO数据（历史N年）"""
        try:
            logger.info(f"开始抓取科创板IPO数据（近{years}年）...")
            
            import akshare as ak
            
            # 获取新股申购数据
            df = ak.stock_new_ipo_cninfo()
            
            # 筛选科创板（688开头）
            df = df[df['证券代码'].str.startswith('688')]
            
            # 保存数据
            output_file = DATA_DIR / f'ipo_data_{self.today}.csv'
            df.to_csv(output_file, index=False, encoding='utf-8-sig')
            logger.info(f"IPO数据已保存: {output_file}")
            logger.info(f"共 {len(df)} 条IPO记录")
            
            return df
            
        except Exception as e:
            logger.error(f"抓取IPO数据失败: {e}")
            return None
    
    def get_market_overview(self):
        """获取科创板市场整体概况"""
        try:
            logger.info("开始抓取科创板市场概况...")
            
            import akshare as ak
            
            # 获取科创板指数
            df_index = ak.index_zh_a_hist(symbol="000688", period="daily")
            
            # 获取最近30天的数据
            df_index = df_index.tail(30)
            
            # 保存数据
            output_file = DATA_DIR / f'market_overview_{self.today}.csv'
            df_index.to_csv(output_file, index=False, encoding='utf-8-sig')
            logger.info(f"市场概况已保存: {output_file}")
            
            # 生成统计信息
            stats = {
                'date': self.today,
                'index_name': '科创50',
                'latest_close': float(df_index['收盘'].iloc[-1]),
                'latest_change_pct': float(df_index['涨跌幅'].iloc[-1]),
                'avg_volume_30d': float(df_index['成交量'].mean()),
                'max_price_30d': float(df_index['最高'].max()),
                'min_price_30d': float(df_index['最低'].min())
            }
            
            # 保存统计信息
            stats_file = DATA_DIR / f'market_stats_{self.today}.json'
            with open(stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats, f, ensure_ascii=False, indent=2)
            
            logger.info(f"市场统计: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"抓取市场概况失败: {e}")
            return None
    
    def run(self):
        """运行所有抓取任务"""
        logger.info("=" * 50)
        logger.info("开始科创板数据抓取任务")
        logger.info("=" * 50)
        
        # 抓取股票列表
        stock_list = self.get_stock_list()
        
        # 抓取IPO数据
        ipo_data = self.get_ipo_data()
        
        # 抓取市场概况
        market_stats = self.get_market_overview()
        
        logger.info("=" * 50)
        logger.info("科创板数据抓取完成")
        logger.info("=" * 50)
        
        return {
            'stock_list': stock_list,
            'ipo_data': ipo_data,
            'market_stats': market_stats
        }


if __name__ == '__main__':
    scraper = StarMarketScraper()
    results = scraper.run()
