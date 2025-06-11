
import { useState, useCallback } from 'react';

interface Message {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface UseStreamingChatProps {
  messages: Message[];
  setMessages: React.Dispatch<React.SetStateAction<Message[]>>;
  setIsLoading: React.Dispatch<React.SetStateAction<boolean>>;
}

export const useStreamingChat = ({ messages, setMessages, setIsLoading }: UseStreamingChatProps) => {
  const [streamingMessageId, setStreamingMessageId] = useState<string | null>(null);

  const sendStreamingMessage = useCallback(async (
    messageContent: string,
    files: File[],
    isDeepResearch: boolean
  ) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: messageContent,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    // Create assistant message placeholder for streaming
    const assistantMessageId = (Date.now() + 1).toString();
    const assistantMessage: Message = {
      id: assistantMessageId,
      type: 'assistant',
      content: '',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, assistantMessage]);
    setStreamingMessageId(assistantMessageId);

    try {
      const endpoint = isDeepResearch ? 'report' : 'stream_completion';
      const encodedQuery = encodeURIComponent(messageContent);
      
      // Convert messages to the required format
      const allMessages = [...messages, userMessage];
      const formattedMessages = allMessages.map(msg => ({
        role: msg.type === 'user' ? 'user' : 'assistant',
        content: msg.content
      }));

      const formData = new FormData();
      formData.append('messages', JSON.stringify(formattedMessages));
      
      files.forEach(file => {
        formData.append('files', file);
      });

      const response = await fetch(`http://localhost:8000/${endpoint}/${encodedQuery}`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      if (isDeepResearch) {
        // Handle non-streaming response for deep research
        const data = await response.json();
        
        if (data.error) {
          throw new Error(data.error);
        }

        setMessages(prev => 
          prev.map(msg => 
            msg.id === assistantMessageId 
              ? { ...msg, content: data.report }
              : msg
          )
        );
      } else {
        // Handle streaming response for quick completion
        const reader = response.body?.getReader();
        const decoder = new TextDecoder();

        if (!reader) {
          throw new Error('No response stream available');
        }

        let accumulatedContent = '';

        while (true) {
          const { done, value } = await reader.read();
          
          if (done) break;

          const chunk = decoder.decode(value, { stream: true });
          accumulatedContent += chunk;

          // Update the assistant message with accumulated content
          setMessages(prev => 
            prev.map(msg => 
              msg.id === assistantMessageId 
                ? { ...msg, content: accumulatedContent }
                : msg
            )
          );
        }
      }

    } catch (error) {
      const errorMessage = "Sorry, I encountered an error while generating your report. Please try again.";
      
      setMessages(prev => 
        prev.map(msg => 
          msg.id === assistantMessageId 
            ? { ...msg, content: errorMessage }
            : msg
        )
      );

      console.error('Streaming error:', error);
    } finally {
      setIsLoading(false);
      setStreamingMessageId(null);
    }
  }, [messages, setMessages, setIsLoading]);

  return {
    sendStreamingMessage,
    streamingMessageId
  };
};
