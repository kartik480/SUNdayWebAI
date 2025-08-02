'use client'

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Bot, 
  Send, 
  Mic, 
  MicOff, 
  Settings, 
  Sparkles, 
  Brain, 
  Zap, 
  MessageCircle, 
  Clock, 
  Star,
  ChevronRight,
  Play,
  Pause,
  Volume2
} from 'lucide-react'

interface Message {
  id: string
  text: string
  sender: 'user' | 'ai'
  timestamp: Date
  type: 'text' | 'voice' | 'image'
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([])
  const [inputText, setInputText] = useState('')
  const [isListening, setIsListening] = useState(false)
  const [isTyping, setIsTyping] = useState(false)
  const [isPlaying, setIsPlaying] = useState(false)
  const [currentTime, setCurrentTime] = useState(new Date())
  const [isClient, setIsClient] = useState(false)
  const [isLoading, setIsLoading] = useState(true)

  // Load fresh welcome message only (clear chat display, keep backend memory)
  useEffect(() => {
    const loadFreshWelcome = async () => {
      try {
        // Get a fresh welcome message from backend
        const response = await fetch('/api/welcome')
        if (response.ok) {
          const data = await response.json()
          setMessages([{
            id: '1',
            text: data.message,
            sender: 'ai',
            timestamp: new Date(),
            type: 'text'
          }])
        } else {
          // Fallback welcome message
          setMessages([{
            id: '1',
            text: "⚡ Boss! SUNDAY-PAAI is charged up and ready to go! Your AI companion, created by Basireddy Karthik, is here to supercharge your day. What's the energy we're bringing? 🔋",
            sender: 'ai',
            timestamp: new Date(),
            type: 'text'
          }])
        }
      } catch (error) {
        console.error('Error loading welcome message:', error)
        // Fallback welcome message
        setMessages([{
          id: '1',
          text: "⚡ Boss! SUNDAY-PAAI is charged up and ready to go! Your AI companion, created by Basireddy Karthik, is here to supercharge your day. What's the energy we're bringing? 🔋",
          sender: 'ai',
          timestamp: new Date(),
          type: 'text'
        }])
      } finally {
        setIsLoading(false)
      }
    }

    loadFreshWelcome()
  }, [])

  useEffect(() => {
    setIsClient(true)
    const timer = setInterval(() => setCurrentTime(new Date()), 1000)
    return () => clearInterval(timer)
  }, [])

  const sendMessage = async () => {
    if (!inputText.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputText,
      sender: 'user',
      timestamp: new Date(),
      type: 'text'
    }

    setMessages((prev: Message[]) => [...prev, userMessage])
    setInputText('')
    setIsTyping(true)

    // Get AI response from Flask backend
    try {
      const response = await fetch('/api/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: inputText }),
      })
      
      if (response.ok) {
        const data = await response.json()
        if (data.success && data.messages.length >= 2) {
          const aiResponse: Message = {
            id: (Date.now() + 1).toString(),
            text: data.messages[1].text,
            sender: 'ai',
            timestamp: new Date(),
            type: 'text'
          }
          setMessages((prev: Message[]) => [...prev, aiResponse])
        }
      } else {
        // Fallback response if API fails
        const aiResponse: Message = {
          id: (Date.now() + 1).toString(),
          text: "I'm having trouble connecting right now. Please try again!",
          sender: 'ai',
          timestamp: new Date(),
          type: 'text'
        }
        setMessages((prev: Message[]) => [...prev, aiResponse])
      }
    } catch (error) {
      console.error('Error getting AI response:', error)
      const aiResponse: Message = {
        id: (Date.now() + 1).toString(),
        text: "Sorry, I'm having connection issues. Please try again!",
        sender: 'ai',
        timestamp: new Date(),
        type: 'text'
      }
      setMessages((prev: Message[]) => [...prev, aiResponse])
    }
    
