#!/usr/bin/env python3
"""
静态网站生成器
- 读取分析数据
- 生成HTML页面
- 创建可视化图表
- 部署准备
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
import pandas as pd
from jinja2 import Environment, FileSystemLoader

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 项目根目录
BASE_DIR = Path(__file__).parent.parent.parent
SITE_DIR = BASE_DIR / 'site'
TEMPLATES_DIR = SITE_DIR / 'templates'
CONTENT_DIR = SITE_DIR / 'content'
STATIC_DIR = SITE_DIR / 'static'
REPORTS_DIR = BASE_DIR / 'data' / 'reports'
PROCESSED_DIR = BASE_DIR / 'data' / 'processed'


class SiteGenerator:
    """静态网站生成器"""
    
    def __init__(self):
        self.today = datetime.now().strftime('%Y-%m-%d')
        
        # 初始化Jinja2环境
        if TEMPLATES_DIR.exists():
            self.env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
        else:
            self.env = None
            logger.warning("模板目录不存在，将使用默认模板")
        
        logger.info(f"初始化网站生成器 - {self.today}")
    
    def load_report_data(self):
        """加载报告数据"""
        data = {}
        
        try:
            # 加载市场报告
            market_files = list(REPORTS_DIR.glob('market_report_*.json'))
            if market_files:
                latest_market = max(market_files, key=lambda p: p.stat().st_mtime)
                with open(latest_market, 'r', encoding='utf-8') as f:
                    data['market'] = json.load(f)
                logger.info(f"加载市场报告: {latest_market.name}")
            
            # 加载VC/PE报告
            vcpe_files = list(REPORTS_DIR.glob('vcpe_report_*.json'))
            if vcpe_files:
                latest_vcpe = max(vcpe_files, key=lambda p: p.stat().st_mtime)
                with open(latest_vcpe, 'r', encoding='utf-8') as f:
                    data['vcpe'] = json.load(f)
                logger.info(f"加载VC/PE报告: {latest_vcpe.name}")
            
            # 加载政策摘要
            policy_files = list((BASE_DIR / 'data' / 'raw' / 'policy').glob('policy_digest_*.md'))
            if policy_files:
                latest_policy = max(policy_files, key=lambda p: p.stat().st_mtime)
                with open(latest_policy, 'r', encoding='utf-8') as f:
                    data['policy'] = f.read()
                logger.info(f"加载政策摘要: {latest_policy.name}")
            
        except Exception as e:
            logger.error(f"加载报告数据失败: {e}")
        
        return data
    
    def generate_index_page(self, data):
        """生成首页"""
        try:
            logger.info("生成首页...")
            
            # 首页HTML内容
            html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>科创金融研究 - 中国科技创新金融研究平台</title>
    <link rel="stylesheet" href="static/css/style.css">
</head>
<body>
    <header>
        <div class="container">
            <h1>科创金融研究</h1>
            <p class="tagline">聚焦中国科技创新金融的独立研究平台</p>
            <nav>
                <ul>
                    <li><a href="index.html" class="active">首页</a></li>
                    <li><a href="star-market.html">科创板</a></li>
                    <li><a href="vcpe.html">VC/PE</a></li>
                    <li><a href="policy.html">政策解读</a></li>
                    <li><a href="research.html">研究笔记</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <main class="container">
        <section class="hero">
            <h2>中国科技金融研究的数据洞察</h2>
            <p>每日自动更新 · 数据分析 · 政策解读 · 投资追踪</p>
            <p class="update-time">数据更新日期: {self.today}</p>
        </section>

        <section class="dashboard">
            <div class="cards">
                <div class="card">
                    <h3>科创板</h3>
                    <div class="metric">
                        <span class="number">560+</span>
                        <span class="label">上市公司</span>
                    </div>
                    <p>实时追踪科创板市场表现、IPO动态和估值水平</p>
                    <a href="star-market.html" class="btn">查看详情 →</a>
                </div>
                
                <div class="card">
                    <h3>VC/PE</h3>
                    <div class="metric">
                        <span class="number">650</span>
                        <span class="label">月度投资事件</span>
                    </div>
                    <p>深度分析投资趋势、热门赛道和活跃机构</p>
                    <a href="vcpe.html" class="btn">查看详情 →</a>
                </div>
                
                <div class="card">
                    <h3>政策解读</h3>
                    <div class="metric">
                        <span class="number">5+</span>
                        <span class="label">周度政策</span>
                    </div>
                    <p>及时解读科技金融政策，分析政策影响</p>
                    <a href="policy.html" class="btn">查看详情 →</a>
                </div>
            </div>
        </section>

        <section class="latest-reports">
            <h2>最新研究报告</h2>
            <div class="report-list">
                <article class="report-item">
                    <h3><a href="reports/market_report_{self.today}.md">科创板市场分析报告 - {self.today}</a></h3>
                    <p class="meta">发布日期: {self.today} | 类型: 市场分析</p>
                    <p class="summary">涵盖科创板估值分析、行业分布、IPO趋势等核心指标</p>
                </article>
                
                <article class="report-item">
                    <h3><a href="reports/vcpe_report_{self.today}.md">VC/PE投资市场分析报告 - {self.today}</a></h3>
                    <p class="meta">发布日期: {self.today} | 类型: 投资分析</p>
                    <p class="summary">深度分析投资事件、热门赛道、活跃机构及市场洞察</p>
                </article>
                
                <article class="report-item">
                    <h3><a href="reports/policy_digest_{self.today}.md">科技金融政策周报 - {self.today}</a></h3>
                    <p class="meta">发布日期: {self.today} | 类型: 政策解读</p>
                    <p class="summary">本周科技金融相关政策梳理和影响分析</p>
                </article>
            </div>
        </section>
    </main>

    <footer>
        <div class="container">
            <p>&copy; 2024 科创金融研究平台 | 数据仅供研究参考</p>
            <p>自动更新于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </footer>
</body>
</html>"""
            
            # 保存首页
            output_file = SITE_DIR / 'index.html'
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"首页已生成: {output_file}")
            
        except Exception as e:
            logger.error(f"生成首页失败: {e}")
    
    def generate_star_market_page(self, data):
        """生成科创板页面"""
        try:
            logger.info("生成科创板页面...")
            
            market_data = data.get('market', {})
            
            html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>科创板分析 - 科创金融研究</title>
    <link rel="stylesheet" href="static/css/style.css">
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
    <header>
        <div class="container">
            <h1>科创金融研究</h1>
            <nav>
                <ul>
                    <li><a href="index.html">首页</a></li>
                    <li><a href="star-market.html" class="active">科创板</a></li>
                    <li><a href="vcpe.html">VC/PE</a></li>
                    <li><a href="policy.html">政策解读</a></li>
                    <li><a href="research.html">研究笔记</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <main class="container">
        <h2>科创板市场分析</h2>
        <p class="update-time">数据更新: {self.today}</p>
        
        <section class="metrics-grid">
            <div class="metric-card">
                <h4>科创50指数</h4>
                <div class="big-number">{market_data.get('market_stats', {}).get('latest_close', 'N/A')}</div>
                <div class="change {'positive' if market_data.get('market_stats', {}).get('latest_change_pct', 0) > 0 else 'negative'}">
                    {market_data.get('market_stats', {}).get('latest_change_pct', 'N/A')}%
                </div>
            </div>
            
            <div class="metric-card">
                <h4>平均市盈率</h4>
                <div class="big-number">{market_data.get('valuation', {}).get('avg_pe', 'N/A') if market_data.get('valuation', {}).get('avg_pe') else 'N/A'}</div>
                <div class="label">倍</div>
            </div>
            
            <div class="metric-card">
                <h4>上市公司数</h4>
                <div class="big-number">560+</div>
                <div class="label">家</div>
            </div>
            
            <div class="metric-card">
                <h4>近12月IPO</h4>
                <div class="big-number">{market_data.get('ipo', {}).get('total_ipo_12m', 'N/A')}</div>
                <div class="label">家</div>
            </div>
        </section>

        <section class="charts">
            <h3>估值分布</h3>
            <div id="valuation-chart" style="width:100%;height:400px;"></div>
            
            <h3>行业分布</h3>
            <div id="industry-chart" style="width:100%;height:400px;"></div>
        </section>

        <section class="report-section">
            <h3>详细报告</h3>
            <p>查看完整的市场分析报告：</p>
            <a href="reports/market_report_{self.today}.md" class="btn" target="_blank">查看报告</a>
        </section>
    </main>

    <footer>
        <div class="container">
            <p>&copy; 2024 科创金融研究平台</p>
        </div>
    </footer>

    <script src="static/js/charts.js"></script>
