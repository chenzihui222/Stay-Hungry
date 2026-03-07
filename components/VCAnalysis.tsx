'use client'

import React from 'react'
import { TrendingUp, DollarSign, Building, Users, Calendar, Target } from 'lucide-react'

// VC市场数据（示例数据）
const vcStats = {
  totalInvestment: '1,248.5亿',
  dealCount: '3,456',
  avgDealSize: '3,612万',
  activeFunds: '892',
  quarterlyGrowth: '+12.4%',
  exitCount: '156',
}

const topSectors = [
  { sector: '人工智能', investment: '385.2亿', deals: 456, growth: '+45.2%', trend: 'up' },
  { sector: '生物医药', investment: '298.6亿', deals: 324, growth: '+18.7%', trend: 'up' },
  { sector: '新能源', investment: '198.4亿', deals: 245, growth: '+32.1%', trend: 'up' },
  { sector: '半导体', investment: '156.8亿', deals: 198, growth: '-5.3%', trend: 'down' },
  { sector: '企业服务', investment: '124.5亿', deals: 167, growth: '+8.9%', trend: 'up' },
]

const recentDeals = [
  { date: '2024-03-06', company: '智谱AI', sector: '人工智能', round: 'C轮', amount: '25亿元', investor: '阿里巴巴、腾讯' },
  { date: '2024-03-05', company: '晶泰科技', sector: '生物医药', round: 'D轮', amount: '4亿美元', investor: '软银愿景、红杉中国' },
  { date: '2024-03-04', company: '蜂巢能源', sector: '新能源', round: 'B+轮', amount: '60亿元', investor: '国投招商、碧桂园创投' },
  { date: '2024-03-03', company: '壁仞科技', sector: '半导体', round: 'B轮', amount: '20亿元', investor: '高瓴创投、启明创投' },
  { date: '2024-03-02', company: '神策数据', sector: '企业服务', round: 'D轮', amount: '2亿美元', investor: 'Tiger Global、凯雷' },
]

const activeVCs = [
  { name: '红杉中国', deals: 89, focus: '科技、消费、医疗', stage: '全阶段' },
  { name: '高瓴资本', deals: 76, focus: '硬科技、医疗', stage: '中后期' },
  { name: 'IDG资本', deals: 68, focus: 'TMT、企业服务', stage: '全阶段' },
  { name: '启明创投', deals: 54, focus: '科技、医疗', stage: '早期' },
  { name: '五源资本', deals: 48, focus: '互联网、科技', stage: '早期' },
]

