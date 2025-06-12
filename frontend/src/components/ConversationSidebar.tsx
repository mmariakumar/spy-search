
import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { 
  Sidebar,
  SidebarContent,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
} from "@/components/ui/sidebar";
import { MessageSquare, Plus, Trash2 } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

interface ConversationItem {
  title: string;
  messages: Array<{
    id: string;
    type: 'user' | 'assistant';
    content: string;
    timestamp: Date;
  }>;
}

interface ConversationSidebarProps {
  currentConversationTitle: string | null;
  onConversationSelect: (title: string) => void;
  onNewConversation: () => void;
}

export const ConversationSidebar = ({ 
  currentConversationTitle, 
  onConversationSelect, 
  onNewConversation
}: ConversationSidebarProps) => {
  const [conversations, setConversations] = useState<ConversationItem[]>([]);
  const { toast } = useToast();

  // Load conversations from backend on mount
  useEffect(() => {
    loadConversations();
  }, []);

  const loadConversations = async () => {
    try {
      const savedTitles = localStorage.getItem('conversation-titles');
      if (savedTitles) {
        const titles = JSON.parse(savedTitles);
        const conversationPromises = titles.map(async (title: string) => {
          try {
            const response = await fetch('http://localhost:8000/load_message', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ title }),
            });
            if (response.ok) {
              const messages = await response.json();
              return {
                title,
                messages: messages.map((msg: any, index: number) => ({
                  id: `${index}`,
                  type: msg.role === 'user' ? 'user' : 'assistant',
                  content: msg.content,
                  timestamp: new Date()
                }))
              };
            }
          } catch (error) {
            console.error(`Failed to load conversation ${title}:`, error);
          }
          return null;
        });
        
        const loadedConversations = await Promise.all(conversationPromises);
        setConversations(loadedConversations.filter(conv => conv !== null));
      }
    } catch (error) {
      console.error('Failed to load conversations:', error);
    }
  };

  const deleteConversation = async (title: string, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      const response = await fetch('http://localhost:8000/delete_message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title }),
      });
      
      if (response.ok) {
        setConversations(prev => prev.filter(conv => conv.title !== title));
        
        // Update local titles list
        const savedTitles = localStorage.getItem('conversation-titles');
        if (savedTitles) {
          const titles = JSON.parse(savedTitles);
          const updatedTitles = titles.filter((t: string) => t !== title);
          localStorage.setItem('conversation-titles', JSON.stringify(updatedTitles));
        }
        
        if (currentConversationTitle === title) {
          onNewConversation();
        }
        
        toast({
          title: "Conversation deleted",
          description: "The conversation has been removed successfully.",
        });
      }
    } catch (error) {
      console.error('Failed to delete conversation:', error);
      toast({
        title: "Error",
        description: "Failed to delete conversation. Please try again.",
        variant: "destructive",
      });
    }
  };

  return (
    <Sidebar>
      <SidebarHeader className="p-4">
        <Button
          onClick={onNewConversation}
          className="w-full justify-start"
          variant="outline"
        >
          <Plus className="h-4 w-4 mr-2" />
          New conversation
        </Button>
      </SidebarHeader>
      <SidebarContent>
        <ScrollArea className="h-full">
          <SidebarMenu className="p-2">
            {conversations.map((conversation) => (
              <SidebarMenuItem key={conversation.title}>
                <SidebarMenuButton
                  onClick={() => onConversationSelect(conversation.title)}
                  isActive={currentConversationTitle === conversation.title}
                  className="w-full justify-between group"
                >
                  <div className="flex items-center min-w-0">
                    <MessageSquare className="h-4 w-4 mr-2 flex-shrink-0" />
                    <span className="truncate text-sm">{conversation.title}</span>
                  </div>
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={(e) => deleteConversation(conversation.title, e)}
                    className="opacity-0 group-hover:opacity-100 h-6 w-6 p-0"
                  >
                    <Trash2 className="h-3 w-3" />
                  </Button>
                </SidebarMenuButton>
              </SidebarMenuItem>
            ))}
          </SidebarMenu>
        </ScrollArea>
      </SidebarContent>
    </Sidebar>
  );
};

// Export conversation manager functions
export const conversationManager = {
  saveMessage: async (title: string, role: 'user' | 'assistant', content: string) => {
    try {
      const response = await fetch('http://localhost:8000/append_message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: {
            role: role,
            content: content
          },
          title: title
        }),
      });
      
      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }
      
      // Update local titles list
      const savedTitles = localStorage.getItem('conversation-titles');
      const titles = savedTitles ? JSON.parse(savedTitles) : [];
      if (!titles.includes(title)) {
        titles.unshift(title);
        localStorage.setItem('conversation-titles', JSON.stringify(titles));
      }
      
      return true;
    } catch (error) {
      console.error('Failed to save message:', error);
      return false;
    }
  }
};
