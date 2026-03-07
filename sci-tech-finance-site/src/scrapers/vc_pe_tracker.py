#!/usr/bin/env python3
"""
VC/PE投资数据抓取模块
- 抓取最新投资事件
- 抓取投资机构数据
- 抓取行业投资趋势
"""

import os
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
import requests
from bs4 import BeautifulSoup

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 项目根目录
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / 'data' / 'raw' / 'vcpe'

# 确保目录存在
DATA_DIR.mkdir(parents=True, exist_ok=True)


class VCPETracker:
    """VC/PE投资数据追踪器"""
    
    def __init__(self):
        self.today = datetime.now().strftime('%Y-%m-%d')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        logger.info(f"初始化VC/PE追踪器 - {self.today}")
    
    def get_investment_events(self, days=7):
        """获取最近投资事件"""
        try:
            logger.info(f"开始抓取近{days}天投资事件...")
            
            # 模拟数据（实际项目需要对接真实数据源）
            # 可以使用投中网、IT桔子等API
            
            # 生成示例数据
            sample_events = [
                {
                    'date': (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d'),
                    'company': f'科创企业_{i}',
                    'sector': ['人工智能', '生物医药', '新能源', '半导体', '企业服务'][i % 5],
                    'stage': ['种子轮', '天使轮', 'A轮', 'B轮', 'C轮', 'D轮'][i % 6],
                    'amount': f'{10 + i * 5} 百万美元',
                    'investors': f'某知名投资机构_{i}'
                }
                for i in range(days * 3)
            ]
            
            df = pd.DataFrame(sample_events)
            
            # 保存数据
            output_file = DATA_DIR / f'investment_events_{self.today}.csv'
            df.to_csv(output_file, index=False, encoding='utf-8-sig')
            logger.info(f"投资事件已保存: {output_file}")
            logger.info(f"共 {len(df)} 条投资记录")
            
            return df
            
        except Exception as e:
            logger.error(f"抓取投资事件失败: {e}")
            return None
    
    def get_sector_trends(self):
        """获取行业投资趋势"""
        try:
            logger.info("开始分析行业投资趋势...")
            
            # 模拟行业趋势数据
            sector_data = {
                'sectors': ['人工智能', '生物医药', '新能源', '半导体', '企业服务', '先进制造', '新材料'],
                'deal_count': [156, 134, 98, 87, 76, 65, 54],
                'total_amount': [45.2, 38.6, 32.1, 28.4, 22.3, 18.7, 15.2],  # 亿美元
                'avg_deal_size': [28.9, 28.8, 32.8, 32.6, 29.3, 28.8, 28.1]  # 百万美元
            }
            
            df = pd.DataFrame(sector_data)
            
            # 保存数据
            output_file = DATA_DIR / f'sector_trends_{self.today}.csv'
            df.to_csv(output_file, index=False, encoding='utf-8-sig')
            logger.info(f"行业趋势已保存: {output_file}")
            
            return df
            
        except Exception as e:
            logger.error(f"抓取行业趋势失败: {e}")
            return None
    
    def get_top_investors(self):
        """获取活跃投资机构排名"""
        try:
            logger.info("开始抓取活跃投资机构...")
            
            # 模拟投资机构数据
            investor_data = {
                'rank': list(range(1, 21)),
                'investor_name': [
                    '红杉中国', '高瓴资本', 'IDG资本', '腾讯投资', '阿里巴巴',
                    '深创投', '经纬创投', '启明创投', '五源资本', 'GGV纪源资本',
                    '顺为资本', '源码资本', '君联资本', '高榕资本', 'DCM中国',
                    '今日资本', '华兴资本', '挚信资本', '软银中国', '百度风投'
                ],
                'deal_count': [45, 42, 38, 35, 33, 31, 29, 27, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14],
                'total_amount': [12.5, 11.8, 9.6, 8.9, 8.2, 7.5, 6.8, 6.2, 5.9, 5.5, 
                               5.2, 4.8, 4.5, 4.2, 3.9, 3.6, 3.3, 3.1, 2.9, 2.7]
            }
            
            df = pd.DataFrame(investor_data)
            
            # 保存数据
            output_file = DATA_DIR / f'top_investors_{self.today}.csv'
            df.to_csv(output_file, index=False, encoding='utf-8-sig')
            logger.info(f"投资机构排名已保存: {output_file}")
            
            return df
            
        except Exception as e:
            logger.error(f"抓取投资机构失败: {e}")
            return None
    
    def generate_summary(self):
        """生成VC/PE市场摘要"""
        try:
            logger.info("生成市场摘要...")
            
            summary = {
                'date': self.today,
                'period': '本月',
                'total_deals': 650,
                'total_amount_usd': 18.5,  # 亿美元
                'yoy_growth': 12.5,  # 同比增长
                'mom_growth': 3.2,  # 环比增长
                'hot_sectors': ['人工智能', '生物医药', '新能源'],
                'top_deal': {
                    'company': '某AI芯片公司',
                    'amount': '5亿美元',
                    'investors': '多家知名机构联合投资'
                }
            }
            
            # 保存摘要
            output_file = DATA_DIR / f'market_summary_{self.today}.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, ensure_ascii=False, indent=2)
            
            logger.info(f"市场摘要已保存: {output_file}")
            return summary
            
        except Exception as e:
            logger.error(f"生成市场摘要失败: {e}")
            return None
    
    def run(self):
        """运行所有抓取任务"""
        logger.info("=" * 50)
        logger.info("开始VC/PE数据抓取任务")
        logger.info("=" * 50)
        
        # 抓取投资事件
        events = self.get_investment_events()
        
        # 抓取行业趋势
        trends = self.get_sector_trends()
        
        # 抓取投资机构
        investors = self.get_top_investors()
        
        # 生成摘要
        summary = self.generate_summary()
        
        logger.info("=" * 50)
        logger.info("VC/PE数据抓取完成")
        logger.info("=" * 50)
        
        return {
            'events': events,
            'trends': trends,
            'investors': investors,
            'summary': summary
        }


if __name__ == '__main__':
    tracker = VCPETracker()
    results = tracker.run()
