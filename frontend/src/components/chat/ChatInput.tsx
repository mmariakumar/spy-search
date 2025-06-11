
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Send, Paperclip, Zap, Search } from "lucide-react";
import { FileUpload } from "./FileUpload";

interface ChatInputProps {
  input: string;
  setInput: (value: string) => void;
  isLoading: boolean;
  agents: string[];
  onSendMessage: (message: string, files: File[], isDeepResearch: boolean) => void;
}

export const ChatInput = ({ input, setInput, isLoading, agents, onSendMessage }: ChatInputProps) => {
  const [files, setFiles] = useState<File[]>([]);
  const [isDragOver, setIsDragOver] = useState(false);

  const handleSubmit = (isDeepResearch: boolean) => {
    if (!input.trim() || isLoading) return;
    
    onSendMessage(input.trim(), files, isDeepResearch);
    setInput("");
    setFiles([]);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(false);
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto">
      <FileUpload 
        uploadedFiles={files}
        setUploadedFiles={setFiles}
        isDragOver={isDragOver}
        setIsDragOver={setIsDragOver}
      />
      
      <div className="flex items-center gap-3 p-4 bg-background border border-border/20 rounded-3xl shadow-sm focus-within:border-primary/20 focus-within:shadow-lg transition-all hover:shadow-md">
        <div className="flex-1">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask anything..."
            disabled={isLoading}
            className="border-0 bg-transparent px-0 text-base focus-visible:ring-0 focus-visible:ring-offset-0 placeholder:text-muted-foreground/60 font-medium"
            style={{ minHeight: "24px" }}
          />
        </div>

        <div className="flex items-center gap-2">
          <Button
            onClick={() => handleSubmit(false)}
            disabled={!input.trim() || isLoading}
            size="sm"
            className="rounded-2xl px-6 py-2.5 h-auto bg-primary hover:bg-primary/90 text-primary-foreground font-medium transition-all hover:scale-105"
          >
            <Zap className="h-4 w-4 mr-2" />
            Quick
          </Button>
          
          <Button
            onClick={() => handleSubmit(true)}
            disabled={!input.trim() || isLoading}
            variant="outline"
            size="sm"
            className="rounded-2xl px-6 py-2.5 h-auto border-border/40 hover:bg-muted/50 transition-all hover:scale-105"
          >
            <Search className="h-4 w-4 mr-2" />
            Deep
          </Button>
        </div>
      </div>
    </div>
  );
};
