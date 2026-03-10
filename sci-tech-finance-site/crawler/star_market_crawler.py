#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
科创板数据爬虫
Star Market Data Crawler

数据来源: 上海证券交易所科创板
使用技术: requests + BeautifulSoup + AKShare + SQLAlchemy

功能:
1. 爬取科创板上市公司基本信息
2. 存储到 PostgreSQL/SQLite 数据库
3. 导出为 JSON 格式
4. 支持增量更新

作者: Data Engineer
日期: 2026-03-10
"""

import json
import logging
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict

import requests
from bs4 import BeautifulSoup
import akshare as ak
from sqlalchemy import create_engine, Column, String, Float, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ==================== 配置 ====================

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crawler.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 数据库配置
DB_TYPE = "sqlite"  # 可选: "sqlite" 或 "postgresql"
DB_PATH = "star_market.db"  # SQLite 数据库路径
DB_URL = "postgresql://user:password@localhost:5432/stock_db"  # PostgreSQL 配置 (如需使用请取消注释)

# 请求配置
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
}

# ==================== 数据模型 ====================

Base = declarative_base()


class StarMarketCompany(Base):
    """科创板公司数据库模型"""
    __tablename__ = 'star_market_companies'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_code = Column(String(10), unique=True, nullable=False, index=True, comment='股票代码')
    stock_name = Column(String(50), nullable=False, comment='公司名称')
    industry = Column(String(100), comment='所属行业')
    market_cap = Column(Float, comment='总市值（亿元）')
    listing_date = Column(String(20), comment='上市时间')
    price = Column(Float, comment='当前股价')
    change_pct = Column(Float, comment='涨跌幅(%)')
    volume = Column(Float, comment='成交量(万股)')
    created_at = Column(DateTime, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    def __repr__(self):
        return f"<StarMarketCompany({self.stock_code}: {self.stock_name})>"
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'id': self.id,
            'stock_code': self.stock_code,
            'stock_name': self.stock_name,
            'industry': self.industry,
            'market_cap': self.market_cap,
            'listing_date': self.listing_date,
            'price': self.price,
            'change_pct': self.change_pct,
            'volume': self.volume,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


@dataclass
class CompanyData:
    """公司数据 dataclass"""
    stock_code: str
    stock_name: str
    industry: Optional[str] = None
    market_cap: Optional[float] = None
    listing_date: Optional[str] = None
    price: Optional[float] = None
    change_pct: Optional[float] = None
    volume: Optional[float] = None


# ==================== 数据库操作类 ====================

class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, db_type: str = "sqlite", db_path: str = "star_market.db", db_url: str = None):
        self.db_type = db_type
        self.db_path = db_path
        self.db_url = db_url or DB_URL
        self.engine = None
        self.Session = None
        self._init_db()
    
    def _init_db(self):
        """初始化数据库连接"""
        try:
            if self.db_type == "sqlite":
                self.engine = create_engine(
                    f'sqlite:///{self.db_path}',
                    echo=False,
                    connect_args={'check_same_thread': False}
                )
            elif self.db_type == "postgresql":
                self.engine = create_engine(
                    self.db_url,
                    echo=False,
                    pool_size=5,
                    max_overflow=10
                )
            else:
                raise ValueError(f"不支持的数据库类型: {self.db_type}")
            
            # 创建表
            Base.metadata.create_all(self.engine)
            self.Session = sessionmaker(bind=self.engine)
            logger.info(f"数据库初始化成功: {self.db_type}")
            
        except Exception as e:
            logger.error(f"数据库初始化失败: {e}")
            raise
    
    def get_session(self):
        """获取数据库会话"""
        return self.Session()
    
    def insert_or_update(self, company_data: CompanyData) -> bool:
        """插入或更新公司数据"""
        session = self.get_session()
        try:
            # 查询是否已存在
            existing = session.query(StarMarketCompany).filter_by(
                stock_code=company_data.stock_code
            ).first()
            
            if existing:
                # 更新现有记录
                existing.stock_name = company_data.stock_name
                existing.industry = company_data.industry
                existing.market_cap = company_data.market_cap
                existing.listing_date = company_data.listing_date
                existing.price = company_data.price
                existing.change_pct = company_data.change_pct
                existing.volume = company_data.volume
                existing.updated_at = datetime.now()
                logger.debug(f"更新数据: {company_data.stock_code}")
            else:
                # 插入新记录
                new_company = StarMarketCompany(
                    stock_code=company_data.stock_code,
                    stock_name=company_data.stock_name,
                    industry=company_data.industry,
                    market_cap=company_data.market_cap,
                    listing_date=company_data.listing_date,
                    price=company_data.price,
                    change_pct=company_data.change_pct,
                    volume=company_data.volume
                )
                session.add(new_company)
                logger.debug(f"插入新数据: {company_data.stock_code}")
            
            session.commit()
            return True
            
        except Exception as e:
            session.rollback()
            logger.error(f"数据库操作失败 {company_data.stock_code}: {e}")
            return False
        finally:
            session.close()
    
    def get_all_companies(self) -> List[Dict]:
        """获取所有公司数据"""
        session = self.get_session()
        try:
            companies = session.query(StarMarketCompany).all()
            return [company.to_dict() for company in companies]
        finally:
            session.close()
    
    def get_company_count(self) -> int:
        """获取公司总数"""
        session = self.get_session()
        try:
            return session.query(StarMarketCompany).count()
        finally:
            session.close()
    
    def get_latest_update(self) -> Optional[datetime]:
        """获取最新更新时间"""
        session = self.get_session()
        try:
            result = session.query(StarMarketCompany).order_by(
                StarMarketCompany.updated_at.desc()
            ).first()
            return result.updated_at if result else None
        finally:
            session.close()


# ==================== 爬虫类 ====================

class StarMarketCrawler:
    """科创板数据爬虫"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
    
    def fetch_by_akshare(self) -> List[CompanyData]:
        """
        使用 AKShare 获取科创板数据
        优势: 稳定、快速、已清洗
        """
        logger.info("使用 AKShare 获取科创板数据...")
        companies = []
        
        try:
            # 获取科创板实时行情
            df = ak.stock_zh_kcb_spot_em()
            logger.info(f"获取到 {len(df)} 条数据")
            
            for _, row in df.iterrows():
                try:
                    company = CompanyData(
                        stock_code=str(row.get('代码', '')).strip(),
                        stock_name=str(row.get('名称', '')).strip(),
                        industry=str(row.get('所属行业', '')).strip() if pd.notna(row.get('所属行业')) else None,
                        market_cap=float(row.get('总市值', 0)) / 100000000 if pd.notna(row.get('总市值')) else None,  # 转换为亿元
                        price=float(row.get('最新价', 0)) if pd.notna(row.get('最新价')) else None,
                        change_pct=float(row.get('涨跌幅', 0)) if pd.notna(row.get('涨跌幅')) else None,
                        volume=float(row.get('成交量', 0)) / 10000 if pd.notna(row.get('成交量')) else None,  # 转换为万股
                    )
                    companies.append(company)
                except Exception as e:
                    logger.warning(f"解析数据行失败: {e}")
                    continue
            
            logger.info(f"成功解析 {len(companies)} 条数据")
            return companies
            
        except Exception as e:
            logger.error(f"AKShare 获取数据失败: {e}")
            return []
    
    def fetch_listing_info(self) -> Dict[str, str]:
        """
        获取科创板公司上市信息（上市时间）
        使用 AKShare 的 IPO 数据接口
        """
        logger.info("获取科创板 IPO 信息...")
        listing_info = {}
        
        try:
            # 获取科创板IPO列表
            df = ak.stock_zh_kcb_report_em()
            
            for _, row in df.iterrows():
                stock_code = str(row.get('股票代码', '')).strip()
                listing_date = str(row.get('上市日期', '')).strip()
                if stock_code and listing_date:
                    listing_info[stock_code] = listing_date
            
            logger.info(f"获取到 {len(listing_info)} 条上市信息")
            return listing_info
            
        except Exception as e:
            logger.error(f"获取上市信息失败: {e}")
            return {}
    
    def fetch_by_requests(self) -> List[CompanyData]:
        """
        使用 requests + BeautifulSoup 爬取上交所页面
        作为 AKShare 的备用方案
        """
        logger.info("使用 Requests + BeautifulSoup 爬取数据...")
        companies = []
        
        try:
            # 上交所科创板公司列表页面
            url = "http://query.sse.com.cn/commonQuery.do"
            params = {
                'sqlId': 'COMMON_SSE_SCREENSELECTION_LIST',
                'productId': 'kcb',
            }
            headers = {
                **HEADERS,
                'Referer': 'http://kcb.sse.com.cn/',
                'X-Requested-With': 'XMLHttpRequest'
            }
            
            response = self.session.get(url, params=params, headers=headers, timeout=30)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                data = response.json()
                result = data.get('result', [])
                
                for item in result:
                    try:
                        company = CompanyData(
                            stock_code=item.get('SECURITY_CODE_A', ''),
                            stock_name=item.get('SECURITY_ABBR_A', ''),
                            industry=item.get('INDUSTRY_NAME', ''),
                            listing_date=item.get('LISTING_DATE', ''),
                        )
                        companies.append(company)
                    except Exception as e:
                        logger.warning(f"解析数据项失败: {e}")
                        continue
                
                logger.info(f"成功获取 {len(companies)} 条数据")
            else:
                logger.error(f"请求失败: HTTP {response.status_code}")
                
        except Exception as e:
            logger.error(f"爬取失败: {e}")
        
        return companies
    
    def run(self, use_akshare: bool = True) -> bool:
        """
        执行爬取任务
        
        Args:
            use_akshare: 是否优先使用 AKShare（推荐）
        
        Returns:
            bool: 是否成功
        """
        logger.info("=" * 50)
        logger.info("开始爬取科创板数据...")
        logger.info(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 50)
        
        try:
            # 1. 获取基础数据
            if use_akshare:
                companies = self.fetch_by_akshare()
            else:
                companies = self.fetch_by_requests()
            
            if not companies:
                logger.error("未获取到任何数据")
                return False
            
            # 2. 获取上市时间信息（补充）
            listing_info = self.fetch_listing_info()
            
            # 3. 合并数据并入库
            success_count = 0
            for company in companies:
                # 补充上市时间
                if company.stock_code in listing_info:
                    company.listing_date = listing_info[company.stock_code]
                
                # 入库
                if self.db_manager.insert_or_update(company):
                    success_count += 1
            
            logger.info("=" * 50)
            logger.info(f"爬取完成!")
            logger.info(f"获取数据: {len(companies)} 条")
            logger.info(f"成功入库: {success_count} 条")
            logger.info(f"数据库总数: {self.db_manager.get_company_count()} 条")
            logger.info("=" * 50)
            
            return True
            
        except Exception as e:
            logger.error(f"爬取任务失败: {e}", exc_info=True)
            return False


