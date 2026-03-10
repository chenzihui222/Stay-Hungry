#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
国务院政策文件爬虫
State Council Policy Document Crawler

数据来源: 国务院政策文件库 (https://www.gov.cn/zhengce/)

采集字段:
- 政策名称 (title)
- 发布时间 (publish_date)
- 发布机构 (source)
- 政策摘要 (summary)
- 政策链接 (url)
- 关键词/标签 (tags)
- 政策正文内容 (content) - 可选

特性:
1. 支持增量更新（基于政策链接去重）
2. 每日自动运行
3. 智能摘要提取
4. 数据库存储（SQLite/PostgreSQL）
5. 完整的日志记录
6. 失败重试机制

作者: Data Engineer
日期: 2026-03-10
"""

import hashlib
import json
import logging
import re
import sqlite3
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, String, Text, DateTime, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ==================== 配置 ====================

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('policy_crawler.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 数据库配置
DB_TYPE = "sqlite"
DB_PATH = "policies.db"

# 请求配置
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Referer': 'https://www.gov.cn/',
}

# 爬虫配置
CONFIG = {
    'base_url': 'https://www.gov.cn/zhengce/',
    'search_url': 'http://sousuo.gov.cn/column/30412/0.htm',  # 政策文件库搜索页
    'list_url': 'http://sousuo.gov.cn/list.htm',  # 列表页
    'page_size': 20,  # 每页条数
    'max_pages': 5,  # 每次爬取最大页数（控制频率）
    'retry_times': 3,  # 失败重试次数
    'retry_delay': 2,  # 重试间隔（秒）
    'request_delay': 1,  # 请求间隔（秒）
}

# ==================== 数据模型 ====================

Base = declarative_base()


class PolicyDocument(Base):
    """政策文件数据库模型"""
    __tablename__ = 'policies'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(500), nullable=False, comment='政策名称')
    publish_date = Column(String(20), index=True, comment='发布时间')
    source = Column(String(200), comment='发布机构')
    summary = Column(Text, comment='政策摘要')
    url = Column(String(500), unique=True, nullable=False, index=True, comment='政策链接')
    url_hash = Column(String(64), unique=True, index=True, comment='URL哈希（用于去重）')
    content = Column(Text, comment='政策正文（可选）')
    tags = Column(String(500), comment='关键词标签，JSON格式')
    is_valid = Column(Boolean, default=True, comment='是否有效')
    crawl_status = Column(String(20), default='pending', comment='爬取状态')
    created_at = Column(DateTime, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    last_crawled_at = Column(DateTime, comment='最后爬取时间')
    
    def __repr__(self):
        return f"<PolicyDocument({self.title[:30]}...)>"
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'id': self.id,
            'title': self.title,
            'publish_date': self.publish_date,
            'source': self.source,
            'summary': self.summary,
            'url': self.url,
            'tags': json.loads(self.tags) if self.tags else [],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


@dataclass
class PolicyData:
    """政策数据 dataclass"""
    title: str
    url: str
    publish_date: Optional[str] = None
    source: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
    
    def generate_hash(self) -> str:
        """生成URL哈希用于去重"""
        return hashlib.md5(self.url.encode('utf-8')).hexdigest()


# ==================== 数据库操作类 ====================

class PolicyDatabase:
    """政策数据库管理器"""
    
    def __init__(self, db_type: str = "sqlite", db_path: str = "policies.db"):
        self.db_type = db_type
        self.db_path = db_path
        self.engine = None
        self.Session = None
        self._init_db()
    
    def _init_db(self):
        """初始化数据库"""
        try:
            if self.db_type == "sqlite":
                self.engine = create_engine(
                    f'sqlite:///{self.db_path}',
                    echo=False,
                    connect_args={'check_same_thread': False}
                )
            else:
                raise ValueError(f"不支持的数据库类型: {self.db_type}")
            
            Base.metadata.create_all(self.engine)
            self.Session = sessionmaker(bind=self.engine)
            logger.info(f"数据库初始化成功: {self.db_type}")
            
        except Exception as e:
            logger.error(f"数据库初始化失败: {e}")
            raise
    
    def get_session(self):
        """获取数据库会话"""
        return self.Session()
    
    def is_url_exists(self, url: str) -> bool:
        """检查URL是否已存在"""
        session = self.get_session()
        try:
            url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()
            exists = session.query(PolicyDocument).filter_by(url_hash=url_hash).first()
            return exists is not None
        finally:
            session.close()
    
    def insert_or_update(self, policy: PolicyData) -> Tuple[bool, str]:
        """
        插入或更新政策数据
        
        Returns:
            (success, action) - action: 'inserted', 'updated', 'skipped'
        """
        session = self.get_session()
        try:
            url_hash = policy.generate_hash()
            
            # 检查是否已存在
            existing = session.query(PolicyDocument).filter_by(url_hash=url_hash).first()
            
            if existing:
                # 检查是否需要更新
                if (existing.title != policy.title or 
                    existing.summary != policy.summary or
                    existing.source != policy.source):
                    
                    existing.title = policy.title
                    existing.source = policy.source
                    existing.summary = policy.summary
                    existing.content = policy.content
                    existing.tags = json.dumps(policy.tags, ensure_ascii=False) if policy.tags else None
                    existing.updated_at = datetime.now()
                    existing.last_crawled_at = datetime.now()
                    
                    session.commit()
                    logger.info(f"更新政策: {policy.title[:50]}...")
                    return True, 'updated'
                else:
                    # 数据未变化，跳过
                    existing.last_crawled_at = datetime.now()
                    session.commit()
                    return True, 'skipped'
            else:
                # 插入新记录
                new_policy = PolicyDocument(
                    title=policy.title,
                    publish_date=policy.publish_date,
                    source=policy.source,
                    summary=policy.summary,
                    url=policy.url,
                    url_hash=url_hash,
                    content=policy.content,
                    tags=json.dumps(policy.tags, ensure_ascii=False) if policy.tags else None,
                    crawl_status='success',
                    last_crawled_at=datetime.now()
                )
                session.add(new_policy)
                session.commit()
                logger.info(f"插入新政策: {policy.title[:50]}...")
                return True, 'inserted'
                
        except Exception as e:
            session.rollback()
            logger.error(f"数据库操作失败: {e}")
            return False, 'error'
        finally:
            session.close()
    
    def get_statistics(self) -> Dict:
        """获取统计信息"""
        session = self.get_session()
        try:
            total = session.query(PolicyDocument).count()
            today = datetime.now().strftime('%Y-%m-%d')
            today_count = session.query(PolicyDocument).filter(
                PolicyDocument.created_at >= today
            ).count()
            
            # 按来源统计
            source_stats = session.query(
                PolicyDocument.source,
                Integer.count(PolicyDocument.id)
            ).group_by(PolicyDocument.source).all()
            
            return {
                'total': total,
                'today': today_count,
                'by_source': dict(source_stats)
            }
        finally:
            session.close()
    
    def get_recent_policies(self, days: int = 7, limit: int = 50) -> List[Dict]:
        """获取最近的政策"""
        session = self.get_session()
        try:
            start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            policies = session.query(PolicyDocument).filter(
                PolicyDocument.publish_date >= start_date
            ).order_by(PolicyDocument.publish_date.desc()).limit(limit).all()
            
            return [p.to_dict() for p in policies]
        finally:
            session.close()


# ==================== 爬虫类 ====================

class PolicyCrawler:
    """国务院政策爬虫"""
    
    def __init__(self, db: PolicyDatabase):
        self.db = db
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.stats = {
            'total': 0,
            'inserted': 0,
            'updated': 0,
            'skipped': 0,
            'failed': 0
        }
    
    def fetch_page(self, page: int = 0) -> Optional[str]:
        """
        获取政策列表页
        
        Args:
            page: 页码，从0开始
        
        Returns:
            HTML 内容或 None
        """
        url = CONFIG['search_url']
        params = {
            'page': page,
            'sort': 'time',  # 按时间排序
        }
        
        for attempt in range(CONFIG['retry_times']):
            try:
                logger.info(f"获取第 {page + 1} 页，尝试 {attempt + 1}/{CONFIG['retry_times']}")
                
                response = self.session.get(
                    url,
                    params=params,
                    timeout=30,
                    allow_redirects=True
                )
                response.encoding = 'utf-8'
                
                if response.status_code == 200:
                    logger.info(f"成功获取第 {page + 1} 页")
                    return response.text
                else:
                    logger.warning(f"HTTP {response.status_code}")
                    
            except requests.RequestException as e:
                logger.error(f"请求失败: {e}")
                if attempt < CONFIG['retry_times'] - 1:
                    time.sleep(CONFIG['retry_delay'])
                    continue
        
        return None
    
    def parse_list_page(self, html: str) -> List[PolicyData]:
        """
        解析政策列表页
        
        Args:
            html: 页面HTML
        
        Returns:
            政策数据列表
        """
        policies = []
        soup = BeautifulSoup(html, 'html.parser')
        
        # 查找政策列表项
        # 国务院政策库通常使用以下选择器
        list_items = soup.select('.list li') or soup.select('.result-list li') or soup.select('.news-list li')
        
        if not list_items:
            # 尝试其他可能的选择器
            list_items = soup.find_all('li', class_=lambda x: x and ('list' in x or 'item' in x))
        
        logger.info(f"找到 {len(list_items)} 个列表项")
        
        for item in list_items:
            try:
                # 提取链接和标题
                link_elem = item.find('a')
                if not link_elem:
                    continue
                
                title = link_elem.get_text(strip=True)
                href = link_elem.get('href', '')
                
                if not title or not href:
                    continue
                
                # 处理相对URL
                if href.startswith('/'):
                    url = urljoin('https://www.gov.cn', href)
                elif href.startswith('http'):
                    url = href
                else:
                    url = urljoin(CONFIG['base_url'], href)
                
                # 提取日期
                date_elem = item.find('span', class_='date') or item.find('span', class_='time')
                publish_date = None
                if date_elem:
                    date_text = date_elem.get_text(strip=True)
                    # 提取日期格式：2026-03-10 或 2026年03月10日
                    date_match = re.search(r'(\d{4})[-年](\d{2})[-月](\d{2})', date_text)
                    if date_match:
                        publish_date = f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}"
                
                # 提取来源
                source_elem = item.find('span', class_='source') or item.find('span', class_='from')
                source = None
                if source_elem:
                    source = source_elem.get_text(strip=True)
                
                # 提取摘要
                summary_elem = item.find('p', class_='summary') or item.find('div', class_='content')
                summary = None
                if summary_elem:
                    summary = summary_elem.get_text(strip=True)
                
                policy = PolicyData(
                    title=title,
                    url=url,
                    publish_date=publish_date,
                    source=source,
                    summary=summary
                )
                
                policies.append(policy)
                
            except Exception as e:
                logger.warning(f"解析列表项失败: {e}")
                continue
        
        return policies
    
    def fetch_policy_detail(self, url: str) -> Optional[str]:
        """获取政策详情页内容"""
        for attempt in range(CONFIG['retry_times']):
            try:
                response = self.session.get(url, timeout=30)
                response.encoding = 'utf-8'
                
                if response.status_code == 200:
                    return response.text
                    
            except requests.RequestException as e:
                logger.error(f"获取详情页失败 {url}: {e}")
                if attempt < CONFIG['retry_times'] - 1:
                    time.sleep(CONFIG['retry_delay'])
                    continue
        
        return None
    
    def parse_policy_detail(self, html: str, policy: PolicyData) -> PolicyData:
        """
        解析政策详情页，提取更多信息
        
        Args:
            html: 详情页HTML
            policy: 基础政策数据
        
        Returns:
            补充后的政策数据
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        try:
            # 提取发布机构（如果在列表页未获取到）
            if not policy.source:
                source_elem = soup.find('span', class_='source') or \
                             soup.find('span', string=re.compile('来源')) or \
                             soup.find('meta', attrs={'name': 'source'})
                if source_elem:
                    if source_elem.name == 'meta':
                        policy.source = source_elem.get('content', '').strip()
                    else:
                        policy.source = source_elem.get_text(strip=True).replace('来源：', '').strip()
            
            # 提取发布时间（如果在列表页未获取到）
            if not policy.publish_date:
                date_elem = soup.find('span', class_='date') or \
                           soup.find('span', string=re.compile('发布时间')) or \
                           soup.find('meta', attrs={'name': 'publishdate'})
                if date_elem:
                    if date_elem.name == 'meta':
                        date_text = date_elem.get('content', '')
                    else:
                        date_text = date_elem.get_text(strip=True)
                    
                    date_match = re.search(r'(\d{4})[-年](\d{2})[-月](\d{2})', date_text)
                    if date_match:
                        policy.publish_date = f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}"
            
            # 提取正文内容
            content_elem = soup.find('div', class_='content-detail') or \
                          soup.find('div', class_='main-content') or \
                          soup.find('div', id='content')
            
            if content_elem:
                # 清理HTML标签
                for script in content_elem.find_all(['script', 'style']):
                    script.decompose()
                
                policy.content = content_elem.get_text(separator='\n', strip=True)
                
                # 提取摘要（如果列表页未获取到）
                if not policy.summary and policy.content:
                    # 取前200字符作为摘要
                    policy.summary = policy.content[:200] + '...' if len(policy.content) > 200 else policy.content
            
            # 提取关键词标签
            tags_elem = soup.find('div', class_='tags') or soup.find('meta', attrs={'name': 'keywords'})
            if tags_elem:
                if tags_elem.name == 'meta':
                    keywords = tags_elem.get('content', '')
                    policy.tags = [t.strip() for t in keywords.split(',') if t.strip()]
                else:
                    tags = tags_elem.find_all('a') or tags_elem.find_all('span')
                    policy.tags = [t.get_text(strip=True) for t in tags]
            
        except Exception as e:
            logger.warning(f"解析详情页失败: {e}")
        
        return policy
    
    def crawl_page(self, page: int, fetch_detail: bool = False) -> List[PolicyData]:
        """
        爬取单页数据
        
        Args:
            page: 页码
            fetch_detail: 是否获取详情页
        
        Returns:
            政策数据列表
        """
        html = self.fetch_page(page)
        if not html:
            return []
        
        policies = self.parse_list_page(html)
        
        if fetch_detail:
            # 获取详情页补充信息
            for policy in policies:
                if not self.db.is_url_exists(policy.url):
                    # 只有新数据才获取详情
                    detail_html = self.fetch_policy_detail(policy.url)
                    if detail_html:
                        policy = self.parse_policy_detail(detail_html, policy)
                    time.sleep(CONFIG['request_delay'])  #  polite delay
        
        return policies
    
    def run(self, max_pages: int = None, fetch_detail: bool = False) -> Dict:
        """
        执行爬取任务
        
        Args:
            max_pages: 最大爬取页数，None则使用配置
            fetch_detail: 是否获取详情页内容
        
        Returns:
            统计信息
        """
        max_pages = max_pages or CONFIG['max_pages']
        
        logger.info("=" * 60)
        logger.info("国务院政策爬虫启动")
        logger.info(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"计划爬取: {max_pages} 页")
        logger.info("=" * 60)
        
        # 重置统计
        self.stats = {
            'total': 0,
            'inserted': 0,
            'updated': 0,
            'skipped': 0,
            'failed': 0
        }
        
        try:
            for page in range(max_pages):
                logger.info(f"\n正在爬取第 {page + 1}/{max_pages} 页...")
                
                policies = self.crawl_page(page, fetch_detail)
                
                if not policies:
                    logger.warning(f"第 {page + 1} 页无数据，可能已到达末尾")
                    break
                
                self.stats['total'] += len(policies)
                
                # 保存到数据库
                for policy in policies:
                    success, action = self.db.insert_or_update(policy)
                    if success:
                        self.stats[action] += 1
                    else:
                        self.stats['failed'] += 1
                
                logger.info(f"第 {page + 1} 页完成: 获取 {len(policies)} 条")
                
                # 请求间隔
                if page < max_pages - 1:
                    time.sleep(CONFIG['request_delay'])
            
            # 输出统计
            logger.info("\n" + "=" * 60)
            logger.info("爬取完成!")
            logger.info(f"总计获取: {self.stats['total']} 条")
            logger.info(f"新增: {self.stats['inserted']} 条")
            logger.info(f"更新: {self.stats['updated']} 条")
            logger.info(f"跳过(重复): {self.stats['skipped']} 条")
            logger.info(f"失败: {self.stats['failed']} 条")
            logger.info("=" * 60)
            
            return self.stats
            
        except Exception as e:
            logger.error(f"爬取过程发生错误: {e}", exc_info=True)
            return self.stats


