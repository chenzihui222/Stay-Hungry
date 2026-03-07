'use client'

import React from 'react'
import { FileText, Scale, Building2, TrendingUp, Calendar, ExternalLink } from 'lucide-react'

// 政策数据（示例数据）
const recentPolicies = [
  {
    id: 1,
    title: '关于深化科创板改革 服务科技创新和新质生产力发展的八条措施',
    issuer: '中国证监会',
    date: '2024-03-05',
    category: '资本市场',
    impact: 'high',
    summary: '强化科创板"硬科技"定位，优化发行承销制度，更大力度支持并购重组，完善股权激励制度。',
  },
  {
    id: 2,
    title: '创业投资高质量发展指导意见',
    issuer: '国务院办公厅',
    date: '2024-02-28',
    category: '创投政策',
    impact: 'high',
    summary: '完善创业投资"募投管退"机制，拓宽长期资金来源，发挥政府引导基金作用。',
  },
  {
    id: 3,
    title: '国家集成电路产业投资基金三期成立',
    issuer: '财政部等',
    date: '2024-02-20',
    category: '产业基金',
    impact: 'medium',
    summary: '注册资本3440亿元，重点投向集成电路全产业链，支持半导体设备、材料等领域。',
  },
  {
    id: 4,
    title: '关于支持科技型企业融资的实施意见',
    issuer: '央行、科技部',
    date: '2024-02-15',
    category: '金融支持',
    impact: 'medium',
    summary: '完善科技型企业信贷服务，健全科技金融专营体系，创新科技信贷产品。',
  },
  {
    id: 5,
    title: '新《公司法》关于股份有限公司注册资本实缴规定',
    issuer: '全国人大',
    date: '2024-01-01',
    category: '法律法规',
    impact: 'high',
    summary: '股份有限公司注册资本实缴制度调整，涉及股东出资义务、公司治理结构等。',
  },
]

const policyCategories = [
  { name: '资本市场', count: 12, color: 'bg-blue-500' },
  { name: '创投政策', count: 8, color: 'bg-green-500' },
  { name: '产业基金', count: 6, color: 'bg-purple-500' },
  { name: '金融支持', count: 15, color: 'bg-orange-500' },
  { name: '税收优惠', count: 4, color: 'bg-pink-500' },
  { name: '法律法规', count: 9, color: 'bg-cyan-500' },
]

const regulatoryUpdates = [
  { 
    date: '2024-03-07', 
    title: '上交所修订科创板上市审核规则', 
    source: '上交所',
    type: '监管动态'
  },
  { 
    date: '2024-03-06', 
    title: '北交所发布直联机制优化举措', 
    source: '北交所',
    type: '监管动态'
  },
  { 
    date: '2024-03-05', 
    title: '证监会召开科技监管工作座谈会', 
    source: '证监会',
    type: '会议动态'
  },
  { 
    date: '2024-03-04', 
    title: '中基协发布私募基金登记备案新规', 
    source: '中基协',
    type: '监管动态'
  },
]

