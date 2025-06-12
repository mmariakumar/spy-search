import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Bot } from "lucide-react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { MessageList } from "./chat/MessageList";
import { ChatInput } from "./chat/ChatInput";
import { useStreamingChat } from "@/hooks/useStreamingChat";

interface Message {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface ChatInterfaceProps {
  agents: string[];
  messages: Message[];
  setMessages: React.Dispatch<React.SetStateAction<Message[]>>;
  isLoading: boolean;
  setIsLoading: React.Dispatch<React.SetStateAction<boolean>>;
  currentConversationId?: string | null;
  onConversationCreated?: (title: string) => void;
}

export const ChatInterface = ({ 
  agents, 
  messages, 
  setMessages, 
  isLoading, 
  setIsLoading,
  currentConversationId,
  onConversationCreated 
}: ChatInterfaceProps) => {
  const [input, setInput] = useState("");

  const { sendStreamingMessage, streamingMessageId } = useStreamingChat({
    messages,
    setMessages,
    setIsLoading,
    currentConversationTitle: currentConversationId,
    onConversationCreated
  });

  const clearChat = () => {
    setMessages([]);
    setIsLoading(false);
  };

  const handleSendMessage = async (messageContent: string, files: File[], isDeepResearch: boolean) => {
    await sendStreamingMessage(messageContent, files, isDeepResearch);
  };

  return (
    <div className="flex flex-col h-full max-w-none mx-auto bg-background">
      {messages.length === 0 ? (
        <div className="flex-1 flex flex-col items-center justify-center px-4">
          <div className="w-full max-w-4xl mx-auto">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-light text-foreground mb-4">
                What can I help you with?
              </h2>
              <p className="text-lg text-muted-foreground font-light max-w-2xl mx-auto">
                Ask anything to generate comprehensive intelligence reports
              </p>
            </div>
            
            <div className="mb-8">
              <ChatInput
                input={input}
                setInput={setInput}
                isLoading={isLoading}
                agents={agents}
                onSendMessage={handleSendMessage}
              />
            </div>

            <div className="flex flex-wrap gap-3 justify-center max-w-3xl mx-auto">
              {[
                "Current Events", 
                "Parenting", 
                "Compare", 
                "Troubleshoot", 
                "Health"
              ].map((topic) => (
                <Button
                  key={topic}
                  variant="ghost"
                  size="sm"
                  onClick={() => setInput(`Tell me about ${topic.toLowerCase()}`)}
                  className="rounded-full border border-border/40 text-muted-foreground hover:text-foreground hover:bg-muted/50 transition-all"
                >
                  {topic}
                </Button>
              ))}
            </div>
          </div>
        </div>
      ) : (
        <>
          <div className="flex justify-between items-center p-4 border-b border-border/20 bg-background/95 backdrop-blur-sm">
            <div className="flex items-center gap-2">
              <Bot className="h-5 w-5 text-primary" />
              <h2 className="text-base font-medium text-foreground">Intelligence Chat</h2>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={clearChat}
              className="text-muted-foreground hover:text-foreground text-sm"
            >
              Clear Chat
            </Button>
          </div>

          <div className="flex-1 flex flex-col min-h-0">
            <ScrollArea className="flex-1 px-4 md:px-6">
              <div className="max-w-4xl mx-auto py-6">
                <MessageList 
                  messages={messages} 
                  isLoading={isLoading} 
                  isDeepResearch={false}
                  streamingMessageId={streamingMessageId}
                />
              </div>
            </ScrollArea>

            <div className="border-t border-border/20 bg-background/98 backdrop-blur-sm">
              <div className="max-w-4xl mx-auto px-4 md:px-6 py-4">
                <ChatInput
                  input={input}
                  setInput={setInput}
                  isLoading={isLoading}
                  agents={agents}
                  onSendMessage={handleSendMessage}
                />
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default ChatInterface;
