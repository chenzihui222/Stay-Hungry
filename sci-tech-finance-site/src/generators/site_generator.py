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
import shutil
from datetime import datetime
from pathlib import Path
import pandas as pd

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 项目根目录
BASE_DIR = Path(__file__).parent.parent.parent
SITE_DIR = BASE_DIR / 'site'
REPORTS_DIR = BASE_DIR / 'data' / 'reports'
PROCESSED_DIR = BASE_DIR / 'data' / 'processed'

# 网站配置
SITE_TITLE = "Stay Hungry"
SITE_TAGLINE = "聚焦中国科技创新金融的独立学习研究平台"
SITE_AUTHOR = "Stay Hungry Team"


class SiteGenerator:
    """静态网站生成器"""
    
    def __init__(self):
        self.today = datetime.now().strftime('%Y-%m-%d')
        logger.info(f"初始化网站生成器 - {self.today}")
    
    def load_report_data(self):
        """加载报告数据"""
        data = {}
        
        try:
            # 加载科创板报告
            star_market_files = list(REPORTS_DIR.glob('star_market_report_*.json'))
            if star_market_files:
                latest_star = max(star_market_files, key=lambda p: p.stat().st_mtime)
                with open(latest_star, 'r', encoding='utf-8') as f:
                    data['star_market'] = json.load(f)
                logger.info(f"加载科创板报告: {latest_star.name}")
            
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
    
    def get_header(self, active_page='index'):
        """生成统一的页头"""
        nav_items = [
            ('index', '首页', 'index.html'),
            ('star-market', '科创板', 'star-market.html'),
            ('vcpe', 'VC/PE', 'vcpe.html'),
            ('policy', '政策解读', 'policy.html'),
            ('research', '研究笔记', 'research.html'),
            ('features', '功能介绍', 'features.html'),
        ]
        
        nav_html = ''
        for page_id, page_name, page_url in nav_items:
            active_class = 'active' if page_id == active_page else ''
            nav_html += f'                    <li><a href="{page_url}" class="{active_class}">{page_name}</a></li>\n'
        
        return f"""    <header style="position: relative;">
        <div class="container">
            <h1>{SITE_TITLE}</h1>
            <p class="tagline">{SITE_TAGLINE}</p>
            <nav>
                <ul>
{nav_html}                </ul>
            </nav>
        </div>
        <div class="user-section" style="position: absolute; top: 20px; right: 20px;">
            <a href="research.html" class="github-login-btn" style="text-decoration: none; display: inline-flex; align-items: center; gap: 8px; padding: 10px 20px; background: linear-gradient(135deg, #24292e, #586069); color: white; border-radius: 8px; font-size: 14px; font-weight: 600;">
                <svg viewBox="0 0 16 16" fill="currentColor" style="width: 20px; height: 20px;">
                    <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
                </svg>
                登录
            </a>
        </div>
    </header>"""
    
    def get_footer(self):
        """生成统一的页脚"""
        return f"""    <footer>
        <div class="container">
            <p>&copy; {datetime.now().year} {SITE_TITLE} | 数据仅供研究参考</p>
            <p>Stay hungry, stay foolish. 保持饥饿，保持愚蠢。</p>
            <p>自动更新于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </footer>"""
    
    def generate_index_page(self, data):
        """生成首页"""
        try:
            logger.info("生成首页...")
            
            html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{SITE_TITLE} - 中国科技创新金融研究平台</title>
    <link rel="stylesheet" href="static/css/style.css">
</head>
<body>
{self.get_header('index')}

    <main class="container">
        <section class="hero">
            <h2>中国科技金融研究的数据洞察</h2>
            <p>每日自动更新 · 数据分析 · 投资追踪 · 政策解读</p>
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

