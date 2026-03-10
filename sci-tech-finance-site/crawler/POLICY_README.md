# 国务院政策爬虫

国务院政策文件库自动采集系统

## 📋 功能特性

- ✅ **权威数据源**: 国务院官网 (gov.cn)
- ✅ **智能去重**: URL MD5 哈希去重机制
- ✅ **每日更新**: APScheduler 定时任务
- ✅ **数据持久化**: SQLite / PostgreSQL 支持
- ✅ **增量爬取**: 只采集新发布政策
- ✅ **完整日志**: 记录爬取过程和错误

## 📊 采集字段

| 字段名 | 说明 | 示例 |
|--------|------|------|
| title | 政策名称 | 关于进一步优化营商环境降低市场主体制度性交易成本的意见 |
| publish_date | 发布时间 | 2026-03-10 |
| source | 发布机构 | 国务院办公厅 |
| summary | 政策摘要 | 为深入贯彻党中央、国务院决策部署... |
| url | 政策链接 | https://www.gov.cn/zhengce/... |
| content | 政策正文 | （可选）完整正文内容 |
| tags | 关键词标签 | ["营商环境", "制度改革"] |

## 🗄️ 数据库表结构

```sql
CREATE TABLE policies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,              -- 政策名称
    publish_date TEXT,                -- 发布时间
    source TEXT,                      -- 发布机构
    summary TEXT,                     -- 摘要
    url TEXT UNIQUE NOT NULL,         -- 链接
    url_hash TEXT UNIQUE NOT NULL,    -- URL哈希（去重）
    content TEXT,                     -- 正文（可选）
    tags TEXT,                        -- 标签JSON
    is_valid BOOLEAN DEFAULT TRUE,    -- 是否有效
    crawl_status TEXT,                -- 爬取状态
    created_at TIMESTAMP,             -- 创建时间
    updated_at TIMESTAMP,             -- 更新时间
    last_crawled_at TIMESTAMP         -- 最后爬取时间
);
```

## 🚀 使用方法

### 1. 安装依赖

```bash
cd crawler
pip install -r requirements.txt
```

### 2. 运行爬虫

#### 方式一：简化版（推荐新手）

```bash
python policy_simple.py
```

**功能**:
- 爬取前3页政策
- 自动去重
- 保存到 SQLite
- 导出 JSON

#### 方式二：完整版（生产环境）

```bash
# 基本运行
python policy_crawler.py

# 带参数运行
python policy_crawler.py --pages 5 --detail --export

# 参数说明
--pages, -p    爬取页数（默认5页）
--detail, -d   获取详情页内容
--export, -e   导出数据到JSON/CSV
--daily        每日更新模式
```

#### 方式三：定时自动更新

```bash
# 启动定时调度器（每天09:00自动更新）
python scheduler.py
```

## 📁 输出文件

运行后会生成：

- `policies.db` - SQLite 数据库
- `policies.json` - JSON 格式数据
- `policies.csv` - CSV 格式数据
- `policy_crawler.log` - 爬取日志

## 📊 数据结构示例

```json
{
  "export_time": "2026-03-10T18:50:00",
  "total_count": 156,
  "data_source": "国务院政策文件库",
  "url": "https://www.gov.cn/zhengce/",
  "data": [
    {
      "id": 1,
      "title": "关于进一步优化营商环境降低市场主体制度性交易成本的意见",
      "publish_date": "2026-03-10",
      "source": "国务院办公厅",
      "summary": "为深入贯彻党中央、国务院决策部署...",
      "url": "https://www.gov.cn/zhengce/2026-03/10/content_12345678.htm",
      "tags": ["营商环境", "制度改革", "市场主体"],
      "created_at": "2026-03-10T18:50:00"
    }
  ]
}
```

## 🔍 去重机制

```python
# 1. URL MD5 哈希生成
url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()

# 2. 数据库唯一索引约束
CREATE UNIQUE INDEX idx_url_hash ON policies(url_hash);

# 3. 插入前检查
INSERT OR IGNORE INTO policies ...
```

## ⏰ 定时任务配置

### Linux/Mac (crontab)

