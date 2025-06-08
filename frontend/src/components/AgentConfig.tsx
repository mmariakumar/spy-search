
import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Users, Settings2 } from "lucide-react";

interface AgentConfigProps {
  agents: string[];
  onAgentConfigSave: (agents: string[]) => void;
}

export const AgentConfig = ({ agents, onAgentConfigSave }: AgentConfigProps) => {
  const [selectedAgents, setSelectedAgents] = useState<string[]>(agents);

  const availableAgents = [
    { id: "searcher", label: "Searcher", required: false, disabled: false },
    { id: "local-retrieval", label: "Local Retrieval Searcher", required: false, disabled: true },
    { id: "executor", label: "Executor", required: false, disabled: true },
    { id: "reporter", label: "Reporter", required: false, disabled: false, group: "output" },
    { id: "summary", label: "Summary", required: false, disabled: true, group: "output" },
    { id: "email", label: "Email", required: false, disabled: true },
    { id: "notion", label: "Notion", required: false, disabled: true },
    { id: "google-drive", label: "Google Drive", required: false, disabled: true }
  ];

  // Ensure planner is always included but not shown
  useEffect(() => {
    if (!selectedAgents.includes("planner")) {
      setSelectedAgents(prev => [...prev, "planner"]);
    }
  }, [selectedAgents]);

  const handleAgentChange = (agentId: string, checked: boolean) => {
    const agent = availableAgents.find(a => a.id === agentId);
    if (agent?.disabled) return; // Disabled agents cannot be toggled
    
    if (checked) {
      setSelectedAgents(prev => [...prev, agentId]);
    } else {
      setSelectedAgents(prev => prev.filter(agent => agent !== agentId));
    }
  };

  const handleSave = () => {
    // Validate that reporter is selected since summary is disabled
    const hasReporter = selectedAgents.includes("reporter");
    
    if (!hasReporter) {
      // Auto-select reporter if not selected
      const finalAgents = [...selectedAgents, "reporter"];
      setSelectedAgents(finalAgents);
      onAgentConfigSave(finalAgents);
      return;
    }
    
    const finalAgents = selectedAgents.includes("planner") ? selectedAgents : [...selectedAgents, "planner"];
    onAgentConfigSave(finalAgents);
  };

  const isReporterSelected = selectedAgents.includes("reporter");

  return (
    <div className="space-y-8">
      {/* Agent Selection */}
      <Card className="glass-card border-0">
        <CardHeader className="pb-4">
          <CardTitle className="flex items-center gap-3 text-lg font-medium">
            <Users className="h-5 w-5 text-primary" />
            Agent Selection
          </CardTitle>
          <CardDescription>Select which agents to use for intelligence gathering</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {availableAgents.map((agent) => (
            <div key={agent.id} className="flex items-center space-x-3">
              <Checkbox
                id={agent.id}
                checked={selectedAgents.includes(agent.id)}
                onCheckedChange={(checked) => handleAgentChange(agent.id, checked as boolean)}
                disabled={agent.disabled}
                className="border-primary/50"
              />
              <Label 
                htmlFor={agent.id} 
                className={`text-foreground font-medium cursor-pointer ${
                  agent.disabled ? 'text-muted-foreground opacity-60' : ''
                }`}
              >
                {agent.label}
                {agent.disabled && (
                  <span className="text-xs text-muted-foreground ml-2">(Disabled)</span>
                )}
                {agent.id === "reporter" && (
                  <span className="text-xs text-orange-500 ml-2">(Required)</span>
                )}
              </Label>
            </div>
          ))}
          
          {!isReporterSelected && (
            <div className="text-sm text-orange-500 mt-2 p-2 bg-orange-500/10 rounded">
              Note: Reporter is required and will be auto-selected if not chosen.
            </div>
          )}
        </CardContent>
      </Card>

      {/* Save Configuration */}
      <Button
        onClick={handleSave}
        className="w-full bg-primary hover:bg-primary/90 text-primary-foreground font-medium py-6 text-lg rounded-xl"
      >
        <Settings2 className="mr-3 h-5 w-5" />
        Save Agent Configuration
      </Button>
    </div>
  );
};
