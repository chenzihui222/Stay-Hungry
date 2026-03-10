# 自动更新系统

科技金融数据平台 - 自动更新系统

## 📋 系统概述

整合所有数据爬虫（科创板、VC/PE、政策），实现每日自动更新。

## 🗂️ 项目结构

```
crawler/                          # 爬虫目录
├── auto_update.py                # ⭐ 主调度器（自动更新系统入口）
├── config.py                     # 配置文件
├── requirements.txt              # Python依赖
│
├── spiders/                      # 爬虫模块目录
│   ├── __init__.py
│   ├── star_market_simple.py     # 科创板爬虫
│   ├── k36_simple.py             # 36氪VC/PE爬虫
│   └── policy_simple.py          # 政策爬虫
│
├── database/                     # 数据库相关
│   ├── __init__.py
│   ├── models.py                 # 数据模型
│   └── manager.py                # 数据库管理
│
├── api/                          # API接口（FastAPI）
│   ├── __init__.py
│   ├── main.py                   # FastAPI入口
│   └── routers/
│       ├── star_market.py        # 科创板API
│       ├── funding.py            # 融资数据API
│       └── policy.py             # 政策API
│
├── logs/                         # 日志目录
│   ├── auto_update.log           # 自动更新日志
│   ├── crawler.log               # 爬虫日志
│   └── scheduler.log             # 调度器日志
│
├── data/                         # 数据目录
│   ├── star_market.db            # 科创板数据库
│   ├── funding_data.db           # 融资数据库
│   └── policies.db               # 政策数据库
│
├── docs/                         # 文档
│   ├── README.md                 # 主文档
│   ├── API.md                    # API文档
│   └── DEPLOY.md                 # 部署文档
│
└── scripts/                      # 脚本工具
    ├── init_db.py                # 初始化数据库
    ├── backup.sh                 # 备份脚本
    └── health_check.py           # 健康检查

backend/                          # 后端服务目录
└── ...                           # FastAPI项目（可选单独部署）

frontend/                         # 前端目录
└── ...                           # Next.js项目
```

## ⚙️ 定时任务配置

| 时间 | 任务 | 说明 |
|------|------|------|
| 00:30 | 科创板数据更新 | 获取科创板实时行情 |
| 01:00 | VC/PE融资数据更新 | 获取36氪融资新闻 |
| 02:00 | 政策数据更新 | 获取国务院政策文件 |
| 08:00 | 数据质量检查 | 检查数据完整性 |

## 🚀 安装和运行

### 1. 安装依赖

```bash
cd crawler
pip install -r requirements.txt
```

### 2. 初始化数据库

```bash
python scripts/init_db.py
```

### 3. 启动自动更新系统

#### 方式一：后台运行（推荐）

```bash
# Linux/Mac
nohup python auto_update.py > logs/auto_update.log 2>&1 &

# 或使用 supervisor
supervisorctl start data-updater
```

#### 方式二：Docker运行

```bash
docker-compose up -d
```

#### 方式三：手动运行一次

```bash
# 运行全部更新
python auto_update.py --run-once all

# 只更新科创板
python auto_update.py --run-once star_market

# 只更新VC/PE
python auto_update.py --run-once funding

# 只更新政策
python auto_update.py --run-once policy
```

### 4. 查看状态

```bash
python auto_update.py --status
```

## 📊 API接口

### 启动API服务

```bash
# 方式一：直接运行
python api/main.py

# 方式二：使用uvicorn
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

### API端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/v1/star-market` | GET | 获取科创板数据 |
| `/api/v1/funding` | GET | 获取融资数据 |
| `/api/v1/policies` | GET | 获取政策数据 |
| `/api/v1/status` | GET | 获取系统状态 |

### 示例请求

```bash
# 获取科创板列表
curl http://localhost:8000/api/v1/star-market

# 获取融资数据（分页）
curl "http://localhost:8000/api/v1/funding?page=1&size=20"

# 获取最近政策
curl "http://localhost:8000/api/v1/policies?days=7"

# 获取系统状态
curl http://localhost:8000/api/v1/status
```

## 🔧 配置说明

### 数据库配置

编辑 `config.py`:

```python
# SQLite配置（默认）
DB_CONFIG = {
    'star_market': 'data/star_market.db',
    'funding': 'data/funding_data.db',
    'policy': 'data/policies.db',
}

# PostgreSQL配置（生产环境）
# DB_CONFIG = {
#     'star_market': 'postgresql://user:pass@localhost/star_market',
#     'funding': 'postgresql://user:pass@localhost/funding',
#     'policy': 'postgresql://user:pass@localhost/policies',
# }
```

### 定时任务配置

编辑 `auto_update.py`:

```python
# 修改调度时间
self.scheduler.add_job(
    self.update_star_market,
    CronTrigger(hour=1, minute=0),  # 改为每天01:00
    id='star_market',
    name='科创板数据更新',
)
```

## 🐳 Docker部署

### 1. 构建镜像

```bash
docker build -t data-updater:latest .
```

### 2. 运行容器

```bash
docker run -d \
  --name data-updater \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  -p 8000:8000 \
  data-updater:latest
```

### 3. Docker Compose

```bash
docker-compose up -d
```

## 📈 监控和日志

### 查看日志

```bash
# 实时查看更新日志
tail -f logs/auto_update.log

# 查看爬虫日志
tail -f logs/crawler.log

# 查看API日志
tail -f logs/api.log
```

### 健康检查

```bash
# 运行健康检查
python scripts/health_check.py

# 输出示例
✅ 科创板数据库: 正常 (586条记录)
✅ 融资数据库: 正常 (1256条记录)
✅ 政策数据库: 正常 (342条记录)
⚠️  最后更新时间: 2小时前
```

## 🔒 安全建议

1. **API认证**: 生产环境启用JWT认证
2. **访问控制**: 限制API访问IP
3. **数据备份**: 定期备份数据库
4. **日志脱敏**: 日志中不记录敏感信息

## 📝 更新日志

### v1.0.0 (2026-03-10)
- 初始版本发布
- 整合科创板、VC/PE、政策三个爬虫
- 实现APScheduler定时调度
- 提供FastAPI接口

## 🆘 故障排查

### 问题1: 定时任务不执行

**检查**:
```bash
# 检查调度器状态
python auto_update.py --status

# 检查日志
tail -f logs/auto_update.log
```

**解决**:
- 确保 `auto_update.py` 正在运行
- 检查系统时间是否正确
- 查看是否有异常报错

### 问题2: 数据库连接失败

**检查**:
```bash
# 检查数据库文件是否存在
ls -lh data/*.db

# 检查权限
chmod 755 data/
```

### 问题3: 爬虫获取数据为空

**检查**:
```bash
# 手动运行爬虫测试
python spiders/star_market_simple.py

# 检查网络连接
curl -I https://36kr.com/feed
```

## 📞 支持

如有问题，请：
1. 查看日志文件
2. 检查配置文件
3. 提交Issue

---

**系统架构**: Python + APScheduler + FastAPI + SQLite/PostgreSQL  
**运行环境**: Linux/macOS/Windows + Python 3.8+  
**维护团队**: Data Engineering Team
