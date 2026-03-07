# 科创金融研究网站 - 部署指南

## 快速部署步骤

### 1. 创建 GitHub 仓库

1. 在 GitHub 上创建新仓库，命名为 `sci-tech-finance-site`
2. 将本地代码推送到仓库：

```bash
cd sci-tech-finance-site
git init
git add .
git commit -m "初始提交: 科创金融研究网站"
git branch -M main
git remote add origin https://github.com/你的用户名/sci-tech-finance-site.git
git push -u origin main
```

### 2. 配置 GitHub Pages

1. 进入 GitHub 仓库页面
2. 点击 **Settings** → **Pages**
3. 在 **Source** 部分选择 **Deploy from a branch**
4. 选择 **gh-pages** 分支和 **/(root)** 文件夹
5. 点击 **Save**

### 3. 启用 GitHub Actions

1. 进入仓库的 **Actions** 标签页
2. 如果看到提示 "Workflows aren't being run on this repository"，点击 **I understand my workflows, go ahead and enable them**
3. 工作流将自动运行

### 4. 验证部署

1. 等待 GitHub Actions 完成（约 5-10 分钟）
2. 访问 `https://你的用户名.github.io/sci-tech-finance-site`
3. 你应该能看到网站首页

## 配置自定义域名（可选）

如果你想使用自己的域名：

### 1. 配置 DNS

在你的域名服务商处添加 CNAME 记录：
- 主机记录: `www` 或 `@`
- 记录类型: `CNAME`
- 记录值: `你的用户名.github.io`

### 2. 更新 GitHub Pages 设置

1. 进入仓库 **Settings** → **Pages**
2. 在 **Custom domain** 处输入你的域名
3. 勾选 **Enforce HTTPS**（推荐）
4. 点击 **Save**

### 3. 更新工作流文件

编辑 `.github/workflows/auto-update.yml`，将 `cname` 改为你的域名：

```yaml
- name: 部署到 GitHub Pages
  uses: peaceiris/actions-gh-pages@v3
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    publish_dir: ./site
    cname: 'www.yourdomain.com'  # 修改为你的域名
```

## 本地开发

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行数据抓取

```bash
# 抓取科创板数据
python src/scrapers/star_market.py

# 抓取 VC/PE 数据
python src/scrapers/vc_pe_tracker.py

# 抓取政策数据
python src/scrapers/policy_monitor.py
```

### 运行数据分析

```bash
# 分析市场数据
python src/analyzers/market_analyzer.py

# 分析 VC/PE 数据
python src/analyzers/vcpe_analyzer.py
```

### 生成网站

```bash
python src/generators/site_generator.py
```

### 本地预览

```bash
cd site
python -m http.server 8000
```

然后访问 `http://localhost:8000`

## 目录结构说明

```
sci-tech-finance-site/
├── .github/workflows/     # GitHub Actions 工作流
│   ├── auto-update.yml    # 自动更新工作流
│   └── health-check.yml   # 健康检查工作流
├── data/                  # 数据目录
│   ├── raw/              # 原始抓取数据
│   ├── processed/        # 处理后数据
│   └── reports/          # 生成的报告
├── src/                   # 源代码
│   ├── scrapers/         # 数据抓取脚本
│   ├── analyzers/        # 数据分析脚本
│   └── generators/       # 网站生成器
├── site/                  # 生成的网站
│   ├── index.html        # 首页
│   ├── star-market.html  # 科创板页面
│   ├── vcpe.html         # VC/PE页面
│   ├── policy.html       # 政策页面
│   ├── static/           # 静态资源
│   └── reports/          # 报告文件
├── config.yaml           # 配置文件
├── requirements.txt      # Python 依赖
└── README.md            # 项目说明
```

## 自动化说明

### 定时任务

- **每日 08:00** (北京时间)：自动抓取数据、生成报告、更新网站
- **每 6 小时**：运行健康检查

### 手动触发

你可以在 GitHub Actions 页面手动触发工作流：
1. 进入仓库 **Actions** 标签页
2. 选择 **自动更新科创金融研究网站** 工作流
3. 点击 **Run workflow** 按钮

## 故障排除

### 工作流运行失败

1. 进入 **Actions** 标签页查看错误日志
2. 常见问题：
   - 依赖安装失败：检查 `requirements.txt`
   - 数据抓取失败：检查数据源可用性
   - 权限问题：确保 GitHub Token 有正确权限

### 网站未更新

1. 检查 `gh-pages` 分支是否有更新
2. 检查 GitHub Pages 设置是否正确
3. 检查自定义域名配置（如果使用）

### 本地运行错误

1. 确保 Python 版本 >= 3.8
2. 重新安装依赖：`pip install -r requirements.txt --force-reinstall`
3. 检查数据目录权限

## 扩展功能

### 添加新的数据源

1. 在 `src/scrapers/` 创建新的抓取脚本
2. 在 `src/analyzers/` 创建对应的分析脚本
3. 更新 `.github/workflows/auto-update.yml` 添加新的步骤

### 自定义报告模板

1. 编辑 `src/generators/site_generator.py` 中的模板
2. 修改 `site/static/css/style.css` 自定义样式

### 添加新页面

1. 在 `src/generators/site_generator.py` 中添加新的页面生成函数
2. 更新导航栏链接

## 安全注意事项

1. **不要在代码中提交敏感信息**（API 密钥、密码等）
2. 使用 GitHub Secrets 管理敏感信息
3. 定期更新依赖包
4. 监控工作流的资源使用情况

## 技术支持

- GitHub Actions 文档：https://docs.github.com/cn/actions
- GitHub Pages 文档：https://docs.github.com/cn/pages
- 项目 Issues：在 GitHub 仓库提交 Issue

---

**部署完成后，你的网站将每天自动更新，无需手动维护！**
