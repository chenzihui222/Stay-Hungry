/** Dashboard JavaScript - 科技金融数据平台 */

// ===== Dashboard 数据层 =====
const DashboardData = {
    
    // 1. 科创板数据
    starMarket: {
        summary: {
            totalCompanies: 586,
            totalMarketCap: 8.24, // 万亿
            yearlyIPO: 67,
            growth: 12.5
        },
        ipoTrend: {
            years: ['2022', '2023', '2024', '2025', '2026'],
            counts: [124, 156, 142, 98, 67],
            amounts: [1892, 2341, 1987, 1456, 1023] // 亿元
        }
    },

    // 2. VC/PE 数据
    vcpe: {
        summary: {
            monthlyDeals: 328,
            aiSectorAmount: 156.8, // 亿元
            totalAmount: 423.5,
            growth: 8.3
        },
        monthlyTrend: {
            months: ['2025-10', '2025-11', '2025-12', '2026-01', '2026-02', '2026-03'],
            monthLabels: ['10月', '11月', '12月', '1月', '2月', '3月'],
            deals: [298, 312, 328, 345, 321, 338],
            amounts: [380, 410, 423, 445, 398, 456]
        },
        aiSector: {
            labels: ['大模型', 'AI芯片', '自动驾驶', '智能客服', 'AI医疗', '其他'],
            data: [45.2, 38.6, 28.4, 18.9, 15.7, 10.0],
            colors: ['#1e3a5f', '#2563eb', '#0891b2', '#10b981', '#f59e0b', '#94a3b8']
        },
        topInvestors: [
            { rank: 1, name: '红杉中国', deals: 42, trend: 'up', change: 15 },
            { rank: 2, name: '高瓴资本', deals: 38, trend: 'up', change: 8 },
            { rank: 3, name: 'IDG资本', deals: 35, trend: 'flat', change: 0 },
            { rank: 4, name: '腾讯投资', deals: 31, trend: 'down', change: -5 },
            { rank: 5, name: '深创投', deals: 28, trend: 'up', change: 12 }
        ]
    },

    // 3. 政策数据
    policy: {
        summary: {
            monthlyNew: 12,
            nationalLevel: 3,
            localLevel: 9,
            highImpact: 5
        },
        categories: [
            { name: '融资支持', count: 3, level: 'national' },
            { name: '税收优惠', count: 2, level: 'local' },
            { name: '上市指导', count: 2, level: 'national' },
            { name: '创投扶持', count: 3, level: 'local' },
            { name: '知识产权保护', count: 2, level: 'national' }
        ]
    },

    // 4. 研究数据
    research: {
        latestReports: [
            {
                id: 1,
                title: '2026年Q1科创板IPO深度分析',
                type: 'report',
                author: '研究团队',
                date: '2026-03-08',
                summary: '本季度科创板IPO数量同比下降15%，但募资总额保持稳定...'
            },
            {
                id: 2,
                title: 'AI赛道投资热力图：大模型与芯片双轮驱动',
                type: 'report',
                author: '研究团队',
                date: '2026-03-07',
                summary: 'AI领域融资占科技金融总融资的37%，创历史新高...'
            },
            {
                id: 3,
                title: '科技保险新政解读及市场影响',
                type: 'report',
                author: '政策研究组',
                date: '2026-03-06',
                summary: '四部门联合发布的科技保险政策将带来千亿级市场机会...'
            },
            {
                id: 4,
                title: '2026年2月VC/PE市场月度报告',
                type: 'report',
                author: '研究团队',
                date: '2026-03-01',
                summary: '2月融资事件数环比增长5%，AI赛道持续火热...'
            }
        ],
        latestNotes: [
            {
                id: 1,
                title: '中芯国际财报分析要点',
                type: 'note',
                author: '研究员A',
                date: '2026-03-10',
                preview: 'Q4营收同比增长34%，毛利率超预期，先进制程占比提升...'
            },
            {
                id: 2,
                title: '寒武纪 vs 英伟达：国产AI芯片的机会',
                type: 'note',
                author: '研究员B',
                date: '2026-03-09',
                preview: '从算力、能效比、软件生态三个维度对比分析...'
            },
            {
                id: 3,
                title: '科创板半导体板块估值分析',
                type: 'note',
                author: '研究员C',
                date: '2026-03-08',
                preview: '当前PE中位数为45倍，处于历史30%分位...'
            },
            {
                id: 4,
                title: 'DeepSeek融资案例研究',
                type: 'note',
                author: '研究员D',
                date: '2026-03-07',
                preview: '本轮估值达到200亿美元，创下AI领域新纪录...'
            }
        ]
    },

    // 5. 系统数据
    system: {
        lastUpdate: '2026-03-10 14:30:00',
        nextUpdate: '2026-03-11 08:00:00'
    }
};

