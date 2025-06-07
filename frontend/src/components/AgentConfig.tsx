
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
    { id: "planner", label: "Planner", required: true, disabled: false },
    { id: "searcher", label: "Searcher", required: false, disabled: false },
    { id: "local-retrieval", label: "Local Retrieval Searcher", required: false, disabled: false },
    { id: "executor", label: "Executor", required: false, disabled: true },
    { id: "reporter", label: "Reporter", required: false, disabled: false, group: "output" },
    { id: "summary", label: "Summary", required: false, disabled: false, group: "output" },
    { id: "email", label: "Email", required: false, disabled: true },
    { id: "notion", label: "Notion", required: false, disabled: true },
    { id: "google-drive", label: "Google Drive", required: false, disabled: true }
  ];

  // Ensure planner is always included
  useEffect(() => {
    if (!selectedAgents.includes("planner")) {
      setSelectedAgents(prev => [...prev, "planner"]);
    }
  }, [selectedAgents]);

  const handleAgentChange = (agentId: string, checked: boolean) => {
    if (agentId === "planner") return; // Planner cannot be unchecked
    
    const agent = availableAgents.find(a => a.id === agentId);
    if (agent?.disabled) return; // Disabled agents cannot be toggled
    
    if (checked) {
      setSelectedAgents(prev => [...prev, agentId]);
    } else {
      setSelectedAgents(prev => prev.filter(agent => agent !== agentId));
    }
  };

  const handleSave = () => {
    // Validate that either reporter or summary is selected
    const hasReporter = selectedAgents.includes("reporter");
    const hasSummary = selectedAgents.includes("summary");
    
    if (!hasReporter && !hasSummary) {
      // Auto-select reporter if neither is selected
      const finalAgents = [...selectedAgents, "reporter"];
      setSelectedAgents(finalAgents);
      onAgentConfigSave(finalAgents);
      return;
    }
    
    const finalAgents = selectedAgents.includes("planner") ? selectedAgents : [...selectedAgents, "planner"];
    onAgentConfigSave(finalAgents);
  };

  const isOutputGroupSelected = selectedAgents.includes("reporter") || selectedAgents.includes("summary");

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
                disabled={agent.required || agent.disabled}
                className="border-primary/50"
              />
              <Label 
                htmlFor={agent.id} 
                className={`text-foreground font-medium cursor-pointer ${
                  agent.required ? 'text-primary' : ''
                } ${
                  agent.disabled ? 'text-muted-foreground opacity-60' : ''
                }`}
              >
                {agent.label}
                {agent.required && (
                  <span className="text-xs text-primary ml-2">(Required)</span>
                )}
                {agent.disabled && (
                  <span className="text-xs text-muted-foreground ml-2">(Disabled)</span>
                )}
                {agent.group === "output" && (
                  <span className="text-xs text-orange-500 ml-2">(One required)</span>
                )}
              </Label>
            </div>
          ))}
          
          {!isOutputGroupSelected && (
            <div className="text-sm text-orange-500 mt-2 p-2 bg-orange-500/10 rounded">
              Note: Either Reporter or Summary must be selected. Reporter will be auto-selected if neither is chosen.
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
