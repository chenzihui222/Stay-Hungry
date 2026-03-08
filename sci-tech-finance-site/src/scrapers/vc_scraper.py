#!/usr/bin/env python3
"""
VC投资数据抓取器
数据源：清科 / IT桔子 / Crunchbase / 新闻
"""

import re
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional
import requests
from bs4 import BeautifulSoup

from .base_scraper import BaseScraper, DataItem


class VCScraper(BaseScraper):
    """VC投资数据抓取器"""
    
    # 数据源配置
    SOURCES = {
        'chinaventure': {
            'name': '清科',
            'base_url': 'https://www.chinaventure.com.cn',
            'enabled': True
        },
        'itjuzi': {
            'name': 'IT桔子',
            'base_url': 'https://www.itjuzi.com',
            'enabled': True
        },
        'crunchbase': {
            'name': 'Crunchbase',
            'base_url': 'https://www.crunchbase.com',
            'enabled': False  # 需要API key
        },
        'pedaily': {
            'name': '投资界',
            'base_url': 'https://www.pedaily.cn',
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
        """执行VC数据抓取"""
        items = []
        
        # 1. 抓取清科数据
        if self.SOURCES['chinaventure']['enabled']:
            items.extend(self._scrape_chinaventure())
        
        # 2. 抓取IT桔子数据
        if self.SOURCES['itjuzi']['enabled']:
            items.extend(self._scrape_itjuzi())
        
        # 3. 抓取投资界数据
        if self.SOURCES['pedaily']['enabled']:
            items.extend(self._scrape_pedaily())
        
        # 4. 抓取新闻数据
        items.extend(self._scrape_news())
        
        # 5. 如果没有抓取到数据，生成示例数据
        if not items:
            self.logger.warning("未抓取到任何VC数据，生成示例数据...")
            items.extend(self._generate_sample_vc_data('综合示例'))
        
        return items
    
    def _scrape_chinaventure(self) -> List[DataItem]:
        """抓取清科投资数据"""
        items = []
        
        try:
            self.logger.info("开始抓取清科投资数据...")
            
            # 清科投资事件列表页
            url = 'https://www.chinaventure.com.cn/invest/list.html'
            response = self.session.get(url, timeout=30)
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 解析投资事件列表
            events = soup.find_all('div', class_='invest-item') or soup.find_all('tr')
            
            for event in events[:20]:  # 限制前20条
                try:
                    # 提取公司名
                    company_elem = event.find('a', class_='company') or event.find('td', class_='company')
                    company = company_elem.get_text(strip=True) if company_elem else '未知公司'
                    
                    # 提取投资轮次
                    round_elem = event.find('span', class_='round') or event.find('td', class_='round')
                    round_name = round_elem.get_text(strip=True) if round_elem else '未知轮次'
                    
                    # 提取投资金额
                    amount_elem = event.find('span', class_='amount') or event.find('td', class_='amount')
                    amount = amount_elem.get_text(strip=True) if amount_elem else '未披露'
                    
                    # 提取投资方
                    investor_elem = event.find('span', class_='investor') or event.find('td', class_='investor')
                    investor = investor_elem.get_text(strip=True) if investor_elem else '未披露'
                    
                    # 提取行业
                    sector_elem = event.find('span', class_='sector') or event.find('td', class_='sector')
                    sector = sector_elem.get_text(strip=True) if sector_elem else '未知行业'
                    
                    # 提取日期
                    date_elem = event.find('span', class_='date') or event.find('td', class_='date')
                    date_str = date_elem.get_text(strip=True) if date_elem else self.today
                    
                    # 标准化日期格式
                    date_str = self._normalize_date(date_str)
                    
                    content = f"""
                    被投资公司: {company}
                    投资轮次: {round_name}
                    投资金额: {amount}
                    投资方: {investor}
                    所属行业: {sector}
                    投资日期: {date_str}
                    """.strip()
                    
                    item = DataItem(
                        date=date_str,
                        title=f"融资事件：{company} {round_name}",
                        type='vc',
                        content=content,
                        source='清科',
                        url=f'https://www.chinaventure.com.cn/invest/detail/{company}.html',
                        tags=['VC', '投资', sector, round_name],
                        metadata={
                            'company': company,
                            'round': round_name,
                            'amount': amount,
                            'investor': investor,
                            'sector': sector
                        }
                    )
                    items.append(item)
                    
                except Exception as e:
                    self.logger.warning(f"解析单条投资事件失败: {e}")
                    continue
            
            self.logger.info(f"从清科抓取 {len(items)} 条投资数据")
            
        except Exception as e:
            self.logger.error(f"抓取清科数据失败: {e}")
            # 使用示例数据
            items.extend(self._generate_sample_vc_data('清科'))
        
        return items
    
    def _scrape_itjuzi(self) -> List[DataItem]:
        """抓取IT桔子投资数据"""
        items = []
        
        try:
            self.logger.info("开始抓取IT桔子投资数据...")
            
            # IT桔子投资事件页
            url = 'https://www.itjuzi.com/investevents'
            response = self.session.get(url, timeout=30)
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找投资事件列表
            events = soup.find_all('li', class_='invest-item') or soup.find_all('div', class_='list-item')
            
            for event in events[:20]:
                try:
                    # 提取公司信息
                    company_elem = event.find('a', href=re.compile(r'company'))
                    company = company_elem.get_text(strip=True) if company_elem else '未知公司'
                    
                    # 提取轮次
                    round_elem = event.find('span', class_=re.compile(r'round'))
                    round_name = round_elem.get_text(strip=True) if round_elem else '未知轮次'
                    
                    # 提取金额
                    amount_match = re.search(r'(\d+[\.\d]*[万亿千万]?(?:美元|人民币|元|￥|\$))', event.get_text())
                    amount = amount_match.group(1) if amount_match else '未披露'
                    
                    # 提取投资方
                    investor_elem = event.find('a', href=re.compile(r'investor'))
                    investor = investor_elem.get_text(strip=True) if investor_elem else '未披露'
                    
                    # 提取行业
                    sector_elem = event.find('span', class_=re.compile(r'tag|industry'))
                    sector = sector_elem.get_text(strip=True) if sector_elem else '未知行业'
                    
                    # 提取日期
                    date_match = re.search(r'(\d{4}[-/年]\d{1,2}[-/月]\d{1,2})', event.get_text())
                    date_str = date_match.group(1).replace('/', '-').replace('年', '-').replace('月', '-').replace('日', '') if date_match else self.today
                    date_str = self._normalize_date(date_str)
                    
                    content = f"""
                    被投资公司: {company}
                    投资轮次: {round_name}
                    投资金额: {amount}
                    投资方: {investor}
                    所属行业: {sector}
                    投资日期: {date_str}
                    """.strip()
                    
                    item = DataItem(
                        date=date_str,
                        title=f"融资事件：{company} {round_name}",
                        type='vc',
                        content=content,
                        source='IT桔子',
                        url=f'https://www.itjuzi.com/company/{company}',
                        tags=['VC', '投资', sector, round_name, 'IT桔子'],
                        metadata={
                            'company': company,
                            'round': round_name,
                            'amount': amount,
                            'investor': investor,
                            'sector': sector
                        }
                    )
                    items.append(item)
                    
                except Exception as e:
                    self.logger.warning(f"解析单条投资事件失败: {e}")
                    continue
            
            self.logger.info(f"从IT桔子抓取 {len(items)} 条投资数据")
            
        except Exception as e:
            self.logger.error(f"抓取IT桔子数据失败: {e}")
            items.extend(self._generate_sample_vc_data('IT桔子'))
        
        return items
    
    def _scrape_pedaily(self) -> List[DataItem]:
        """抓取投资界数据"""
        items = []
        
        try:
            self.logger.info("开始抓取投资界数据...")
            
            # 投资界投融资页面
            url = 'https://www.pedaily.cn/invest/'
            response = self.session.get(url, timeout=30)
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找新闻列表
            news_list = soup.find_all('div', class_='news-list') or soup.find_all('li', class_='item')
            
            for news in news_list[:15]:
                try:
                    # 提取标题
                    title_elem = news.find('a')
                    title = title_elem.get_text(strip=True) if title_elem else ''
                    link = title_elem.get('href', '') if title_elem else ''
                    
                    if not title or '融资' not in title:
                        continue
                    
                    # 提取日期
                    date_elem = news.find('span', class_='date') or news.find('time')
                    date_str = date_elem.get_text(strip=True) if date_elem else self.today
                    date_str = self._normalize_date(date_str)
                    
                    # 提取摘要
                    summary_elem = news.find('p', class_='desc') or news.find('div', class_='summary')
                    summary = summary_elem.get_text(strip=True) if summary_elem else title
                    
                    content = f"""
                    投资动态: {title}
                    摘要: {summary}
                    发布时间: {date_str}
                    """.strip()
                    
                    item = DataItem(
                        date=date_str,
                        title=title[:100],
                        type='vc',
                        content=content,
                        source='投资界',
                        url=str(link) if str(link).startswith('http') else f'https://www.pedaily.cn{link}',
                        tags=['VC', '投资', '投融资', '新闻'],
                        metadata={
                            'summary': summary,
                            'news_type': 'investment'
                        }
                    )
                    items.append(item)
                    
                except Exception as e:
                    self.logger.warning(f"解析单条新闻失败: {e}")
                    continue
            
            self.logger.info(f"从投资界抓取 {len(items)} 条数据")
            
        except Exception as e:
            self.logger.error(f"抓取投资界数据失败: {e}")
            items.extend(self._generate_sample_vc_data('投资界'))
        
        return items
    
    def _scrape_news(self) -> List[DataItem]:
        """抓取VC/PE相关新闻"""
        items = []
        
        try:
            self.logger.info("开始抓取VC/PE新闻...")
            
            # 搜索科技投资相关新闻（简化版）
            keywords = ['融资', '投资', '创投', 'VC', 'PE']
            
            # 这里可以使用RSS feed或新闻API
            # 当前使用简化方案
            
            self.logger.info(f"从新闻源抓取 {len(items)} 条数据")
            
        except Exception as e:
            self.logger.error(f"抓取新闻失败: {e}")
        
        return items
    
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
                '%m-%d-%Y'
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
    
    def _generate_sample_vc_data(self, source_name: str) -> List[DataItem]:
        """生成示例VC数据（备用）"""
        items = []
        
        # 更真实的示例数据
        sample_deals = [
            {
                'company': '智源AI科技',
                'sector': '人工智能',
                'round': 'B轮',
                'amount': '5000万美元',
                'investor': '红杉中国、高瓴资本',
                'date_offset': 0,
                'description': '专注于大语言模型研发的人工智能公司'
            },
            {
                'company': '康宁生物医药',
                'sector': '生物医药',
                'round': 'C轮',
                'amount': '1.2亿美元',
                'investor': '启明创投、礼来亚洲基金',
                'date_offset': 1,
                'description': '肿瘤免疫治疗创新药物研发企业'
            },
            {
                'company': '清源新能源',
                'sector': '新能源',
                'round': 'A轮',
                'amount': '3000万美元',
                'investor': 'IDG资本、经纬创投',
                'date_offset': 2,
                'description': '固态电池技术研发与产业化公司'
            },
            {
                'company': '芯科半导体',
                'sector': '半导体',
                'round': 'Pre-IPO轮',
                'amount': '8000万美元',
                'investor': '中金资本、深创投',
                'date_offset': 3,
                'description': '高端芯片设计公司，专注AI芯片'
            },
            {
                'company': '云途企业服务',
                'sector': '企业服务',
                'round': 'D轮',
                'amount': '6000万美元',
                'investor': '腾讯投资、阿里巴巴',
                'date_offset': 4,
                'description': '企业数字化转型解决方案提供商'
            },
            {
                'company': '精工智造',
                'sector': '先进制造',
                'round': '战略融资',
                'amount': '4000万美元',
                'investor': '软银中国、百度风投',
                'date_offset': 5,
                'description': '工业机器人及智能制造系统提供商'
            },
            {
                'company': '量子芯科技',
                'sector': '量子计算',
                'round': '天使轮',
                'amount': '1500万美元',
                'investor': '红杉种子、真格基金',
                'date_offset': 6,
                'description': '量子计算芯片研发初创公司'
            },
            {
                'company': '智慧医疗云',
                'sector': '医疗健康',
                'round': 'B+轮',
                'amount': '3500万美元',
                'investor': 'GGV纪源资本、顺为资本',
                'date_offset': 7,
                'description': '医疗AI诊断平台及SaaS服务'
            }
        ]
        
        for deal in sample_deals:
            date = (datetime.now() - timedelta(days=deal['date_offset'])).strftime('%Y-%m-%d')
            
            content = f"""
            被投资公司: {deal['company']}
            公司简介: {deal['description']}
            投资轮次: {deal['round']}
            投资金额: {deal['amount']}
            投资方: {deal['investor']}
            所属行业: {deal['sector']}
            投资日期: {date}
            信息来源: {source_name}
            数据类型: 示例数据
            """.strip()
            
            item = DataItem(
                date=date,
                title=f"融资事件：{deal['company']} 完成{deal['round']}融资 {deal['amount']}",
                type='vc',
                content=content,
                source=source_name,
                url='',
                tags=['VC', '投资', deal['sector'], deal['round'], '科技金融'],
                metadata={
                    'company': deal['company'],
                    'company_description': deal['description'],
                    'round': deal['round'],
                    'amount': deal['amount'],
                    'investor': deal['investor'],
                    'sector': deal['sector'],
                    'is_sample': True,
                    'deal_date': date
                }
            )
            items.append(item)
        
        self.logger.info(f"从{source_name}生成 {len(items)} 条示例VC数据")
        return items


if __name__ == '__main__':
    # 测试
    from pathlib import Path
    
    data_dir = Path(__file__).parent.parent.parent / 'data' / 'raw' / 'vc'
    scraper = VCScraper(data_dir)
    
    items = scraper.run()
    
    if items:
        scraper.save_to_json()
        scraper.save_to_ndjson()
        
        # 打印示例
        print("\n示例数据项:")
        print(json.dumps(items[0].to_dict(), ensure_ascii=False, indent=2))
