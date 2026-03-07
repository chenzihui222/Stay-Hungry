'use client'

import React, { useState, useEffect, useCallback } from 'react'
import { ChevronLeft, ChevronRight, TrendingUp, Building2, FileText, ArrowRight } from 'lucide-react'

interface CarouselSlide {
  id: string
  title: string
  subtitle: string
  description: string
  icon: React.ElementType
  gradient: string
  accentColor: string
}

const slides: CarouselSlide[] = [
  {
    id: 'starboard',
    title: '科创板数据',
    subtitle: 'STAR Market',
    description: '实时行情 · 板块表现 · 资金流向 · 个股分析',
    icon: TrendingUp,
    gradient: 'from-blue-900 via-blue-800 to-cyan-700',
    accentColor: 'bg-blue-500'
  },
  {
    id: 'vc',
    title: 'VC市场分析',
    subtitle: 'Venture Capital',
    description: '投资趋势 · 赛道热度 · 机构动态 · 项目追踪',
    icon: Building2,
    gradient: 'from-emerald-900 via-teal-800 to-emerald-700',
    accentColor: 'bg-emerald-500'
  },
  {
    id: 'policy',
    title: '政策解读',
    subtitle: 'Policy Insights',
    description: '监管政策 · 行业动态 · 深度分析 · 前瞻性研究',
    icon: FileText,
    gradient: 'from-amber-900 via-orange-800 to-amber-700',
    accentColor: 'bg-amber-500'
  }
]

interface CarouselProps {
  onSlideClick?: (slideId: string) => void
}

