'use client'

import React, { useState } from 'react'
import { TrendingUp, Building2, FileText, Activity, BarChart3, Globe } from 'lucide-react'
import StarBoardData from '../components/StarBoardData'
import VCAnalysis from '../components/VCAnalysis'
import PolicyInsight from '../components/PolicyInsight'

export default function Home() {
  const [activeTab, setActiveTab] = useState<'starboard' | 'vc' | 'policy'>('starboard')

  const tabs = [
    { id: 'starboard' as const, label: '科创板数据', icon: TrendingUp },
    { id: 'vc' as const, label: 'VC市场分析', icon: Building2 },
    { id: 'policy' as const, label: '政策解读', icon: FileText },
  ]

  return (
    <main className="min-h-screen bg-tech-dark">
      {/* Header */}
      <header className="border-b border-tech-border bg-tech-dark/80 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-tech-accent to-blue-600 flex items-center justify-center">
                <Activity className="w-5 h-5 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-white">
                  科创金融研究院
                </h1>
                <p className="text-xs text-tech-text-muted">Tech Finance Hub</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <span className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-tech-accent-dim text-tech-accent text-sm">
                <span className="w-2 h-2 rounded-full bg-tech-accent live-indicator"></span>
                实时数据更新
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="border-b border-tech-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-1">
            {tabs.map((tab) => {
              const Icon = tab.icon
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-2 px-6 py-4 text-sm font-medium transition-colors border-b-2 ${
                    activeTab === tab.id
                      ? 'border-tech-accent text-tech-accent'
                      : 'border-transparent text-tech-text-muted hover:text-white'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  {tab.label}
                </button>
              )
            })}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'starboard' && <StarBoardData />}
        {activeTab === 'vc' && <VCAnalysis />}
        {activeTab === 'policy' && <PolicyInsight />}
      </div>

      {/* Footer */}
      <footer className="border-t border-tech-border mt-16 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <p className="text-sm text-tech-text-muted">
              © 2024 科创金融研究院 | Stay Hungry, Stay Foolish
            </p>
            <div className="flex items-center gap-4 text-sm text-tech-text-muted">
              <span className="flex items-center gap-1">
                <Globe className="w-4 h-4" />
                Data sources: 科创板 | Wind | 公开信息
              </span>
            </div>
          </div>
        </div>
      </footer>
    </main>
  )
}
