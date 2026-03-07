'use client'

import React from 'react'
import { ArrowUp, ArrowDown, TrendingUp, Activity, BarChart3, PieChart } from 'lucide-react'

// 科创板统计数据（示例数据，后续可替换为真实API数据）
const starBoardStats = {
  totalCompanies: 573,
  totalMarketCap: '6.85万亿',
  avgPE: 42.3,
  tradingVolume: '892亿',
  dailyChange: '+1.24%',
  upCount: 342,
  downCount: 231,
}

const topPerformers = [
  { code: '688981', name: '中芯国际', price: 52.18, change: '+5.23%', volume: '45.2亿', pe: 58.2 },
  { code: '688111', name: '金山办公', price: 298.50, change: '+3.85%', volume: '12.8亿', pe: 85.4 },
  { code: '688012', name: '中微公司', price: 168.90, change: '+2.96%', volume: '8.5亿', pe: 72.1 },
  { code: '688599', name: '天合光能', price: 28.65, change: '+2.47%', volume: '6.2亿', pe: 15.8 },
  { code: '688396', name: '华润微', price: 45.32, change: '+1.89%', volume: '4.1亿', pe: 32.4 },
]

const sectorDistribution = [
  { sector: '半导体', count: 156, percent: 27.2 },
  { sector: '新能源', count: 98, percent: 17.1 },
  { sector: '生物医药', count: 87, percent: 15.2 },
  { sector: '人工智能', count: 65, percent: 11.3 },
  { sector: '高端装备', count: 52, percent: 9.1 },
  { sector: '其他', count: 115, percent: 20.1 },
]

export default function StarBoardData() {
  return (
    <div className="space-y-8">
      {/* Page Title */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-white mb-2">科创板数据</h2>
        <p className="text-tech-text-muted">STAR Market Data · 实时跟踪科创板市场动态</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="上市公司"
          value={starBoardStats.totalCompanies}
          suffix="家"
          icon={Activity}
          change="+3 本月新增"
          positive={true}
        />
        <StatCard
          title="总市值"
          value={starBoardStats.totalMarketCap}
          icon={BarChart3}
          change="+2.1% 今日"
          positive={true}
        />
        <StatCard
          title="平均市盈率"
          value={starBoardStats.avgPE}
          icon={PieChart}
          change="历史均值: 45.2"
          positive={false}
        />
        <StatCard
          title="成交额"
          value={starBoardStats.tradingVolume}
          icon={TrendingUp}
          change="较昨日 +15.3%"
          positive={true}
        />
      </div>

      {/* Two Column Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left: Top Performers */}
        <div className="lg:col-span-2 bg-tech-card border border-tech-border rounded-2xl p-6 card-glow">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-white">涨跌排行</h3>
            <div className="flex items-center gap-2 text-sm">
              <span className="flex items-center gap-1 text-green-400">
                <ArrowUp className="w-4 h-4" /> {starBoardStats.upCount}
              </span>
              <span className="text-tech-text-muted">/</span>
              <span className="flex items-center gap-1 text-red-400">
                <ArrowDown className="w-4 h-4" /> {starBoardStats.downCount}
              </span>
            </div>
          </div>
          
          <div className="overflow-x-auto">
            <table className="data-table">
              <thead>
                <tr>
                  <th>股票代码</th>
                  <th>名称</th>
                  <th className="text-right">最新价</th>
                  <th className="text-right">涨跌幅</th>
                  <th className="text-right">成交额</th>
                  <th className="text-right">市盈率</th>
                </tr>
              </thead>
              <tbody>
                {topPerformers.map((stock) => (
                  <tr key={stock.code}>
                    <td className="font-mono text-tech-accent">{stock.code}</td>
                    <td className="font-medium text-white">{stock.name}</td>
                    <td className="text-right number-font">¥{stock.price}</td>
                    <td className="text-right">
                      <span className="text-green-400">{stock.change}</span>
                    </td>
                    <td className="text-right text-tech-text-muted number-font">{stock.volume}</td>
                    <td className="text-right text-tech-text-muted number-font">{stock.pe}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Right: Sector Distribution */}
        <div className="bg-tech-card border border-tech-border rounded-2xl p-6 card-glow">
          <h3 className="text-lg font-semibold text-white mb-6">行业分布</h3>
          
          <div className="space-y-4">
            {sectorDistribution.map((item) => (
              <div key={item.sector}>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-tech-text">{item.sector}</span>
                  <span className="text-sm text-tech-text-muted">
                    {item.count}家 ({item.percent}%)
                  </span>
                </div>
                <div className="h-2 bg-tech-border rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-tech-accent to-blue-500 rounded-full"
                    style={{ width: `${item.percent}%` }}
                  />
                </div>
              </div>
            ))}
          </div>

          <div className="mt-6 pt-6 border-t border-tech-border">
            <div className="text-xs text-tech-text-muted space-y-2">
              <p>• 半导体占比最高，达27.2%</p>
              <p>• 新能源和生物医药合计占比超30%</p>
              <p>• 硬科技企业占科创板80%以上</p>
            </div>
          </div>
        </div>
      </div>

      {/* Data Source Note */}
      <div className="mt-8 p-4 bg-tech-accent-dim border border-tech-accent/20 rounded-xl">
        <p className="text-sm text-tech-accent">
          <strong>数据来源说明：</strong> 本页面展示科创板市场数据，
          数据来源包括上交所官方披露、Wind金融终端等。数据更新时间为交易日实时，
          具体API接口将在后续开发中对接。
        </p>
      </div>
    </div>
  )
}

// Stat Card Component
function StatCard({ 
  title, 
  value, 
  suffix = '', 
  icon: Icon, 
  change, 
  positive 
}: { 
  title: string
  value: string | number
  suffix?: string
  icon: React.ElementType
  change: string
  positive: boolean
}) {
  return (
    <div className="bg-tech-card border border-tech-border rounded-2xl p-6 card-glow">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-tech-text-muted mb-1">{title}</p>
          <p className="text-3xl font-bold text-white number-font">
            {value}<span className="text-lg ml-1">{suffix}</span>
          </p>
          <p className={`text-sm mt-2 ${positive ? 'text-green-400' : 'text-tech-text-muted'}`}>
            {change}
          </p>
        </div>
        <div className="w-12 h-12 rounded-xl bg-tech-accent-dim flex items-center justify-center">
          <Icon className="w-6 h-6 text-tech-accent" />
        </div>
      </div>
    </div>
  )
}
