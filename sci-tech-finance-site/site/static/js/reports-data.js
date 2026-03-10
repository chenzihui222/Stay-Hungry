/** 研究报告数据 - Report Data */

const ReportsData = {
    
    // 所有报告数据
    reports: [
        {
            id: 1,
            title: "2026年Q1科创板IPO深度分析",
            date: "2026-03-08",
            tags: ["科创板", "IPO", "市场分析", "季度报告"],
            summary: "本季度科创板IPO数量同比下降15%，但募资总额保持稳定。中芯国际、寒武纪等龙头企业表现亮眼，半导体和AI芯片赛道持续火热。",
            content: "详细报告内容...",
            type: "market",
            category: "科创板",
            author: "研究团队",
            views: 2156,
            file: "star_market_report_2026-03-08.md"
        },
        {
            id: 2,
            title: "VC/PE投资市场月度报告 - 2026年3月",
            date: "2026-03-08",
            tags: ["VC/PE", "投资趋势", "月度报告", "AI"],
            summary: "3月VC/PE市场融资事件328起，总金额423.5亿元。AI赛道融资占比37%，大模型和AI芯片领域投资活跃。",
            content: "详细报告内容...",
            type: "vc",
            category: "VC/PE",
            author: "投资研究组",
            views: 1893,
            file: "vcpe_report_2026-03-08.md"
        },
        {
            id: 3,
            title: "科技金融政策深度解读：科技保险新政",
            date: "2026-03-08",
            tags: ["政策解读", "科技保险", "监管政策", "国家级"],
            summary: "四部门联合发布科技保险新政，建立多层次科技保险产品体系，预计带来千亿级市场机会。深度解析政策背景、实施细则及行业影响。",
            content: "详细报告内容...",
            type: "policy",
            category: "政策解读",
            author: "政策研究组",
            views: 3421,
            file: "policy_analysis_2026-03-08.md"
        },
        {
            id: 4,
            title: "AI赛道投资热力图：大模型与芯片双轮驱动",
            date: "2026-03-07",
            tags: ["AI", "大模型", "AI芯片", "投资分析", "VC/PE"],
            summary: "AI领域融资占科技金融总融资的37%，创历史新高。深度分析大模型、AI芯片、自动驾驶等细分赛道的投资机会。",
            content: "详细报告内容...",
            type: "vc",
            category: "VC/PE",
            author: "AI研究组",
            views: 4532,
            file: "ai_investment_2026-03-07.md"
        },
        {
            id: 5,
            title: "科创板半导体板块估值分析报告",
            date: "2026-03-07",
            tags: ["科创板", "半导体", "估值分析", "行业研究"],
            summary: "当前半导体板块PE中位数为45倍，处于历史30%分位。中芯国际、中微公司、澜起科技等龙头企业估值具有吸引力。",
            content: "详细报告内容...",
            type: "market",
            category: "科创板",
            author: "行业研究组",
            views: 1678,
            file: "semiconductor_valuation_2026-03-07.md"
        },
        {
            id: 6,
            title: "2026年2月VC/PE市场回顾与展望",
            date: "2026-03-01",
            tags: ["VC/PE", "市场回顾", "投资展望", "月度报告"],
            summary: "2月融资事件312起，环比增长5%。硬科技、医疗健康、企业服务为热门赛道。展望Q2，预计AI和新能源领域投资将继续升温。",
            content: "详细报告内容...",
            type: "vc",
            category: "VC/PE",
            author: "投资研究组",
            views: 1234,
            file: "vcpe_review_2026-03-01.md"
        },
        {
            id: 7,
            title: "科技金融政策周报 - 第10期",
            date: "2026-03-07",
            tags: ["政策解读", "周报", "科技金融", "创投政策"],
            summary: "本周共监测到12条科技金融相关政策，其中国家级政策3条。重点关注科技保险、创投税收优惠、科创板再融资等政策动向。",
            content: "详细报告内容...",
            type: "policy",
            category: "政策解读",
            author: "政策研究组",
            views: 987,
            file: "policy_weekly_2026-03-07.md"
        },
        {
            id: 8,
            title: "DeepSeek融资案例深度研究",
            date: "2026-03-06",
            tags: ["案例研究", "DeepSeek", "大模型", "独角兽", "VC/PE"],
            summary: "DeepSeek本轮估值达到200亿美元，创下AI领域新纪录。深度解析其商业模式、技术壁垒、融资历程及对行业的启示。",
            content: "详细报告内容...",
            type: "vc",
            category: "案例研究",
            author: "案例研究组",
            views: 5623,
            file: "deepseek_case_2026-03-06.md"
        },
        {
            id: 9,
            title: "科创板2025年度总结与2026展望",
            date: "2026-02-28",
            tags: ["科创板", "年度总结", "市场展望", "年度报告"],
            summary: "2025年科创板新增上市公司98家，募资总额1456亿元。展望2026年，预计IPO节奏将保持稳定，硬科技企业仍是上市主力。",
            content: "详细报告内容...",
            type: "market",
            category: "科创板",
            author: "研究团队",
            views: 3245,
            file: "star_market_annual_2026-02-28.md"
        },
        {
            id: 10,
            title: "新能源赛道投资分析报告",
            date: "2026-02-25",
            tags: ["新能源", "光伏", "储能", "投资分析", "行业研究"],
            summary: "新能源赛道2月融资事件45起，总金额89亿元。光伏技术迭代加速，储能领域成为新的投资热点。",
            content: "详细报告内容...",
            type: "vc",
            category: "行业研究",
            author: "行业研究组",
            views: 2134,
            file: "new_energy_2026-02-25.md"
        },
        {
            id: 11,
            title: "生物医药科创板上市专题研究",
            date: "2026-02-20",
            tags: ["科创板", "生物医药", "上市研究", "行业专题"],
            summary: "科创板生物医药企业占比达23%，平均研发投入占比28%。创新药、医疗器械、CXO三大细分领域发展态势良好。",
            content: "详细报告内容...",
            type: "market",
            category: "科创板",
            author: "医药研究组",
            views: 1876,
            file: "biotech_star_market_2026-02-20.md"
        },
        {
            id: 12,
            title: "2026年科技金融政策趋势预测",
            date: "2026-02-15",
            tags: ["政策解读", "趋势预测", "科技金融", "年度展望"],
            summary: "基于政策信号和历史数据分析，预测2026年科技金融政策将聚焦科技保险、创投退出、科创板改革三大方向。",
            content: "详细报告内容...",
            type: "policy",
            category: "政策解读",
            author: "政策研究组",
            views: 4532,
            file: "policy_trend_2026-02-15.md"
        }
    ],

    // 所有标签（用于筛选）
    allTags: [
        "科创板", "IPO", "市场分析", "VC/PE", "投资趋势", 
        "政策解读", "AI", "大模型", "AI芯片", "半导体",
        "新能源", "生物医药", "科技保险", "估值分析",
        "案例研究", "月度报告", "季度报告", "年度报告",
        "行业研究", "监管政策", "国家级"
    ],

    // 报告类型
    reportTypes: {
        market: { label: "市场分析", color: "#1e40af", bgColor: "#dbeafe" },
        vc: { label: "VC/PE研究", color: "#166534", bgColor: "#dcfce7" },
        policy: { label: "政策解读", color: "#92400e", bgColor: "#fef3c7" }
    },

    // 分类
    categories: ["科创板", "VC/PE", "政策解读", "行业研究", "案例研究"],

    // 获取所有报告
    getAllReports() {
        return this.reports;
    },

    // 根据ID获取报告
    getReportById(id) {
        return this.reports.find(r => r.id === id);
    },

    // 根据文件获取报告
    getReportByFile(filename) {
        return this.reports.find(r => r.file === filename);
    },

    // 获取热门标签（按使用频次）
    getPopularTags(limit = 10) {
        const tagCount = {};
        this.reports.forEach(report => {
            report.tags.forEach(tag => {
                tagCount[tag] = (tagCount[tag] || 0) + 1;
            });
        });
        
        return Object.entries(tagCount)
            .sort((a, b) => b[1] - a[1])
            .slice(0, limit)
            .map(([tag, count]) => ({ tag, count }));
    },

    // 获取按时间排序的报告
    getReportsByDate(order = 'desc') {
        return [...this.reports].sort((a, b) => {
            const dateA = new Date(a.date);
            const dateB = new Date(b.date);
            return order === 'desc' ? dateB - dateA : dateA - dateB;
        });
    },

    // 获取按浏览量排序的报告
    getReportsByViews(limit = 5) {
        return [...this.reports]
            .sort((a, b) => b.views - a.views)
            .slice(0, limit);
    },

    // 获取最新报告
    getLatestReports(limit = 5) {
        return this.getReportsByDate('desc').slice(0, limit);
    },

    // 获取报告统计
    getStatistics() {
        return {
            total: this.reports.length,
            byType: {
                market: this.reports.filter(r => r.type === 'market').length,
                vc: this.reports.filter(r => r.type === 'vc').length,
                policy: this.reports.filter(r => r.type === 'policy').length
            },
            byCategory: this.categories.map(cat => ({
                category: cat,
                count: this.reports.filter(r => r.category === cat).length
            })),
            totalViews: this.reports.reduce((sum, r) => sum + r.views, 0)
        };
    }
};

// 导出数据（如果在模块环境中）
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ReportsData;
}