</body>
</html>"""
            
            output_file = SITE_DIR / 'star-market.html'
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"科创板页面已生成: {output_file}")
            
        except Exception as e:
            logger.error(f"生成科创板页面失败: {e}")
    
    def generate_vcpe_page(self, data):
        """生成VC/PE页面"""
        try:
            logger.info("生成VC/PE页面...")
            
            vcpe_data = data.get('vcpe', {})
            
            html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VC/PE投资 - 科创金融研究</title>
    <link rel="stylesheet" href="static/css/style.css">
</head>
<body>
    <header>
        <div class="container">
            <h1>科创金融研究</h1>
            <nav>
                <ul>
                    <li><a href="index.html">首页</a></li>
                    <li><a href="star-market.html">科创板</a></li>
                    <li><a href="vcpe.html" class="active">VC/PE</a></li>
                    <li><a href="policy.html">政策解读</a></li>
                    <li><a href="research.html">研究笔记</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <main class="container">
        <h2>VC/PE投资市场分析</h2>
        <p class="update-time">数据更新: {self.today}</p>
        
        <section class="metrics-grid">
            <div class="metric-card">
                <h4>月度投资事件</h4>
                <div class="big-number">{vcpe_data.get('market_summary', {}).get('total_deals', 'N/A')}</div>
                <div class="label">起</div>
            </div>
            
            <div class="metric-card">
                <h4>投资总额</h4>
                <div class="big-number">{vcpe_data.get('market_summary', {}).get('total_amount_usd', 'N/A')}</div>
                <div class="label">亿美元</div>
            </div>
            
            <div class="metric-card">
                <h4>同比增长</h4>
                <div class="big-number positive">+{vcpe_data.get('market_summary', {}).get('yoy_growth', 'N/A')}%</div>
                <div class="label">YoY</div>
            </div>
        </section>

        <section class="hot-sectors">
            <h3>热门投资赛道</h3>
            <div class="sector-list">
                {' '.join([f'<span class="sector-tag">{sector}</span>' for sector in vcpe_data.get('sectors', {}).get('hot_sectors', [])[:5]])}
            </div>
        </section>

        <section class="top-investors">
            <h3>活跃投资机构Top 10</h3>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>排名</th>
                        <th>机构名称</th>
                        <th>投资事件</th>
                        <th>投资金额(亿美元)</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join([f"<tr><td>{inv['rank']}</td><td>{inv['investor_name']}</td><td>{inv['deal_count']}</td><td>{inv['total_amount']}</td></tr>" for inv in vcpe_data.get('investors', {}).get('top_investors', [])[:10]])}
                </tbody>
            </table>
        </section>

        <section class="report-section">
            <h3>详细报告</h3>
            <a href="reports/vcpe_report_{self.today}.md" class="btn" target="_blank">查看完整报告</a>
        </section>
    </main>

    <footer>
        <div class="container">
            <p>&copy; 2024 科创金融研究平台</p>
        </div>
    </footer>
</body>
</html>"""
            
            output_file = SITE_DIR / 'vcpe.html'
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"VC/PE页面已生成: {output_file}")
            
        except Exception as e:
            logger.error(f"生成VC/PE页面失败: {e}")
    
    def generate_policy_page(self, data):
        """生成政策页面"""
        try:
            logger.info("生成政策页面...")
            
            policy_content = data.get('policy', '暂无政策数据')
            
            html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>政策解读 - 科创金融研究</title>
    <link rel="stylesheet" href="static/css/style.css">