// ===== 图表配置 =====
const ChartConfig = {
    colors: {
        primary: '#1e3a5f',
        primaryLight: '#2563eb',
        success: '#10b981',
        warning: '#f59e0b',
        info: '#0891b2',
        danger: '#ef4444',
        gray: '#94a3b8'
    },
    font: {
        family: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
    }
};

// ===== Dashboard 控制器 =====
const DashboardController = {
    
    // 图表实例存储
    charts: {},
    
    // 初始化
    init() {
        this.renderKPICards();
        this.renderCharts();
        this.renderTopInvestors();
        this.renderLatestActivity('reports');
        this.startRealTimeUpdate();
        this.bindEvents();
        this.updateTimestamps();
    },

    // 渲染KPI卡片（带动画）
    renderKPICards() {
        const cards = document.querySelectorAll('.kpi-value');
        cards.forEach((card, index) => {
            const target = parseInt(card.dataset.target);
            setTimeout(() => {
                this.animateNumber(card, target);
            }, index * 150);
        });
    },

    // 数字动画
    animateNumber(element, target) {
        let current = 0;
        const duration = 1500;
        const increment = target / (duration / 16);
        const startTime = performance.now();
        
        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // 使用 easeOutQuart 缓动函数
            const easeProgress = 1 - Math.pow(1 - progress, 4);
            current = Math.floor(target * easeProgress);
            
            element.textContent = current.toLocaleString();
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            } else {
                element.textContent = target.toLocaleString();
            }
        };
        
        requestAnimationFrame(animate);
    },

    // 渲染所有图表
    renderCharts() {
        this.renderIPOTrend();
        this.renderVCMonthly();
        this.renderAISector();
        this.renderPolicyCategory();
    },

    // 1. IPO趋势图 (Plotly)
    renderIPOTrend() {
        const data = DashboardData.starMarket.ipoTrend;
        
        const trace1 = {
            x: data.years,
            y: data.counts,
            type: 'scatter',
            mode: 'lines+markers',
            name: 'IPO数量',
            fill: 'tozeroy',
            fillcolor: 'rgba(30, 58, 95, 0.1)',
            line: { 
                color: '#1e3a5f', 
                width: 3,
                shape: 'spline'
            },
            marker: { 
                size: 10, 
                color: '#2563eb',
                line: { color: 'white', width: 2 }
            },
            hovertemplate: '%{x}年<br>IPO数量: %{y}家<extra></extra>'
        };

        const layout = {
            margin: { t: 10, r: 20, b: 40, l: 50 },
            xaxis: { 
                title: { text: '', font: { size: 12 } },
                gridcolor: '#f1f5f9',
                zeroline: false
            },
            yaxis: { 
                title: { text: 'IPO数量 (家)', font: { size: 12, color: '#64748b' } },
                gridcolor: '#f1f5f9',
                zeroline: false
            },
            paper_bgcolor: 'transparent',
            plot_bgcolor: 'transparent',
            showlegend: false,
            hovermode: 'x unified',
            dragmode: false
        };

        const config = {
            responsive: true,
            displayModeBar: false
        };

        Plotly.newPlot('ipoTrendChart', [trace1], layout, config);
        
        // 存储图表引用
        this.charts.ipoTrend = document.getElementById('ipoTrendChart');
    },

    // 2. VC月度融资图 (Chart.js)
    renderVCMonthly() {
        const ctx = document.getElementById('vcMonthlyChart');
        if (!ctx) return;
        
        const data = DashboardData.vcpe.monthlyTrend;
        
        this.charts.vcMonthly = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.monthLabels,
                datasets: [{
                    label: '融资金额(亿元)',
                    data: data.amounts,
                    backgroundColor: data.amounts.map((_, i) => {
                        const colors = [
                            'rgba(30, 58, 95, 0.6)',
                            'rgba(37, 99, 235, 0.6)',
                            'rgba(8, 145, 178, 0.6)',
                            'rgba(16, 185, 129, 0.6)',
                            'rgba(245, 158, 11, 0.6)',
                            'rgba(30, 58, 95, 0.8)'
                        ];
                        return colors[i];
                    }),
                    borderColor: data.amounts.map((_, i) => {
                        const colors = [
                            '#1e3a5f', '#2563eb', '#0891b2', 
                            '#10b981', '#f59e0b', '#1e3a5f'
                        ];
                        return colors[i];
                    }),
                    borderWidth: 2,
                    borderRadius: 8,
                    borderSkipped: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: '#1e3a5f',
                        padding: 12,
                        cornerRadius: 8,
                        titleFont: { size: 13 },
                        bodyFont: { size: 13 },
                        callbacks: {
                            label: function(context) {
                                return `融资额: ${context.parsed.y}亿元`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { 
                            color: '#f1f5f9',
                            drawBorder: false
                        },
                        ticks: {
                            color: '#64748b',
                            font: { size: 11 }
                        }
                    },
                    x: {
                        grid: { display: false },
                        ticks: {
                            color: '#64748b',
                            font: { size: 11 }
                        }
                    }
                },
                animation: {
                    duration: 1000,
                    easing: 'easeOutQuart'
                }
            }
        });
    },

    // 3. AI赛道分布 (Chart.js 环形图)
    renderAISector() {
        const ctx = document.getElementById('aiSectorChart');
        if (!ctx) return;
        
        const data = DashboardData.vcpe.aiSector;
        
        this.charts.aiSector = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.labels,
                datasets: [{
                    data: data.data,
                    backgroundColor: data.colors,
                    borderWidth: 0,
                    cutout: '65%',
                    hoverOffset: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { 
                        display: false 
                    },
                    tooltip: {
                        backgroundColor: '#1e3a5f',
                        padding: 12,
                        cornerRadius: 8,
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.parsed;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((value / total) * 100).toFixed(1);
                                return `${label}: ${value}亿元 (${percentage}%)`;
                            }
                        }
                    }
                },
                animation: {
                    animateRotate: true,
                    duration: 1200
                }
            }
        });
        
        // 生成自定义图例
        this.renderAISectorLegend(data);
    },

    // AI赛道图例
    renderAISectorLegend(data) {
        const legendContainer = document.getElementById('aiSectorLegend');
        if (!legendContainer) return;
        
        const total = data.data.reduce((a, b) => a + b, 0);
        
        legendContainer.innerHTML = data.labels.map((label, i) => {
            const value = data.data[i];
            const percentage = ((value / total) * 100).toFixed(1);
            return `
                <div class="legend-item">
                    <div class="legend-color" style="background: ${data.colors[i]}"></div>
                    <span>${label} (${percentage}%)</span>
                </div>
            `;
        }).join('');
    },

    // 4. 政策分类 (Plotly 横向条形图)
    renderPolicyCategory() {
        const data = DashboardData.policy.categories;
        
        const trace = {
            y: data.map(d => d.name),
            x: data.map(d => d.count),
            type: 'bar',
            orientation: 'h',
            marker: {
                color: data.map(d => d.level === 'national' ? '#1e3a5f' : '#0891b2'),
                line: {
                    color: 'white',
                    width: 2
                }
            },
            text: data.map(d => d.count + '条'),
            textposition: 'outside',
            textfont: {
                size: 12,
                color: '#64748b'
            },
            hovertemplate: '%{y}<br>政策数量: %{x}条<extra></extra>'
        };

        const layout = {
            margin: { t: 10, r: 60, b: 20, l: 100 },
            xaxis: { 
                title: { text: '', font: { size: 12 } },
                gridcolor: '#f1f5f9',
                zeroline: false,
                tickfont: { size: 11, color: '#64748b' }
            },
            yaxis: { 
                gridcolor: 'transparent',
                tickfont: { size: 12, color: '#1f2937' }
            },
            paper_bgcolor: 'transparent',
            plot_bgcolor: 'transparent',
            showlegend: false,
            dragmode: false
        };

        const config = {
            responsive: true,
            displayModeBar: false
        };

        Plotly.newPlot('policyCategoryChart', [trace], layout, config);
        
        this.charts.policyCategory = document.getElementById('policyCategoryChart');
    },

    // 渲染活跃投资机构
    renderTopInvestors() {
        const container = document.getElementById('topInvestorsList');
        if (!container) return;
        
        const investors = DashboardData.vcpe.topInvestors;
        
        container.innerHTML = investors.map(inv => {
            const trendIcon = inv.trend === 'up' ? 'fa-arrow-up' : 
                             inv.trend === 'down' ? 'fa-arrow-down' : 'fa-minus';
            const trendClass = inv.trend === 'up' ? 'up' : 
                              inv.trend === 'down' ? 'down' : 'flat';
            
            return `
                <div class="investor-item" onclick="window.location.href='vcpe.html'">
                    <div class="investor-rank ${inv.rank <= 3 ? 'top' : 'normal'}">
                        ${inv.rank}
                    </div>
                    <div class="investor-info">
                        <div class="investor-name">${inv.name}</div>
                        <div class="investor-deals">本月投资 ${inv.deals} 个项目</div>
                    </div>
                    <div class="investor-trend ${trendClass}">
                        <i class="fas ${trendIcon}"></i>
                        ${inv.change > 0 ? '+' : ''}${inv.change}%
                    </div>
                </div>
            `;
        }).join('');
    },

    // 渲染最新动态
    renderLatestActivity(type) {
        const container = document.getElementById('latestActivity');
        if (!container) return;
        
        let items = [];
        
        if (type === 'reports') {
            items = DashboardData.research.latestReports.map(r => ({
                icon: 'file-alt',
                iconClass: 'report',
                title: r.title,
                meta: `${r.author} · ${r.date}`,
                badge: '报告',
                badgeClass: 'report'
            }));
        } else {
            items = DashboardData.research.latestNotes.map(n => ({
                icon: 'sticky-note',
                iconClass: 'note',
                title: n.title,
                meta: `${n.author} · ${n.date}`,
                badge: '笔记',
                badgeClass: 'note'
            }));
        }
        
        container.innerHTML = items.map((item, index) => `
            <div class="timeline-item" style="animation-delay: ${index * 0.1}s" 
                 onclick="window.location.href='${type === 'reports' ? 'report-viewer.html' : 'research.html'}'">
                <div class="timeline-icon ${item.iconClass}">
                    <i class="fas fa-${item.icon}"></i>
                </div>
                <div class="timeline-content">
                    <div class="timeline-title">${item.title}</div>
                    <div class="timeline-meta">
                        <span class="timeline-badge ${item.badgeClass}">${item.badge}</span>
                        <span>${item.meta}</span>
                    </div>
                </div>
            </div>
        `).join('');
    },

    // 绑定事件
    bindEvents() {
        // Tab切换
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                e.currentTarget.classList.add('active');
                this.renderLatestActivity(e.currentTarget.dataset.tab);
            });
        });

        // 图表筛选按钮
        document.querySelectorAll('.chart-filter').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const parent = e.currentTarget.closest('.chart-actions');
                parent.querySelectorAll('.chart-filter').forEach(b => b.classList.remove('active'));
                e.currentTarget.classList.add('active');
                
                // 这里可以添加切换图表数据的逻辑
                console.log('Filter:', e.currentTarget.dataset.filter);
            });
        });

        // KPI卡片点击效果
        document.querySelectorAll('.kpi-card').forEach(card => {
            card.addEventListener('click', function() {
                this.style.transform = 'scale(0.98)';
                setTimeout(() => {
                    this.style.transform = '';
                }, 150);
            });
        });

        // 搜索框
        const searchInput = document.querySelector('.search-box input');
        if (searchInput) {
            searchInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    const query = e.target.value.trim();
                    if (query) {
                        alert(`搜索: ${query}\n(搜索功能开发中)`);
                    }
                }
            });
        }

        // 时间范围按钮
        document.querySelectorAll('.time-range .btn-sm').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const parent = e.currentTarget.closest('.time-range');
                parent.querySelectorAll('.btn-sm').forEach(b => b.classList.remove('active'));
                e.currentTarget.classList.add('active');
            });
        });

        // 响应式图表重绘
        window.addEventListener('resize', () => {
            this.handleResize();
        });
    },

    // 处理窗口大小变化
    handleResize() {
        // Plotly图表自动响应
        const plotlyCharts = ['ipoTrendChart', 'policyCategoryChart'];
        plotlyCharts.forEach(id => {
            const chart = document.getElementById(id);
            if (chart) {
                Plotly.Plots.resize(chart);
            }
        });
    },

    // 更新时间戳
    updateTimestamps() {
        const lastUpdateEl = document.getElementById('lastUpdateTime');
        const nextUpdateEl = document.getElementById('nextUpdateTime');
        
        if (lastUpdateEl) {
            lastUpdateEl.textContent = DashboardData.system.lastUpdate;
        }
        if (nextUpdateEl) {
            nextUpdateEl.textContent = DashboardData.system.nextUpdate;
        }
    },

    // 实时更新
    startRealTimeUpdate() {
        // 每分钟更新时间显示
        setInterval(() => {
            const now = new Date();
            const timeString = now.toLocaleString('zh-CN', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            });
            
            const lastUpdateEl = document.getElementById('lastUpdateTime');
            if (lastUpdateEl) {
                lastUpdateEl.textContent = timeString;
            }
        }, 60000);

        // 模拟实时数据推送效果（每30秒）
        setInterval(() => {
            this.simulateRealTimeUpdate();
        }, 30000);
    },

    // 模拟实时数据更新
    simulateRealTimeUpdate() {
        // 随机微调VC/PE数据
        const vcCard = document.querySelector('.kpi-success .kpi-value');
        if (vcCard && Math.random() > 0.7) {
            const currentVal = parseInt(vcCard.textContent.replace(/,/g, ''));
            if (currentVal < 350) {
                vcCard.textContent = (currentVal + 1).toLocaleString();
                vcCard.style.color = '#10b981';
                setTimeout(() => {
                    vcCard.style.color = '';
                }, 1000);
            }
        }

        // 随机更新通知数
        const badgeCount = document.querySelector('.badge-count');
        if (badgeCount && Math.random() > 0.8) {
            const current = parseInt(badgeCount.textContent);
            if (current < 10) {
                badgeCount.textContent = current + 1;
                badgeCount.style.animation = 'pulse 0.5s ease';
            }
        }
    }
};

// ===== 工具函数 =====
const Utils = {
    // 格式化数字
    formatNumber(num) {
        return num.toLocaleString('zh-CN');
    },

    // 格式化日期
    formatDate(dateStr) {
        const date = new Date(dateStr);
        return date.toLocaleDateString('zh-CN', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    },

    // 防抖函数
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
};

// ===== 页面加载完成后初始化 =====
document.addEventListener('DOMContentLoaded', () => {
    DashboardController.init();
});

// ===== 添加CSS动画 =====
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.2); }
    }
    
    .timeline-item {
        animation: fadeInUp 0.4s ease-out forwards;
        opacity: 0;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);
