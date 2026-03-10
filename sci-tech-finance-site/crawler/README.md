# 科创板数据爬虫

科创板（STAR Market）上市公司数据采集系统

## 📋 功能特性

- ✅ **实时数据获取**：使用 AKShare 获取科创板实时行情
- ✅ **多数据源支持**：上交所官方 API + 财经数据接口
- ✅ **数据持久化**：支持 SQLite / PostgreSQL
- ✅ **增量更新**：智能去重，支持数据更新
- ✅ **多格式导出**：JSON / CSV / Excel
- ✅ **完整日志**：记录爬取过程和错误信息

## 🔧 采集字段

| 字段名 | 说明 | 示例 |
|--------|------|------|
| stock_code | 股票代码 | 688981 |
| stock_name | 公司名称 | 中芯国际 |
| industry | 所属行业 | 半导体 |
| market_cap | 总市值（亿元） | 4256.32 |
| listing_date | 上市日期 | 2020-07-16 |
| price | 当前股价 | 53.28 |
| change_pct | 涨跌幅(%) | 2.35 |
| volume | 成交量（万股） | 125.6 |

## 📦 安装依赖

```bash
cd crawler
pip install -r requirements.txt
```

## 🚀 快速开始

### 方法1：使用简化版（推荐新手）

```bash
python star_market_simple.py
```

### 方法2：使用完整版（推荐生产环境）

```bash
python star_market_crawler.py
```

## 📊 输出文件

运行后会生成以下文件：

- `star_market.db` - SQLite 数据库文件
- `star_market_data.json` - JSON 格式数据
- `star_market_data.csv` - CSV 格式数据
- `crawler.log` - 爬虫运行日志

## 🗄️ 数据库表结构

```sql
CREATE TABLE star_market_companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stock_code TEXT UNIQUE NOT NULL,
    stock_name TEXT NOT NULL,
    industry TEXT,
    market_cap REAL,
    listing_date TEXT,
    price REAL,
    change_pct REAL,
    volume REAL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

## 🔍 数据来源

1. **AKShare** (主要)
   - 东方财富科创板实时行情
   - 接口：`stock_zh_kcb_spot_em()`

2. **上海证券交易所** (补充)
   - 科创板 IPO 信息
   - 上市日期数据

## ⚙️ 配置说明

编辑 `star_market_crawler.py`：

```python
# 数据库类型: "sqlite" 或 "postgresql"
DB_TYPE = "sqlite"

# SQLite 数据库路径
DB_PATH = "star_market.db"

# PostgreSQL 连接URL（如使用PostgreSQL）
DB_URL = "postgresql://user:password@localhost:5432/stock_db"
```

## 📈 使用示例

### 1. 查询数据库

```python
import sqlite3

conn = sqlite3.connect('star_market.db')
cursor = conn.cursor()

# 查询所有公司
cursor.execute('SELECT * FROM star_market_companies')
companies = cursor.fetchall()

# 查询市值前10
cursor.execute('''
    SELECT stock_name, market_cap 
    FROM star_market_companies 
    ORDER BY market_cap DESC 
    LIMIT 10
''')
top10 = cursor.fetchall()

conn.close()
```

### 2. 定时运行（Linux/Mac）

添加 crontab 任务，每天 9:30 自动运行：

```bash
# 编辑 crontab
crontab -e

# 添加以下行（每天9:30执行）
30 9 * * * cd /path/to/crawler && /usr/bin/python3 star_market_simple.py >> /var/log/star_market_cron.log 2>&1
```

### 3. 集成到现有项目

```python
from star_market_crawler import StarMarketCrawler, DatabaseManager

# 初始化
db = DatabaseManager(db_type="sqlite", db_path="my.db")
crawler = StarMarketCrawler(db)

# 运行爬取
crawler.run(use_akshare=True)

# 获取数据
companies = db.get_all_companies()
print(f"共有 {len(companies)} 家公司")
```

## 🐛 常见问题

### Q1: 安装 akshare 失败？

```bash
# 升级 pip
pip install --upgrade pip

# 使用国内镜像安装
pip install akshare -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q2: 运行时报 SSL 错误？

```bash
# macOS
brew install ca-certificates

# Linux
sudo apt-get install ca-certificates
```

### Q3: 如何只获取部分字段？

修改 `process_data` 函数，保留需要的字段即可。

## 📚 技术栈

- **Python 3.8+**
- **AKShare** - 财经数据接口
- **SQLAlchemy** - ORM 框架
- **Pandas** - 数据处理
- **Requests** - HTTP 请求
- **BeautifulSoup** - HTML 解析

## 📝 更新日志

### v1.0.0 (2026-03-10)
- 初始版本发布
- 支持科创板数据爬取
- 支持 SQLite/PostgreSQL
- 支持 JSON/CSV 导出

## ⚠️ 免责声明

本爬虫仅供学习研究使用，获取的数据仅供参考，不构成投资建议。
请遵守相关法律法规，不要频繁请求以免对数据源造成压力。

## 📞 联系方式

如有问题，请提交 Issue 或联系开发团队。

---

**数据来源**: 上海证券交易所、东方财富
**更新频率**: 建议每日一次（交易日 9:30 后）
