# 科创金融研究网站

一个聚焦中国科技创新金融（Sci-Tech Finance）的自动化研究平台。

## 功能模块

### 1. 科创板数据分析
- 自动抓取科创板上市公司数据
- IPO 统计分析
- 行业分布与估值跟踪

### 2. VC/PE 投资市场动态
- 投资事件追踪
- 热门赛道分析
- 投资机构排名

### 3. 政策解读
- 科技金融政策抓取
- 智能摘要生成
- 影响分析

### 4. 研究笔记
- 市场观察记录
- 深度研究报告
- 数据洞察分享

### 5. 数据可视化
- 交互式图表
- 实时数据看板
- 趋势分析报告

## 技术栈

- **数据抓取**: Python + requests + BeautifulSoup + akshare
- **数据分析**: pandas + numpy + matplotlib + plotly
- **报告生成**: Jinja2 + Markdown
- **静态网站**: 纯 HTML/CSS/JS
- **自动化**: GitHub Actions
- **部署**: GitHub Pages

## 项目结构

```
sci-tech-finance-site/
├── data/                   # 数据目录
│   ├── raw/               # 原始数据
│   ├── processed/         # 处理后数据
│   └── reports/           # 生成的报告
├── src/                   # 源代码
│   ├── scrapers/          # 数据抓取脚本
│   ├── analyzers/         # 数据分析脚本
│   └── generators/        # 网站生成器
├── site/                  # 网站内容
│   ├── content/           # 内容文件
│   ├── templates/         # HTML模板
│   └── static/            # 静态资源
├── .github/workflows/     # GitHub Actions
├── docs/                  # 文档
└── tests/                 # 测试
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行数据抓取

```bash
python src/scrapers/star_market.py
python src/scrapers/vc_pe_tracker.py
python src/scrapers/policy_monitor.py
```

### 3. 生成分析报告

```bash
python src/analyzers/market_analyzer.py
python src/analyzers/vcpe_analyzer.py
```

### 4. 生成网站

```bash
python src/generators/site_generator.py
```

### 5. 本地预览

```bash
cd site && python -m http.server 8000
```

## 自动化流程

项目配置了 GitHub Actions 实现完全自动化：

1. **每日 08:00**: 自动抓取最新数据
2. **每日 09:00**: 自动生成分析报告
3. **每日 10:00**: 自动更新网站并部署

## 数据源

- 上海证券交易所 (SSE)
- 东方财富网
- 投中网
- 中国政府网政策库
- 其他公开数据源

## 许可证

MIT License

## 联系方式

如有问题或建议，欢迎提交 Issue 或 PR。
