"use client"

import { ScrollArea } from "@/components/ui/scroll-area"
import { formatDistanceToNow } from "date-fns"
import { Bot, User } from "lucide-react"
import { useEffect, useRef } from "react"

interface ChatInterfaceProps {
  messages: Array<{
    id: string
    role: "user" | "assistant"
    content: string
    timestamp: Date
  }>
  title: string
}

export default function ChatInterface({ messages, title }: ChatInterfaceProps) {
  const scrollAreaRef = useRef<HTMLDivElement>(null)

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    if (scrollAreaRef.current) {
      const scrollArea = scrollAreaRef.current
      scrollArea.scrollTop = scrollArea.scrollHeight
    }
  }, [messages])

  return (
    <div className="flex-1 flex flex-col">
      <div className="p-4 border-b border-zinc-800">
        <h2 className="text-xl font-bold truncate">{title}</h2>
      </div>
      <ScrollArea className="flex-1 p-4" ref={scrollAreaRef}>
        <div className="max-w-3xl mx-auto space-y-6">
          {messages.map((message) => (
            <div key={message.id} className={`flex gap-3 ${message.role === "user" ? "justify-end" : "justify-start"}`}>
              {message.role === "assistant" && (
                <div className="w-8 h-8 rounded-full bg-zinc-700 flex items-center justify-center">
                  <Bot size={16} />
                </div>
              )}
              <div
                className={`max-w-[80%] p-3 rounded-lg ${
                  message.role === "user" ? "bg-zinc-700 text-zinc-100" : "bg-zinc-800 text-zinc-100"
                }`}
              >
                <div className="text-sm">{message.content}</div>
                <div className="mt-1 text-xs text-zinc-400">
                  {formatDistanceToNow(message.timestamp, { addSuffix: true })}
                </div>
              </div>
              {message.role === "user" && (
                <div className="w-8 h-8 rounded-full bg-zinc-700 flex items-center justify-center">
                  <User size={16} />
                </div>
              )}
            </div>
          ))}
        </div>
      </ScrollArea>
    </div>
  )
}
