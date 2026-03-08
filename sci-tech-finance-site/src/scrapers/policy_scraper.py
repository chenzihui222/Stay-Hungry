#!/usr/bin/env python3
"""
政策数据抓取器
数据源：国务院 / 证监会 / 科技部
"""

import re
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional
import requests
from bs4 import BeautifulSoup

from .base_scraper import BaseScraper, DataItem


class PolicyScraper(BaseScraper):
    """政策数据抓取器"""
    
    # 数据源配置
    SOURCES = {
        'gov_cn': {
            'name': '中国政府网',
            'base_url': 'http://www.gov.cn',
            'search_keywords': ['科技金融', '科创板', '创业投资', '科技创新'],
            'enabled': True
        },
        'csrc': {
            'name': '中国证监会',
            'base_url': 'http://www.csrc.gov.cn',
            'search_keywords': ['科创板', '科技金融', '上市公司', '信息披露'],
            'enabled': True
        },
        'most': {
            'name': '科学技术部',
            'base_url': 'https://www.most.gov.cn',
            'search_keywords': ['科技成果转化', '科技金融', '创新创业', '科技企业'],
            'enabled': True
        }
    }
    
    def __init__(self, data_dir: Path):
        super().__init__(data_dir)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def scrape(self) -> List[DataItem]:
        """执行政策数据抓取"""
        items = []
        
        # 1. 抓取国务院政策
        if self.SOURCES['gov_cn']['enabled']:
            items.extend(self._scrape_gov_cn())
        
        # 2. 抓取证监会政策
        if self.SOURCES['csrc']['enabled']:
            items.extend(self._scrape_csrc())
        
        # 3. 抓取科技部政策
        if self.SOURCES['most']['enabled']:
            items.extend(self._scrape_most())
        
        return items
    
    def _scrape_gov_cn(self) -> List[DataItem]:
        """抓取国务院政策"""
        items = []
        
        try:
            self.logger.info("开始抓取国务院政策...")
            
            # 国务院政策文件库
            url = 'http://www.gov.cn/zhengce/zhengceku/search.htm?q=科技金融'
            response = self.session.get(url, timeout=30)
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找政策列表
            policy_list = soup.find_all('div', class_='result') or soup.find_all('li', class_='item')
            
            for policy in policy_list[:15]:
                try:
                    # 提取标题
                    title_elem = policy.find('a')
                    title = title_elem.get_text(strip=True) if title_elem else ''
                    link = title_elem.get('href', '') if title_elem else ''
                    
                    if not title or not self._is_relevant_policy(title):
                        continue
                    
                    # 提取日期
                    date_elem = policy.find('span', class_='time') or policy.find('span', class_='date')
                    date_str = date_elem.get_text(strip=True) if date_elem else self.today
                    date_str = self._normalize_date(date_str)
                    
                    # 提取摘要
                    summary_elem = policy.find('p', class_='summary') or policy.find('div', class_='content')
                    summary = summary_elem.get_text(strip=True) if summary_elem else title
                    
                    content = f"""
                    政策标题: {title}
                    发布机构: 国务院
                    发布日期: {date_str}
                    政策摘要: {summary}
                    """.strip()
                    
                    item = DataItem(
                        date=date_str,
                        title=title[:100],
                        type='policy',
                        content=content,
                        source='国务院',
                        url=str(link) if str(link).startswith('http') else f'http://www.gov.cn{link}',
                        tags=['政策', '国务院', '科技金融'],
                        metadata={
                            'policy_type': '国家级政策',
                            'summary': summary,
                            'department': '国务院'
                        }
                    )
                    items.append(item)
                    
                except Exception as e:
                    self.logger.warning(f"解析单条政策失败: {e}")
                    continue
            
            self.logger.info(f"从国务院抓取 {len(items)} 条政策")
            
        except Exception as e:
            self.logger.error(f"抓取国务院政策失败: {e}")
            items.extend(self._generate_sample_policy_data('国务院'))
        
        return items
    
    def _scrape_csrc(self) -> List[DataItem]:
        """抓取证监会政策"""
        items = []
        
        try:
            self.logger.info("开始抓取证监会政策...")
            
            # 证监会法规政策
            url = 'http://www.csrc.gov.cn/csrc/c101954/common_list.shtml'
            response = self.session.get(url, timeout=30)
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找公告列表
            notice_list = soup.find_all('div', class_='row') or soup.find_all('tr')
            
            for notice in notice_list[:15]:
                try:
                    # 提取标题
                    title_elem = notice.find('a')
                    title = title_elem.get_text(strip=True) if title_elem else ''
                    link = title_elem.get('href', '') if title_elem else ''
                    
                    if not title or not self._is_relevant_policy(title):
                        continue
                    
                    # 提取日期
                    date_elem = notice.find('span', class_='date') or notice.find('td', class_='date')
                    date_str = date_elem.get_text(strip=True) if date_elem else self.today
                    date_str = self._normalize_date(date_str)
                    
                    content = f"""
                    政策标题: {title}
                    发布机构: 中国证监会
                    发布日期: {date_str}
                    政策类型: 监管规定/办法/通知
                    """.strip()
                    
                    item = DataItem(
                        date=date_str,
                        title=title[:100],
                        type='policy',
                        content=content,
                        source='证监会',
                        url=str(link) if str(link).startswith('http') else f'http://www.csrc.gov.cn{link}',
                        tags=['政策', '证监会', '科创板', '监管'],
                        metadata={
                            'policy_type': '监管政策',
                            'department': '中国证监会'
                        }
                    )
                    items.append(item)
                    
                except Exception as e:
                    self.logger.warning(f"解析单条政策失败: {e}")
                    continue
            
            self.logger.info(f"从证监会抓取 {len(items)} 条政策")
            
        except Exception as e:
            self.logger.error(f"抓取证监会政策失败: {e}")
            items.extend(self._generate_sample_policy_data('证监会'))
        
        return items
    
    def _scrape_most(self) -> List[DataItem]:
        """抓取科技部政策"""
        items = []
        
        try:
            self.logger.info("开始抓取科技部政策...")
            
            # 科技部政策法规
            url = 'https://www.most.gov.cn/kjbgz/'
            response = self.session.get(url, timeout=30)
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找政策列表
            policy_list = soup.find_all('li') or soup.find_all('tr')
            
            for policy in policy_list[:15]:
                try:
                    # 提取标题
                    title_elem = policy.find('a')
                    title = title_elem.get_text(strip=True) if title_elem else ''
                    link = title_elem.get('href', '') if title_elem else ''
                    
                    if not title or not self._is_relevant_policy(title):
                        continue
                    
                    # 提取日期
                    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', policy.get_text())
                    date_str = date_match.group(1) if date_match else self.today
                    date_str = self._normalize_date(date_str)
                    
                    content = f"""
                    政策标题: {title}
                    发布机构: 科学技术部
                    发布日期: {date_str}
                    政策类型: 科技政策/通知/办法
                    """.strip()
                    
                    item = DataItem(
                        date=date_str,
                        title=title[:100],
                        type='policy',
                        content=content,
                        source='科技部',
                        url=str(link) if str(link).startswith('http') else f'https://www.most.gov.cn{link}',
                        tags=['政策', '科技部', '科技创新'],
                        metadata={
                            'policy_type': '科技政策',
                            'department': '科学技术部'
                        }
                    )
                    items.append(item)
                    
                except Exception as e:
                    self.logger.warning(f"解析单条政策失败: {e}")
                    continue
            
            self.logger.info(f"从科技部抓取 {len(items)} 条政策")
            
        except Exception as e:
            self.logger.error(f"抓取科技部政策失败: {e}")
            items.extend(self._generate_sample_policy_data('科技部'))
        
        return items
    
    def _is_relevant_policy(self, title: str) -> bool:
        """判断是否为科技金融相关政策"""
        keywords = [
            '科技', '科创', '金融', '投资', '融资', '上市',
            '科创板', '创投', '创新', '创业', '资本', '证券',
            '基金', 'IPO', '并购', '重组'
        ]
        
        title_lower = title.lower()
        return any(keyword in title_lower for keyword in keywords)
    
    def _normalize_date(self, date_str: str) -> str:
        """标准化日期格式"""
        try:
            # 尝试多种日期格式
            formats = [
                '%Y-%m-%d',
                '%Y/%m/%d',
                '%Y年%m月%d日',
                '%m月%d日',
                '%d-%m-%Y',
                '%m-%d-%Y',
                '%Y%m%d'
            ]
            
            for fmt in formats:
                try:
                    dt = datetime.strptime(date_str, fmt)
                    return dt.strftime('%Y-%m-%d')
                except ValueError:
                    continue
            
            # 如果都无法解析，返回今日
            return self.today
            
        except Exception:
            return self.today
    
    def _generate_sample_policy_data(self, source_name: str) -> List[DataItem]:
        """生成示例政策数据（备用）"""
        items = []
        
        sample_policies = [
            {
                'title': '关于支持科技型企业融资的指导意见',
                'content': '支持符合条件的科技型企业上市融资，完善科技金融支持体系，推动科技成果转化。',
                'tags': ['融资', '科技型企业', '指导意见']
            },
            {
                'title': '科创板上市公司持续监管办法（试行）',
                'content': '规范科创板上市公司信息披露和公司治理，加强投资者保护。',
                'tags': ['科创板', '监管', '上市公司']
            },
            {
                'title': '促进创业投资持续健康发展的若干政策',
                'content': '鼓励创投机构投早投小投科技，完善创业投资退出渠道。',
                'tags': ['创投', '投资', '政策']
            },
            {
                'title': '关于加强知识产权质押融资工作的通知',
                'content': '扩大知识产权质押融资规模，支持科技企业创新发展。',
                'tags': ['知识产权', '融资', '科技企业']
            },
            {
                'title': '金融科技发展规划（2024-2028年）',
                'content': '推动金融科技赋能，提升金融服务实体经济能力，支持科技创新。',
                'tags': ['金融科技', '规划', '创新']
            }
        ]
        
        for i, policy in enumerate(sample_policies):
            date = (datetime.now() - timedelta(days=i*3)).strftime('%Y-%m-%d')
            
            content = f"""
            政策标题: {policy['title']}
            发布机构: {source_name}
            发布日期: {date}
            政策摘要: {policy['content']}
            数据来源: 示例数据
            """.strip()
            
            item = DataItem(
                date=date,
                title=policy['title'],
                type='policy',
                content=content,
                source=source_name,
                url='',
                tags=['政策'] + policy['tags'],
                metadata={
                    'is_sample': True,
                    'department': source_name
                }
            )
            items.append(item)
        
        self.logger.info(f"从{source_name}生成 {len(items)} 条示例政策数据")
        return items
    
    def generate_policy_summary(self) -> Dict[str, Any]:
        """生成政策摘要报告"""
        summary = {
            'date': self.today,
            'total_policies': len(self.items),
            'source_summary': {},
            'recent_policies': []
        }
        
        # 统计各来源数量
        for item in self.items:
            source = item.source
            summary['source_summary'][source] = summary['source_summary'].get(source, 0) + 1
        
        # 最近5条政策
        sorted_items = sorted(self.items, key=lambda x: x.date, reverse=True)
        summary['recent_policies'] = [item.to_dict() for item in sorted_items[:5]]
        
        return summary


if __name__ == '__main__':
    # 测试
    from pathlib import Path
    
    data_dir = Path(__file__).parent.parent.parent / 'data' / 'raw' / 'policy'
    scraper = PolicyScraper(data_dir)
    
    items = scraper.run()
    
    if items:
        scraper.save_to_json()
        scraper.save_to_ndjson()
        
        # 打印示例
        print("\n示例数据项:")
        print(json.dumps(items[0].to_dict(), ensure_ascii=False, indent=2))
        
        # 打印摘要
        summary = scraper.generate_policy_summary()
        print("\n政策摘要:")
        print(json.dumps(summary, ensure_ascii=False, indent=2))
