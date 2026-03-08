#!/usr/bin/env python3
"""
科创板数据抓取器
数据源：上海证券交易所科创板
"""

import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional
import requests
from bs4 import BeautifulSoup
import pandas as pd

from .base_scraper import BaseScraper, DataItem


class MarketScraper(BaseScraper):
    """科创板数据抓取器"""
    
    # 上交所科创板数据源
    SOURCES = {
        'sse_kcb_list': 'http://query.sse.com.cn/commonQuery.do?sqlId=COMMON_SSE_SCREENCEOINFO_CPRNEW',
        'sse_ipo': 'http://query.sse.com.cn/commonQuery.do?sqlId=COMMON_SSE_SCREENCEOINFO_CPRNEW',
        'akshare': 'akshare_library'
    }
    
    def __init__(self, data_dir: Path):
        super().__init__(data_dir)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'http://www.sse.com.cn/'
        })
        
    def scrape(self) -> List[DataItem]:
        """执行科创板数据抓取"""
        items = []
        
        # 1. 抓取科创板公司列表
        stock_items = self._scrape_stock_list()
        items.extend(stock_items)
        
        # 2. 抓取IPO数据
        ipo_items = self._scrape_ipo_data()
        items.extend(ipo_items)
        
        # 3. 抓取市场动态
        news_items = self._scrape_market_news()
        items.extend(news_items)
        
        # 4. 如果没有抓到公司列表数据，使用备用方案
        if not stock_items:
            self.logger.warning("未抓取到公司列表数据，使用备用方案...")
            fallback_items = self._scrape_stock_list_fallback()
            items.extend(fallback_items)
        
        return items
    
    def _scrape_stock_list(self) -> List[DataItem]:
        """抓取科创板上市公司列表"""
        items = []
        
        try:
            self.logger.info("开始抓取科创板上市公司列表...")
            
            # 使用akshare获取科创板数据
            try:
                import akshare as ak
                df = ak.stock_kcg_board_em()
                
                for _, row in df.iterrows():
                    company_name = row.get('名称', '')
                    stock_code = row.get('代码', '')
                    industry = row.get('所属行业', '')
                    listing_date = row.get('上市日期', '')
                    
                    content = f"""
                    公司名称: {company_name}
                    股票代码: {stock_code}
                    所属行业: {industry}
                    上市日期: {listing_date}
                    最新价: {row.get('最新价', 'N/A')}
                    涨跌幅: {row.get('涨跌幅', 'N/A')}%
                    总市值: {row.get('总市值', 'N/A')}亿元
                    市盈率: {row.get('市盈率', 'N/A')}
                    """.strip()
                    
                    item = DataItem(
                        date=listing_date if listing_date else self.today,
                        title=f"科创板上市公司：{company_name} ({stock_code})",
                        type='market',
                        content=content,
                        source='上交所科创板',
                        url=f'http://www.sse.com.cn/assortment/stock/list/info/company/index.shtml?COMPANY_CODE={stock_code}',
                        tags=['科创板', '上市公司', industry],
                        metadata={
                            'stock_code': stock_code,
                            'industry': industry,
                            'market_cap': row.get('总市值', 0),
                            'pe_ratio': row.get('市盈率', 0)
                        }
                    )
                    items.append(item)
                
                self.logger.info(f"成功抓取 {len(items)} 条科创板公司数据")
                
            except ImportError:
                self.logger.warning("akshare未安装，使用备用方案")
                items.extend(self._scrape_stock_list_fallback())
                
        except Exception as e:
            self.logger.error(f"抓取科创板公司列表失败: {e}")
            items.extend(self._scrape_stock_list_fallback())
        
        return items
    
    def _scrape_stock_list_fallback(self) -> List[DataItem]:
        """备用方案：生成示例科创板公司数据"""
        items = []
        
        self.logger.info("使用备用数据源生成示例数据...")
        
        # 科创板示例公司数据
        sample_companies = [
            {'name': '中芯国际', 'code': '688981', 'industry': '半导体', 'date': '2020-07-16'},
            {'name': '金山办公', 'code': '688111', 'industry': '软件服务', 'date': '2019-11-18'},
            {'name': '传音控股', 'code': '688036', 'industry': '消费电子', 'date': '2019-09-30'},
            {'name': '澜起科技', 'code': '688008', 'industry': '半导体', 'date': '2019-07-22'},
            {'name': '中国通号', 'code': '688009', 'industry': '铁路设备', 'date': '2019-07-22'},
            {'name': '中微公司', 'code': '688012', 'industry': '半导体设备', 'date': '2019-07-22'},
            {'name': '南微医学', 'code': '688029', 'industry': '医疗器械', 'date': '2019-07-22'},
            {'name': '心脉医疗', 'code': '688016', 'industry': '医疗器械', 'date': '2019-07-22'},
            {'name': '安集科技', 'code': '688019', 'industry': '半导体材料', 'date': '2019-07-22'},
            {'name': '乐鑫科技', 'code': '688018', 'industry': '集成电路', 'date': '2019-07-22'},
        ]
        
        for company in sample_companies:
            content = f"""
            公司名称: {company['name']}
            股票代码: {company['code']}
            所属行业: {company['industry']}
            上市日期: {company['date']}
            市场: 科创板
            数据来源: 示例数据（备用方案）
            """.strip()
            
            item = DataItem(
                date=company['date'],
                title=f"科创板上市公司：{company['name']} ({company['code']})",
                type='market',
                content=content,
                source='上交所科创板（示例）',
                url=f'http://www.sse.com.cn/assortment/stock/list/info/company/index.shtml?COMPANY_CODE={company["code"]}',
                tags=['科创板', '上市公司', company['industry']],
                metadata={
                    'stock_code': company['code'],
                    'industry': company['industry'],
                    'is_sample': True
                }
            )
            items.append(item)
        
        self.logger.info(f"生成 {len(items)} 条科创板示例数据")
        return items
    
    def _scrape_ipo_data(self) -> List[DataItem]:
        """抓取科创板IPO数据"""
        items = []
        
        try:
            self.logger.info("开始抓取科创板IPO数据...")
            
            try:
                import akshare as ak
                df = ak.stock_new_ipo_cninfo()
                
                # 筛选科创板（688开头）
                df = df[df['证券代码'].astype(str).str.startswith('688')]
                
                for _, row in df.iterrows():
                    company_name = row.get('公司名称', '')
                    stock_code = row.get('证券代码', '')
                    ipo_date = row.get('上市日期', '')
                    issue_price = row.get('发行价格', '')
                    raise_amount = row.get('募集资金总额', '')
                    
                    content = f"""
                    IPO公司: {company_name}
                    股票代码: {stock_code}
                    上市日期: {ipo_date}
                    发行价格: {issue_price}元
                    募集资金: {raise_amount}亿元
                    申购代码: {row.get('申购代码', 'N/A')}
                    发行市盈率: {row.get('发行市盈率', 'N/A')}
                    """.strip()
                    
                    item = DataItem(
                        date=str(ipo_date) if ipo_date else self.today,
                        title=f"科创板IPO：{company_name} ({stock_code})",
                        type='market',
                        content=content,
                        source='上交所IPO',
                        url=f'http://www.sse.com.cn/assortment/stock/list/info/ipo/index.shtml',
                        tags=['科创板', 'IPO', '新股'],
                        metadata={
                            'stock_code': stock_code,
                            'issue_price': issue_price,
                            'raise_amount': raise_amount,
                            'ipo_date': ipo_date
                        }
                    )
                    items.append(item)
                
                self.logger.info(f"成功抓取 {len(items)} 条IPO数据")
                
            except ImportError:
                self.logger.warning("akshare未安装，跳过IPO数据抓取")
                
        except Exception as e:
            self.logger.error(f"抓取IPO数据失败: {e}")
        
        return items
    
    def _scrape_market_news(self) -> List[DataItem]:
        """抓取科创板市场动态新闻"""
        items = []
        
        try:
            self.logger.info("开始抓取科创板市场动态...")
            
            # 上交所公告栏
            url = 'http://www.sse.com.cn/disclosure/listedinfo/announcement/'
            response = self.session.get(url, timeout=30)
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找公告列表
            news_list = soup.find_all('a', href=re.compile(r'announcement'))
            
            for news in news_list[:10]:  # 只取前10条
                title = news.get_text(strip=True)
                link = news.get('href', '')
                
                link_str = str(link) if link else ''
                if link_str and not link_str.startswith('http'):
                    link_str = 'http://www.sse.com.cn' + link_str
                
                if title and '688' in title:  # 科创板相关公告
                    item = DataItem(
                        date=self.today,
                        title=title[:100],  # 限制长度
                        type='market',
                        content=f"上交所公告: {title}",
                        source='上交所公告',
                        url=link_str,
                        tags=['科创板', '公告', '市场动态'],
                        metadata={}
                    )
                    items.append(item)
            
            self.logger.info(f"成功抓取 {len(items)} 条市场动态")
            
        except Exception as e:
            self.logger.error(f"抓取市场动态失败: {e}")
        
        return items
    
    def get_market_summary(self) -> Dict[str, Any]:
        """获取市场摘要统计"""
        try:
            import akshare as ak
            
            # 获取科创50指数
            df = ak.index_zh_a_hist(symbol="000688", period="daily")
            latest = df.iloc[-1]
            
            summary = {
                'date': self.today,
                'index_name': '科创50',
                'latest_close': float(latest['收盘']),
                'latest_change_pct': float(latest['涨跌幅']),
                'latest_change_amount': float(latest['涨跌额']),
                'volume': float(latest['成交量']),
                'amount': float(latest['成交额']),
                'high_30d': float(df['最高'].tail(30).max()),
                'low_30d': float(df['最低'].tail(30).min()),
                'avg_volume_30d': float(df['成交量'].tail(30).mean())
            }
            
            # 创建摘要数据项
            content = f"""
            科创50指数: {summary['latest_close']}
            涨跌幅: {summary['latest_change_pct']}%
            涨跌额: {summary['latest_change_amount']}
            成交量: {summary['volume']}万手
            成交额: {summary['amount']}亿元
            30日最高: {summary['high_30d']}
            30日最低: {summary['low_30d']}
            """.strip()
            
            summary_item = DataItem(
                date=self.today,
                title=f"科创50指数日报 ({self.today})",
                type='market',
                content=content,
                source='上交所科创50',
                url='http://www.sse.com.cn/market/sseindex/daily/',
                tags=['科创板', '指数', '科创50'],
                metadata=summary
            )
            
            return {
                'summary': summary,
                'data_item': summary_item
            }
            
        except Exception as e:
            self.logger.error(f"获取市场摘要失败: {e}")
            return {}


if __name__ == '__main__':
    # 测试
    from pathlib import Path
    
    data_dir = Path(__file__).parent.parent.parent / 'data' / 'raw' / 'market'
    scraper = MarketScraper(data_dir)
    
    items = scraper.run()
    
    if items:
        scraper.save_to_json()
        scraper.save_to_ndjson()
        
        # 打印示例
        print("\n示例数据项:")
        print(items[0].to_dict())