export default function VCAnalysis() {
  return (
    <div className="space-y-8">
      {/* Page Title */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-white mb-2">VC市场分析</h2>
        <p className="text-tech-text-muted">VC Market Analysis · 洞察风险投资市场趋势</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <StatCard
          title="总投资额"
          value={vcStats.totalInvestment}
          icon={DollarSign}
          change="同比 +23.5%"
          positive={true}
        />
        <StatCard
          title="交易数量"
          value={vcStats.dealCount}
          icon={Target}
          change="同比 +15.2%"
          positive={true}
        />
        <StatCard
          title="平均交易额"
          value={vcStats.avgDealSize}
          icon={TrendingUp}
          change="较Q3 +8.7%"
          positive={true}
        />
      </div>

      {/* Sector Analysis */}
      <div className="bg-tech-card border border-tech-border rounded-2xl p-6 card-glow">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold text-white">热门赛道</h3>
          <span className="text-sm text-tech-text-muted">2024年Q1数据</span>
        </div>
        
        <div className="overflow-x-auto">
          <table className="data-table">
            <thead>
              <tr>
                <th>赛道</th>
                <th className="text-right">投资金额</th>
                <th className="text-right">交易数</th>
                <th className="text-right">环比增长</th>
                <th>趋势</th>
              </tr>
            </thead>
            <tbody>
              {topSectors.map((sector) => (
                <tr key={sector.sector}>
                  <td className="font-medium text-white">{sector.sector}</td>
                  <td className="text-right number-font">{sector.investment}</td>
                  <td className="text-right number-font">{sector.deals}</td>
                  <td className="text-right">
                    <span className={sector.trend === 'up' ? 'text-green-400' : 'text-red-400'}>
                      {sector.growth}
                    </span>
                  </td>
                  <td>
                    <div className="flex items-center gap-2">
                      <div className="flex-1 h-2 bg-tech-border rounded-full overflow-hidden max-w-24">
                        <div
                          className={`h-full rounded-full ${
                            sector.trend === 'up' ? 'bg-green-500' : 'bg-red-500'
                          }`}
                          style={{ width: `${Math.min(parseFloat(sector.growth) * 2, 100)}%` }}
                        />
                      </div>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Two Column Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Recent Deals */}
        <div className="bg-tech-card border border-tech-border rounded-2xl p-6 card-glow">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-white">近期大额交易</h3>
            <Calendar className="w-5 h-5 text-tech-text-muted" />
          </div>
          
          <div className="space-y-4">
            {recentDeals.map((deal, index) => (
              <div key={index} className="p-4 bg-tech-dark rounded-xl border border-tech-border hover:border-tech-accent/30 transition-colors">
                <div className="flex items-start justify-between mb-2">
                  <div>
                    <p className="font-semibold text-white">{deal.company}</p>
                    <p className="text-sm text-tech-text-muted">{deal.sector} · {deal.round}</p>
                  </div>
                  <span className="text-tech-accent font-mono font-semibold">{deal.amount}</span>
                </div>
                <p className="text-sm text-tech-text-muted">投资方: {deal.investor}</p>
                <p className="text-xs text-tech-text-muted mt-1">{deal.date}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Active VCs */}
        <div className="bg-tech-card border border-tech-border rounded-2xl p-6 card-glow">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-white">活跃投资机构</h3>
            <Building className="w-5 h-5 text-tech-text-muted" />
          </div>
          
          <div className="space-y-3">
            {activeVCs.map((vc, index) => (
              <div key={index} className="flex items-center gap-4 p-4 bg-tech-dark rounded-xl border border-tech-border">
                <div className="w-10 h-10 rounded-lg bg-tech-accent-dim flex items-center justify-center text-tech-accent font-bold">
                  {index + 1}
                </div>
                <div className="flex-1">
                  <p className="font-medium text-white">{vc.name}</p>
                  <p className="text-sm text-tech-text-muted">{vc.focus}</p>
                </div>
                <div className="text-right">
                  <p className="font-mono text-tech-accent">{vc.deals}笔</p>
                  <p className="text-xs text-tech-text-muted">{vc.stage}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Market Insight */}
      <div className="bg-gradient-to-r from-tech-accent-dim to-transparent border border-tech-accent/20 rounded-2xl p-6">
        <h3 className="text-lg font-semibold text-white mb-4">市场洞察</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm">
          <div>
            <p className="text-tech-text-muted mb-2">🚀 AI赛道持续火热</p>
            <p className="text-tech-text">人工智能领域投资同比增长45%，大模型、自动驾驶成为投资热点</p>
          </div>
          <div>
            <p className="text-tech-text-muted mb-2">💰 大额融资增多</p>
            <p className="text-tech-text">单笔超过10亿元的融资占比提升至15%，头部效应明显</p>
          </div>
          <div>
            <p className="text-tech-text-muted mb-2">🌍 国际化布局加速</p>
            <p className="text-tech-text">出海企业融资活跃，东南亚、中东成为新的投资目的地</p>
          </div>
        </div>
      </div>
    </div>
  )
}

// Stat Card Component
function StatCard({ 
  title, 
  value, 
  icon: Icon, 
  change, 
  positive 
}: { 
  title: string
  value: string
  icon: React.ElementType
  change: string
  positive: boolean
}) {
  return (
    <div className="bg-tech-card border border-tech-border rounded-2xl p-6 card-glow">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-tech-text-muted mb-1">{title}</p>
          <p className="text-2xl font-bold text-white number-font">{value}</p>
          <p className={`text-sm mt-2 ${positive ? 'text-green-400' : 'text-red-400'}`}>
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
