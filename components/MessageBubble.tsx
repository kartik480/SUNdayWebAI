'use client'

import { motion } from 'framer-motion'
import { Bot, User, Clock, Mic, Image } from 'lucide-react'

interface MessageBubbleProps {
  message: {
    id: string
    text: string
    sender: 'user' | 'ai'
    timestamp: Date
    type: 'text' | 'voice' | 'image'
  }
  isTyping?: boolean
}

export default function MessageBubble({ message, isTyping = false }: MessageBubbleProps) {
  const isUser = message.sender === 'user'
  
  const getTypeIcon = () => {
    switch (message.type) {
      case 'voice':
        return <Mic className="w-3 h-3" />
      case 'image':
        return <Image className="w-3 h-3" />
      default:
        return null
    }
  }

  if (isTyping) {
    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        className="flex justify-start"
      >
        <div className="bg-white/10 backdrop-blur-sm p-4 rounded-2xl max-w-[80%]">
          <div className="flex items-center space-x-2 mb-2">
            <Bot className="w-4 h-4 text-ai-400" />
            <span className="text-xs text-slate-300">Assistant is typing...</span>
          </div>
          <div className="flex space-x-1">
            <div className="w-2 h-2 bg-ai-400 rounded-full animate-bounce" />
            <div className="w-2 h-2 bg-ai-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
            <div className="w-2 h-2 bg-ai-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
          </div>
        </div>
      </motion.div>
    )
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: -20, scale: 0.95 }}
      transition={{ duration: 0.3, ease: "easeOut" }}
      className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}
    >
      <div className={`max-w-[80%] p-4 rounded-2xl relative group ${
        isUser 
          ? 'bg-gradient-to-r from-ai-500 to-purple-600 text-white' 
          : 'bg-white/10 backdrop-blur-sm border border-white/10'
      }`}>
        {/* Message header */}
        <div className="flex items-center space-x-2 mb-2">
          {isUser ? (
            <User className="w-4 h-4 text-white/80" />
          ) : (
            <Bot className="w-4 h-4 text-ai-400" />
          )}
          <span className="text-xs opacity-60">
            {isUser ? 'You' : 'Assistant'}
          </span>
          {getTypeIcon() && (
            <div className="opacity-60">
              {getTypeIcon()}
            </div>
          )}
        </div>

        {/* Message content */}
        <div className="space-y-2">
          <p className="text-sm leading-relaxed">{message.text}</p>
          
          {/* Timestamp */}
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-1 text-xs opacity-60">
              <Clock className="w-3 h-3" />
              <span>{message.timestamp.toLocaleTimeString()}</span>
            </div>
            
            {/* Message actions */}
            <div className="opacity-0 group-hover:opacity-100 transition-opacity flex items-center space-x-2">
              <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                className="p-1 rounded hover:bg-white/20 transition-colors"
                title="Copy message"
              >
                <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
              </motion.button>
              
              {!isUser && (
                <motion.button
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                  className="p-1 rounded hover:bg-white/20 transition-colors"
                  title="Read aloud"
                >
                  <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
                  </svg>
                </motion.button>
              )}
            </div>
          </div>
        </div>

        {/* Message tail */}
        <div className={`absolute top-4 ${
          isUser ? '-right-2' : '-left-2'
        } w-4 h-4 transform rotate-45 ${
          isUser 
            ? 'bg-gradient-to-r from-ai-500 to-purple-600' 
            : 'bg-white/10 border-l border-b border-white/10'
        }`} />
      </div>
    </motion.div>
  )
} 