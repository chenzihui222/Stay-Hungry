// 科创金融研究网站 - 图表脚本

// 颜色配置
const CHART_COLORS = {
    primary: '#1e3a5f',      // 深蓝色 - 主要趋势线
    secondary: '#0891b2',    // 青绿色 - 辅助趋势线
    accent: '#f97316',       // 橙色 - 对比线/强调
    colors: [
        '#1e3a5f', '#0891b2', '#f97316', '#10b981',
        '#8b5cf6', '#06b6d4', '#ec4899', '#f59e0b'
    ]
};

// 等待DOM加载完成
document.addEventListener('DOMContentLoaded', function() {
    // 初始化图表
    initValuationChart();
    initIndustryChart();
    initInvestmentTrendChart();
    initSectorHeatChart();
});

// 通用图表布局配置
function getChartLayout(title) {
    return {
        title: {
            text: title,
            font: {
                size: 18,
                weight: 700,
                color: '#1e3a5f'
            }
        },
        font: { 
            family: "'Noto Sans SC', -apple-system, BlinkMacSystemFont, sans-serif",
            size: 12
        },
        hovermode: 'closest',
        hoverlabel: {
            bgcolor: '#1e3a5f',
            bordercolor: '#1e3a5f',
            font: {
                family: "'Noto Sans SC', sans-serif",
                size: 13,
                color: '#ffffff'
            }
        },
        margin: { t: 60, r: 20, b: 60, l: 60 },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)'
    };
}

// 估值分布图表
function initValuationChart() {
    const chartDiv = document.getElementById('valuation-chart');
    if (!chartDiv) return;
    
    // 模拟估值分布数据
    const peRanges = ['<20倍', '20-40倍', '40-60倍', '60-80倍', '80-100倍', '>100倍'];
    const peCounts = [45, 128, 156, 89, 67, 75];
    
    const data = [{
        x: peRanges,
        y: peCounts,
        type: 'bar',
        marker: {
            color: CHART_COLORS.primary,
            opacity: 0.85
        },
        hovertemplate: '<b>%{x}</b><br>公司数量: %{y}<extra></extra>'
    }];
    
    const layout = {
        ...getChartLayout('科创板市盈率分布'),
        xaxis: { 
            title: { text: '市盈率区间', font: { size: 14 } },
            tickfont: { size: 12 }
        },
        yaxis: { 
            title: { text: '公司数量', font: { size: 14 } },
            tickfont: { size: 12 }
        }
    };
    
    Plotly.newPlot('valuation-chart', data, layout, {responsive: true, displayModeBar: false});
}

// 行业分布图表
function initIndustryChart() {
    const chartDiv = document.getElementById('industry-chart');
    if (!chartDiv) return;
    
    // 模拟行业分布数据
    const industries = [
        '半导体', '生物医药', '新能源', '人工智能', 
        '先进制造', '软件服务', '新材料', '其他'
    ];
    const industryCounts = [89, 76, 65, 54, 48, 42, 38, 148];
    
    const data = [{
        values: industryCounts,
        labels: industries,
        type: 'pie',
        hole: 0.4,
        marker: {
            colors: CHART_COLORS.colors
        },
        textinfo: 'label+percent',
        textposition: 'outside',
        hovertemplate: '<b>%{label}</b><br>公司数量: %{value}<br>占比: %{percent}<extra></extra>'
    }];
    
    const layout = {
        ...getChartLayout('科创板行业分布'),
        showlegend: false,
        margin: { t: 60, r: 20, b: 20, l: 20 }
    };
    
    Plotly.newPlot('industry-chart', data, layout, {responsive: true, displayModeBar: false});
}

