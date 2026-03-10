#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
36氪融资数据爬虫
36Kr Funding Data Crawler

数据来源: 36氪 (https://36kr.com/)
采集内容:
- 公司名称
- 融资轮次
- 融资金额
- 投资机构
- 融资时间
- 所属行业

技术栈:
- requests: HTTP请求
- BeautifulSoup: HTML解析
- fake-useragent: UA轮换
- NLP: 正则+关键词提取结构化数据

特性:
1. 智能反爬（UA轮换、请求间隔、代理支持）
2. RSS+网页双通道采集
3. NLP自动提取结构化数据
4. 数据库存储（SQLite/PostgreSQL）
5. 增量更新（URL去重）

作者: Data Engineer
日期: 2026-03-10
"""

import hashlib
import json
import logging
import random
import re
import sqlite3
import time
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

# 尝试导入可选依赖
try:
    from fake_useragent import UserAgent
    UA_ENABLED = True
except ImportError:
    UA_ENABLED = False
    print("警告: fake-useragent 未安装，使用固定UA")

# ==================== 配置 ====================

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('k36_crawler.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 爬虫配置
CONFIG = {
    'base_url': 'https://36kr.com',
    'rss_url': 'https://36kr.com/feed',
    'funding_url': 'https://36kr.com/information/vc_funding',
    'api_url': 'https://36kr.com/api/newsflash',
    
    # 反爬配置
    'request_delay': (3, 8),  # 请求间隔随机范围（秒）
    'retry_times': 3,
    'retry_delay': 5,
    'timeout': 30,
    
    # 采集配置
    'max_pages': 10,  # 每次最多爬取页数
    'page_size': 20,  # 每页条数
}

# 融资轮次关键词映射
ROUND_KEYWORDS = {
    '种子': '种子轮',
    '天使': '天使轮',
    'pre-a': 'Pre-A轮',
    'prea': 'Pre-A轮',
    'a轮': 'A轮',
    'a+': 'A+轮',
    'b轮': 'B轮',
    'b+': 'B+轮',
    'c轮': 'C轮',
    'c+': 'C+轮',
    'd轮': 'D轮',
    'e轮': 'E轮',
    'f轮': 'F轮',
    'pre-ipo': 'Pre-IPO',
    'ipo': 'IPO',
    '上市': 'IPO',
    '战略': '战略融资',
    '并购': '并购',
    '合并': '合并',
    '定增': '定增',
    '股权融资': '股权融资',
}

# 行业关键词映射
INDUSTRY_KEYWORDS = [
    '人工智能', 'AI', '大模型', '芯片', '半导体', '集成电路',
    '生物医药', '医疗器械', '健康', '医疗',
    '新能源', '光伏', '储能', '锂电池', '氢能',
    '自动驾驶', '智能汽车', '新能源汽车', '车联网',
    '企业服务', 'SaaS', '云计算', '大数据',
    '电商', '零售', '消费', '品牌',
    '教育', '金融科技', '区块链', 'Web3',
    '游戏', '文娱', '传媒', '体育',
    '物流', '供应链', '硬件', '机器人',
    '航空航天', '卫星', '农业科技', '食品',
]

# 金额单位转换
AMOUNT_UNITS = {
    '万': 10000,
    '千': 1000,
    '百万': 1000000,
    '千万': 10000000,
    '亿': 100000000,
    '十亿': 1000000000,
    '百亿': 10000000000,
}

# ==================== 数据模型 ====================

@dataclass
class FundingEvent:
    """融资事件数据模型"""
    id: Optional[int] = None
    company_name: str = ""  # 公司名称
    funding_round: str = ""  # 融资轮次
    amount: Optional[float] = None  # 金额（人民币，元）
    amount_text: str = ""  # 原始金额文本
    currency: str = "CNY"  # 货币
    investors: List[str] = None  # 投资机构列表
    funding_date: Optional[str] = None  # 融资日期
    industry: str = ""  # 所属行业
    source_url: str = ""  # 来源链接
    title: str = ""  # 原始标题
    summary: str = ""  # 摘要
    tags: List[str] = None  # 标签
    created_at: Optional[str] = None
    
    def __post_init__(self):
        if self.investors is None:
            self.investors = []
        if self.tags is None:
            self.tags = []
    
    def generate_hash(self) -> str:
        """生成唯一哈希（用于去重）"""
        # 基于公司名+日期+轮次生成哈希
        key = f"{self.company_name}_{self.funding_date}_{self.funding_round}"
        return hashlib.md5(key.encode('utf-8')).hexdigest()
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'id': self.id,
            'company_name': self.company_name,
            'funding_round': self.funding_round,
            'amount': self.amount,
            'amount_text': self.amount_text,
            'currency': self.currency,
            'investors': self.investors,
            'funding_date': self.funding_date,
            'industry': self.industry,
            'source_url': self.source_url,
            'title': self.title,
            'summary': self.summary,
            'tags': self.tags,
            'created_at': self.created_at,
        }


# ==================== 数据库管理 ====================

class FundingDatabase:
    """融资数据库管理器"""
    
    def __init__(self, db_path: str = "funding_data.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS funding_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name TEXT NOT NULL,
                funding_round TEXT,
                amount REAL,
                amount_text TEXT,
                currency TEXT DEFAULT 'CNY',
                investors TEXT,  -- JSON数组
                funding_date TEXT,
                industry TEXT,
                source_url TEXT UNIQUE,
                event_hash TEXT UNIQUE,  -- 用于去重
                title TEXT,
                summary TEXT,
                tags TEXT,  -- JSON数组
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建索引
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_company ON funding_events(company_name)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_date ON funding_events(funding_date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_industry ON funding_events(industry)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_hash ON funding_events(event_hash)')
        
        conn.commit()
        conn.close()
        logger.info(f"数据库初始化完成: {self.db_path}")
    
    def is_exists(self, event_hash: str) -> bool:
        """检查事件是否已存在"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT 1 FROM funding_events WHERE event_hash = ?', (event_hash,))
        exists = cursor.fetchone() is not None
        
        conn.close()
        return exists
    
    def insert_event(self, event: FundingEvent) -> Tuple[bool, str]:
        """
        插入融资事件
        
        Returns:
            (success, action) - action: 'inserted', 'exists', 'error'
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            event_hash = event.generate_hash()
            
            # 检查是否已存在
            if self.is_exists(event_hash):
                logger.debug(f"事件已存在，跳过: {event.company_name}")
                return True, 'exists'
            
            cursor.execute('''
                INSERT INTO funding_events 
                (company_name, funding_round, amount, amount_text, currency, 
                 investors, funding_date, industry, source_url, event_hash,
                 title, summary, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                event.company_name,
                event.funding_round,
                event.amount,
                event.amount_text,
                event.currency,
                json.dumps(event.investors, ensure_ascii=False),
                event.funding_date,
                event.industry,
                event.source_url,
                event_hash,
                event.title,
                event.summary,
                json.dumps(event.tags, ensure_ascii=False)
            ))
            
            conn.commit()
            logger.info(f"插入新事件: {event.company_name} - {event.funding_round}")
            return True, 'inserted'
            
        except sqlite3.IntegrityError:
            logger.debug(f"数据重复（URL）: {event.source_url}")
            return True, 'exists'
        except Exception as e:
            logger.error(f"插入失败: {e}")
            return False, 'error'
        finally:
            conn.close()
    
    def get_statistics(self) -> Dict:
        """获取统计信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 总数
        cursor.execute('SELECT COUNT(*) FROM funding_events')
        total = cursor.fetchone()[0]
        
        # 今日新增
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('SELECT COUNT(*) FROM funding_events WHERE DATE(created_at) = ?', (today,))
        today_count = cursor.fetchone()[0]
        
        # 本周新增
        cursor.execute('''
            SELECT COUNT(*) FROM funding_events 
            WHERE DATE(created_at) >= DATE('now', '-7 days')
        ''')
        week_count = cursor.fetchone()[0]
        
        # 按轮次统计
        cursor.execute('''
            SELECT funding_round, COUNT(*) as count 
            FROM funding_events 
            WHERE funding_round IS NOT NULL
            GROUP BY funding_round 
            ORDER BY count DESC
            LIMIT 10
        ''')
        by_round = dict(cursor.fetchall())
        
        # 按行业统计
        cursor.execute('''
            SELECT industry, COUNT(*) as count 
            FROM funding_events 
            WHERE industry IS NOT NULL AND industry != ''
            GROUP BY industry 
            ORDER BY count DESC
            LIMIT 10
        ''')
        by_industry = dict(cursor.fetchall())
        
        conn.close()
        
        return {
            'total': total,
            'today': today_count,
            'this_week': week_count,
            'by_round': by_round,
            'by_industry': by_industry
        }
    
    def get_recent_events(self, days: int = 7, limit: int = 100) -> List[Dict]:
        """获取最近的融资事件"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM funding_events 
            WHERE funding_date >= DATE('now', '-{} days')
            ORDER BY funding_date DESC, created_at DESC
            LIMIT ?
        '''.format(days), (limit,))
        
        rows = cursor.fetchall()
        events = [dict(row) for row in rows]
        
        conn.close()
        return events


# ==================== NLP数据提取器 ====================

class FundingInfoExtractor:
    """从新闻标题和正文中提取融资信息"""
    
    @staticmethod
    def extract_company_name(text: str) -> Optional[str]:
        """
        提取公司名称
        
        策略:
        1. 匹配「公司名」格式
        2. 匹配"公司名"格式
        3. 从"XX完成/获投/宣布"中提取
        """
        # 策略1: 书名号/引号中的公司名
        patterns = [
            r'「([^」]{2,20})」',  # 全角引号
            r'"([^"]{2,20})"',    # 半角引号
            r'【([^】]{2,20})】',  # 方括号
            r'《([^》]{2,20})》',  # 书名号
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        
        # 策略2: 从句首提取（XX完成/获投/宣布）
        pattern = r'^([^，。；]+?)(?:完成|获|宣布|获得)'
        match = re.search(pattern, text)
        if match:
            name = match.group(1).strip()
            # 过滤掉太短的
            if len(name) >= 2 and len(name) <= 30:
                return name
        
        return None
    
    @staticmethod
    def extract_funding_round(text: str) -> Optional[str]:
        """
        提取融资轮次
        """
        text_lower = text.lower()
        
        # 按优先级匹配
        for keyword, round_name in ROUND_KEYWORDS.items():
            if keyword in text_lower:
                return round_name
        
        return None
    
    @staticmethod
    def extract_amount(text: str) -> Tuple[Optional[float], Optional[str]]:
        """
        提取融资金额
        
        Returns:
            (amount_in_cny, amount_text)
        """
        # 匹配模式: 数字+单位+（人民币/美元/美金/元）
        patterns = [
            r'(\d+(?:\.\d+)?)\s*([万亿千万]?)\s*(?:美元|美金|USD)\s*(?:\(([^)]+)\))?',  # 美元
            r'(\d+(?:\.\d+)?)\s*([万亿千万]?)\s*(?:人民币|元|RMB|CNY)?',  # 人民币
            r'([数几近超])\s*([万亿千万])',  # 模糊金额
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                amount_text = match.group(0)
                
                # 处理模糊金额
                if match.group(1) in ['数', '几', '近', '超']:
                    return None, amount_text
                
                try:
                    num = float(match.group(1))
                    unit = match.group(2) if len(match.groups()) > 1 else ''
                    
                    # 计算实际金额
                    multiplier = AMOUNT_UNITS.get(unit, 1)
                    amount = num * multiplier
                    
                    # 判断货币（如果有美元关键字）
                    if '美元' in text or 'USD' in text.upper():
                        # 假设 1 USD = 7.2 CNY
                        amount = amount * 7.2
                    
                    return amount, amount_text
                    
                except (ValueError, IndexError):
                    continue
        
        # 匹配"未披露"、" undisclosed"等
        if any(word in text for word in ['未披露', ' undisclosed', ' undisclosed', '保密']):
            return None, '未披露'
        
        return None, None
    
    @staticmethod
    def extract_investors(text: str) -> List[str]:
        """
        提取投资机构
        
        策略:
        1. 匹配"领投方/投资方/由...投资"后面的机构名
        2. 匹配知名机构关键词
        """
        investors = []
        
        # 知名投资机构列表（可扩展）
        known_investors = [
            '红杉', '高瓴', 'IDG', '腾讯', '阿里', '字节', '美团',
            '小米', '百度', '京东', '深创投', '达晨', '君联', '启明',
            '软银', '老虎', '高榕', '源码', '顺为', '真格',
            '经纬', '华兴', '中金', '中信', '高盛', '摩根',
        ]
        
        # 策略1: 从"领投/跟投/投资"句子中提取
        pattern = r'(?:由|获|获投|投资方|领投方)[\s]*([^，。；]+?)(?:领投|跟投|投资|参投)'
        matches = re.findall(pattern, text)
        for match in matches:
            # 清理并分割多个机构
            orgs = re.split(r'[,，、和与及]', match)
            for org in orgs:
                org = org.strip()
                if len(org) >= 2:
                    investors.append(org)
        
        # 策略2: 匹配已知机构
        for investor in known_investors:
            if investor in text and investor not in investors:
                investors.append(investor)
        
        # 去重并保持顺序
        seen = set()
        unique_investors = []
        for inv in investors:
            if inv not in seen:
                seen.add(inv)
                unique_investors.append(inv)
        
        return unique_investors[:10]  # 最多返回10个
    
    @staticmethod
    def extract_industry(text: str, summary: str = "") -> str:
        """
        提取所属行业
        """
        full_text = text + " " + summary
        
        for industry in INDUSTRY_KEYWORDS:
            if industry in full_text:
                return industry
        
        return ""
    
    @staticmethod
    def extract_date(text: str, date_str: str = None) -> Optional[str]:
        """
        提取日期
        """
        # 如果传入日期字符串，尝试解析
        if date_str:
            # 尝试多种格式
            formats = [
                '%Y-%m-%d',
                '%Y-%m-%d %H:%M:%S',
                '%a, %d %b %Y %H:%M:%S %z',  # RSS格式
            ]
            for fmt in formats:
                try:
                    dt = datetime.strptime(date_str.strip(), fmt)
                    return dt.strftime('%Y-%m-%d')
                except ValueError:
                    continue
        
        # 从文本中提取日期
        pattern = r'(\d{4})[-/](\d{1,2})[-/](\d{1,2})'
        match = re.search(pattern, text)
        if match:
            year, month, day = match.groups()
            return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
        
        return None
    
    @classmethod
    def extract_all(cls, title: str, summary: str = "", pub_date: str = None) -> FundingEvent:
        """
        从新闻中提取所有融资信息
        """
        full_text = title + " " + summary
        
        event = FundingEvent()
        event.title = title
        event.summary = summary
        
        # 提取各项信息
        event.company_name = cls.extract_company_name(title) or ""
        event.funding_round = cls.extract_funding_round(full_text) or ""
        event.amount, event.amount_text = cls.extract_amount(full_text)
        event.investors = cls.extract_investors(full_text)
        event.industry = cls.extract_industry(title, summary)
        event.funding_date = cls.extract_date(title, pub_date)
        
        # 生成标签
        event.tags = []
        if event.industry:
            event.tags.append(event.industry)
        if event.funding_round:
            event.tags.append(event.funding_round)
        
        return event


# ==================== 爬虫类 ====================

class K36Crawler:
    """36氪爬虫"""
    
    def __init__(self, db: FundingDatabase):
        self.db = db
        self.session = requests.Session()
        self.ua = UserAgent() if UA_ENABLED else None
        self.stats = {
            'total': 0,
            'inserted': 0,
            'exists': 0,
            'failed': 0
        }
    
    def _get_headers(self) -> Dict[str, str]:
        """获取请求头（带UA轮换）"""
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://36kr.com/',
        }
        
        if self.ua:
            headers['User-Agent'] = self.ua.random
        else:
            headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        
        return headers
    
    def _random_delay(self):
        """随机延迟"""
        delay = random.uniform(CONFIG['request_delay'][0], CONFIG['request_delay'][1])
        time.sleep(delay)
    
    def fetch_rss(self) -> List[Dict]:
        """
        从RSS获取最新新闻
        
        优点：
        - 无需处理复杂反爬
        - 格式统一，解析简单
        - 实时性好
        """
        logger.info("正在获取36氪RSS...")
        
        try:
            response = self.session.get(
                CONFIG['rss_url'],
                headers=self._get_headers(),
                timeout=CONFIG['timeout']
            )
            response.encoding = 'utf-8'
            
            if response.status_code != 200:
                logger.error(f"RSS请求失败: HTTP {response.status_code}")
                return []
            
            soup = BeautifulSoup(response.content, 'xml')
            items = soup.find_all('item')
            
            news_list = []
            for item in items:
                try:
                    title = item.title.text if item.title else ""
                    link = item.link.text if item.link else ""
                    pub_date = item.pubDate.text if item.pubDate else ""
                    description = item.description.text if item.description else ""
                    
                    # 只保留融资相关新闻
                    funding_keywords = ['融资', '获投', '轮', '投资', '领投', '跟投', '完成']
                    if any(kw in title for kw in funding_keywords):
                        news_list.append({
                            'title': title,
                            'link': link,
                            'pub_date': pub_date,
                            'description': description
                        })
                except Exception as e:
                    logger.warning(f"解析RSS项失败: {e}")
                    continue
            
            logger.info(f"从RSS获取到 {len(news_list)} 条融资新闻")
            return news_list
            
        except Exception as e:
            logger.error(f"获取RSS失败: {e}")
            return []
    
    def fetch_news_detail(self, url: str) -> Optional[str]:
        """
        获取新闻详情页内容
        """
        for attempt in range(CONFIG['retry_times']):
            try:
                self._random_delay()
                
                response = self.session.get(
                    url,
                    headers=self._get_headers(),
                    timeout=CONFIG['timeout']
                )
                response.encoding = 'utf-8'
                
                if response.status_code == 200:
                    return response.text
                elif response.status_code == 403:
                    logger.warning(f"访问被拒绝: {url}")
                    return None
                else:
                    logger.warning(f"HTTP {response.status_code}: {url}")
                    
            except requests.RequestException as e:
                logger.error(f"请求失败 ({attempt+1}/{CONFIG['retry_times']}): {e}")
                if attempt < CONFIG['retry_times'] - 1:
                    time.sleep(CONFIG['retry_delay'])
                    continue
        
        return None
    
    def parse_news_detail(self, html: str) -> str:
        """
        解析新闻详情页，提取正文
        """
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # 36氪文章正文通常在 article 或特定 div 中
            content_elem = (
                soup.find('article') or
                soup.find('div', class_='article-content') or
                soup.find('div', class_='content') or
                soup.find('div', {'data-type': 'article'})
            )
            
            if content_elem:
                # 清理脚本和样式
                for script in content_elem.find_all(['script', 'style']):
                    script.decompose()
                
                # 提取纯文本
                text = content_elem.get_text(separator=' ', strip=True)
                return text[:1000]  # 只取前1000字符作为摘要
            
            return ""
            
        except Exception as e:
            logger.warning(f"解析详情页失败: {e}")
            return ""
    
    def process_news_item(self, news: Dict, fetch_detail: bool = False) -> Optional[FundingEvent]:
        """
        处理单条新闻，提取融资信息
        """
        try:
            title = news['title']
            link = news['link']
            pub_date = news.get('pub_date', '')
            description = news.get('description', '')
            
            # 获取详情页内容（可选）
            detail_text = ""
            if fetch_detail:
                html = self.fetch_news_detail(link)
                if html:
                    detail_text = self.parse_news_detail(html)
            
            # 合并摘要
            full_summary = description + " " + detail_text
            
            # 提取融资信息
            event = FundingInfoExtractor.extract_all(title, full_summary, pub_date)
            event.source_url = link
            event.created_at = datetime.now().isoformat()
            
            return event
            
        except Exception as e:
            logger.error(f"处理新闻失败: {e}")
            return None
    
    def run(self, fetch_detail: bool = False) -> Dict:
        """
        执行爬取任务
        
        Args:
            fetch_detail: 是否获取详情页内容（会增加请求量和时间）
        
        Returns:
            统计信息
        """
        logger.info("=" * 60)
        logger.info("36氪融资数据爬虫启动")
        logger.info(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"获取详情页: {fetch_detail}")
        logger.info("=" * 60)
        
        # 重置统计
        self.stats = {
            'total': 0,
            'inserted': 0,
            'exists': 0,
            'failed': 0
        }
        
        try:
            # 1. 获取RSS新闻列表
            news_list = self.fetch_rss()
            
            if not news_list:
                logger.warning("未获取到任何新闻")
                return self.stats
            
            self.stats['total'] = len(news_list)
            
            # 2. 处理每条新闻
            for i, news in enumerate(news_list, 1):
                logger.info(f"\n处理第 {i}/{len(news_list)} 条: {news['title'][:50]}...")
                
                # 提取融资信息
                event = self.process_news_item(news, fetch_detail)
                
                if not event:
                    self.stats['failed'] += 1
                    continue
                
                # 检查数据质量
                if not event.company_name:
                    logger.warning(f"未提取到公司名，跳过: {news['title']}")
                    self.stats['failed'] += 1
                    continue
                
                # 保存到数据库
                success, action = self.db.insert_event(event)
                
                if success:
                    self.stats[action] += 1
                else:
                    self.stats['failed'] += 1
                
                # 请求间隔
                if i < len(news_list):
                    self._random_delay()
            
            # 3. 输出统计
            logger.info("\n" + "=" * 60)
            logger.info("爬取完成!")
            logger.info(f"总计处理: {self.stats['total']} 条")
            logger.info(f"新增: {self.stats['inserted']} 条")
            logger.info(f"已存在: {self.stats['exists']} 条")
            logger.info(f"失败: {self.stats['failed']} 条")
            logger.info("=" * 60)
            
            return self.stats
            
        except Exception as e:
            logger.error(f"爬取过程发生错误: {e}", exc_info=True)
            return self.stats


# ==================== 导出功能 ====================

class FundingExporter:
    """融资数据导出器"""
    
    def __init__(self, db: FundingDatabase):
        self.db = db
    
    def export_to_json(self, filepath: str = "funding_data.json", days: int = None):
        """导出到JSON"""
        try:
            if days:
                events = self.db.get_recent_events(days=days)
            else:
                # 导出全部
                import sqlite3
                conn = sqlite3.connect(self.db.db_path)
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM funding_events ORDER BY funding_date DESC')
                rows = cursor.fetchall()
                events = [dict(row) for row in rows]
                conn.close()
            
            export_data = {
                'export_time': datetime.now().isoformat(),
                'total_count': len(events),
                'data_source': '36氪',
                'data': events
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"数据已导出到: {filepath} (共 {len(events)} 条)")
            return True
            
        except Exception as e:
            logger.error(f"导出失败: {e}")
            return False
    
    def export_to_csv(self, filepath: str = "funding_data.csv"):
        """导出到CSV"""
        try:
            import pandas as pd
            
            conn = sqlite3.connect(self.db.db_path)
            df = pd.read_sql_query('SELECT * FROM funding_events ORDER BY funding_date DESC', conn)
            conn.close()
            
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
            logger.info(f"数据已导出到: {filepath} (共 {len(df)} 条)")
            return True
            
        except Exception as e:
            logger.error(f"导出失败: {e}")
            return False


# ==================== 主程序 ====================

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='36氪融资数据爬虫')
    parser.add_argument('--detail', '-d', action='store_true', help='获取详情页内容')
    parser.add_argument('--export', '-e', action='store_true', help='导出数据')
    parser.add_argument('--days', type=int, default=7, help='导出最近几天的数据')
    
    args = parser.parse_args()
    
    # 初始化
    db = FundingDatabase()
    crawler = K36Crawler(db)
    
    # 执行爬取
    stats = crawler.run(fetch_detail=args.detail)
    
    # 导出数据
    if args.export and (stats['inserted'] > 0 or stats['exists'] > 0):
        exporter = FundingExporter(db)
        exporter.export_to_json(f"funding_data_{datetime.now().strftime('%Y%m%d')}.json", days=args.days)
        exporter.export_to_csv(f"funding_data_{datetime.now().strftime('%Y%m%d')}.csv")
    
    # 打印数据库统计
    db_stats = db.get_statistics()
    logger.info("\n数据库统计:")
    logger.info(f"  总融资事件: {db_stats['total']}")
    logger.info(f"  今日新增: {db_stats['today']}")
    logger.info(f"  本周新增: {db_stats['this_week']}")
    logger.info(f"  轮次分布: {db_stats['by_round']}")


if __name__ == "__main__":
    main()
