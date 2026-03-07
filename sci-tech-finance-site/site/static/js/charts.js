// 科创金融研究网站 - 图表脚本

// 等待DOM加载完成
document.addEventListener('DOMContentLoaded', function() {
    // 初始化图表
    initValuationChart();
    initIndustryChart();
});

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
            color: '#1a5fb4',
            opacity: 0.8
        }
    }];
    
    const layout = {
        title: '科创板市盈率分布',
        xaxis: { title: '市盈率区间' },
        yaxis: { title: '公司数量' },
        font: { family: '-apple-system, BlinkMacSystemFont, sans-serif' }
    };
    
    Plotly.newPlot('valuation-chart', data, layout, {responsive: true});
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
            colors: [
                '#1a5fb4', '#26a269', '#e66100', '#c01c28',
                '#8b5cf6', '#06b6d4', '#f59e0b', '#9ca3af'
            ]
        },
        textinfo: 'label+percent',
        textposition: 'outside'
    }];
    
    const layout = {
        title: '科创板行业分布',
        showlegend: true,
        legend: { orientation: 'h', y: -0.1 },
        font: { family: '-apple-system, BlinkMacSystemFont, sans-serif' }
    };
    
    Plotly.newPlot('industry-chart', data, layout, {responsive: true});
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
        line: { color: '#1a5fb4', width: 3 },
        marker: { size: 8 }
    };
    
    const trace2 = {
        x: months,
        y: dealAmounts,
        name: '投资金额(亿美元)',
        type: 'scatter',
        mode: 'lines+markers',
        yaxis: 'y2',
        line: { color: '#26a269', width: 3 },
        marker: { size: 8 }
    };
    
    const data = [trace1, trace2];
    
    const layout = {
        title: 'VC/PE投资趋势（近12个月）',
        xaxis: { title: '月份' },
        yaxis: { title: '投资事件数', side: 'left' },
        yaxis2: {
            title: '投资金额(亿美元)',
            overlaying: 'y',
            side: 'right'
        },
        legend: { x: 0.1, y: 1.15, orientation: 'h' },
        font: { family: '-apple-system, BlinkMacSystemFont, sans-serif' }
    };
    
    Plotly.newPlot('investment-trend-chart', data, layout, {responsive: true});
}

// 行业热度图表
function initSectorHeatChart() {
    const chartDiv = document.getElementById('sector-heat-chart');
    if (!chartDiv) return;
    
    const sectors = ['人工智能', '生物医药', '新能源', '半导体', '企业服务', 
                     '先进制造', '新材料', '金融科技', '消费升级', '企业服务'];
    const heatIndices = [95, 88, 82, 78, 72, 68, 65, 62, 58, 55];
    
    const data = [{
        y: sectors,
        x: heatIndices,
        type: 'bar',
        orientation: 'h',
        marker: {
            color: heatIndices,
            colorscale: 'Viridis',
            showscale: true
        }
    }];
    
    const layout = {
        title: '投资赛道热度指数',
        xaxis: { title: '热度指数' },
        yaxis: { automargin: true },
        font: { family: '-apple-system, BlinkMacSystemFont, sans-serif' }
    };
    
    Plotly.newPlot('sector-heat-chart', data, layout, {responsive: true});
}