// 投资趋势图表
function initInvestmentTrendChart() {
    const chartDiv = document.getElementById('investment-trend-chart');
    if (!chartDiv) return;
    
    // 模拟12个月的投资趋势
    const months = ['1月', '2月', '3月', '4月', '5月', '6月', 
                    '7月', '8月', '9月', '10月', '11月', '12月'];
    const dealCounts = [45, 52, 48, 61, 58, 67, 72, 68, 75, 82, 78, 85];
    const dealAmounts = [12.5, 14.2, 13.8, 16.5, 15.9, 18.2, 19.8, 18.5, 20.2, 22.1, 21.3, 23.5];
    
    const trace1 = {
        x: months,
        y: dealCounts,
        name: '投资事件数',
        type: 'scatter',
        mode: 'lines+markers',
        line: { 
            color: CHART_COLORS.primary, 
            width: 3 
        },
        marker: { 
            size: 8,
            color: CHART_COLORS.primary
        },
        hovertemplate: '<b>%{x}</b><br>投资事件: %{y}起<extra></extra>'
    };
    
    const trace2 = {
        x: months,
        y: dealAmounts,
        name: '投资金额(亿美元)',
        type: 'scatter',
        mode: 'lines+markers',
        yaxis: 'y2',
        line: { 
            color: CHART_COLORS.secondary, 
            width: 3 
        },
        marker: { 
            size: 8,
            color: CHART_COLORS.secondary
        },
        hovertemplate: '<b>%{x}</b><br>投资金额: %{y}亿美元<extra></extra>'
    };
    
    const data = [trace1, trace2];
    
    const layout = {
        ...getChartLayout('VC/PE投资趋势（近12个月）'),
        xaxis: { 
            title: { text: '月份', font: { size: 14 } },
            tickfont: { size: 12 }
        },
        yaxis: { 
            title: { text: '投资事件数', font: { size: 14 } },
            tickfont: { size: 12 },
            side: 'left' 
        },
        yaxis2: {
            title: { text: '投资金额(亿美元)', font: { size: 14 } },
            tickfont: { size: 12 },
            overlaying: 'y',
            side: 'right'
        },
        legend: { 
            x: 0.5, 
            y: 1.15, 
            xanchor: 'center',
            orientation: 'h',
            font: { size: 12 }
        }
    };
    
    Plotly.newPlot('investment-trend-chart', data, layout, {responsive: true, displayModeBar: false});
}

// 行业热度图表
function initSectorHeatChart() {
    const chartDiv = document.getElementById('sector-heat-chart');
    if (!chartDiv) return;
    
    const sectors = ['人工智能', '生物医药', '新能源', '半导体', '企业服务', 
                     '先进制造', '新材料', '金融科技', '消费升级'];
    const heatIndices = [95, 88, 82, 78, 72, 68, 65, 62, 58];
    
    // 根据热度设置颜色
    const colors = heatIndices.map(value => {
        if (value >= 90) return CHART_COLORS.primary;
        if (value >= 80) return CHART_COLORS.secondary;
        if (value >= 70) return CHART_COLORS.accent;
        return '#9ca3af';
    });
    
    const data = [{
        y: sectors,
        x: heatIndices,
        type: 'bar',
        orientation: 'h',
        marker: {
            color: colors
        },
        text: heatIndices.map(v => v.toString()),
        textposition: 'outside',
        hovertemplate: '<b>%{y}</b><br>热度指数: %{x}<extra></extra>'
    }];
    
    const layout = {
        ...getChartLayout('投资赛道热度指数'),
        xaxis: { 
            title: { text: '热度指数', font: { size: 14 } },
            tickfont: { size: 12 },
            range: [0, 105]
        },
        yaxis: { 
            automargin: true,
            tickfont: { size: 12 }
        },
        margin: { t: 60, r: 40, b: 60, l: 100 }
    };
    
    Plotly.newPlot('sector-heat-chart', data, layout, {responsive: true, displayModeBar: false});
}

// 动态更新图表数据（用于交互）
function updateChartData(chartId, newData) {
    const chartDiv = document.getElementById(chartId);
    if (!chartDiv) return;
    
    Plotly.animate(chartId, {
        data: newData,
        traces: [0],
        layout: {}
    }, {
        transition: {
            duration: 500,
            easing: 'cubic-in-out'
        },
        frame: {
            duration: 500
        }
    });
}

// 切换时间维度
function switchTimeRange(chartId, range) {
    // 模拟不同时间范围的数据
    const timeData = {
        '1M': { x: ['第1周', '第2周', '第3周', '第4周'], y: [12, 15, 18, 20] },
        '3M': { x: ['第1月', '第2月', '第3月'], y: [45, 52, 65] },
        '6M': { x: ['1月', '2月', '3月', '4月', '5月', '6月'], y: [45, 52, 48, 61, 58, 67] },
        '1Y': { x: ['2025-03', '2025-06', '2025-09', '2025-12', '2026-03'], y: [180, 220, 195, 240, 260] }
    };
    
    const data = timeData[range];
    if (data) {
        updateChartData(chartId, [{ x: data.x, y: data.y }]);
    }
}

// 行业筛选
function filterByIndustry(chartId, industry) {
    // 模拟不同行业的数据
    const industryData = {
        'all': { values: [89, 76, 65, 54, 48, 42, 38, 148] },
        'semiconductor': { values: [120, 45, 30, 25, 20, 15, 12, 83] },
        'biotech': { values: [35, 140, 25, 20, 18, 15, 12, 115] },
        'new-energy': { values: [30, 25, 130, 20, 18, 15, 12, 110] }
    };
    
    const data = industryData[industry];
    if (data) {
        updateChartData(chartId, [{ values: data.values }]);
    }
}