# ==================== 导出功能 ====================

class PolicyExporter:
    """政策数据导出器"""
    
    def __init__(self, db: PolicyDatabase):
        self.db = db
    
    def export_to_json(self, filepath: str = "policies.json", days: int = None) -> bool:
        """导出到 JSON"""
        try:
            if days:
                data = self.db.get_recent_policies(days=days)
            else:
                # 导出所有数据
                import sqlite3
                conn = sqlite3.connect(self.db.db_path)
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM policies ORDER BY publish_date DESC')
                rows = cursor.fetchall()
                data = [dict(row) for row in rows]
                conn.close()
            
            export_data = {
                'export_time': datetime.now().isoformat(),
                'total_count': len(data),
                'data_source': '国务院政策文件库',
                'url': 'https://www.gov.cn/zhengce/',
                'data': data
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"数据已导出到: {filepath} (共 {len(data)} 条)")
            return True
            
        except Exception as e:
            logger.error(f"导出失败: {e}")
            return False
    
    def export_to_csv(self, filepath: str = "policies.csv") -> bool:
        """导出到 CSV"""
        try:
            import pandas as pd
            
            conn = sqlite3.connect(self.db.db_path)
            df = pd.read_sql_query('SELECT * FROM policies ORDER BY publish_date DESC', conn)
            conn.close()
            
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
            logger.info(f"数据已导出到: {filepath} (共 {len(df)} 条)")
            return True
            
        except Exception as e:
            logger.error(f"导出失败: {e}")
            return False


