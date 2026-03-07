#!/usr/bin/env python3
"""
VC/PE投资数据分析模块
- 投资趋势分析
- 行业热度分析
- 机构活跃度分析
- 生成投资洞察报告
"""

import os
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
import numpy as np

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 项目根目录
BASE_DIR = Path(__file__).parent.parent.parent
RAW_DATA_DIR = BASE_DIR / 'data' / 'raw' / 'vcpe'
PROCESSED_DIR = BASE_DIR / 'data' / 'processed'
REPORTS_DIR = BASE_DIR / 'data' / 'reports'

# 确保目录存在
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


class VCPEAnalyzer:
    """VC/PE投资分析器"""
    
    def __init__(self):
        self.today = datetime.now().strftime('%Y-%m-%d')
        logger.info(f"初始化VC/PE分析器 - {self.today}")
        
        # 加载数据
        self.load_data()
    
    def load_data(self):
        """加载原始数据"""
        try:
            # 查找最新的数据文件
            events_files = list(RAW_DATA_DIR.glob('investment_events_*.csv'))
            trends_files = list(RAW_DATA_DIR.glob('sector_trends_*.csv'))
            investors_files = list(RAW_DATA_DIR.glob('top_investors_*.csv'))
            summary_files = list(RAW_DATA_DIR.glob('market_summary_*.json'))
            
            if events_files:
                latest_events = max(events_files, key=lambda p: p.stat().st_mtime)
                self.events_df = pd.read_csv(latest_events)
                logger.info(f"加载投资事件: {latest_events.name}")
            else:
                self.events_df = None
            
            if trends_files:
                latest_trends = max(trends_files, key=lambda p: p.stat().st_mtime)
                self.trends_df = pd.read_csv(latest_trends)
                logger.info(f"加载行业趋势: {latest_trends.name}")
            else:
                self.trends_df = None
            
            if investors_files:
                latest_investors = max(investors_files, key=lambda p: p.stat().st_mtime)
                self.investors_df = pd.read_csv(latest_investors)
                logger.info(f"加载投资机构: {latest_investors.name}")
            else:
                self.investors_df = None
            
            if summary_files:
                latest_summary = max(summary_files, key=lambda p: p.stat().st_mtime)
                with open(latest_summary, 'r') as f:
                    self.market_summary = json.load(f)
                logger.info(f"加载市场摘要: {latest_summary.name}")
            else:
                self.market_summary = None
                
        except Exception as e:
            logger.error(f"加载数据失败: {e}")
            self.events_df = None
            self.trends_df = None
            self.investors_df = None
            self.market_summary = None
    
    def analyze_investment_trends(self):
        """投资趋势分析"""
        try:
            logger.info("开始投资趋势分析...")
            
            if self.events_df is None:
                logger.warning("没有投资事件数据")
                return None
            
            # 按阶段统计
            stage_counts = self.events_df['stage'].value_counts()
            
            # 按时间统计（假设有日期列）
            trend_analysis = {
                'total_deals': len(self.events_df),
                'stage_distribution': stage_counts.to_dict(),
                'top_stages': stage_counts.head(5).to_dict()
            }
            
            # 保存分析结果
            output_file = PROCESSED_DIR / f'investment_trends_{self.today}.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(trend_analysis, f, ensure_ascii=False, indent=2)
            
            logger.info(f"投资趋势分析完成")
            return trend_analysis
            
        except Exception as e:
            logger.error(f"投资趋势分析失败: {e}")
            return None
    
    def analyze_sector_heat(self):
        """行业热度分析"""
        try:
            logger.info("开始行业热度分析...")
            
            if self.trends_df is None:
                logger.warning("没有行业趋势数据")
                return None
            
            # 计算热度指数（基于交易数量和金额）
            self.trends_df['heat_index'] = (
                self.trends_df['deal_count'] * 0.4 + 
                self.trends_df['total_amount'] * 0.6
            )
            
            # 排序获取热门行业
            hot_sectors = self.trends_df.sort_values('heat_index', ascending=False)
            
            sector_analysis = {
                'hot_sectors': hot_sectors.head(5)['sectors'].tolist(),
                'sector_details': hot_sectors.head(5).to_dict('records')
            }
            
            # 保存分析结果
            output_file = PROCESSED_DIR / f'sector_heat_{self.today}.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(sector_analysis, f, ensure_ascii=False, indent=2)
            
            # 保存可视化数据
            viz_file = PROCESSED_DIR / f'sector_heat_data_{self.today}.csv'
            hot_sectors[['sectors', 'deal_count', 'total_amount', 'heat_index']].to_csv(
                viz_file, index=False, encoding='utf-8-sig'
            )
            
            logger.info(f"行业热度分析完成: {len(sector_analysis['hot_sectors'])} 个热门行业")
            return sector_analysis
            
        except Exception as e:
            logger.error(f"行业热度分析失败: {e}")
            return None
    
    def analyze_investor_activity(self):
        """机构活跃度分析"""
        try:
            logger.info("开始机构活跃度分析...")
            
            if self.investors_df is None:
                logger.warning("没有投资机构数据")
                return None
            
            # 分析活跃度
            top_active = self.investors_df.head(10)
            
            investor_analysis = {
                'top_investors': top_active.to_dict('records'),
                'total_deals_top20': int(self.investors_df['deal_count'].sum()),
                'avg_deals_per_investor': float(self.investors_df['deal_count'].mean())
            }
            
            # 保存分析结果
            output_file = PROCESSED_DIR / f'investor_activity_{self.today}.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(investor_analysis, f, ensure_ascii=False, indent=2)
            
            logger.info(f"机构活跃度分析完成")
            return investor_analysis
            
        except Exception as e:
            logger.error(f"机构活跃度分析失败: {e}")
            return None
    
    def generate_vcpe_report(self):
        """生成VC/PE投资分析报告"""
        try:
            logger.info("生成VC/PE投资分析报告...")
            
            # 获取各项分析结果
            trends = self.analyze_investment_trends()
            sectors = self.analyze_sector_heat()
            investors = self.analyze_investor_activity()
            
            # 生成Markdown报告
            report_lines = [
                "# VC/PE投资市场分析报告",
                f"\n**报告日期**: {self.today}",
                "\n---\n",
                
                "## 市场概况\n",
            ]
            
            if self.market_summary:
                report_lines.extend([
                    f"- **本月投资事件**: {self.market_summary.get('total_deals', 'N/A')} 起",
                    f"- **本月投资总额**: {self.market_summary.get('total_amount_usd', 'N/A')} 亿美元",
                    f"- **同比增长**: {self.market_summary.get('yoy_growth', 'N/A')}%",
                    f"- **环比增长**: {self.market_summary.get('mom_growth', 'N/A')}%",
                    "\n"
                ])
            
            if sectors:
                report_lines.extend([
                    "## 热门赛道\n",
                    "本月最热门的投资赛道：\n"
                ])
                for idx, sector in enumerate(sectors['hot_sectors'][:5], 1):
                    report_lines.append(f"{idx}. **{sector}**\n")
                report_lines.append("\n")
            
            if investors:
                report_lines.extend([
                    "## 活跃投资机构\n",
                    "本月最活跃的投资机构Top 10：\n"
                ])
                for idx, investor in enumerate(investors['top_investors'][:10], 1):
                    report_lines.append(
                        f"{idx}. **{investor['investor_name']}** - "
                        f"{investor['deal_count']}笔投资, "
                        f"{investor['total_amount']}亿美元\n"
                    )
                report_lines.append("\n")
            
            if trends:
                report_lines.extend([
                    "## 投资阶段分布\n",
                    "不同阶段的投资事件分布：\n",
                    "| 阶段 | 事件数量 |\n",
                    "|------|----------|\n"
                ])
                for stage, count in list(trends.get('stage_distribution', {}).items())[:6]:
                    report_lines.append(f"| {stage} | {count} |\n")
                report_lines.append("\n")
            
            report_lines.extend([
                "## 市场洞察\n",
                "1. 科技金融投资持续活跃，人工智能和生物医药仍是热门赛道\n",
                "2. 早期投资（种子轮到A轮）占比提升，显示市场对创新项目的信心\n",
                "3. 头部机构保持高频投资节奏，市场马太效应明显\n",
                "4. 硬科技投资受到政策和市场双重驱动\n",
                "\n",
                "---\n",
                "*本报告由科创金融研究平台自动生成*\n",
                f"*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
            ])
            
            report_content = ''.join(report_lines)
            
            # 保存报告
            report_file = REPORTS_DIR / f'vcpe_report_{self.today}.md'
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            logger.info(f"VC/PE投资分析报告已保存: {report_file}")
            
            # 同时生成JSON格式的报告数据
            report_data = {
                'date': self.today,
                'market_summary': self.market_summary,
                'trends': trends,
                'sectors': sectors,
                'investors': investors
            }
            
            json_file = REPORTS_DIR / f'vcpe_report_{self.today}.json'
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, ensure_ascii=False, indent=2)
            
            return report_data
            
        except Exception as e:
            logger.error(f"生成VC/PE报告失败: {e}")
            return None
    
    def run(self):
        """运行所有分析任务"""
        logger.info("=" * 50)
        logger.info("开始VC/PE分析任务")
        logger.info("=" * 50)
        
        # 生成完整的VC/PE报告
        report = self.generate_vcpe_report()
        
        logger.info("=" * 50)
        logger.info("VC/PE分析任务完成")
        logger.info("=" * 50)
        
        return report


if __name__ == '__main__':
    analyzer = VCPEAnalyzer()
    results = analyzer.run()
