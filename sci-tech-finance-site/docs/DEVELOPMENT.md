# 开发指南

## 项目架构

本项目采用模块化设计，分为以下几个层次：

### 1. 数据抓取层 (Scrapers)

负责从各种数据源获取原始数据。

- **star_market.py**: 科创板数据抓取
- **vc_pe_tracker.py**: VC/PE投资数据抓取
- **policy_monitor.py**: 政策数据监控

### 2. 数据分析层 (Analyzers)

负责处理和分析抓取的数据。

- **market_analyzer.py**: 科创板市场分析
- **vcpe_analyzer.py**: VC/PE投资分析

### 3. 网站生成层 (Generators)

负责生成静态网站。

- **site_generator.py**: 网站生成器

### 4. 自动化层 (Workflows)

GitHub Actions 工作流实现全自动运行。

## 添加新的数据源

### 步骤 1: 创建抓取脚本

在 `src/scrapers/` 目录下创建新的 Python 文件：

```python
#!/usr/bin/env python3
"""
新数据源抓取模块
"""

import logging
from datetime import datetime
from pathlib import Path
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / 'data' / 'raw' / 'new_source'
DATA_DIR.mkdir(parents=True, exist_ok=True)

class NewSourceScraper:
    def __init__(self):
        self.today = datetime.now().strftime('%Y-%m-%d')
    
    def fetch_data(self):
        """抓取数据"""
        # 实现数据抓取逻辑
        pass
    
    def run(self):
        """运行抓取任务"""
        logger.info(f"开始抓取新数据源 - {self.today}")
        self.fetch_data()
        logger.info("抓取完成")

if __name__ == '__main__':
    scraper = NewSourceScraper()
    scraper.run()
```

### 步骤 2: 创建分析脚本

在 `src/analyzers/` 目录下创建对应的分析脚本。

### 步骤 3: 更新网站生成器

在 `src/generators/site_generator.py` 中添加新的页面或组件。

### 步骤 4: 更新工作流

编辑 `.github/workflows/auto-update.yml`，添加新的步骤：

```yaml
- name: 抓取新数据源
  run: |
    echo "开始抓取新数据源..."
    python src/scrapers/new_source.py
```

## 自定义报告模板

### 修改报告格式

编辑 `src/analyzers/` 中的分析脚本，修改 Markdown 报告生成部分：

```python
def generate_report(self):
    report_lines = [
        "# 报告标题",
        f"\n**日期**: {self.today}",
        "\n## 章节标题\n",
        "内容..."
    ]
    
    report_content = ''.join(report_lines)
    
    # 保存报告
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_content)
```

### 修改网站样式

编辑 `site/static/css/style.css`：

```css
/* 添加自定义样式 */
.custom-class {
    color: #your-color;
    font-size: 16px;
}
```

## 数据存储格式

### CSV 文件

用于存储结构化数据：

```csv
date,name,value,category
2024-01-01,示例,100,A
```

### JSON 文件

用于存储统计数据：

```json
{
  "date": "2024-01-01",
  "total": 100,
  "average": 50.5
}
```

### Markdown 文件

用于存储报告：

```markdown
# 报告标题

**日期**: 2024-01-01

## 内容

正文...
```

## 配置说明

编辑 `config.yaml`：

```yaml
# 网站信息
SITE_NAME: "你的站点名称"
SITE_DESCRIPTION: "站点描述"

# 数据源配置
SCRAPING:
  source_name:
    enabled: true
    update_frequency: "daily"

# 分析配置
ANALYSIS:
  metrics:
    - "metric1"
    - "metric2"
```

## 测试

### 运行单个脚本

```bash
# 测试抓取脚本
python src/scrapers/star_market.py

# 测试分析脚本
python src/analyzers/market_analyzer.py

# 测试生成器
python src/generators/site_generator.py
```

### 验证数据

检查生成的数据文件：

```bash
ls -la data/raw/star_market/
ls -la data/processed/
ls -la data/reports/
```

### 本地预览网站

```bash
cd site
python -m http.server 8000
# 访问 http://localhost:8000
```

## 调试技巧

### 启用详细日志

在脚本开头添加：

```python
import logging
logging.basicConfig(
    level=logging.DEBUG,  # 改为 DEBUG 级别
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### 查看 GitHub Actions 日志

1. 进入仓库 Actions 标签页
2. 点击失败的 workflow
3. 查看具体步骤的日志输出

### 本地模拟 Actions 环境

使用 `act` 工具在本地运行 GitHub Actions：

```bash
# 安装 act
brew install act  # macOS

# 运行 workflow
act push
```

## 性能优化

### 数据抓取优化

- 使用并发请求：`aiohttp` + `asyncio`
- 添加请求延迟：避免被封禁
- 使用缓存：避免重复抓取

### 数据分析优化

- 使用向量化操作：避免 Python 循环
- 增量更新：只处理新数据
- 数据分区：按日期分片存储

### 网站生成优化

- 懒加载：图片和数据可视化
- CDN：静态资源加速
- 压缩：启用 Gzip

## 贡献指南

### 提交 Issue

- 描述问题现象
- 提供复现步骤
- 附上错误日志

### 提交 PR

1. Fork 仓库
2. 创建 feature 分支：`git checkout -b feature-name`
3. 提交更改：`git commit -am 'Add new feature'`
4. 推送分支：`git push origin feature-name`
5. 创建 Pull Request

### 代码规范

- 遵循 PEP 8 规范
- 添加 docstring
- 编写类型注解
- 保持函数简洁（<50 行）

## 常用命令

```bash
# 安装依赖
pip install -r requirements.txt

# 更新依赖
pip freeze > requirements.txt

# 格式化代码
black src/

# 检查代码风格
flake8 src/

# 运行测试
pytest tests/

# 清理数据
cd data && find . -name "*.csv" -mtime +30 -delete
```

## 参考资源

- [akshare 文档](https://www.akshare.xyz/)
- [pandas 文档](https://pandas.pydata.org/docs/)
- [Plotly 文档](https://plotly.com/python/)
- [GitHub Actions 文档](https://docs.github.com/cn/actions)
