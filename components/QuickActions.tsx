'use client'

import { motion } from 'framer-motion'
import { 
  MessageCircle, 
  Clock, 
  Star, 
  Zap, 
  Calendar, 
  Search, 
  FileText, 
  Music,
  ChevronRight,
  Sparkles
} from 'lucide-react'

interface QuickAction {
  id: string
  icon: any
  text: string
  description: string
  color: string
  gradient: string
  action: () => void
}

interface QuickActionsProps {
  onAction?: (actionId: string) => void
}

export default function QuickActions({ onAction }: QuickActionsProps) {
  const actions: QuickAction[] = [
    {
      id: 'chat',
      icon: MessageCircle,
      text: 'Start Chat',
      description: 'Begin a conversation',
      color: 'from-blue-500 to-cyan-500',
      gradient: 'hover:from-blue-600 hover:to-cyan-600',
      action: () => onAction?.('chat')
    },
    {
      id: 'schedule',
      icon: Clock,
      text: 'Schedule Task',
      description: 'Set up reminders',
      color: 'from-green-500 to-emerald-500',
      gradient: 'hover:from-green-600 hover:to-emerald-600',
      action: () => onAction?.('schedule')
    },
    {
      id: 'reminder',
      icon: Star,
      text: 'Set Reminder',
      description: 'Create notifications',
      color: 'from-yellow-500 to-orange-500',
      gradient: 'hover:from-yellow-600 hover:to-orange-600',
      action: () => onAction?.('reminder')
    },
    {
      id: 'search',
      icon: Search,
      text: 'Quick Search',
      description: 'Find information',
      color: 'from-purple-500 to-pink-500',
      gradient: 'hover:from-purple-600 hover:to-pink-600',
      action: () => onAction?.('search')
    },
    {
      id: 'calendar',
      icon: Calendar,
      text: 'Calendar',
      description: 'Manage events',
      color: 'from-indigo-500 to-blue-500',
      gradient: 'hover:from-indigo-600 hover:to-blue-600',
      action: () => onAction?.('calendar')
    },
    {
      id: 'notes',
      icon: FileText,
      text: 'Take Notes',
      description: 'Create documents',
      color: 'from-teal-500 to-green-500',
      gradient: 'hover:from-teal-600 hover:to-green-600',
      action: () => onAction?.('notes')
    },
    {
      id: 'music',
      icon: Music,
      text: 'Play Music',
      description: 'Control audio',
      color: 'from-red-500 to-pink-500',
      gradient: 'hover:from-red-600 hover:to-pink-600',
      action: () => onAction?.('music')
    },
    {
      id: 'assistant',
      icon: Sparkles,
      text: 'AI Assistant',
      description: 'Get help',
      color: 'from-ai-500 to-purple-500',
      gradient: 'hover:from-ai-600 hover:to-purple-600',
      action: () => onAction?.('assistant')
    }
  ]

  return (
    <div className="space-y-4">
      <div className="flex items-center space-x-2 mb-4">
        <Sparkles className="w-5 h-5 text-ai-400" />
        <h3 className="text-lg font-semibold">Quick Actions</h3>
      </div>
      
      <div className="grid grid-cols-2 gap-3">
        {actions.map((action, index) => (
          <motion.button
            key={action.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            whileHover={{ 
              scale: 1.02, 
              x: 5,
              transition: { duration: 0.2 }
            }}
            whileTap={{ scale: 0.98 }}
            onClick={action.action}
            className={`p-4 bg-gradient-to-r ${action.color} ${action.gradient} rounded-xl flex flex-col items-center justify-center text-white font-medium transition-all duration-200 shadow-lg hover:shadow-xl group`}
          >
            <div className="flex items-center justify-between w-full mb-2">
              <action.icon className="w-5 h-5" />
              <ChevronRight className="w-4 h-4 opacity-0 group-hover:opacity-100 transition-opacity" />
            </div>
            
            <div className="text-center">
              <p className="font-semibold text-sm">{action.text}</p>
              <p className="text-xs opacity-80 mt-1">{action.description}</p>
            </div>

            {/* Hover effect */}
            <motion.div
              className="absolute inset-0 bg-white/10 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity"
              initial={false}
            />
          </motion.button>
        ))}
      </div>

      {/* Recent Actions */}
      <div className="mt-6">
        <h4 className="text-sm font-medium text-slate-300 mb-3">Recent Actions</h4>
        <div className="space-y-2">
          {[
            { text: 'Set reminder for meeting', time: '2 min ago' },
            { text: 'Searched for weather', time: '5 min ago' },
            { text: 'Started music playlist', time: '10 min ago' }
          ].map((recent, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              className="flex items-center justify-between p-3 bg-white/5 rounded-lg hover:bg-white/10 transition-colors cursor-pointer"
            >
              <span className="text-sm text-slate-300">{recent.text}</span>
              <span className="text-xs text-slate-400">{recent.time}</span>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  )
} 