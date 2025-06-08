
import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent } from "@/components/ui/card";
import { Send, User, Bot, Loader2, Download, Copy, Check, Search, Zap, FileText, Upload, X } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";

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
}

export const ChatInterface = ({ agents, messages, setMessages, isLoading, setIsLoading }: ChatInterfaceProps) => {
  const [input, setInput] = useState("");
  const [copied, setCopied] = useState<string | null>(null);
  const [isDeepResearch, setIsDeepResearch] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);
  const [isDragOver, setIsDragOver] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { toast } = useToast();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleFileUpload = (files: FileList | null) => {
    if (!files) return;
    
    const pdfFiles = Array.from(files).filter(file => file.type === 'application/pdf');
    if (pdfFiles.length === 0) {
      toast({
        title: "Invalid file type",
        description: "Only PDF files are allowed.",
        variant: "destructive",
      });
      return;
    }
    
    setUploadedFiles(prev => [...prev, ...pdfFiles]);
  };

  const removeFile = (index: number) => {
    setUploadedFiles(prev => prev.filter((_, i) => i !== index));
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    handleFileUpload(e.dataTransfer.files);
  };

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: input.trim(),
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    const currentInput = input.trim();
    setInput("");
    setIsLoading(true);

    try {
      const endpoint = isDeepResearch ? 'report' : 'quick';
      const encodedQuery = encodeURIComponent(currentInput);
      
      // Convert messages to the required format (including the current query)
      const allMessages = [...messages, userMessage];
      const formattedMessages = allMessages.map(msg => ({
        role: msg.type === 'user' ? 'user' : 'assistant',
        content: msg.content
      }));

      const formData = new FormData();
      formData.append('messages', JSON.stringify(formattedMessages));
      
      uploadedFiles.forEach(file => {
        formData.append('files', file);
      });

      const response = await fetch(`http://localhost:8000/${endpoint}/${encodedQuery}`, {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.error) {
        throw new Error(data.error);
      }
      
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: data.report,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);
      setUploadedFiles([]);
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: "Sorry, I encountered an error while generating your report. Please try again.",
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
      
      toast({
        title: "Generation Failed",
        description: error instanceof Error ? error.message : "Failed to generate report",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const copyToClipboard = async (content: string, messageId: string) => {
    try {
      await navigator.clipboard.writeText(content);
      setCopied(messageId);
      setTimeout(() => setCopied(null), 2000);
      toast({
        title: "Copied!",
        description: "Message copied to clipboard.",
      });
    } catch (err) {
      toast({
        title: "Copy Failed",
        description: "Failed to copy message to clipboard.",
        variant: "destructive",
      });
    }
  };

  const downloadAsMarkdown = (content: string) => {
    const blob = new Blob([content], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `spy-search-report-${new Date().toISOString().slice(0, 10)}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    toast({
      title: "Downloaded!",
      description: "Report downloaded as markdown file.",
    });
  };

  const downloadAsPDF = (content: string) => {
    // Convert markdown content to basic HTML for PDF
    const htmlContent = `
      <!DOCTYPE html>
      <html>
      <head>
        <title>Spy Search Report</title>
        <meta charset="UTF-8">
        <style>
          body { 
            font-family: Arial, sans-serif; 
            line-height: 1.6; 
            margin: 40px; 
            color: #333;
          }
          h1, h2, h3 { 
            color: #2c3e50; 
            margin-top: 30px;
            margin-bottom: 15px;
          }
          h1 { font-size: 24px; }
          h2 { font-size: 20px; }
          h3 { font-size: 16px; }
          p { margin-bottom: 12px; }
          pre { 
            background: #f8f9fa; 
            padding: 15px; 
            border-radius: 5px; 
            border-left: 4px solid #007acc;
            overflow-x: auto;
            white-space: pre-wrap;
          }
          code {
            background: #f1f3f4;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
          }
          ul, ol { margin-bottom: 15px; }
          li { margin-bottom: 5px; }
          .report-header {
            text-align: center;
            border-bottom: 2px solid #007acc;
            padding-bottom: 20px;
            margin-bottom: 30px;
          }
          .timestamp {
            color: #666;
            font-size: 12px;
            text-align: right;
            margin-top: 20px;
          }
        </style>
      </head>
      <body>
        <div class="report-header">
          <h1>Spy Search Intelligence Report</h1>
        </div>
        <div class="report-content">
          <pre>${content}</pre>
        </div>
        <div class="timestamp">
          Generated on: ${new Date().toLocaleString()}
        </div>
      </body>
      </html>
    `;
    
    const blob = new Blob([htmlContent], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `spy-search-report-${new Date().toISOString().slice(0, 10)}.html`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    toast({
      title: "Downloaded!",
      description: "Report downloaded as HTML file (can be printed to PDF).",
    });
  };

  const isLongReport = (content: string) => content.length > 500;

  return (
    <div className="flex flex-col h-[600px] max-w-4xl mx-auto">
      {/* Chat Messages */}
      <Card className="flex-1 glass-card border-0 mb-4 min-h-0">
        <CardContent className="p-0 h-full">
          <ScrollArea className="h-full p-6">
            {messages.length === 0 ? (
              <div className="flex items-center justify-center h-full text-center">
                <div className="space-y-4">
                  <Bot className="h-12 w-12 text-primary mx-auto" />
                  <div>
                    <h3 className="text-lg font-medium text-foreground">Welcome to Spy Search</h3>
                    <p className="text-muted-foreground">Start a conversation to generate intelligence reports</p>
                  </div>
                </div>
              </div>
            ) : (
              <div className="space-y-6">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex gap-4 ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    {message.type === 'assistant' && (
                      <div className="flex-shrink-0">
                        <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
                          <Bot className="h-4 w-4 text-primary" />
                        </div>
                      </div>
                    )}
                    
                    <div className={`max-w-[80%] min-w-0 ${message.type === 'user' ? 'order-2' : ''}`}>
                      <div
                        className={`rounded-2xl px-4 py-3 ${
                          message.type === 'user'
                            ? 'bg-primary text-primary-foreground'
                            : 'bg-secondary/50 text-foreground border border-border/50'
                        }`}
                      >
                        <pre className="whitespace-pre-wrap text-sm leading-relaxed font-sans break-words">
                          {message.content}
                        </pre>
                      </div>
                      
                      {message.type === 'assistant' && (
                        <div className="flex gap-2 mt-2">
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => copyToClipboard(message.content, message.id)}
                            className="h-7 px-2 text-xs"
                          >
                            {copied === message.id ? (
                              <>
                                <Check className="h-3 w-3 mr-1" />
                                Copied
                              </>
                            ) : (
                              <>
                                <Copy className="h-3 w-3 mr-1" />
                                Copy
                              </>
                            )}
                          </Button>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => downloadAsMarkdown(message.content)}
                            className="h-7 px-2 text-xs"
                          >
                            <FileText className="h-3 w-3 mr-1" />
                            MD
                          </Button>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => downloadAsPDF(message.content)}
                            className="h-7 px-2 text-xs"
                          >
                            <Download className="h-3 w-3 mr-1" />
                            PDF
                          </Button>
                        </div>
                      )}
                    </div>

                    {message.type === 'user' && (
                      <div className="flex-shrink-0 order-3">
                        <div className="w-8 h-8 rounded-full bg-secondary flex items-center justify-center">
                          <User className="h-4 w-4 text-foreground" />
                        </div>
                      </div>
                    )}
                  </div>
                ))}
                
                {isLoading && (
                  <div className="flex gap-4 justify-start">
                    <div className="flex-shrink-0">
                      <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
                        <Bot className="h-4 w-4 text-primary" />
                      </div>
                    </div>
                    <div className="max-w-[80%]">
                      <div className="rounded-2xl px-4 py-3 bg-secondary/50 text-foreground border border-border/50">
                        <div className="flex items-center gap-2">
                          <Loader2 className="h-4 w-4 animate-spin" />
                          <span className="text-sm">Generating {isDeepResearch ? 'deep research' : 'quick'} report...</span>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
                
                <div ref={messagesEndRef} />
              </div>
            )}
          </ScrollArea>
        </CardContent>
      </Card>

      {/* Input Area */}
      <Card className="glass-card border-0 flex-shrink-0">
        <CardContent className="p-4">
          {/* Research Mode Toggle */}
          <div className="flex items-center justify-center gap-3 mb-4 p-3 bg-secondary/30 rounded-xl">
            <div className="flex items-center gap-3">
              <Zap className="h-4 w-4 text-primary" />
              <Label htmlFor="research-mode" className="text-sm font-medium">
                Quick Response
              </Label>
              <Switch
                id="research-mode"
                checked={isDeepResearch}
                onCheckedChange={setIsDeepResearch}
                className="data-[state=checked]:bg-primary"
              />
              <Label htmlFor="research-mode" className="text-sm font-medium">
                Deep Research
              </Label>
              <Search className="h-4 w-4 text-primary" />
            </div>
          </div>

          {/* File Upload Area */}
          {uploadedFiles.length > 0 && (
            <div className="mb-3 p-3 bg-secondary/30 rounded-xl">
              <div className="flex flex-wrap gap-2">
                {uploadedFiles.map((file, index) => (
                  <div key={index} className="flex items-center gap-2 bg-background/50 px-3 py-1 rounded-lg text-sm">
                    <FileText className="h-3 w-3" />
                    <span className="truncate max-w-[150px]">{file.name}</span>
                    <button
                      onClick={() => removeFile(index)}
                      className="text-muted-foreground hover:text-foreground"
                    >
                      <X className="h-3 w-3" />
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Chat Input */}
          <div
            className={`flex gap-3 ${isDragOver ? 'bg-primary/10 border-2 border-dashed border-primary rounded-xl p-2' : ''}`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf"
              multiple
              onChange={(e) => handleFileUpload(e.target.files)}
              className="hidden"
            />
            <Button
              variant="outline"
              size="sm"
              onClick={() => fileInputRef.current?.click()}
              className="self-end px-3 py-3 rounded-xl flex-shrink-0"
            >
              <Upload className="h-4 w-4" />
            </Button>
            <Textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder={isDragOver ? "Drop PDF files here..." : "Ask me to generate an intelligence report..."}
              className="min-h-[50px] max-h-[150px] resize-none apple-input"
              disabled={isLoading}
            />
            <Button
              onClick={sendMessage}
              disabled={isLoading || !input.trim()}
              className="self-end bg-primary hover:bg-primary/90 px-4 py-3 rounded-xl flex-shrink-0"
            >
              {isLoading ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Send className="h-4 w-4" />
              )}
            </Button>
          </div>
          
          {agents.length > 0 && (
            <div className="text-xs text-muted-foreground mt-2 text-center">
              Active agents: {agents.join(', ')} • {isDeepResearch ? 'Deep Research' : 'Quick Response'} Mode • Backend: localhost:8000
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};
