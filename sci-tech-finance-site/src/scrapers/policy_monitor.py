#!/usr/bin/env python3
"""
科技金融政策监控模块
- 抓取政府科技金融政策
- 抓取证监会/银保监会政策
- 生成政策摘要和影响分析
"""

import os
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 项目根目录
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / 'data' / 'raw' / 'policy'

# 确保目录存在
DATA_DIR.mkdir(parents=True, exist_ok=True)


class PolicyMonitor:
    """政策监控器"""
    
    def __init__(self):
        self.today = datetime.now().strftime('%Y-%m-%d')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        logger.info(f"初始化政策监控器 - {self.today}")
    
    def fetch_gov_policies(self):
        """抓取政府科技金融相关政策"""
        try:
            logger.info("开始抓取政府政策...")
            
            # 模拟政策数据（实际项目需要从真实政府网站抓取）
            policies = [
                {
                    'title': '关于支持科技型企业融资的指导意见',
                    'source': '国务院',
                    'date': (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d'),
                    'category': '融资支持',
                    'summary': '支持符合条件的科技型企业上市融资，完善科技金融支持体系',
                    'impact_level': '高',
                    'key_points': ['扩大直接融资', '完善退出机制', '加强风险控制']
                },
                {
                    'title': '科创板上市公司持续监管办法（试行）',
                    'source': '证监会',
                    'date': (datetime.now() - timedelta(days=12)).strftime('%Y-%m-%d'),
                    'category': '市场监管',
                    'summary': '规范科创板上市公司信息披露和公司治理',
                    'impact_level': '中',
                    'key_points': ['信息披露', '公司治理', '投资者保护']
                },
                {
                    'title': '促进创业投资持续健康发展的若干政策',
                    'source': '发改委',
                    'date': (datetime.now() - timedelta(days=20)).strftime('%Y-%m-%d'),
                    'category': '创投支持',
                    'summary': '鼓励创投机构投早投小投科技',
                    'impact_level': '高',
                    'key_points': ['税收优惠', '退出渠道', '长期投资']
                },
                {
                    'title': '金融科技发展规划（2024-2028年）',
                    'source': '人民银行',
                    'date': (datetime.now() - timedelta(days=8)).strftime('%Y-%m-%d'),
                    'category': '金融科技',
                    'summary': '推动金融科技赋能，提升金融服务实体经济能力',
                    'impact_level': '高',
                    'key_points': ['数字化转型', '风险管理', '普惠金融']
                },
                {
                    'title': '关于加强知识产权质押融资工作的通知',
                    'source': '银保监会',
                    'date': (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d'),
                    'category': '知识产权',
                    'summary': '扩大知识产权质押融资规模，支持科技企业创新发展',
                    'impact_level': '中',
                    'key_points': ['质押融资', '评估体系', '风险分担']
                }
            ]
            
            df = pd.DataFrame(policies)
            
            # 保存数据
            output_file = DATA_DIR / f'gov_policies_{self.today}.csv'
            df.to_csv(output_file, index=False, encoding='utf-8-sig')
            logger.info(f"政府政策已保存: {output_file}")
            logger.info(f"共 {len(df)} 条政策")
            
            return df
            
        except Exception as e:
            logger.error(f"抓取政府政策失败: {e}")
            return None
    
    def analyze_policy_impact(self, policies_df):
        """分析政策影响"""
        try:
            logger.info("开始分析政策影响...")
            
            if policies_df is None or policies_df.empty:
                logger.warning("没有政策数据可供分析")
                return None
            
            # 按影响等级统计
            impact_stats = policies_df['impact_level'].value_counts().to_dict()
            
            # 按类别统计
            category_stats = policies_df['category'].value_counts().to_dict()
            
            # 生成高影响政策列表
            high_impact = policies_df[policies_df['impact_level'] == '高'].to_dict('records')
            
            analysis = {
                'date': self.today,
                'total_policies': len(policies_df),
                'impact_distribution': impact_stats,
                'category_distribution': category_stats,
                'high_impact_policies': high_impact,
                'summary': f"近期共发布{len(policies_df)}项科技金融相关政策，其中高影响政策{len(high_impact)}项，"
                          f"主要集中在{list(category_stats.keys())[0]}领域。"
            }
            
            # 保存分析结果
            output_file = DATA_DIR / f'policy_analysis_{self.today}.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, ensure_ascii=False, indent=2)
            
            logger.info(f"政策分析已保存: {output_file}")
            return analysis
            
        except Exception as e:
            logger.error(f"分析政策影响失败: {e}")
            return None
    
    def generate_policy_digest(self, policies_df):
        """生成政策摘要报告"""
        try:
            logger.info("生成政策摘要...")
            
            if policies_df is None or policies_df.empty:
                return None
            
            # 按日期排序
            policies_df = policies_df.sort_values('date', ascending=False)
            
            # 生成Markdown格式摘要
            digest_lines = [
                "# 科技金融政策周报",
                f"\n**报告日期**: {self.today}",
                f"\n**统计周期**: 近30天",
                f"\n---\n",
                f"## 概览\n",
                f"本周共监测到 **{len(policies_df)}** 项科技金融相关政策，",
                f"其中高影响政策 **{len(policies_df[policies_df['impact_level'] == '高'])}** 项。\n"
            ]
            
            # 添加重点政策
            digest_lines.append("## 重点政策\n")
            for _, policy in policies_df[policies_df['impact_level'] == '高'].head(3).iterrows():
                digest_lines.extend([
                    f"### {policy['title']}\n",
                    f"- **来源**: {policy['source']}\n",
                    f"- **发布时间**: {policy['date']}\n",
                    f"- **类别**: {policy['category']}\n",
                    f"- **影响等级**: {policy['impact_level']}\n",
                    f"- **摘要**: {policy['summary']}\n",
                    f"- **关键要点**: {', '.join(policy['key_points'])}\n",
                    "\n"
                ])
            
            # 添加政策分类统计
            digest_lines.extend([
                "## 政策分类统计\n",
                "| 类别 | 数量 |\n",
                "|------|------|\n"
            ])
            category_counts = policies_df['category'].value_counts()
            for category, count in category_counts.items():
                digest_lines.append(f"| {category} | {count} |\n")
            
            digest_content = ''.join(digest_lines)
            
            # 保存摘要
            output_file = DATA_DIR / f'policy_digest_{self.today}.md'
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(digest_content)
            
            logger.info(f"政策摘要已保存: {output_file}")
            return digest_content
            
        except Exception as e:
            logger.error(f"生成政策摘要失败: {e}")
            return None
    
    def run(self):
        """运行所有监控任务"""
        logger.info("=" * 50)
        logger.info("开始政策监控任务")
        logger.info("=" * 50)
        
        # 抓取政策
        policies = self.fetch_gov_policies()
        
        # 分析影响
        analysis = None
        digest = None
        if policies is not None:
            analysis = self.analyze_policy_impact(policies)
            digest = self.generate_policy_digest(policies)
        
        logger.info("=" * 50)
        logger.info("政策监控任务完成")
        logger.info("=" * 50)
        
        return {
            'policies': policies,
            'analysis': analysis,
            'digest': digest
        }


if __name__ == '__main__':
    monitor = PolicyMonitor()
    results = monitor.run()
