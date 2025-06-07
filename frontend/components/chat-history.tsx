"use client"

import { ScrollArea } from "@/components/ui/scroll-area"
import { formatDistanceToNow } from "date-fns"
import { MessageSquare, Plus } from "lucide-react"

interface Conversation {
  id: string
  title: string
  lastMessage: string
  timestamp: Date
  messageCount: number
  messages?: Array<{
    id: string
    role: "user" | "assistant"
    content: string
    timestamp: Date
  }>
}

interface ChatHistoryProps {
  conversations: Conversation[]
  activeConversationId: string
  onSelectConversation: (id: string) => void
  onNewChat: () => void
}

export default function ChatHistory({
  conversations,
  activeConversationId,
  onSelectConversation,
  onNewChat,
}: ChatHistoryProps) {
  return (
    <div className="h-full flex flex-col">
      <div className="p-4 border-b border-zinc-800">
        <h2 className="text-xl font-bold">Chat History</h2>
      </div>
      <ScrollArea className="flex-1">
        <div className="p-4 space-y-3">
          {conversations.map((conversation) => (
            <div
              key={conversation.id}
              className={`p-3 rounded-lg cursor-pointer transition-colors border ${
                activeConversationId === conversation.id
                  ? "bg-zinc-800 border-zinc-700"
                  : "hover:bg-zinc-800 border-zinc-800 hover:border-zinc-700"
              }`}
              onClick={() => onSelectConversation(conversation.id)}
            >
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-center gap-2">
                  <MessageSquare className="w-4 h-4 text-zinc-400" />
                  <h3 className="text-sm font-medium truncate">{conversation.title}</h3>
                </div>
                <span className="text-xs text-zinc-500 whitespace-nowrap ml-2">
                  {formatDistanceToNow(conversation.timestamp, { addSuffix: true })}
                </span>
              </div>
              <p className="text-xs text-zinc-400 line-clamp-2 mb-2">{conversation.lastMessage}</p>
              <div className="flex justify-between items-center">
                <span className="text-xs text-zinc-500">{conversation.messageCount} messages</span>
                {activeConversationId === conversation.id && <div className="w-2 h-2 bg-blue-500 rounded-full"></div>}
              </div>
            </div>
          ))}
        </div>
      </ScrollArea>
      <div className="p-4 border-t border-zinc-800">
        <button
          className="w-full py-2 bg-zinc-800 hover:bg-zinc-700 rounded-md text-sm transition-colors flex items-center justify-center gap-2"
          onClick={onNewChat}
        >
          <Plus className="w-4 h-4" />
          New Chat
        </button>
      </div>
    </div>
  )
}
