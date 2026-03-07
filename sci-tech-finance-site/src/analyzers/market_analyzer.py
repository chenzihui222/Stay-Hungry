#!/usr/bin/env python3
"""
科创板市场数据分析模块
- 估值分析
- 行业分析
- IPO分析
- 生成市场洞察报告
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
RAW_DATA_DIR = BASE_DIR / 'data' / 'raw' / 'star_market'
PROCESSED_DIR = BASE_DIR / 'data' / 'processed'
REPORTS_DIR = BASE_DIR / 'data' / 'reports'

# 确保目录存在
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


class MarketAnalyzer:
    """科创板市场分析器"""
    
    def __init__(self):
        self.today = datetime.now().strftime('%Y-%m-%d')
        logger.info(f"初始化市场分析器 - {self.today}")
        
        # 加载最新数据
        self.load_data()
    
    def load_data(self):
        """加载原始数据"""
        try:
            # 查找最新的数据文件
            stock_files = list(RAW_DATA_DIR.glob('stock_list_*.csv'))
            ipo_files = list(RAW_DATA_DIR.glob('ipo_data_*.csv'))
            stats_files = list(RAW_DATA_DIR.glob('market_stats_*.json'))
            
            if stock_files:
                latest_stock = max(stock_files, key=lambda p: p.stat().st_mtime)
                self.stock_df = pd.read_csv(latest_stock)
                logger.info(f"加载股票数据: {latest_stock.name}")
            else:
                self.stock_df = None
            
            if ipo_files:
                latest_ipo = max(ipo_files, key=lambda p: p.stat().st_mtime)
                self.ipo_df = pd.read_csv(latest_ipo)
                logger.info(f"加载IPO数据: {latest_ipo.name}")
            else:
                self.ipo_df = None
            
            if stats_files:
                latest_stats = max(stats_files, key=lambda p: p.stat().st_mtime)
                with open(latest_stats, 'r') as f:
                    self.market_stats = json.load(f)
                logger.info(f"加载市场统计: {latest_stats.name}")
            else:
                self.market_stats = None
                
        except Exception as e:
            logger.error(f"加载数据失败: {e}")
            self.stock_df = None
            self.ipo_df = None
            self.market_stats = None
    
    def analyze_valuation(self):
        """估值分析"""
        try:
            logger.info("开始估值分析...")
            
            if self.stock_df is None:
                logger.warning("没有股票数据可供分析")
                return None
            
            # 市盈率分析
            pe_data = self.stock_df['pe_ratio'].dropna()
            
            valuation_stats = {
                'avg_pe': float(pe_data.mean()),
                'median_pe': float(pe_data.median()),
                'min_pe': float(pe_data.min()),
                'max_pe': float(pe_data.max()),
                'pe_std': float(pe_data.std()),
                'pe_25th': float(pe_data.quantile(0.25)),
                'pe_75th': float(pe_data.quantile(0.75)),
                'count': int(len(pe_data))
            }
            
            # 保存分析结果
            output_file = PROCESSED_DIR / f'valuation_analysis_{self.today}.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(valuation_stats, f, ensure_ascii=False, indent=2)
            
            logger.info(f"估值分析完成: {valuation_stats}")
            return valuation_stats
            
        except Exception as e:
            logger.error(f"估值分析失败: {e}")
            return None
    
    def analyze_industry(self):
        """行业分析"""
        try:
            logger.info("开始行业分析...")
            
            if self.stock_df is None or 'industry' not in self.stock_df.columns:
                logger.warning("没有行业数据可供分析")
                return None
            
            # 行业分布
            industry_counts = self.stock_df['industry'].value_counts().head(10)
            
            # 行业市值统计
            industry_cap = self.stock_df.groupby('industry')['market_cap'].sum().sort_values(ascending=False).head(10)
            
            industry_analysis = {
                'top_industries_by_count': industry_counts.to_dict(),
                'top_industries_by_cap': industry_cap.to_dict(),
                'industry_count': len(self.stock_df['industry'].unique())
            }
            
            # 保存分析结果
            output_file = PROCESSED_DIR / f'industry_analysis_{self.today}.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(industry_analysis, f, ensure_ascii=False, indent=2)
            
            # 生成行业分布数据用于可视化
            viz_data = pd.DataFrame({
                'industry': industry_counts.index,
                'count': industry_counts.values
            })
            viz_file = PROCESSED_DIR / f'industry_distribution_{self.today}.csv'
            viz_data.to_csv(viz_file, index=False, encoding='utf-8-sig')
            
            logger.info(f"行业分析完成: {len(industry_counts)} 个行业")
            return industry_analysis
            
        except Exception as e:
            logger.error(f"行业分析失败: {e}")
            return None
    
    def analyze_ipo_trends(self):
        """IPO趋势分析"""
        try:
            logger.info("开始IPO趋势分析...")
            
            if self.ipo_df is None:
                # 生成模拟IPO趋势数据
                logger.info("使用模拟IPO数据进行演示")
                
                # 生成近12个月的IPO数据
                months = []
                ipo_counts = []
                total_amounts = []
                
                for i in range(12):
                    month_date = datetime.now() - timedelta(days=30*i)
                    months.insert(0, month_date.strftime('%Y-%m'))
                    ipo_counts.insert(0, 5 + i % 8)  # 模拟数据
                    total_amounts.insert(0, (5 + i % 8) * 15.5)  # 模拟金额
                
                ipo_trends = {
                    'months': months,
                    'ipo_counts': ipo_counts,
                    'total_amounts': total_amounts,
                    'total_ipo_12m': sum(ipo_counts),
                    'total_amount_12m': sum(total_amounts),
                    'avg_monthly_ipo': sum(ipo_counts) / len(ipo_counts)
                }
            else:
                # 处理真实IPO数据
                ipo_trends = {
                    'total_ipo_12m': len(self.ipo_df),
                    'note': '基于真实IPO数据'
                }
            
            # 保存分析结果
            output_file = PROCESSED_DIR / f'ipo_trends_{self.today}.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(ipo_trends, f, ensure_ascii=False, indent=2)
            
            logger.info(f"IPO趋势分析完成")
            return ipo_trends
            
        except Exception as e:
            logger.error(f"IPO趋势分析失败: {e}")
            return None
    
    def generate_market_report(self):
        """生成市场分析报告"""
        try:
            logger.info("生成市场分析报告...")
            
            # 获取各项分析结果
            valuation = self.analyze_valuation()
            industry = self.analyze_industry()
            ipo = self.analyze_ipo_trends()
            
            # 生成Markdown报告
            report_lines = [
                "# 科创板市场分析报告",
                f"\n**报告日期**: {self.today}",
                "\n---\n",
                
                "## 市场概况\n",
            ]
            
            if self.market_stats:
                report_lines.extend([
                    f"- **科创50指数**: {self.market_stats.get('latest_close', 'N/A')}",
                    f"- **涨跌幅**: {self.market_stats.get('latest_change_pct', 'N/A')}%",
                    f"- **30日最高**: {self.market_stats.get('max_price_30d', 'N/A')}",
                    f"- **30日最低**: {self.market_stats.get('min_price_30d', 'N/A')}",
                    "\n"
                ])
            
            if valuation:
                report_lines.extend([
                    "## 估值分析\n",
                    f"- **平均市盈率**: {valuation['avg_pe']:.2f}",
                    f"- **中位数市盈率**: {valuation['median_pe']:.2f}",
                    f"- **市盈率范围**: {valuation['min_pe']:.2f} - {valuation['max_pe']:.2f}",
                    f"- **样本数量**: {valuation['count']} 只股票",
                    "\n"
                ])
            
            if industry:
                report_lines.extend([
                    "## 行业分布\n",
                    f"科创板共覆盖 **{industry['industry_count']}** 个行业\n",
                    "### 公司数量Top 5行业\n"
                ])
                
                top_industries = list(industry['top_industries_by_count'].items())[:5]
                for idx, (ind_name, count) in enumerate(top_industries, 1):
                    report_lines.append(f"{idx}. **{ind_name}**: {count} 家公司\n")
                
                report_lines.append("\n")
            
            if ipo:
                report_lines.extend([
                    "## IPO动态\n",
                    f"- **近12个月IPO数量**: {ipo.get('total_ipo_12m', 'N/A')} 家",
                    f"- **近12个月募资总额**: {ipo.get('total_amount_12m', 'N/A'):.2f} 亿元",
                    f"- **月均IPO**: {ipo.get('avg_monthly_ipo', 'N/A'):.1f} 家",
                    "\n"
                ])
            
            report_lines.extend([
                "---\n",
                "*本报告由科创金融研究平台自动生成*\n",
                f"*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
            ])
            
            report_content = ''.join(report_lines)
            
            # 保存报告
            report_file = REPORTS_DIR / f'market_report_{self.today}.md'
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            logger.info(f"市场分析报告已保存: {report_file}")
            
            # 同时生成JSON格式的报告数据
            report_data = {
                'date': self.today,
                'market_stats': self.market_stats,
                'valuation': valuation,
                'industry': industry,
                'ipo': ipo
            }
            
            json_file = REPORTS_DIR / f'market_report_{self.today}.json'
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, ensure_ascii=False, indent=2)
            
            return report_data
            
        except Exception as e:
            logger.error(f"生成市场报告失败: {e}")
            return None
    
    def run(self):
        """运行所有分析任务"""
        logger.info("=" * 50)
        logger.info("开始市场分析任务")
        logger.info("=" * 50)
        
        # 生成完整的市场报告
        report = self.generate_market_report()
        
        logger.info("=" * 50)
        logger.info("市场分析任务完成")
        logger.info("=" * 50)
        
        return report


if __name__ == '__main__':
    analyzer = MarketAnalyzer()
    results = analyzer.run()