    setIsTyping(false)
  }

  const toggleVoice = () => {
    setIsListening(!isListening)
    // Add voice recognition logic here
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  if (!isClient || isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white flex items-center justify-center">
        <div className="text-center">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
            className="w-16 h-16 bg-gradient-to-r from-ai-500 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-4"
          >
            <Brain className="w-8 h-8 text-white" />
          </motion.div>
          <h1 className="text-2xl font-bold gradient-text">SUNDAY-PAAI</h1>
          <p className="text-slate-300 mt-2">Connecting to Boss...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white">
      {/* Animated Background */}
      <div className="fixed inset-0 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900" />
        <div className="absolute inset-0">
          {[...Array(20)].map((_, i) => (
            <motion.div
              key={i}
              className="absolute w-2 h-2 bg-ai-400 rounded-full opacity-20"
              animate={{
                x: [0, Math.random() * 1000],
                y: [0, Math.random() * 1000],
                scale: [0, 1, 0],
              }}
              transition={{
                duration: Math.random() * 10 + 10,
                repeat: Infinity,
                ease: "linear"
              }}
              style={{
                left: Math.random() * 100 + '%',
                top: Math.random() * 100 + '%',
              }}
            />
          ))}
        </div>
      </div>

      {/* Header */}
      <motion.header 
        initial={{ y: -100, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="relative z-10 p-6"
      >
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
              className="w-12 h-12 bg-gradient-to-r from-ai-500 to-purple-600 rounded-full flex items-center justify-center"
            >
              <Brain className="w-6 h-6 text-white" />
            </motion.div>
            <div>
              <h1 className="text-2xl font-bold gradient-text">SUNDAY-PAAI</h1>
              <p className="text-slate-300 text-sm">My Life</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="text-right">
              <p className="text-sm text-slate-300">
                {currentTime.toLocaleTimeString()}
              </p>
              <p className="text-xs text-slate-400">
                {currentTime.toLocaleDateString()}
              </p>
            </div>
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              className="p-3 bg-glass rounded-full hover:bg-white/20 transition-colors"
            >
              <Settings className="w-5 h-5" />
            </motion.button>
          </div>
        </div>
      </motion.header>

      {/* Main Content */}
      <main className="relative z-10 max-w-7xl mx-auto px-6 pb-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[calc(100vh-200px)]">
          
          {/* AI Assistant Interface */}
          <div className="lg:col-span-2">
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              className="h-full bg-glass rounded-2xl p-6 flex flex-col"
            >
              {/* AI Avatar */}
              <div className="flex items-center space-x-4 mb-6">
                <motion.div
                  animate={{ 
                    scale: [1, 1.1, 1],
                    rotate: [0, 5, -5, 0]
                  }}
                  transition={{ 
                    duration: 4,
                    repeat: Infinity,
                    ease: "easeInOut"
                  }}
                  className="w-16 h-16 bg-gradient-to-r from-ai-500 to-purple-600 rounded-full flex items-center justify-center relative"
                >
                  <Bot className="w-8 h-8 text-white" />
                  <div className="absolute -top-1 -right-1 w-4 h-4 bg-green-500 rounded-full animate-pulse" />
                </motion.div>
                <div>
                  <h2 className="text-xl font-semibold">Assistant</h2>
                  <p className="text-slate-300 text-sm">Online & Ready</p>
                </div>
              </div>

              {/* Messages */}
              <div className="flex-1 overflow-y-auto space-y-4 mb-6">
                <AnimatePresence>
                  {messages.map((message) => (
                    <motion.div
                      key={message.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -20 }}
                      className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div className={`max-w-[80%] p-4 rounded-2xl ${
                        message.sender === 'user' 
                          ? 'bg-gradient-to-r from-ai-500 to-purple-600 text-white' 
                          : 'bg-white/10 backdrop-blur-sm'
                      }`}>
                        <p className="text-sm">{message.text}</p>
                        <p className="text-xs opacity-60 mt-2">
                          {message.timestamp.toLocaleTimeString()}
                        </p>
                      </div>
                    </motion.div>
                  ))}
                  
                  {isTyping && (
                    <motion.div
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      className="flex justify-start"
                    >
                      <div className="bg-white/10 backdrop-blur-sm p-4 rounded-2xl">
                        <div className="flex space-x-1">
                          <div className="w-2 h-2 bg-ai-400 rounded-full animate-bounce" />
                          <div className="w-2 h-2 bg-ai-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
                          <div className="w-2 h-2 bg-ai-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                        </div>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>

              {/* Input Area */}
              <div className="flex items-center space-x-4">
                <div className="flex-1 relative">
                  <input
                    type="text"
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Ask me anything..."
                    className="w-full bg-white/10 backdrop-blur-sm border border-white/20 rounded-full px-6 py-4 text-white placeholder-slate-300 focus:outline-none focus:ring-2 focus:ring-ai-500 focus:border-transparent"
                  />
                </div>
                <motion.button
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                  onClick={toggleVoice}
                  className={`p-4 rounded-full transition-colors ${
                    isListening 
                      ? 'bg-red-500 hover:bg-red-600' 
                      : 'bg-ai-500 hover:bg-ai-600'
                  }`}
                >
                  {isListening ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
                </motion.button>
                <motion.button
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                  onClick={sendMessage}
                  className="p-4 bg-gradient-to-r from-ai-500 to-purple-600 rounded-full hover:from-ai-600 hover:to-purple-700 transition-all"
                >
                  <Send className="w-5 h-5" />
                </motion.button>
              </div>
            </motion.div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Quick Actions */}
            <motion.div
              initial={{ x: 100, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              transition={{ delay: 0.2 }}
              className="bg-glass rounded-2xl p-6"
            >
              <h3 className="text-lg font-semibold mb-4 flex items-center">
                <Sparkles className="w-5 h-5 mr-2 text-ai-400" />
                Quick Actions
              </h3>
              <div className="space-y-3">
                {[
                  { icon: MessageCircle, text: 'Start Chat', color: 'from-blue-500 to-cyan-500' },
                  { icon: Clock, text: 'Schedule Task', color: 'from-green-500 to-emerald-500' },
                  { icon: Star, text: 'Set Reminder', color: 'from-yellow-500 to-orange-500' },
                  { icon: Zap, text: 'Quick Search', color: 'from-purple-500 to-pink-500' },
                ].map((action, index) => (
                  <motion.button
                    key={action.text}
                    whileHover={{ scale: 1.02, x: 5 }}
                    whileTap={{ scale: 0.98 }}
                    className={`w-full p-3 bg-gradient-to-r ${action.color} rounded-xl flex items-center justify-between text-white font-medium`}
                  >
                    <div className="flex items-center">
                      <action.icon className="w-4 h-4 mr-3" />
                      {action.text}
                    </div>
                    <ChevronRight className="w-4 h-4" />
                  </motion.button>
                ))}
              </div>
            </motion.div>

            {/* AI Status */}
            <motion.div
              initial={{ x: 100, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              transition={{ delay: 0.4 }}
              className="bg-glass rounded-2xl p-6"
            >
              <h3 className="text-lg font-semibold mb-4 flex items-center">
                <Brain className="w-5 h-5 mr-2 text-ai-400" />
                AI Status
              </h3>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-slate-300">Processing Power</span>
                  <div className="w-20 h-2 bg-slate-700 rounded-full overflow-hidden">
                    <motion.div
                      animate={{ width: ['60%', '80%', '60%'] }}
                      transition={{ duration: 2, repeat: Infinity }}
                      className="h-full bg-gradient-to-r from-ai-400 to-purple-500"
                    />
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-slate-300">Memory Usage</span>
                  <div className="w-20 h-2 bg-slate-700 rounded-full overflow-hidden">
                    <motion.div
                      animate={{ width: ['40%', '60%', '40%'] }}
                      transition={{ duration: 3, repeat: Infinity }}
                      className="h-full bg-gradient-to-r from-green-400 to-blue-500"
                    />
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-slate-300">Response Time</span>
                  <span className="text-sm text-green-400">~1.2s</span>
                </div>
              </div>
            </motion.div>

            {/* Voice Controls */}
            <motion.div
              initial={{ x: 100, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              transition={{ delay: 0.6 }}
              className="bg-glass rounded-2xl p-6"
            >
              <h3 className="text-lg font-semibold mb-4 flex items-center">
                <Volume2 className="w-5 h-5 mr-2 text-ai-400" />
                Voice Controls
              </h3>
              <div className="space-y-4">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => setIsPlaying(!isPlaying)}
                  className={`w-full p-3 rounded-xl flex items-center justify-center space-x-2 ${
                    isPlaying 
                      ? 'bg-red-500 hover:bg-red-600' 
                      : 'bg-ai-500 hover:bg-ai-600'
                  } text-white font-medium`}
                >
                  {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
                  <span>{isPlaying ? 'Stop' : 'Start'} Voice</span>
                </motion.button>
                <div className="text-center">
                  <p className="text-xs text-slate-400">Voice recognition active</p>
                  <p className="text-xs text-slate-400">Say "Hey Assistant" to activate</p>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </main>
    </div>
  )
} 