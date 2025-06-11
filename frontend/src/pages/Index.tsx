
import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Settings, Eye, MessageSquare, Newspaper } from "lucide-react";
import { ChatInterface } from "@/components/ChatInterface";
import { AgentConfig } from "@/components/AgentConfig";
import { useToast } from "@/hooks/use-toast";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";

interface Message {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

const Index = () => {
  const [agents, setAgents] = useState<string[]>(["planner", "reporter"]);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const { toast } = useToast();

  const handleAgentConfigSave = async (config: {
    agents: string[];
    provider: string;
    model: string;
  }) => {
    setAgents(config.agents);
    
    const agentsToSend = config.agents.filter(agent => agent !== "planner");
    
    try {
      const response = await fetch('http://localhost:8000/agents_selection', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          agents: agentsToSend,
          provider: config.provider,
          model: config.model
        }),
      });
      
      const data = await response.json();
      
      if (data.success) {
        toast({
          title: "Configuration Saved",
          description: `Agent selection, provider (${config.provider}), and model (${config.model}) have been saved successfully.`,
        });
        setShowSettings(false);
      } else {
        throw new Error("Failed to save configuration");
      }
    } catch (error) {
      toast({
        title: "Configuration Failed",
        description: "Failed to save agent configuration. Please try again.",
        variant: "destructive",
      });
    }
  };

  if (showSettings) {
    return (
      <div className="min-h-screen bg-background">
        <div className="container mx-auto px-4 py-6">
          {/* Header */}
          <div className="flex items-center justify-between mb-8">
            <Button
              variant="ghost"
              onClick={() => setShowSettings(false)}
              className="text-muted-foreground hover:text-foreground"
            >
              ← Back to Chat
            </Button>
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-xl bg-primary/10 border border-primary/20">
                <Settings className="h-5 w-5 text-primary" />
              </div>
              <h1 className="text-2xl font-light text-foreground">Settings</h1>
            </div>
            <div className="w-24"></div>
          </div>

          {/* Settings Content */}
          <div className="max-w-3xl mx-auto">
            <Card className="glass-card border-0">
              <CardHeader className="pb-8">
                <CardTitle className="flex items-center gap-3 text-2xl font-light">
                  <Settings className="h-6 w-6 text-primary" />
                  Agent Configuration
                </CardTitle>
              </CardHeader>
              <CardContent>
                <AgentConfig
                  agents={agents}
                  onAgentConfigSave={handleAgentConfigSave}
                />
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-6">
        {/* Top Navigation */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-6">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-xl bg-primary/10 border border-primary/20">
                <Eye className="h-5 w-5 text-primary" />
              </div>
              <h1 className="text-xl font-light gradient-text">Spy Search</h1>
            </div>
            <Link to="/news">
              <Button variant="ghost" size="sm" className="text-muted-foreground hover:text-foreground">
                <Newspaper className="h-4 w-4 mr-2" />
                Discover
              </Button>
            </Link>
          </div>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setShowSettings(true)}
            className="text-muted-foreground hover:text-foreground"
          >
            <Settings className="h-4 w-4 mr-2" />
            Settings
          </Button>
        </div>

        {/* Main Chat Interface */}
        <ChatInterface 
          agents={agents} 
          messages={messages}
          setMessages={setMessages}
          isLoading={isLoading}
          setIsLoading={setIsLoading}
        />
      </div>
    </div>
  );
};

export default Index;
