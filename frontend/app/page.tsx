"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { ChevronLeft, ChevronRight, Send } from "lucide-react"
import ChatHistory from "@/components/chat-history"
import ChatInterface from "@/components/chat-interface"
import ConfigPanel from "@/components/config-panel"

// Mock conversation data
const initialConversations = [
  {
    id: "1",
    title: "Market Analysis Report Q4 2024",
    lastMessage: "Generated comprehensive market analysis with trends and forecasts",
    timestamp: new Date(Date.now() - 1000 * 60 * 30), // 30 minutes ago
    messageCount: 12,
    messages: [
      {
        id: "1-1",
        role: "assistant",
        content: "Hello! I'm your AI agent. How can I help you generate a market analysis report?",
        timestamp: new Date(Date.now() - 1000 * 60 * 45),
      },
      {
        id: "1-2",
        role: "user",
        content: "I need a comprehensive market analysis for Q4 2024 focusing on tech industry trends.",
        timestamp: new Date(Date.now() - 1000 * 60 * 40),
      },
      {
        id: "1-3",
        role: "assistant",
        content:
          "I'll generate a comprehensive market analysis with trends and forecasts for the tech industry in Q4 2024.",
        timestamp: new Date(Date.now() - 1000 * 60 * 30),
      },
    ],
  },
  {
    id: "2",
    title: "Customer Satisfaction Survey Analysis",
    lastMessage: "Analyzed survey data from 1,500 customers across 5 regions",
    timestamp: new Date(Date.now() - 1000 * 60 * 60 * 2), // 2 hours ago
    messageCount: 8,
    messages: [
      {
        id: "2-1",
        role: "assistant",
        content: "Hello! I'm your AI agent. How can I help you today?",
        timestamp: new Date(Date.now() - 1000 * 60 * 60 * 3),
      },
      {
        id: "2-2",
        role: "user",
        content: "I need to analyze customer satisfaction survey data from our recent campaign.",
        timestamp: new Date(Date.now() - 1000 * 60 * 60 * 2.5),
      },
    ],
  },
]

export default function Home() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true)
  const [isConfigOpen, setIsConfigOpen] = useState(true)
  const [message, setMessage] = useState("")
  const [conversations, setConversations] = useState(initialConversations)
  const [activeConversationId, setActiveConversationId] = useState(initialConversations[0].id)

  // Get the active conversation
  const activeConversation = conversations.find((conv) => conv.id === activeConversationId) || conversations[0]

  const handleSendMessage = () => {
    if (!message.trim()) return

    // Add user message to active conversation
    const userMessage = {
      id: Date.now().toString(),
      role: "user" as const,
      content: message,
      timestamp: new Date(),
    }

    // Update the conversations state
    setConversations((prevConversations) =>
      prevConversations.map((conv) => {
        if (conv.id === activeConversationId) {
          return {
            ...conv,
            messages: [...(conv.messages || []), userMessage],
            lastMessage: message,
            messageCount: (conv.messageCount || 0) + 1,
            timestamp: new Date(),
          }
        }
        return conv
      }),
    )

    setMessage("")

    // Simulate AI response
    setTimeout(() => {
      const aiResponse = {
        id: (Date.now() + 1).toString(),
        role: "assistant" as const,
        content: "I've received your message. I'm processing your request for a report.",
        timestamp: new Date(),
      }

      setConversations((prevConversations) =>
        prevConversations.map((conv) => {
          if (conv.id === activeConversationId) {
            return {
              ...conv,
              messages: [...(conv.messages || []), aiResponse],
              lastMessage: aiResponse.content,
              messageCount: (conv.messageCount || 0) + 1,
              timestamp: new Date(),
            }
          }
          return conv
        }),
      )
    }, 1000)
  }

  const handleNewChat = () => {
    const newConversation = {
      id: Date.now().toString(),
      title: "New Conversation",
      lastMessage: "Start a new conversation",
      timestamp: new Date(),
      messageCount: 1,
      messages: [
        {
          id: "welcome-" + Date.now(),
          role: "assistant",
          content: "Hello! I'm your AI agent. How can I help you generate reports today?",
          timestamp: new Date(),
        },
      ],
    }

    setConversations([newConversation, ...conversations])
    setActiveConversationId(newConversation.id)
  }

  const handleSelectConversation = (id: string) => {
    setActiveConversationId(id)
  }

  return (
    <div className="flex h-screen bg-zinc-900 text-zinc-100">
      {/* Left Sidebar - Chat History */}
      <div
        className={`${
          isSidebarOpen ? "w-64" : "w-0"
        } transition-all duration-300 ease-in-out overflow-hidden border-r border-zinc-800`}
      >
        <ChatHistory
          conversations={conversations}
          activeConversationId={activeConversationId}
          onSelectConversation={handleSelectConversation}
          onNewChat={handleNewChat}
        />
      </div>

      {/* Toggle Sidebar Button */}
      <button
        onClick={() => setIsSidebarOpen(!isSidebarOpen)}
        className="absolute left-0 top-1/2 transform -translate-y-1/2 bg-zinc-800 p-1 rounded-r-md"
      >
        {isSidebarOpen ? <ChevronLeft size={20} /> : <ChevronRight size={20} />}
      </button>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        <ChatInterface messages={activeConversation.messages || []} title={activeConversation.title} />

        {/* Message Input */}
        <div className="p-4 border-t border-zinc-800">
          <div className="flex gap-2">
            <Textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Type your message here..."
              className="flex-1 bg-zinc-800 border-zinc-700"
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault()
                  handleSendMessage()
                }
              }}
            />
            <Button onClick={handleSendMessage} className="bg-zinc-700 hover:bg-zinc-600">
              <Send size={18} />
            </Button>
          </div>
        </div>
      </div>

      {/* Right Sidebar - Config */}
      <div
        className={`${
          isConfigOpen ? "w-80" : "w-0"
        } transition-all duration-300 ease-in-out overflow-hidden border-l border-zinc-800`}
      >
        <ConfigPanel />
      </div>

      {/* Toggle Config Button */}
      <button
        onClick={() => setIsConfigOpen(!isConfigOpen)}
        className="absolute right-0 top-1/2 transform -translate-y-1/2 bg-zinc-800 p-1 rounded-l-md"
      >
        {isConfigOpen ? <ChevronRight size={20} /> : <ChevronLeft size={20} />}
      </button>
    </div>
  )
}
