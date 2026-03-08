# 科创金融数据抓取系统

## 系统概述

一个统一的科创金融数据抓取系统，自动从多个数据源抓取数据，输出标准JSON格式，支持自动更新。

## 数据源

### 1. 科创板 (market)
- **上交所科创板**: 上市公司列表、IPO数据、市场行情
- **数据源**: akshare库 / 上交所官网
- **覆盖**: 560+科创板上市公司

### 2. VC投资 (vc)
- **清科**: 投资事件、机构数据
- **IT桔子**: 投资事件、公司数据
- **投资界**: 投融资新闻
- **覆盖**: 月度投资事件追踪

### 3. 政策 (policy)
- **中国政府网**: 科技金融相关政策
- **证监会**: 科创板监管政策
- **科技部**: 科技创新政策
- **覆盖**: 周度政策监控

## 统一数据格式

```json
{
  "id": "唯一标识符",
  "date": "YYYY-MM-DD",
  "title": "数据标题",
  "type": "market/vc/policy",
  "content": "详细内容",
  "source": "数据来源",
  "url": "原文链接",
  "tags": ["标签1", "标签2"],
  "metadata": {额外元数据},
  "created_at": "抓取时间"
}
```

## 文件结构

```
src/
├── crawler.py                 # 主运行脚本
└── scrapers/
    ├── __init__.py           # 包初始化
    ├── README.md             # 抓取器文档
    ├── base_scraper.py       # 基类模块
    │   ├── DataItem          # 数据项类
    │   ├── BaseScraper       # 抓取器基类
    │   └── DataMerger        # 数据合并器
    ├── market_scraper.py     # 科创板抓取器
    ├── vc_scraper.py         # VC投资抓取器
    └── policy_scraper.py     # 政策抓取器
```

## 使用方法

### 快速开始

```bash
cd src

# 运行所有抓取器
python crawler.py

# 只抓取科创板数据
python crawler.py --type market

# 只抓取VC投资数据
python crawler.py --type vc

# 只抓取政策数据
python crawler.py --type policy

# 指定输出目录
python crawler.py --output /path/to/data
```

### 输出文件

数据文件保存在 `data/raw/` 目录下：

```
data/raw/
├── market/                   # 科创板数据
│   ├── marketscraper_YYYY-MM-DD.json
│   └── marketscraper_YYYY-MM-DD.ndjson
├── vc/                       # VC投资数据
│   ├── vcscraper_YYYY-MM-DD.json
│   └── vcscraper_YYYY-MM-DD.ndjson
├── policy/                   # 政策数据
│   ├── policyscraper_YYYY-MM-DD.json
│   └── policyscraper_YYYY-MM-DD.ndjson
├── merged/                   # 合并数据
│   ├── all_data_YYYY-MM-DD.json
│   ├── market_data_YYYY-MM-DD.json
│   ├── vc_data_YYYY-MM-DD.json
│   └── policy_data_YYYY-MM-DD.json
└── reports/                  # 统计报告
    ├── crawler_report_YYYY-MM-DD.json
    └── latest_report.json
```

## 自动更新配置

GitHub Actions 每天自动运行：

1. **定时触发**: 每天北京时间 08:00 (UTC 00:00)
2. **手动触发**: 支持在 GitHub Actions 页面手动运行
3. **推送触发**: 代码推送到 main/master 分支时触发

配置文件: `.github/workflows/auto-update.yml`

### 手动运行

1. 进入 GitHub 仓库
2. 点击 "Actions" 标签
3. 选择 "自动更新科创金融研究网站"
4. 点击 "Run workflow"
5. 选择要运行的抓取器类型 (all/market/vc/policy)
6. 点击 "Run workflow" 按钮

## 测试

运行测试脚本：

```bash
python test_crawler.py
```

测试内容包括：
- DataItem 数据项创建
- MarketScraper 科创板抓取器
- VCScraper VC投资抓取器
- PolicyScraper 政策抓取器
- DataMerger 数据合并器

## 技术栈

- **Python 3.10+**: 核心语言
- **requests**: HTTP请求
- **beautifulsoup4**: HTML解析
- **pandas**: 数据处理
- **akshare**: 金融数据接口
- **GitHub Actions**: 自动化部署

## 依赖安装

```bash
pip install -r requirements.txt
```

requirements.txt:
```
requests>=2.28.0
beautifulsoup4>=4.11.0
pandas>=1.5.0
akshare>=1.10.0
lxml>=4.9.0
```

## 数据特点

1. **统一格式**: 所有数据统一为JSON格式，便于处理和分析
2. **自动去重**: 相同标题和日期的数据自动去重
3. **日期标准化**: 所有日期统一为 YYYY-MM-DD 格式
4. **标签系统**: 每条数据都有标签，便于分类和搜索
5. **元数据支持**: 支持存储额外结构化数据
6. **双格式输出**: 同时输出JSON和NDJSON格式

## 扩展指南

### 添加新的数据源

1. 在 `src/scrapers/` 创建新的抓取器类，继承 `BaseScraper`
2. 实现 `scrape()` 方法，返回 `List[DataItem]`
3. 在 `crawler.py` 中导入并初始化新的抓取器

示例：

```python
from .base_scraper import BaseScraper, DataItem

class MyScraper(BaseScraper):
    def scrape(self) -> List[DataItem]:
        items = []
        # 抓取逻辑
        item = DataItem(
            date="2026-03-08",
            title="示例",
            type="market",
            content="内容",
            source="我的数据源"
        )
        items.append(item)
        return items
```

## 注意事项

1. **数据量限制**: 每个源默认抓取前15-20条数据，避免过载
2. **备用数据**: 如果数据源不可用，会使用示例数据作为备用
3. **增量更新**: 建议每天运行，获取最新数据
4. **错误处理**: 所有抓取器都有错误处理机制，单个抓取失败不影响其他
5. **日志记录**: 所有操作都会记录到日志，便于排查问题

## License

MIT License
