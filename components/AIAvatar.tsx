'use client'

import { motion } from 'framer-motion'
import { Bot, Brain, Sparkles } from 'lucide-react'

interface AIAvatarProps {
  size?: 'sm' | 'md' | 'lg'
  status?: 'online' | 'offline' | 'thinking'
  showParticles?: boolean
}

export default function AIAvatar({ 
  size = 'md', 
  status = 'online',
  showParticles = true 
}: AIAvatarProps) {
  const sizeClasses = {
    sm: 'w-12 h-12',
    md: 'w-16 h-16',
    lg: 'w-24 h-24'
  }

  const iconSizes = {
    sm: 'w-6 h-6',
    md: 'w-8 h-8',
    lg: 'w-12 h-12'
  }

  const statusColors = {
    online: 'bg-green-500',
    offline: 'bg-red-500',
    thinking: 'bg-yellow-500'
  }

  return (
    <div className="relative">
      <motion.div
        animate={{ 
          scale: [1, 1.05, 1],
          rotate: [0, 5, -5, 0]
        }}
        transition={{ 
          duration: 4,
          repeat: Infinity,
          ease: "easeInOut"
        }}
        className={`${sizeClasses[size]} bg-gradient-to-r from-ai-500 to-purple-600 rounded-full flex items-center justify-center relative overflow-hidden`}
      >
        <Bot className={`${iconSizes[size]} text-white z-10`} />
        
        {/* Animated background pattern */}
        <div className="absolute inset-0 opacity-20">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
            className="w-full h-full"
          >
            <div className="w-full h-full bg-gradient-to-r from-transparent via-white to-transparent opacity-30" />
          </motion.div>
        </div>

        {/* Status indicator */}
        <div className={`absolute -top-1 -right-1 w-4 h-4 ${statusColors[status]} rounded-full animate-pulse`} />
      </motion.div>

      {/* Floating particles */}
      {showParticles && (
        <>
          {[...Array(6)].map((_, i) => (
            <motion.div
              key={i}
              className="absolute w-1 h-1 bg-ai-400 rounded-full"
              animate={{
                x: [0, Math.random() * 40 - 20],
                y: [0, Math.random() * 40 - 20],
                opacity: [0, 1, 0],
                scale: [0, 1, 0],
              }}
              transition={{
                duration: Math.random() * 3 + 2,
                repeat: Infinity,
                delay: i * 0.5,
                ease: "easeInOut"
              }}
              style={{
                left: '50%',
                top: '50%',
              }}
            />
          ))}
        </>
      )}

      {/* Neural network effect */}
      {status === 'thinking' && (
        <motion.div
          animate={{ opacity: [0.3, 1, 0.3] }}
          transition={{ duration: 2, repeat: Infinity }}
          className="absolute inset-0 rounded-full border-2 border-ai-400"
        />
      )}
    </div>
  )
} 