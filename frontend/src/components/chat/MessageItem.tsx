
import { User, Bot } from "lucide-react";
import ReactMarkdown from "react-markdown";

interface Message {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface MessageItemProps {
  message: Message;
  isStreaming?: boolean;
}

export const MessageItem = ({ message, isStreaming }: MessageItemProps) => {
  const isUser = message.type === 'user';

  return (
    <div className={`group flex gap-6 ${isUser ? 'justify-end' : 'justify-start'} mb-8`}>
      {!isUser && (
        <div className="flex-shrink-0 mt-1">
          <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
            <Bot className="h-4 w-4 text-primary" />
          </div>
        </div>
      )}
      
      <div className={`flex-1 max-w-4xl ${isUser ? 'flex justify-end' : ''}`}>
        <div className={`
          rounded-3xl px-6 py-4 text-[15px] leading-7
          ${isUser 
            ? 'bg-primary text-primary-foreground max-w-2xl shadow-sm' 
            : 'bg-background text-foreground'
          }
        `}>
          {isUser ? (
            <div className="whitespace-pre-wrap break-words font-medium">{message.content}</div>
          ) : (
            <div className="prose prose-sm max-w-none dark:prose-invert prose-headings:text-foreground prose-p:text-foreground prose-strong:text-foreground prose-code:text-foreground prose-pre:bg-muted/50 prose-pre:border prose-pre:border-border/20 prose-blockquote:border-primary/20 prose-a:text-primary hover:prose-a:text-primary/80">
              <ReactMarkdown
                components={{
                  code: ({ node, className, children, ...props }) => {
                    const match = /language-(\w+)/.exec(className || '');
                    if (!className) {
                      return (
                        <code 
                          className="px-2 py-1 rounded-md bg-muted/60 border border-border/20 text-sm font-mono text-foreground"
                          {...props}
                        >
                          {children}
                        </code>
                      );
                    }
                    return (
                      <pre className="p-4 rounded-xl bg-muted/40 border border-border/20 overflow-x-auto">
                        <code className="text-sm font-mono text-foreground" {...props}>
                          {children}
                        </code>
                      </pre>
                    );
                  },
                  p: ({ children }) => <p className="mb-4 last:mb-0 text-foreground leading-7">{children}</p>,
                  ul: ({ children }) => <ul className="mb-4 pl-6 space-y-2 text-foreground">{children}</ul>,
                  ol: ({ children }) => <ol className="mb-4 pl-6 space-y-2 text-foreground">{children}</ol>,
                  li: ({ children }) => <li className="text-foreground leading-6">{children}</li>,
                  h1: ({ children }) => <h1 className="text-xl font-bold mb-4 text-foreground">{children}</h1>,
                  h2: ({ children }) => <h2 className="text-lg font-bold mb-3 text-foreground">{children}</h2>,
                  h3: ({ children }) => <h3 className="text-base font-bold mb-2 text-foreground">{children}</h3>,
                  strong: ({ children }) => <strong className="font-bold text-foreground">{children}</strong>,
                  em: ({ children }) => <em className="italic text-foreground">{children}</em>,
                  blockquote: ({ children }) => (
                    <blockquote className="border-l-4 border-primary/30 pl-4 italic text-muted-foreground mb-4 bg-muted/20 py-2 rounded-r-lg">
                      {children}
                    </blockquote>
                  ),
                  a: ({ children, href }) => (
                    <a href={href} className="text-primary hover:text-primary/80 underline font-medium" target="_blank" rel="noopener noreferrer">
                      {children}
                    </a>
                  ),
                }}
              >
                {message.content}
              </ReactMarkdown>
              {isStreaming && (
                <span className="inline-block w-0.5 h-5 bg-foreground animate-pulse ml-1"></span>
              )}
            </div>
          )}
        </div>
      </div>

      {isUser && (
        <div className="flex-shrink-0 mt-1">
          <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center">
            <User className="h-4 w-4 text-primary-foreground" />
          </div>
        </div>
      )}
    </div>
  );
};