```bash
# 编辑 crontab
crontab -e

# 每天 09:00 执行
0 9 * * * cd /path/to/crawler && /usr/bin/python3 policy_simple.py >> /var/log/policy_cron.log 2>&1

# 或每小时执行一次
0 * * * * cd /path/to/crawler && /usr/bin/python3 policy_simple.py >> /var/log/policy_cron.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器：每天 09:00
4. 设置操作：启动程序 `python.exe`
5. 参数：`policy_simple.py`
6. 起始于：`C:\path\to\crawler`

## 🔧 高级用法

### 自定义爬取页数

```python
from policy_crawler import PolicyCrawler, PolicyDatabase

# 初始化
db = PolicyDatabase()
crawler = PolicyCrawler(db)

# 爬取10页
crawler.run(max_pages=10, fetch_detail=True)
```

### 查询最近政策

```python
import sqlite3

conn = sqlite3.connect('policies.db')
cursor = conn.cursor()

# 最近7天的政策
cursor.execute('''
    SELECT * FROM policies 
    WHERE publish_date >= date('now', '-7 days')
    ORDER BY publish_date DESC
''')

policies = cursor.fetchall()
conn.close()
```

### 导出指定日期范围

```python
from policy_crawler import PolicyExporter, PolicyDatabase

db = PolicyDatabase()
exporter = PolicyExporter(db)

# 导出最近30天的政策
exporter.export_to_json('policies_recent.json', days=30)
```

## 🛡️ 反爬虫策略

### 已实现的措施

1. **请求间隔**: 每次请求间隔 1-2 秒
2. **随机 User-Agent**: 模拟真实浏览器
3. **失败重试**: 最多重试 3 次，指数退避
4. **Referer 设置**: 模拟正常访问路径

### 建议的额外措施

```python
# 1. 使用代理池
proxies = {
    'http': 'http://proxy.example.com:8080',
    'https': 'https://proxy.example.com:8080'
}

# 2. 限制爬取频率
max_pages = 5  # 每次最多5页

# 3. 错峰爬取
# 避开工作时间（9:00-18:00）
# 建议在早上6:00或晚上22:00执行
```

## 🐛 常见问题

### Q1: 爬取结果为空？

**原因**: 政府网站结构可能更新

**解决**: 
```bash
# 检查网页结构是否变化
curl -s http://sousuo.gov.cn/column/30412/0.htm | grep -o '<li>.*</li>' | head -5

# 更新选择器（编辑 policy_crawler.py）
list_items = soup.select('.list li')  # 根据实际结构调整
```

### Q2: 如何只爬取特定机构的政策？

```python
# 在 parse_list_page 中添加过滤
if policy.source and '科技部' in policy.source:
    policies.append(policy)
```

### Q3: 如何获取政策正文内容？

```bash
# 运行完整版并开启详情获取
python policy_crawler.py --detail

# 这会访问每个政策的详情页，提取完整正文
# 注意：会增加爬取时间和网络请求
```

## 📈 监控指标

爬虫运行后会输出统计信息：

```
============================================================
爬取完成!
总计获取: 50 条
新增: 12 条
更新: 3 条
跳过(重复): 35 条
失败: 0 条
============================================================
```

## ⚠️ 免责声明

1. 本爬虫仅供学习研究使用
2. 请遵守《中华人民共和国网络安全法》
3. 请控制爬取频率，不要对政府网站造成压力
4. 获取的政策数据仅供参考，以官方发布为准
5. 建议使用代理IP并控制并发数

## 📚 参考资料

- [国务院政策文件库](https://www.gov.cn/zhengce/zhengceku/)
- [Requests 文档](https://docs.python-requests.org/)
- [BeautifulSoup 文档](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [APScheduler 文档](https://apscheduler.readthedocs.io/)

## 📝 更新日志

### v1.0.0 (2026-03-10)
- 初始版本发布
- 支持国务院政策爬取
- 实现 URL 哈希去重
- 支持每日定时更新

## 📞 联系方式

如有问题请提交 Issue

---

**数据源**: 中华人民共和国中央人民政府网  
**更新频率**: 建议每日一次（早上09:00）  
**数据时效**: 实时同步国务院最新政策
