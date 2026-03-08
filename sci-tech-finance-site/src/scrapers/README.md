# 科创金融数据抓取系统

统一的数据抓取系统，自动抓取科创板、VC投资、政策数据，输出标准JSON格式。

## 数据格式

统一的数据项格式：

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

## 数据源

### 1. 科创板 (market)
- **上交所科创板**: 上市公司列表、IPO数据、市场行情
- **数据来源**: akshare库 / 上交所官网
- **输出文件**: `market_data_YYYY-MM-DD.json`

### 2. VC投资 (vc)
- **清科**: 投资事件、机构数据
- **IT桔子**: 投资事件、公司数据
- **投资界**: 投融资新闻
- **输出文件**: `vc_data_YYYY-MM-DD.json`

### 3. 政策 (policy)
- **中国政府网**: 科技金融相关政策
- **证监会**: 科创板监管政策
- **科技部**: 科技创新政策
- **输出文件**: `policy_data_YYYY-MM-DD.json`

## 使用方法

### 运行所有抓取器

```bash
cd src
python crawler.py
```

### 运行单个抓取器

```bash
# 只抓取科创板数据
python crawler.py --type market

# 只抓取VC投资数据
python crawler.py --type vc

# 只抓取政策数据
python crawler.py --type policy
```

### 指定输出目录

```bash
python crawler.py --output /path/to/data
```

## 输出文件

数据文件保存在 `data/raw/` 目录下：

```
data/raw/
├── market/              # 科创板数据
│   ├── marketscraper_YYYY-MM-DD.json
│   └── marketscraper_YYYY-MM-DD.ndjson
├── vc/                  # VC投资数据
│   ├── vcscraper_YYYY-MM-DD.json
│   └── vcscraper_YYYY-MM-DD.ndjson
├── policy/              # 政策数据
│   ├── policyscraper_YYYY-MM-DD.json
│   └── policyscraper_YYYY-MM-DD.ndjson
├── merged/              # 合并数据
│   ├── all_data_YYYY-MM-DD.json
│   ├── market_data_YYYY-MM-DD.json
│   ├── vc_data_YYYY-MM-DD.json
│   └── policy_data_YYYY-MM-DD.json
└── reports/             # 统计报告
    ├── crawler_report_YYYY-MM-DD.json
    └── latest_report.json
```

## 文件格式说明

### JSON格式
每个抓取器生成独立的JSON文件，包含元数据和items数组：

```json
{
  "scraper_type": "MarketScraper",
  "scrape_date": "2026-03-08",
  "total_items": 100,
  "items": [...]
}
```

### NDJSON格式
每行一个JSON对象，便于流式处理：

```
{"id": "xxx", "date": "2026-03-08", ...}
{"id": "yyy", "date": "2026-03-08", ...}
```

## 自动更新

GitHub Actions 每天自动运行（北京时间08:00）：

1. 抓取最新数据
2. 去重处理
3. 生成统计报告
4. 提交数据更新

也可以手动触发：
- 进入 GitHub Actions
- 选择 "自动更新科创金融研究网站"
- 点击 "Run workflow"

## 模块架构

```
scrapers/
├── base_scraper.py      # 基类模块
├── market_scraper.py    # 科创板抓取器
├── vc_scraper.py        # VC投资抓取器
└── policy_scraper.py    # 政策抓取器

crawler.py               # 主运行脚本
```

## 依赖安装

```bash
pip install -r requirements.txt
```

主要依赖：
- requests: HTTP请求
- beautifulsoup4: HTML解析
- pandas: 数据处理
- akshare: 金融数据接口

## 注意事项

1. **数据量限制**: 每个源默认抓取前15-20条数据，避免过载
2. **备用数据**: 如果数据源不可用，会使用示例数据作为备用
3. **日期格式**: 所有日期统一为 YYYY-MM-DD 格式
4. **去重**: 相同标题和日期的数据会自动去重
5. **增量更新**: 建议每天运行，获取最新数据
