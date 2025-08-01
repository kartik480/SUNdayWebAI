import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'SUNDAY-PAAI',
  description: 'SUNDAY-PAAI - Your AI Assistant created by Basireddy Karthik. Experience the future of personal assistance with memory, learning, and internet capabilities.',
  keywords: 'SUNDAY-PAAI, AI, Personal Assistant, Artificial Intelligence, Basireddy Karthik',
  authors: [{ name: 'Basireddy Karthik' }],
  viewport: 'width=device-width, initial-scale=1',
  robots: 'index, follow',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
          {children}
        </div>
      </body>
    </html>
  )
} 