'use client'

import React, { useState, useEffect, useCallback } from 'react'
import { ChevronLeft, ChevronRight, TrendingUp, Building2, FileText } from 'lucide-react'

interface CarouselSlide {
  id: string
  title: string
  subtitle: string
  description: string
  icon: React.ElementType
  gradient: string
  imageUrl: string
}

const slides: CarouselSlide[] = [
  {
    id: 'starboard',
    title: '科创板数据',
    subtitle: 'STAR Market Data',
    description: '实时行情 · 板块表现 · 资金流向 · 个股分析',
    icon: TrendingUp,
    gradient: 'from-blue-600 via-cyan-500 to-blue-400',
    imageUrl: '/images/slide-starboard.jpg'
  },
  {
    id: 'vc',
    title: 'VC市场分析',
    subtitle: 'VC Market Analysis',
    description: '投资趋势 · 赛道热度 · 机构动态 · 项目追踪',
    icon: Building2,
    gradient: 'from-emerald-600 via-teal-500 to-emerald-400',
    imageUrl: '/images/slide-vc.jpg'
  },
  {
    id: 'policy',
    title: '政策解读',
    subtitle: 'Policy Insights',
    description: '监管政策 · 行业动态 · 深度分析 · 前瞻性研究',
    icon: FileText,
    gradient: 'from-amber-600 via-orange-500 to-amber-400',
    imageUrl: '/images/slide-policy.jpg'
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
    const interval = setInterval(nextSlide, 5000)
    return () => clearInterval(interval)
  }, [isAutoPlaying, nextSlide])

  return (
    <div 
      className="relative w-full h-[600px] overflow-hidden bg-gray-900"
      onMouseEnter={() => setIsAutoPlaying(false)}
      onMouseLeave={() => setIsAutoPlaying(true)}
    >
      {/* Slides */}
      <div 
        className="flex transition-transform duration-700 ease-out h-full"
        style={{ transform: `translateX(-${currentIndex * 100}%)` }}
      >
        {slides.map((slide, index) => {
          const Icon = slide.icon
          return (
            <div 
              key={slide.id}
              className="w-full h-full flex-shrink-0 relative cursor-pointer group"
              onClick={() => onSlideClick?.(slide.id)}
            >
              {/* Background with gradient */}
              <div className={`absolute inset-0 bg-gradient-to-br ${slide.gradient} opacity-90`} />
              
              {/* Pattern overlay */}
              <div className="absolute inset-0 opacity-20">
                <div className="absolute inset-0" style={{
                  backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.1'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
                }} />
              </div>

              {/* Content */}
              <div className="relative z-10 h-full flex items-center">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
                  <div className="flex items-center justify-between">
                    {/* Left: Text Content */}
                    <div className="flex-1 pr-8">
                      <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 backdrop-blur-sm mb-6">
                        <Icon className="w-5 h-5 text-white" />
                        <span className="text-white/90 text-sm font-medium">{slide.subtitle}</span>
                      </div>
                      
                      <h2 className="text-5xl md:text-6xl font-bold text-white mb-4 tracking-tight">
                        {slide.title}
                      </h2>
                      
                      <p className="text-xl text-white/80 mb-8 max-w-lg">
                        {slide.description}
                      </p>
                      
                      <button className="inline-flex items-center gap-2 px-8 py-4 bg-white text-gray-900 rounded-full font-semibold hover:bg-white/90 transition-colors group-hover:shadow-lg group-hover:shadow-white/20">
                        <span>查看详情</span>
                        <ChevronRight className="w-5 h-5" />
                      </button>
                    </div>

                    {/* Right: Visual Element */}
                    <div className="hidden lg:flex flex-1 justify-center items-center">
                      <div className="relative">
                        {/* Main icon circle */}
                        <div className="w-64 h-64 rounded-full bg-white/10 backdrop-blur-sm flex items-center justify-center border border-white/20">
                          <Icon className="w-32 h-32 text-white" strokeWidth={1} />
                        </div>
                        
                        {/* Floating elements */}
                        <div className="absolute -top-4 -right-4 w-20 h-20 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center animate-pulse">
                          <div className="w-3 h-3 rounded-full bg-white" />
                        </div>
                        <div className="absolute -bottom-4 -left-4 w-16 h-16 rounded-full bg-white/15 backdrop-blur-sm flex items-center justify-center">
                          <div className="w-2 h-2 rounded-full bg-white" />
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )
        })}
      </div>

      {/* Navigation Arrows */}
      <button
        onClick={prevSlide}
        className="absolute left-4 top-1/2 -translate-y-1/2 w-12 h-12 rounded-full bg-white/10 backdrop-blur-sm flex items-center justify-center text-white hover:bg-white/20 transition-colors border border-white/20"
      >
        <ChevronLeft className="w-6 h-6" />
      </button>
      
      <button
        onClick={nextSlide}
        className="absolute right-4 top-1/2 -translate-y-1/2 w-12 h-12 rounded-full bg-white/10 backdrop-blur-sm flex items-center justify-center text-white hover:bg-white/20 transition-colors border border-white/20"
      >
        <ChevronRight className="w-6 h-6" />
      </button>

      {/* Indicators */}
      <div className="absolute bottom-8 left-1/2 -translate-x-1/2 flex gap-3">
        {slides.map((_, index) => (
          <button
            key={index}
            onClick={() => goToSlide(index)}
            className={`transition-all duration-300 rounded-full ${
              index === currentIndex 
                ? 'w-10 h-2 bg-white' 
                : 'w-2 h-2 bg-white/40 hover:bg-white/60'
            }`}
          />
        ))}
      </div>
    </div>
  )
}
