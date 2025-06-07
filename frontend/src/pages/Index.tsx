
import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Search, Settings, Eye } from "lucide-react";
import { ReportGenerator } from "@/components/ReportGenerator";
import { LLMConfig } from "@/components/LLMConfig";
import { useToast } from "@/hooks/use-toast";

const Index = () => {
  const [apiConfig, setApiConfig] = useState({
    provider: "openai",
    apiKey: "",
    model: "gpt-4",
    agents: ["planner"]
  });
  const { toast } = useToast();

  const handleConfigSave = (config: typeof apiConfig) => {
    setApiConfig(config);
    localStorage.setItem('spy-search-config', JSON.stringify(config));
    toast({
      title: "Configuration Saved",
      description: "Your settings have been saved successfully.",
    });
  };

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-12">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="flex items-center justify-center gap-4 mb-6">
            <div className="p-4 rounded-2xl bg-primary/10 border border-primary/20 backdrop-blur-sm">
              <Eye className="h-10 w-10 text-primary" />
            </div>
            <h1 className="text-6xl font-light gradient-text tracking-tight">
              Spy Search
            </h1>
          </div>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto font-light leading-relaxed">
            Advanced AI-powered intelligence gathering and report generation platform
          </p>
        </div>

        {/* Main Content */}
        <div className="max-w-5xl mx-auto">
          <Tabs defaultValue="generate" className="w-full">
            <TabsList className="grid w-full grid-cols-2 mb-12 bg-secondary/50 backdrop-blur-sm border border-border/50">
              <TabsTrigger value="generate" className="flex items-center gap-3 data-[state=active]:bg-primary/10 data-[state=active]:text-primary">
                <Search className="h-4 w-4" />
                Generate Report
              </TabsTrigger>
              <TabsTrigger value="settings" className="flex items-center gap-3 data-[state=active]:bg-primary/10 data-[state=active]:text-primary">
                <Settings className="h-4 w-4" />
                Configuration
              </TabsTrigger>
            </TabsList>

            <TabsContent value="generate" className="space-y-8">
              <Card className="glass-card border-0">
                <CardHeader className="pb-8">
                  <CardTitle className="flex items-center gap-3 text-2xl font-light">
                    <Search className="h-6 w-6 text-primary" />
                    Intelligence Report Generation
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ReportGenerator apiConfig={apiConfig} />
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="settings" className="space-y-8">
              <Card className="glass-card border-0">
                <CardHeader className="pb-8">
                  <CardTitle className="flex items-center gap-3 text-2xl font-light">
                    <Settings className="h-6 w-6 text-primary" />
                    System Configuration
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <LLMConfig
                    config={apiConfig}
                    onConfigSave={handleConfigSave}
                  />
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  );
};

export default Index;