{self.get_footer()}
</body>
</html>"""
            
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
            
            star_data = data.get('star_market', {})
            summary = star_data.get('summary', {})
            top_companies = star_data.get('top_companies', [])
            ipo_data = star_data.get('ipo_data', {})
            
            html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>科创板分析 - {SITE_TITLE}</title>
    <link rel="stylesheet" href="static/css/style.css">
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
{self.get_header('star-market')}

    <main class="container">
        <h2>科创板市场分析</h2>
        <p class="update-time">数据来源: 上海证券交易所 | 更新日期: {self.today}</p>
        
        <section class="metrics-grid">
            <div class="metric-card">
                <h4>上市公司总数</h4>
                <div class="big-number">{summary.get('total_companies', 'N/A')}</div>
                <div class="label">家</div>
            </div>
            
            <div class="metric-card">
                <h4>总市值</h4>
                <div class="big-number">{summary.get('total_market_cap', 'N/A'):.0f}</div>
                <div class="label">亿元</div>
            </div>
            
            <div class="metric-card">
                <h4>平均市值</h4>
                <div class="big-number">{summary.get('avg_market_cap', 'N/A'):.0f}</div>
                <div class="label">亿元</div>
            </div>
            
            <div class="metric-card">
                <h4>覆盖行业</h4>
                <div class="big-number">{summary.get('industry_count', 'N/A')}</div>
                <div class="label">个</div>
            </div>
        </section>

        <section class="charts" style="background: var(--card-bg); padding: 30px; border-radius: 16px; margin: 30px 0;">
            <h3 style="color: var(--primary-dark); margin-bottom: 20px;">📈 近12个月IPO趋势</h3>
            <div id="ipo-chart" style="width:100%;height:400px;"></div>
        </section>

        <section style="background: var(--card-bg); padding: 30px; border-radius: 16px; margin: 30px 0; box-shadow: 0 4px 6px -1px rgba(249, 115, 22, 0.1);">
            <h3 style="color: var(--primary-dark); margin-bottom: 25px;">🏆 市值Top 10公司</h3>
            <table class="data-table">
                <thead>
                    <tr>
                        <th style="width: 60px;">排名</th>
                        <th>代码</th>
                        <th>名称</th>
                        <th>行业</th>
                        <th style="text-align: right;">市值(亿元)</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join([f"<tr><td>{idx}</td><td>{comp['code']}</td><td><strong>{comp['name']}</strong></td><td>{comp['industry']}</td><td style='text-align: right; font-weight: 600; color: var(--primary-color);'>{comp['market_cap']:.2f}</td></tr>" for idx, comp in enumerate(top_companies[:10], 1)]) if top_companies else '<tr><td colspan="5" style="text-align: center; color: var(--text-muted);">暂无数据</td></tr>'}
                </tbody>
            </table>
        </section>

        <section class="report-section" style="text-align: center; padding: 40px;">
            <h3 style="margin-bottom: 20px;">查看完整市场分析报告</h3>
            <p style="color: var(--text-muted); margin-bottom: 25px;">获取详细的行业分布、IPO分析和市场洞察</p>
            <a href="report-viewer.html?file=star_market_report_{self.today}.md" class="btn" target="_blank" style="padding: 15px 40px; font-size: 16px;">📊 查看详细报告</a>
        </section>
    </main>

{self.get_footer()}

    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <script>
        // IPO趋势图表
        const ipoData = {ipo_data};
        if (ipoData && ipoData.months) {{
            const trace1 = {{
                x: ipoData.months,
                y: ipoData.ipo_counts,
                type: 'bar',
                name: 'IPO数量',
                marker: {{
                    color: '#f97316',
                    opacity: 0.8
                }}
            }};
            
            const layout = {{
                title: '科创板IPO发行数量趋势',
                xaxis: {{ title: '月份' }},
                yaxis: {{ title: 'IPO数量(家)' }},
                font: {{ family: '-apple-system, BlinkMacSystemFont, sans-serif' }},
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)'
            }};
            
            Plotly.newPlot('ipo-chart', [trace1], layout, {{responsive: true}});
        }}
    </script>
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
    <title>VC/PE投资 - {SITE_TITLE}</title>
    <link rel="stylesheet" href="static/css/style.css">
</head>
<body>
{self.get_header('vcpe')}

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
            <a href="report-viewer.html?file=vcpe_report_{self.today}.md" class="btn" target="_blank">查看完整报告</a>
        </section>

        <section class="data-source-section">
            <h3>数据来源</h3>
            <p class="data-source-description">本页面数据来源于以下权威投资数据平台：</p>
            <div class="data-source-links">
                <a href="https://www.chinaventure.com.cn/" target="_blank" class="data-source-link">
                    <span class="source-name">投中网</span>
                    <span class="source-desc">中国创业投资行业权威数据平台</span>
                </a>
                <a href="https://www.itjuzi.com/" target="_blank" class="data-source-link">
                    <span class="source-name">IT桔子</span>
                    <span class="source-desc">中国新经济创投数据服务商</span>
                </a>
                <a href="https://www.36kr.com/" target="_blank" class="data-source-link">
                    <span class="source-name">36氪</span>
                    <span class="source-desc">新经济创投媒体与数据平台</span>
                </a>
                <a href="https://www.pedata.cn/" target="_blank" class="data-source-link">
                    <span class="source-name">清科研究中心</span>
                    <span class="source-desc">股权投资市场权威研究机构</span>
                </a>
            </div>
        </section>
    </main>

{self.get_footer()}
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
    <title>政策解读 - {SITE_TITLE}</title>
    <link rel="stylesheet" href="static/css/style.css">
</head>
<body>
{self.get_header('policy')}

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

{self.get_footer()}
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
