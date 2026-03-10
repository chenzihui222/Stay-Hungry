# 科技金融数据平台 - 自动更新系统

## 🎯 快速开始

### 安装依赖

```bash
pip install requests beautifulsoup4 apscheduler akshare pandas
```

### 启动自动更新

```bash
python auto_update.py
```

### 手动运行一次

```bash
# 全部更新
python auto_update.py --run-once all

# 单个模块
python auto_update.py --run-once star_market
python auto_update.py --run-once funding
python auto_update.py --run-once policy
```

## ⏰ 定时任务时间表

| 时间 | 任务 | 数据源 | 数据库 |
|------|------|--------|--------|
| 00:30 | 科创板数据 | 上交所/东方财富 | star_market.db |
| 01:00 | VC/PE融资 | 36氪 | funding_data.db |
| 02:00 | 政策文件 | 国务院 | policies.db |
| 08:00 | 数据质检 | - | - |

## 📁 文件结构

```
crawler/
├── auto_update.py          ⭐ 主调度器（运行这个）
├── star_market_simple.py   科创板爬虫
├── k36_simple.py          36氪爬虫
├── policy_simple.py       政策爬虫
├── scheduler.py           定时任务
└── requirements.txt       依赖清单
```

## 🗄️ 数据库

自动创建3个SQLite数据库：

1. **star_market.db** - 科创板公司数据
2. **funding_data.db** - VC/PE融资事件
3. **policies.db** - 政策文件

## 📊 使用示例

### 1. 查看更新状态

```bash
python auto_update.py --status
```

### 2. 查询数据库

```python
import sqlite3

# 查询科创板公司
conn = sqlite3.connect('star_market.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM star_market_companies LIMIT 5')
companies = cursor.fetchall()
conn.close()

# 查询融资事件
conn = sqlite3.connect('funding_data.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM funding_events ORDER BY funding_date DESC LIMIT 5')
fundings = cursor.fetchall()
conn.close()
```

### 3. Linux定时任务（crontab）

```bash
# 每小时检查一次
0 * * * * cd /path/to/crawler && python3 auto_update.py --run-once all
```

## 📝 日志

所有操作记录在：
- `auto_update.log` - 自动更新日志
- `k36_crawler.log` - 36氪爬虫日志
- `policy_crawler.log` - 政策爬虫日志

## 🐳 Docker运行（可选）

```bash
# 构建镜像
docker build -t data-updater .

# 运行容器
docker run -d \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  data-updater
```

## ⚠️ 注意事项

1. **首次运行**: 手动运行一次初始化数据库
2. **网络要求**: 需要访问外网（36氪、上交所等）
3. **运行时间**: 建议在凌晨运行，避开网站高峰
4. **数据备份**: 定期备份 *.db 文件

## 🆘 常见问题

**Q: 如何停止自动更新？**
```bash
# 按 Ctrl+C 或查找进程并终止
ps aux | grep auto_update
kill <PID>
```

**Q: 如何修改定时时间？**
```bash
# 编辑 auto_update.py，修改 CronTrigger
self.scheduler.add_job(
    self.update_star_market,
    CronTrigger(hour=1, minute=0),  # 改为01:00
    id='star_market',
)
```

**Q: 数据库文件在哪里？**
```bash
# 在和爬虫代码相同的目录下
ls -lh *.db
```

## 📚 详细文档

- [AUTO_UPDATE.md](docs/AUTO_UPDATE.md) - 完整文档
- [README.md](README.md) - 科创板爬虫文档
- [POLICY_README.md](POLICY_README.md) - 政策爬虫文档
- [K36_README.md](K36_README.md) - 36氪爬虫文档

## 🎉 完成！

现在系统会每天自动：
1. ✅ 爬取科创板数据
2. ✅ 爬取VC/PE融资
3. ✅ 爬取政策文件
4. ✅ 更新数据库
5. ✅ 检查数据质量

数据自动保存在SQLite数据库中，网站前端可以直接调用查询。