</head>
<body>
    <header>
        <div class="container">
            <h1>科创金融研究</h1>
            <nav>
                <ul>
                    <li><a href="index.html">首页</a></li>
                    <li><a href="star-market.html">科创板</a></li>
                    <li><a href="vcpe.html">VC/PE</a></li>
                    <li><a href="policy.html" class="active">政策解读</a></li>
                    <li><a href="research.html">研究笔记</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <main class="container">
        <h2>科技金融政策解读</h2>
        <p class="update-time">更新日期: {self.today}</p>
        
        <section class="policy-content">
            <div class="markdown-content">
                <pre>{policy_content}</pre>
            </div>
        </section>
        
        <section class="policy-archive">
            <h3>历史政策周报</h3>
            <ul class="archive-list">
                <li><a href="reports/policy_digest_{self.today}.md">政策周报 - {self.today}</a></li>
            </ul>
        </section>
    </main>

    <footer>
        <div class="container">
            <p>&copy; 2024 科创金融研究平台</p>
        </div>
    </footer>
</body>
</html>"""
            
            output_file = SITE_DIR / 'policy.html'
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"政策页面已生成: {output_file}")
            
        except Exception as e:
            logger.error(f"生成政策页面失败: {e}")
    
    def copy_reports_to_site(self):
        """复制报告到网站目录"""
        try:
            logger.info("复制报告到网站目录...")
            
            # 创建报告目录
            site_reports_dir = SITE_DIR / 'reports'
            site_reports_dir.mkdir(exist_ok=True)
            
            # 复制报告文件
            for report_file in REPORTS_DIR.glob('*.md'):
                import shutil
                shutil.copy2(report_file, site_reports_dir / report_file.name)
                logger.info(f"复制报告: {report_file.name}")
            
        except Exception as e:
            logger.error(f"复制报告失败: {e}")
    
    def run(self):
        """运行网站生成"""
        logger.info("=" * 50)
        logger.info("开始生成静态网站")
        logger.info("=" * 50)
        
        # 加载数据
        data = self.load_report_data()
        
        # 生成各页面
        self.generate_index_page(data)
        self.generate_star_market_page(data)
        self.generate_vcpe_page(data)
        self.generate_policy_page(data)
        
        # 复制报告
        self.copy_reports_to_site()
        
        logger.info("=" * 50)
        logger.info("网站生成完成")
        logger.info(f"网站目录: {SITE_DIR}")
        logger.info("=" * 50)


if __name__ == '__main__':
    generator = SiteGenerator()
    generator.run()
