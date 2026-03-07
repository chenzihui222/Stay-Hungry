'use client'

import React, { useState } from 'react'
import { Activity, Globe, TrendingUp, Building2, FileText, ArrowUpRight, BarChart3, Shield, Zap, Target } from 'lucide-react'
import Carousel from '../components/Carousel'
import StarBoardData from '../components/StarBoardData'
import VCAnalysis from '../components/VCAnalysis'
import PolicyInsight from '../components/PolicyInsight'

type SectionType = 'home' | 'starboard' | 'vc' | 'policy'

export default function Home() {
  const [activeSection, setActiveSection] = useState<SectionType>('home')
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  const sections = [
    { id: 'home' as const, label: '首页', icon: Activity },
    { id: 'starboard' as const, label: '科创板', icon: TrendingUp },
    { id: 'vc' as const, label: 'VC市场', icon: Building2 },
    { id: 'policy' as const, label: '政策解读', icon: FileText },
  ]

  const handleCarouselClick = (slideId: string) => {
    setActiveSection(slideId as SectionType)
  }

  const cards = [
    { 
      id: 'starboard', 
      title: '科创板数据', 
      subtitle: 'STAR Market',
      desc: '实时行情、板块表现、资金流向、个股分析，全面掌握科创板市场动态',
      icon: TrendingUp,
      stats: [
        { label: '上市公司', value: '573', unit: '家' },
        { label: '总市值', value: '6.85', unit: '万亿' },
      ],
      color: 'blue',
      gradient: 'from-blue-600/20 to-cyan-600/20',
      accent: 'bg-blue-500',
      borderColor: 'border-blue-500/20',
      hoverBorder: 'hover:border-blue-500/40'
    },
    { 
      id: 'vc', 
      title: 'VC市场分析', 
      subtitle: 'Venture Capital',
      desc: '投资趋势、赛道热度、机构动态、项目追踪，深度洞察VC投资生态',
      icon: Building2,
      stats: [
        { label: '活跃机构', value: '1,200+', unit: '' },
        { label: '月度交易', value: '380', unit: '笔' },
      ],
      color: 'emerald',
      gradient: 'from-emerald-600/20 to-teal-600/20',
      accent: 'bg-emerald-500',
      borderColor: 'border-emerald-500/20',
      hoverBorder: 'hover:border-emerald-500/40'
    },
    { 
      id: 'policy', 
      title: '政策解读', 
      subtitle: 'Policy',
      desc: '监管政策、行业动态、深度分析、前瞻性研究，把握政策脉搏',
      icon: FileText,
      stats: [
        { label: '本周更新', value: '12', unit: '条' },
        { label: '深度报告', value: '48', unit: '份' },
      ],
      color: 'amber',
      gradient: 'from-amber-600/20 to-orange-600/20',
      accent: 'bg-amber-500',
      borderColor: 'border-amber-500/20',
      hoverBorder: 'hover:border-amber-500/40'
    },
  ]

  const features = [
    { 
      title: '实时数据', 
      desc: '毫秒级行情更新，实时追踪市场动态',
      icon: Zap,
      color: 'text-yellow-400',
      bgColor: 'bg-yellow-400/10'
    },
    { 
      title: '深度分析', 
      desc: '专业投研团队，提供独到市场见解',
      icon: BarChart3,
      color: 'text-blue-400',
      bgColor: 'bg-blue-400/10'
    },
    { 
      title: '智能预警', 
      desc: '关键指标监控，及时捕捉投资机会',
      icon: Target,
      color: 'text-emerald-400',
      bgColor: 'bg-emerald-400/10'
    },
    { 
      title: '全景报告', 
      desc: '多维度数据分析，生成专业研究报告',
      icon: Shield,
      color: 'text-purple-400',
      bgColor: 'bg-purple-400/10'
    },
  ]

  return (
    <div className="min-h-screen bg-slate-950">
      {/* Navigation */}
      <header className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        activeSection !== 'home' ? 'bg-slate-950/80 backdrop-blur-xl border-b border-white/5' : ''
      }`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-20">
            {/* Logo */}
            <button 
              onClick={() => setActiveSection('home')}
              className="flex items-center gap-3 group"
            >
              <div className="w-10 h-10 rounded-xl bg-white flex items-center justify-center group-hover:scale-105 transition-transform">
                <Activity className="w-5 h-5 text-slate-950" />
              </div>
              <div className="hidden sm:block">
                <h1 className="text-lg font-bold text-white tracking-tight">科创金融研究</h1>
                <p className="text-[10px] text-white/40 tracking-widest uppercase">Tech Finance Research</p>
              </div>
            </button>

            {/* Desktop Navigation */}
            <nav className="hidden md:flex items-center gap-1">
              {sections.map((section) => {
                const Icon = section.icon
                const isActive = activeSection === section.id
                return (
                  <button
                    key={section.id}
                    onClick={() => setActiveSection(section.id)}
                    className={`relative px-5 py-2.5 rounded-full text-sm font-medium transition-all ${
                      isActive
                        ? 'text-white'
                        : 'text-white/50 hover:text-white'
                    }`}
                  >
                    {isActive && (
                      <span className="absolute inset-0 bg-white/10 rounded-full" />
                    )}
                    <span className="relative flex items-center gap-2">
                      <Icon className="w-4 h-4" />
                      {section.label}
                    </span>
                  </button>
                )
              })}
            </nav>

            {/* CTA */}
            <div className="flex items-center gap-4">
              <span className="hidden lg:flex items-center gap-2 px-4 py-2 rounded-full bg-emerald-500/10 text-emerald-400 text-xs font-medium border border-emerald-500/20">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                数据实时更新
              </span>
              
              <button className="md:hidden p-2 text-white" onClick={() => setIsMenuOpen(!isMenuOpen)}>
                <div className="w-6 h-5 flex flex-col justify-between">
                  <span className={`w-full h-0.5 bg-white transition-all ${isMenuOpen ? 'rotate-45 translate-y-2' : ''}`} />
                  <span className={`w-full h-0.5 bg-white transition-all ${isMenuOpen ? 'opacity-0' : ''}`} />
                  <span className={`w-full h-0.5 bg-white transition-all ${isMenuOpen ? '-rotate-45 -translate-y-2' : ''}`} />
                </div>
              </button>
            </div>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden bg-slate-950/95 backdrop-blur-xl border-t border-white/5">
            <nav className="px-4 py-4 space-y-2">
              {sections.map((section) => {
                const Icon = section.icon
                return (
                  <button
                    key={section.id}
                    onClick={() => {
                      setActiveSection(section.id)
                      setIsMenuOpen(false)
                    }}
                    className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-left transition-colors ${
                      activeSection === section.id
                        ? 'bg-white/10 text-white'
                        : 'text-white/60 hover:bg-white/5 hover:text-white'
                    }`}
                  >
                    <Icon className="w-5 h-5" />
                    {section.label}
                  </button>
                )
              })}
            </nav>
          </div>
        )}
      </header>

      {/* Main Content */}
      {activeSection === 'home' ? (
        <>
          {/* Hero Carousel */}
          <Carousel onSlideClick={handleCarouselClick} />

          {/* Quick Access Section */}
          <section className="relative py-32 bg-slate-950">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              {/* Section Header */}
              <div className="text-center mb-20">
                <span className="inline-block px-4 py-1.5 rounded-full bg-white/5 text-white/50 text-xs font-medium tracking-wider uppercase mb-6">
                  Quick Access
                </span>
                <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
                  三大核心板块
                </h2>
                <p className="text-white/40 text-lg max-w-2xl mx-auto">
                  全方位覆盖科创板、VC投资与政策研究，为您的投资决策提供专业数据支持
                </p>
              </div>

              {/* Cards Grid */}
              <div className="grid md:grid-cols-3 gap-6">
                {cards.map((card) => {
                  const Icon = card.icon
                  return (
                    <button
                      key={card.id}
                      onClick={() => setActiveSection(card.id as SectionType)}
                      className={`group relative text-left rounded-2xl p-8 bg-gradient-to-br ${card.gradient} border ${card.borderColor} ${card.hoverBorder} transition-all duration-300 hover:scale-[1.02] hover:shadow-2xl`}
                    >
                      {/* Header */}
                      <div className="flex items-start justify-between mb-8">
                        <div>
                          <span className="text-white/40 text-xs font-medium tracking-wider uppercase">{card.subtitle}</span>
                          <h3 className="text-2xl font-bold text-white mt-1">{card.title}</h3>
                        </div>
                        <div className={`w-12 h-12 rounded-xl ${card.accent} flex items-center justify-center group-hover:scale-110 transition-transform`}>
                          <Icon className="w-6 h-6 text-white" />
                        </div>
                      </div>

                      {/* Description */}
                      <p className="text-white/50 mb-8 leading-relaxed">{card.desc}</p>

                      {/* Stats */}
                      <div className="grid grid-cols-2 gap-4 mb-8">
                        {card.stats.map((stat, idx) => (
                          <div key={idx} className="bg-white/5 rounded-xl p-4">
                            <div className="flex items-baseline gap-1">
                              <span className="text-2xl font-bold text-white">{stat.value}</span>
                              <span className="text-white/40 text-sm">{stat.unit}</span>
                            </div>
                            <span className="text-white/30 text-xs">{stat.label}</span>
                          </div>
                        ))}
                      </div>

                      {/* CTA */}
                      <div className="flex items-center justify-between">
                        <span className="text-white/40 text-sm group-hover:text-white transition-colors">进入板块</span>
                        <div className="w-10 h-10 rounded-full bg-white/5 flex items-center justify-center group-hover:bg-white group-hover:text-slate-950 transition-all">
                          <ArrowUpRight className="w-5 h-5 text-white group-hover:text-slate-950" />
                        </div>
                      </div>
                    </button>
                  )
                })}
              </div>
            </div>
          </section>

          {/* Features Section */}
          <section className="relative py-32 bg-slate-900/30">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="text-center mb-20">
                <span className="inline-block px-4 py-1.5 rounded-full bg-white/5 text-white/50 text-xs font-medium tracking-wider uppercase mb-6">
                  Features
                </span>
                <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
                  专业的研究平台
                </h2>
                <p className="text-white/40 text-lg max-w-2xl mx-auto">
                  深度洞察科创板市场动态、VC投资趋势和政策走向
                </p>
              </div>

              <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                {features.map((feature, index) => {
                  const Icon = feature.icon
                  return (
                    <div key={index} className="group text-center p-8">
                      <div className={`w-16 h-16 rounded-2xl ${feature.bgColor} ${feature.color} flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform`}>
                        <Icon className="w-8 h-8" />
                      </div>
                      <h3 className="text-lg font-semibold text-white mb-3">{feature.title}</h3>
                      <p className="text-white/40 text-sm leading-relaxed">{feature.desc}</p>
                    </div>
                  )
                })}
              </div>
            </div>
          </section>

          {/* Stats Banner */}
          <section className="relative py-20 bg-slate-950 border-y border-white/5">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
                {[
                  { value: '573', label: '科创板上市公司', suffix: '家' },
                  { value: '6.85', label: '总市值', suffix: '万亿' },
                  { value: '1200+', label: '活跃VC机构', suffix: '' },
                  { value: '48', label: '深度研究报告', suffix: '份/月' },
                ].map((stat, index) => (
                  <div key={index} className="text-center">
                    <div className="flex items-baseline justify-center gap-1 mb-2">
                      <span className="text-4xl md:text-5xl font-bold text-white">{stat.value}</span>
                      <span className="text-white/40">{stat.suffix}</span>
                    </div>
                    <span className="text-white/30 text-sm">{stat.label}</span>
                  </div>
                ))}
              </div>
            </div>
          </section>
        </>
      ) : (
        <div className="pt-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            {activeSection === 'starboard' && <StarBoardData />}
            {activeSection === 'vc' && <VCAnalysis />}
            {activeSection === 'policy' && <PolicyInsight />}
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="bg-slate-950 border-t border-white/5">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="flex flex-col md:flex-row items-center justify-between gap-6">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-lg bg-white flex items-center justify-center">
                <Activity className="w-4 h-4 text-slate-950" />
              </div>
              <span className="text-white font-semibold">科创金融研究</span>
            </div>
            
            <p className="text-sm text-white/30">
              © 2024 Tech Finance Research. Stay Hungry, Stay Foolish.
            </p>
            
            <div className="flex items-center gap-2 text-sm text-white/30">
              <Globe className="w-4 h-4" />
              <span>数据来源: 科创板 | Wind | 公开市场</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