const impactLabels: Record<string, { text: string; color: string }> = {
  high: { text: '高影响', color: 'bg-red-500/20 text-red-400 border-red-500/30' },
  medium: { text: '中影响', color: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30' },
  low: { text: '一般', color: 'bg-green-500/20 text-green-400 border-green-500/30' },
}

export default function PolicyInsight() {
  return (
    <div className="space-y-8">
      {/* Page Title */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-white mb-2">政策解读</h2>
        <p className="text-tech-text-muted">Policy Insight · 追踪监管政策与市场动态</p>
      </div>

      {/* Policy Categories */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        {policyCategories.map((cat) => (
          <div 
            key={cat.name}
            className="bg-tech-card border border-tech-border rounded-xl p-4 hover:border-tech-accent/50 transition-colors cursor-pointer"
          >
            <div className={`w-3 h-3 rounded-full ${cat.color} mb-3`}></div>
            <p className="text-white font-medium">{cat.name}</p>
            <p className="text-2xl font-bold text-tech-accent number-font mt-1">{cat.count}</p>
            <p className="text-xs text-tech-text-muted mt-1">条政策</p>
          </div>
        ))}
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left: Recent Policies */}
        <div className="lg:col-span-2 space-y-6">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold text-white flex items-center gap-2">
              <FileText className="w-5 h-5 text-tech-accent" />
              最新政策解读
            </h3>
            <button className="text-sm text-tech-accent hover:underline">查看全部 →</button>
          </div>

          {recentPolicies.map((policy) => {
            const impact = impactLabels[policy.impact]
            return (
              <div 
                key={policy.id}
                className="bg-tech-card border border-tech-border rounded-2xl p-6 card-glow hover:border-tech-accent/30 transition-all"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <span className="px-3 py-1 rounded-full text-xs font-medium border bg-tech-accent-dim text-tech-accent border-tech-accent/30">
                      {policy.category}
                    </span>
                    <span className={`px-3 py-1 rounded-full text-xs font-medium border ${impact.color}`}>
                      {impact.text}
                    </span>
                  </div>
                  <span className="text-sm text-tech-text-muted">{policy.date}</span>
                </div>

                <h4 className="text-lg font-semibold text-white mb-2 hover:text-tech-accent transition-colors cursor-pointer">
                  {policy.title}
                </h4>

                <div className="flex items-center gap-2 text-sm text-tech-text-muted mb-3">
                  <Building2 className="w-4 h-4" />
                  {policy.issuer}
                </div>

                <p className="text-tech-text text-sm leading-relaxed">
                  {policy.summary}
                </p>

                <div className="mt-4 pt-4 border-t border-tech-border flex items-center justify-between">
                  <div className="flex items-center gap-4 text-sm">
                    <span className="text-tech-text-muted">
                      <TrendingUp className="w-4 h-4 inline mr-1" />
                      关注热度: <span className="text-tech-accent">高</span>
                    </span>
                  </div>
                  <button className="flex items-center gap-1 text-sm text-tech-accent hover:underline">
                    阅读全文 <ExternalLink className="w-4 h-4" />
                  </button>
                </div>
              </div>
            )
          })}
        </div>

        {/* Right: Sidebar */}
        <div className="space-y-6">
          {/* Regulatory Updates */}
          <div className="bg-tech-card border border-tech-border rounded-2xl p-6 card-glow">
            <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
              <Scale className="w-5 h-5 text-tech-accent" />
              监管动态
            </h3>

            <div className="space-y-4">
              {regulatoryUpdates.map((update, index) => (
                <div key={index} className="pb-4 border-b border-tech-border last:border-0 last:pb-0">
                  <div className="flex items-center gap-2 text-xs text-tech-text-muted mb-2">
                    <Calendar className="w-3 h-3" /> {update.date}
                    <span className="px-2 py-0.5 rounded bg-tech-accent-dim text-tech-accent">{update.type}</span>
                  </div>
                  <p className="text-sm text-white hover:text-tech-accent cursor-pointer transition-colors">
                    {update.title}
                  </p>
                  <p className="text-xs text-tech-text-muted mt-1">来源: {update.source}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Key Policy Highlights */}
          <div className="bg-gradient-to-br from-tech-accent-dim to-transparent border border-tech-accent/20 rounded-2xl p-6">
            <h3 className="text-lg font-semibold text-white mb-4">重点政策速递</h3>
            
            <div className="space-y-3 text-sm">
              <div className="flex items-start gap-2">
                <span className="w-6 h-6 rounded-full bg-tech-accent/20 text-tech-accent flex items-center justify-center text-xs font-bold flex-shrink-0">1</span>
                <p className="text-tech-text">科创板八条措施正式落地，IPO审核趋严</p>
              </div>
              <div className="flex items-start gap-2">
                <span className="w-6 h-6 rounded-full bg-tech-accent/20 text-tech-accent flex items-center justify-center text-xs font-bold flex-shrink-0">2</span>
                <p className="text-tech-text">大基金三期设立，半导体产业再迎利好</p>
              </div>
              <div className="flex items-start gap-2">
                <span className="w-6 h-6 rounded-full bg-tech-accent/20 text-tech-accent flex items-center justify-center text-xs font-bold flex-shrink-0">3</span>
                <p className="text-tech-text">创投退出机制优化，S基金迎来发展机遇</p>
              </div>
            </div>
          </div>

          {/* Subscribe CTA */}
          <div className="bg-tech-card border border-tech-border rounded-2xl p-6 text-center">
            <h4 className="text-white font-semibold mb-2">获取政策更新</h4>
            <p className="text-sm text-tech-text-muted mb-4">订阅邮件，第一时间掌握政策动态</p>
            <button className="w-full py-2 px-4 bg-tech-accent text-tech-dark font-semibold rounded-lg hover:bg-tech-accent/90 transition-colors">
              立即订阅
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
