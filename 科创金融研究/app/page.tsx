'use client'

import React, { useState, useEffect } from 'react'
import { TrendingUp, Building2, FileText, ArrowUpRight, Circle } from 'lucide-react'
import StarBoardData from '../components/StarBoardData'
import VCAnalysis from '../components/VCAnalysis'
import PolicyInsight from '../components/PolicyInsight'

type SectionType = 'home' | 'starboard' | 'vc' | 'policy'

const sections = [
  {
    id: 'starboard' as const,
    title: '科创板数据',
    subtitle: 'STAR Market Data',
    description: '实时行情、板块表现、资金流向、个股分析',
    icon: TrendingUp,
    color: 'text-blue-400',
    bgColor: 'bg-blue-400/10',
    borderColor: 'border-blue-400/20',
  },
  {
    id: 'vc' as const,
    title: 'VC市场分析',
    subtitle: 'Venture Capital Analysis',
    description: '投资趋势、赛道热度、机构动态、项目追踪',
    icon: Building2,
    color: 'text-emerald-400',
    bgColor: 'bg-emerald-400/10',
    borderColor: 'border-emerald-400/20',
  },
  {
    id: 'policy' as const,
    title: '政策解读',
    subtitle: 'Policy Insights',
    description: '监管政策、行业动态、深度分析、前瞻性研究',
    icon: FileText,
    color: 'text-amber-400',
    bgColor: 'bg-amber-400/10',
    borderColor: 'border-amber-400/20',
  },
]

export default function Home() {
  const [activeSection, setActiveSection] = useState<SectionType>('home')
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 })

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setMousePos({ x: e.clientX, y: e.clientY })
    }
    window.addEventListener('mousemove', handleMouseMove)
    return () => window.removeEventListener('mousemove', handleMouseMove)
  }, [])

  const currentSection = sections.find(s => s.id === activeSection)

  return (
    <div className="min-h-screen bg-[#0a0a0b] text-gray-300 font-sans selection:bg-blue-500/30">
      {/* Accent bar */}
      <div className="fixed top-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-500 via-emerald-500 to-amber-500 z-50" />

      {/* Mouse glow effect */}
      <div 
        className="fixed pointer-events-none z-40 transition-opacity duration-300"
        style={{
          left: mousePos.x - 150,
          top: mousePos.y - 150,
          width: 300,
          height: 300,
          background: 'radial-gradient(circle, rgba(59, 130, 246, 0.08) 0%, transparent 70%)',
          filter: 'blur(40px)',
        }}
      />

      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-30 px-6 py-4">
        <div className="max-w-3xl mx-auto flex items-center justify-between">
          <button 
            onClick={() => setActiveSection('home')}
            className="flex items-center gap-2 text-white hover:opacity-70 transition-opacity"
          >
            <Circle className="w-2 h-2 fill-current" />
            <span className="font-medium tracking-tight">科创金融研究</span>
          </button>

          <div className="flex items-center gap-6 text-sm">
            <a 
              href="https://zihuichen.com" 
              target="_blank" 
              rel="noopener noreferrer"
              className="hover:text-white transition-colors"
            >
              Home
            </a>
            <a 
              href="https://vc.zihuichen.com" 
              target="_blank" 
              rel="noopener noreferrer"
              className="hover:text-white transition-colors"
            >
              VC Radar
            </a>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="pt-24 pb-32 px-6">
        <div className="max-w-3xl mx-auto">
          {activeSection === 'home' ? (
            <>
              {/* Header */}
              <header className="mb-12">
                <h1 className="text-3xl font-semibold text-white mb-3">
                  科创金融研究
                </h1>
                <p className="text-gray-500">
                  科创板 · VC市场 · 政策解读
                </p>
              </header>

              {/* Section Cards */}
              <div className="space-y-4">
                {sections.map((section) => {
                  const Icon = section.icon
                  return (
                    <button
                      key={section.id}
                      onClick={() => setActiveSection(section.id)}
                      className={`w-full text-left group relative p-6 rounded-2xl border ${section.borderColor} ${section.bgColor} hover:bg-opacity-20 transition-all duration-300`}
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex items-start gap-4">
                          <div className={`w-10 h-10 rounded-xl ${section.bgColor} ${section.color} flex items-center justify-center flex-shrink-0`}>
                            <Icon className="w-5 h-5" />
                          </div>
                          
                          <div>
                            <h2 className="text-lg font-medium text-white mb-1 group-hover:text-gray-200 transition-colors">
                              {section.title}
                            </h2>
                            <p className="text-xs text-gray-500 mb-2">{section.subtitle}</p>
                            <p className="text-sm text-gray-400">{section.description}</p>
                          </div>
                        </div>

                        <div className="opacity-0 group-hover:opacity-100 transition-opacity">
                          <ArrowUpRight className={`w-5 h-5 ${section.color}`} />
                        </div>
                      </div>
                    </button>
                  )
                })}
              </div>
            </>
          ) : (
            <>
              {/* Back button */}
              <button
                onClick={() => setActiveSection('home')}
                className="mb-8 text-sm text-gray-500 hover:text-white transition-colors flex items-center gap-2"
              >
                <span>← 返回</span>
              </button>

              {/* Section Header */}
              <header className="mb-8">
                {currentSection && (
                  <>
                    <div className="flex items-center gap-3 mb-4">
                      <div className={`w-10 h-10 rounded-xl ${currentSection.bgColor} ${currentSection.color} flex items-center justify-center`}>
                        <currentSection.icon className="w-5 h-5" />
                      </div>
                      <div>
                        <h1 className="text-2xl font-semibold text-white">{currentSection.title}</h1>
                        <p className="text-xs text-gray-500">{currentSection.subtitle}</p>
                      </div>
                    </div>
                    <p className="text-gray-400">{currentSection.description}</p>
                  </>
                )}
              </header>

              {/* Content */}
              <div className="bg-white/[0.02] rounded-2xl border border-white/5 p-8">
                {activeSection === 'starboard' && <StarBoardData />}
                {activeSection === 'vc' && <VCAnalysis />}
                {activeSection === 'policy' && <PolicyInsight />}
              </div>
            </>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="fixed bottom-0 left-0 right-0 bg-[#0a0a0b]/80 backdrop-blur-sm border-t border-white/5">
        <div className="max-w-3xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between text-sm">
            <div className="flex items-center gap-2 text-gray-500">
              <Circle className="w-1.5 h-1.5 fill-current" />
              <span>科创金融研究</span>
            </div>
            
            <div className="flex items-center gap-4 text-gray-600">
              <span>© 2024</span>
              <a 
                href="https://github.com/chenzihui222" 
                target="_blank" 
                rel="noopener noreferrer"
                className="hover:text-gray-400 transition-colors"
              >
                GitHub
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