# ==================== 定时任务 ====================

def run_daily_update():
    """每日更新任务"""
    logger.info("\n" + "=" * 60)
    logger.info("执行每日政策更新...")
    logger.info("=" * 60)
    
    # 初始化
    db = PolicyDatabase(db_type=DB_TYPE, db_path=DB_PATH)
    crawler = PolicyCrawler(db)
    
    # 执行爬取（只获取列表，不获取详情以加快速度）
    stats = crawler.run(max_pages=3, fetch_detail=False)
    
    # 导出数据
    if stats['total'] > 0:
        exporter = PolicyExporter(db)
        exporter.export_to_json("policies_daily.json")
        exporter.export_to_csv("policies_daily.csv")
    
    logger.info("每日更新完成!")
    return stats


# ==================== 主程序 ====================

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='国务院政策文件爬虫')
    parser.add_argument('--pages', '-p', type=int, default=5, help='爬取页数')
    parser.add_argument('--detail', '-d', action='store_true', help='获取详情页内容')
    parser.add_argument('--export', '-e', action='store_true', help='导出数据')
    parser.add_argument('--daily', action='store_true', help='执行每日更新模式')
    
    args = parser.parse_args()
    
    if args.daily:
        # 每日更新模式
        run_daily_update()
    else:
        # 手动运行模式
        db = PolicyDatabase(db_type=DB_TYPE, db_path=DB_PATH)
        crawler = PolicyCrawler(db)
        
        # 执行爬取
        stats = crawler.run(max_pages=args.pages, fetch_detail=args.detail)
        
        # 导出数据
        if args.export and stats['total'] > 0:
            exporter = PolicyExporter(db)
            exporter.export_to_json()
            exporter.export_to_csv()
        
        # 打印统计
        db_stats = db.get_statistics()
        logger.info("\n数据库统计:")
        logger.info(f"  总政策数: {db_stats['total']}")
        logger.info(f"  今日新增: {db_stats['today']}")


if __name__ == "__main__":
    main()