# ==================== 导出功能 ====================

class DataExporter:
    """数据导出器"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def export_to_json(self, filepath: str = "star_market_data.json") -> bool:
        """导出所有数据到 JSON 文件"""
        try:
            data = self.db_manager.get_all_companies()
            
            export_data = {
                'export_time': datetime.now().isoformat(),
                'total_count': len(data),
                'data': data
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"数据已导出到: {filepath}")
            logger.info(f"导出记录数: {len(data)}")
            return True
            
        except Exception as e:
            logger.error(f"导出失败: {e}")
            return False
    
    def export_to_csv(self, filepath: str = "star_market_data.csv") -> bool:
        """导出所有数据到 CSV 文件"""
        try:
            import pandas as pd
            
            data = self.db_manager.get_all_companies()
            df = pd.DataFrame(data)
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
            
            logger.info(f"数据已导出到: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"导出失败: {e}")
            return False


# ==================== 主程序 ====================

def main():
    """主函数"""
    # 1. 初始化数据库
    db_manager = DatabaseManager(db_type=DB_TYPE, db_path=DB_PATH)
    
    # 2. 初始化爬虫
    crawler = StarMarketCrawler(db_manager)
    
    # 3. 执行爬取
    success = crawler.run(use_akshare=True)
    
    if success:
        # 4. 导出数据
        exporter = DataExporter(db_manager)
        exporter.export_to_json("star_market_data.json")
        exporter.export_to_csv("star_market_data.csv")
        
        logger.info("任务执行成功!")
    else:
        logger.error("任务执行失败!")
    
    return success


if __name__ == "__main__":
    import pandas as pd  # 需要在导入部分添加
    main()
