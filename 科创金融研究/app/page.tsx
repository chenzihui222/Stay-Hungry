'use client'

import React, { useState } from 'react'
import { Activity, Globe, TrendingUp, Building2, FileText, ArrowRight } from 'lucide-react'
import Carousel from '../components/Carousel'
import StarBoardData from '../components/StarBoardData'
import VCAnalysis from '../components/VCAnalysis'
import PolicyInsight from '../components/PolicyInsight'

type SectionType = 'home' | 'starboard' | 'vc' | 'policy'

export default function Home() {
  const [activeSection, setActiveSection] = useState<SectionType>('home')

  const sections = [
    { id: 'home' as const, label: '首页', icon: Activity },
    { id: 'starboard' as const, label: '科创板数据', icon: TrendingUp },
    { id: 'vc' as const, label: 'VC市场分析', icon: Building2 },
    { id: 'policy' as const, label: '政策解读', icon: FileText },
  ]

  const handleCarouselClick = (slideId: string) => {
    setActiveSection(slideId as SectionType)
  }

  return (
    <main className="min-h-screen bg-[#0a0a0f]">
      {/* Header */}
      <header className="bg-[#0a0a0f] border-b border-gray-800 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-400 flex items-center justify-center">
                <Activity className="w-5 h-5 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-white">
                  科创金融研究
                </h1>
                <p className="text-xs text-gray-400">Tech Finance Research</p>
              </div>
            </div>

            {/* Navigation */}
            <nav className="hidden md:flex items-center gap-1">
              {sections.map((section) => {
                const Icon = section.icon
                return (
                  <button
                    key={section.id}
                    onClick={() => setActiveSection(section.id)}
                    className={`flex items-center gap-2 px-5 py-2.5 rounded-lg text-sm font-medium transition-all ${
                      activeSection === section.id
                        ? 'bg-blue-500/10 text-blue-400'
                        : 'text-gray-400 hover:text-white hover:bg-gray-800/50'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    {section.label}
                  </button>
                )
              })}
            </nav>

            {/* Live indicator */}
            <div className="hidden lg:flex items-center gap-2">
              <span className="flex items-center gap-2 px-4 py-2 rounded-full bg-emerald-500/10 text-emerald-400 text-sm border border-emerald-500/20">
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                实时数据
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      {activeSection === 'home' ? (
        <>
          {/* Hero Carousel */}
          <Carousel onSlideClick={handleCarouselClick} />

          {/* Quick Access Cards */}
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 -mt-20 relative z-20">
            <div className="grid md:grid-cols-3 gap-6">
              {[
                { 
                  id: 'starboard', 
                  title: '科创板数据', 
                  desc: '实时行情与深度分析',
                  icon: TrendingUp,
                  color: 'from-blue-600 to-cyan-500',
                  stats: '500+ 上市公司'
                },
                { 
                  id: 'vc', 
                  title: 'VC市场分析', 
                  desc: '投资趋势与机构动态',
                  icon: Building2,
                  color: 'from-emerald-600 to-teal-500',
                  stats: '1000+ 投资机构'
                },
                { 
                  id: 'policy', 
                  title: '政策解读', 
                  desc: '监管动态与深度研究',
                  icon: FileText,
                  color: 'from-amber-600 to-orange-500',
                  stats: '实时政策追踪'
                },
              ].map((card) => {
                const Icon = card.icon
                return (
                  <button
                    key={card.id}
                    onClick={() => setActiveSection(card.id as SectionType)}
                    className="group relative bg-gray-900/80 backdrop-blur-sm rounded-2xl p-6 border border-gray-800 hover:border-gray-700 transition-all text-left hover:shadow-2xl hover:shadow-blue-500/10"
                  >
                    <div className={`absolute top-0 left-0 w-full h-1 bg-gradient-to-r ${card.color} rounded-t-2xl opacity-0 group-hover:opacity-100 transition-opacity`} />
                    
                    <div className={`w-14 h-14 rounded-xl bg-gradient-to-br ${card.color} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
                      <Icon className="w-7 h-7 text-white" />
                    </div>
                    
                    <h3 className="text-xl font-bold text-white mb-2">{card.title}</h3>
                    <p className="text-gray-400 mb-4">{card.desc}</p>
                    
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-500">{card.stats}</span>
                      <ArrowRight className="w-5 h-5 text-gray-500 group-hover:text-white group-hover:translate-x-1 transition-all" />
                    </div>
                  </button>
                )
              })}
            </div>
          </div>

          {/* Features Section */}
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
            <div className="text-center mb-16">
              <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
                专业的科创金融研究平台
              </h2>
              <p className="text-gray-400 max-w-2xl mx-auto">
                深度洞察科创板市场动态、VC投资趋势和政策走向，为投资决策提供数据支持
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
              {[
                { title: '实时数据', desc: '毫秒级行情更新，实时追踪市场动态', icon: '⚡' },
                { title: '深度分析', desc: '专业投研团队，提供独到市场见解', icon: '📊' },
                { title: '智能预警', desc: '关键指标监控，及时捕捉投资机会', icon: '🔔' },
                { title: '全景报告', desc: '多维度数据分析，生成专业研究报告', icon: '📄' },
              ].map((feature, index) => (
                <div key={index} className="text-center">
                  <div className="text-4xl mb-4">{feature.icon}</div>
                  <h3 className="text-lg font-semibold text-white mb-2">{feature.title}</h3>
                  <p className="text-gray-400 text-sm">{feature.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </>
      ) : (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {activeSection === 'starboard' && <StarBoardData />}
          {activeSection === 'vc' && <VCAnalysis />}
          {activeSection === 'policy' && <PolicyInsight />}
        </div>
      )}

      {/* Footer */}
      <footer className="bg-gray-900 border-t border-gray-800 mt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-cyan-400 flex items-center justify-center">
                <Activity className="w-4 h-4 text-white" />
              </div>
              <span className="text-white font-semibold">科创金融研究</span>
            </div>
            
            <p className="text-sm text-gray-500">
              © 2024 科创金融研究 | Stay Hungry, Stay Foolish
            </p>
            
            <div className="flex items-center gap-2 text-sm text-gray-500">
              <Globe className="w-4 h-4" />
              <span>数据来源: 科创板 | Wind | 公开市场</span>
            </div>
          </div>
        </div>
      </footer>
    </main>
  )
}