export default function Carousel({ onSlideClick }: CarouselProps) {
  const [currentIndex, setCurrentIndex] = useState(0)
  const [isAutoPlaying, setIsAutoPlaying] = useState(true)

  const nextSlide = useCallback(() => {
    setCurrentIndex((prev) => (prev + 1) % slides.length)
  }, [])

  const prevSlide = useCallback(() => {
    setCurrentIndex((prev) => (prev - 1 + slides.length) % slides.length)
  }, [])

  const goToSlide = (index: number) => {
    setCurrentIndex(index)
  }

  useEffect(() => {
    if (!isAutoPlaying) return
    const interval = setInterval(nextSlide, 6000)
    return () => clearInterval(interval)
  }, [isAutoPlaying, nextSlide])

  return (
    <div 
      className="relative w-full h-[85vh] min-h-[600px] overflow-hidden bg-slate-950"
      onMouseEnter={() => setIsAutoPlaying(false)}
      onMouseLeave={() => setIsAutoPlaying(true)}
    >
      {/* Background Images with Overlay */}
      <div className="absolute inset-0">
        {slides.map((slide, index) => (
          <div
            key={slide.id}
            className={`absolute inset-0 transition-opacity duration-1000 ${
              index === currentIndex ? 'opacity-100' : 'opacity-0'
            }`}
          >
            {/* Gradient Background */}
            <div className={`absolute inset-0 bg-gradient-to-br ${slide.gradient}`} />
            
            {/* Animated Mesh Gradient */}
            <div className="absolute inset-0 opacity-30">
              <div 
                className="absolute inset-0"
                style={{
                  background: `
                    radial-gradient(ellipse at 20% 80%, rgba(255,255,255,0.15) 0%, transparent 50%),
                    radial-gradient(ellipse at 80% 20%, rgba(255,255,255,0.1) 0%, transparent 50%),
                    radial-gradient(ellipse at 50% 50%, rgba(255,255,255,0.05) 0%, transparent 70%)
                  `
                }}
              />
            </div>

            {/* Grid Pattern */}
            <div 
              className="absolute inset-0 opacity-[0.03]"
              style={{
                backgroundImage: `linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px),
                                  linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px)`,
                backgroundSize: '100px 100px'
              }}
            />
          </div>
        ))}
        
        {/* Dark Overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/60 to-transparent" />
        <div className="absolute inset-0 bg-gradient-to-r from-slate-950/80 via-transparent to-slate-950/80" />
      </div>

      {/* Content */}
      <div className="relative h-full flex items-center">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            {/* Left: Text Content */}
            <div className="space-y-8">
              {slides.map((slide, index) => {
                const Icon = slide.icon
                return (
                  <div
                    key={slide.id}
                    className={`transition-all duration-700 ${
                      index === currentIndex 
                        ? 'opacity-100 translate-y-0' 
                        : 'opacity-0 translate-y-8 absolute pointer-events-none'
                    }`}
                  >
                    {/* Label */}
                    <div className="inline-flex items-center gap-2 mb-6">
                      <div className={`w-12 h-[2px] ${slide.accentColor}`} />
                      <span className="text-white/70 text-sm font-medium tracking-widest uppercase">
                        {slide.subtitle}
                      </span>
                    </div>
                    
                    {/* Title */}
                    <h2 className="text-5xl md:text-7xl font-bold text-white mb-6 leading-tight">
                      {slide.title}
                    </h2>
                    
                    {/* Description */}
                    <p className="text-xl text-white/60 mb-8 max-w-lg leading-relaxed">
                      {slide.description}
                    </p>
                    
                    {/* CTA Button */}
                    <button 
                      onClick={() => onSlideClick?.(slide.id)}
                      className="group inline-flex items-center gap-3 px-8 py-4 bg-white text-slate-900 rounded-full font-semibold hover:bg-white/90 transition-all hover:gap-4"
                    >
                      <span>查看详情</span>
                      <ArrowRight className="w-5 h-5" />
                    </button>
                  </div>
                )
              })}
            </div>

            {/* Right: Visual Element */}
            <div className="hidden lg:flex justify-center items-center">
              <div className="relative">
                {slides.map((slide, index) => {
                  const Icon = slide.icon
                  return (
                    <div
                      key={slide.id}
                      className={`transition-all duration-700 ${
                        index === currentIndex 
                          ? 'opacity-100 scale-100' 
                          : 'opacity-0 scale-90 absolute inset-0'
                      }`}
                    >
                      {/* Main Circle */}
                      <div className={`w-80 h-80 rounded-full border border-white/10 flex items-center justify-center relative`}>
                        <div className={`absolute inset-4 rounded-full bg-gradient-to-br ${slide.gradient} opacity-20`} />
                        <div className="absolute inset-8 rounded-full border border-white/5" />
                        <Icon className="w-32 h-32 text-white/80" strokeWidth={0.5} />
                      </div>
                      
                      {/* Orbiting Elements */}
                      <div className="absolute inset-0 animate-spin" style={{ animationDuration: '20s' }}>
                        <div className={`absolute -top-2 left-1/2 -translate-x-1/2 w-4 h-4 rounded-full ${slide.accentColor}`} />
                      </div>
                      <div className="absolute inset-0 animate-spin" style={{ animationDuration: '15s', animationDirection: 'reverse' }}>
                        <div className={`absolute top-1/2 -right-2 -translate-y-1/2 w-3 h-3 rounded-full bg-white/30`} />
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Indicators */}
      <div className="absolute bottom-12 left-1/2 -translate-x-1/2 flex items-center gap-8">
        {/* Slide Numbers */}
        <div className="flex items-center gap-4">
          {slides.map((slide, index) => (
            <button
              key={index}
              onClick={() => goToSlide(index)}
              className={`group flex items-center gap-3 transition-all duration-300 ${
                index === currentIndex ? 'opacity-100' : 'opacity-40 hover:opacity-70'
              }`}
            >
              <span className={`text-sm font-mono transition-colors ${
                index === currentIndex ? 'text-white' : 'text-white/50'
              }`}>
                {String(index + 1).padStart(2, '0')}
              </span>
              <div className={`h-[2px] transition-all duration-500 ${
                index === currentIndex 
                  ? `w-16 ${slide.accentColor}` 
                  : 'w-8 bg-white/30 group-hover:w-12'
              }`} />
            </button>
          ))}
        </div>
      </div>

      {/* Navigation Arrows */}
      <button
        onClick={prevSlide}
        className="absolute left-8 top-1/2 -translate-y-1/2 w-14 h-14 rounded-full border border-white/10 bg-white/5 backdrop-blur-sm flex items-center justify-center text-white hover:bg-white/10 hover:border-white/20 transition-all"
      >
        <ChevronLeft className="w-6 h-6" />
      </button>
      
      <button
        onClick={nextSlide}
        className="absolute right-8 top-1/2 -translate-y-1/2 w-14 h-14 rounded-full border border-white/10 bg-white/5 backdrop-blur-sm flex items-center justify-center text-white hover:bg-white/10 hover:border-white/20 transition-all"
      >
        <ChevronRight className="w-6 h-6" />
      </button>

      {/* Scroll Indicator */}
      <div className="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 text-white/30">
        <span className="text-xs tracking-widest uppercase">Scroll</span>
        <div className="w-[1px] h-8 bg-gradient-to-b from-white/30 to-transparent" />
      </div>
    </div>
  )
}
