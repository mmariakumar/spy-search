
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Send, Search, Zap } from "lucide-react";

interface ChatInputProps {
  input: string;
  setInput: (value: string) => void;
  isLoading: boolean;
  agents: string[];
  onSendMessage: (message: string, files: File[], isDeepResearch: boolean) => void;
  searchMode?: boolean;
  onSearchModeChange?: (enabled: boolean) => void;
}

export const ChatInput = ({ 
  input, 
  setInput, 
  isLoading, 
  agents, 
  onSendMessage,
  searchMode = false,
  onSearchModeChange
}: ChatInputProps) => {
  const [internalSearchMode, setInternalSearchMode] = useState(searchMode);

  const currentSearchMode = onSearchModeChange ? searchMode : internalSearchMode;

  const handleSubmit = (isDeepResearch: boolean) => {
    if (!input.trim() || isLoading) return;
    
    const messageContent = currentSearchMode ? `search: ${input.trim()}` : input.trim();
    onSendMessage(messageContent, [], isDeepResearch);
    setInput("");
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(false);
    }
  };

  const toggleSearchMode = () => {
    const newMode = !currentSearchMode;
    if (onSearchModeChange) {
      onSearchModeChange(newMode);
    } else {
      setInternalSearchMode(newMode);
    }
  };

  return (
    <div className="w-full max-w-3xl mx-auto">
      <div className="relative group">
        <div className="flex items-center gap-2 p-1.5 bg-white/80 dark:bg-gray-900/80 backdrop-blur-xl border border-gray-200/50 dark:border-gray-700/50 rounded-3xl shadow-sm hover:shadow-md transition-all duration-200 focus-within:border-primary/30 focus-within:shadow-md">
          
          {/* Search Toggle */}
          <button
            onClick={toggleSearchMode}
            className={`flex items-center justify-center w-10 h-10 rounded-full transition-all duration-200 ${
              currentSearchMode 
                ? 'bg-primary/90 text-white shadow-sm shadow-primary/20' 
                : 'bg-gray-100/70 dark:bg-gray-800/70 text-gray-500 dark:text-gray-400 hover:bg-gray-200/70 dark:hover:bg-gray-700/70 hover:text-gray-700 dark:hover:text-gray-300'
            }`}
          >
            <Search className="h-4 w-4" />
          </button>

          {/* Input Field */}
          <div className="flex-1">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={currentSearchMode ? "Search the web..." : "Ask me anything..."}
              disabled={isLoading}
              className="border-0 bg-transparent px-0 text-sm focus-visible:ring-0 focus-visible:ring-offset-0 placeholder:text-gray-400 dark:placeholder:text-gray-500 font-medium h-10"
            />
          </div>

          {/* Action Buttons */}
          <div className="flex items-center gap-1">
            <Button
              onClick={() => handleSubmit(false)}
              disabled={!input.trim() || isLoading}
              size="sm"
              variant="ghost"
              className="rounded-full h-10 w-10 p-0 hover:bg-primary/8 text-primary/80 transition-all duration-200 hover:scale-105 disabled:opacity-50 disabled:hover:scale-100"
            >
              <Zap className="h-4 w-4" />
            </Button>
            
            <Button
              onClick={() => handleSubmit(true)}
              disabled={!input.trim() || isLoading}
              size="sm"
              className="rounded-full h-10 w-10 p-0 bg-primary/90 hover:bg-primary text-white shadow-sm shadow-primary/20 transition-all duration-200 hover:scale-105 disabled:opacity-50 disabled:hover:scale-100"
            >
              <Send className="h-4 w-4" />
            </Button>
          </div>
        </div>

        {/* Search Mode Indicator */}
        {currentSearchMode && (
          <div className="absolute -top-8 left-4 px-3 py-1 bg-primary/90 text-white text-xs font-medium rounded-full shadow-sm animate-fade-in">
            Web Search Active
          </div>
        )}
      </div>
    </div>
  );
};
