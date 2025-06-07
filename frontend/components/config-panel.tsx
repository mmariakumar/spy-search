"use client"

import { useState } from "react"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"
import { Button } from "@/components/ui/button"
import { Eye, EyeOff, Search, Mail, FileText, BarChart3, Globe, Brain } from "lucide-react"

export default function ConfigPanel() {
  // Track which API keys are visible
  const [visibleApiKeys, setVisibleApiKeys] = useState<Record<string, boolean>>({
    plan: false,
    search: false,
    email: false,
    report: false,
    data: false,
    web: false,
    summary: false,
  })

  const toggleApiKeyVisibility = (agentType: string) => {
    setVisibleApiKeys((prev) => ({
      ...prev,
      [agentType]: !prev[agentType],
    }))
  }

  return (
    <div className="h-full flex flex-col">
      <div className="p-4 border-b border-zinc-800">
        <h2 className="text-xl font-bold">Configuration</h2>
      </div>
      <ScrollArea className="flex-1">
        <div className="p-4 space-y-6">
          <Accordion type="single" collapsible defaultValue="agent">
            <AccordionItem value="agent" className="border-zinc-800">
              <AccordionTrigger className="hover:bg-zinc-800 px-3 py-2 rounded-md">
                Agent Configuration
              </AccordionTrigger>
              <AccordionContent className="px-3 py-2">
                <div className="space-y-4">
                  {/* Planning Agent - Required */}
                  <div className="p-3 border border-zinc-700 rounded-lg bg-zinc-800/50">
                    <div className="flex items-center space-x-2 mb-2">
                      <Brain className="w-4 h-4 text-blue-400" />
                      <input
                        type="checkbox"
                        id="plan-agent"
                        checked={true}
                        disabled={true}
                        className="w-4 h-4 text-blue-600 bg-zinc-700 border-zinc-600 rounded focus:ring-blue-500 focus:ring-2"
                      />
                      <label htmlFor="plan-agent" className="text-sm font-medium text-zinc-300">
                        Plan Agent (Required)
                      </label>
                    </div>

                    <div className="space-y-3 mt-3">
                      <div>
                        <Label htmlFor="plan-provider" className="text-xs">
                          Provider
                        </Label>
                        <Select defaultValue="openai">
                          <SelectTrigger className="bg-zinc-800 border-zinc-700 text-xs mt-1">
                            <SelectValue placeholder="Select Provider" />
                          </SelectTrigger>
                          <SelectContent className="bg-zinc-800 border-zinc-700">
                            <SelectItem value="openai">OpenAI</SelectItem>
                            <SelectItem value="anthropic">Anthropic</SelectItem>
                            <SelectItem value="deepseek">DeepSeek</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>

                      <div>
                        <Label htmlFor="plan-model" className="text-xs">
                          Model
                        </Label>
                        <Select defaultValue="gpt-4o">
                          <SelectTrigger className="bg-zinc-800 border-zinc-700 text-xs mt-1">
                            <SelectValue placeholder="Select Model" />
                          </SelectTrigger>
                          <SelectContent className="bg-zinc-800 border-zinc-700">
                            <SelectItem value="gpt-4o">GPT-4o</SelectItem>
                            <SelectItem value="gpt-4-turbo">GPT-4 Turbo</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>

                      <div>
                        <Label htmlFor="plan-api-key" className="text-xs">
                          API Key
                        </Label>
                        <div className="flex mt-1">
                          <Input
                            id="plan-api-key"
                            type={visibleApiKeys.plan ? "text" : "password"}
                            placeholder="Enter API key"
                            className="bg-zinc-800 border-zinc-700 rounded-r-none text-xs"
                          />
                          <Button
                            type="button"
                            variant="outline"
                            className="rounded-l-none border-l-0 bg-zinc-800 border-zinc-700 h-8"
                            onClick={() => toggleApiKeyVisibility("plan")}
                          >
                            {visibleApiKeys.plan ? <EyeOff size={14} /> : <Eye size={14} />}
                          </Button>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Search Agent */}
                  <div className="p-3 border border-zinc-700 rounded-lg">
                    <div className="flex items-center space-x-2 mb-2">
                      <Search className="w-4 h-4 text-green-400" />
                      <input
                        type="checkbox"
                        id="search-agent"
                        defaultChecked={true}
                        className="w-4 h-4 text-blue-600 bg-zinc-700 border-zinc-600 rounded focus:ring-blue-500 focus:ring-2"
                      />
                      <label htmlFor="search-agent" className="text-sm font-medium">
                        Search Agent
                      </label>
                    </div>

                    <div className="space-y-3 mt-3">
                      <div>
                        <Label htmlFor="search-provider" className="text-xs">
                          Provider
                        </Label>
                        <Select defaultValue="openai">
                          <SelectTrigger className="bg-zinc-800 border-zinc-700 text-xs mt-1">
                            <SelectValue placeholder="Select Provider" />
                          </SelectTrigger>
                          <SelectContent className="bg-zinc-800 border-zinc-700">
                            <SelectItem value="openai">OpenAI</SelectItem>
                            <SelectItem value="anthropic">Anthropic</SelectItem>
                            <SelectItem value="deepseek">DeepSeek</SelectItem>
                            <SelectItem value="ollama">Ollama</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>

                      <div>
                        <Label htmlFor="search-model" className="text-xs">
                          Model
                        </Label>
                        <Select defaultValue="gpt-3.5-turbo">
                          <SelectTrigger className="bg-zinc-800 border-zinc-700 text-xs mt-1">
                            <SelectValue placeholder="Select Model" />
                          </SelectTrigger>
                          <SelectContent className="bg-zinc-800 border-zinc-700">
                            <SelectItem value="gpt-3.5-turbo">GPT-3.5 Turbo</SelectItem>
                            <SelectItem value="gpt-4o">GPT-4o</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>

                      <div>
                        <Label htmlFor="search-api-key" className="text-xs">
                          API Key
                        </Label>
                        <div className="flex mt-1">
                          <Input
                            id="search-api-key"
                            type={visibleApiKeys.search ? "text" : "password"}
                            placeholder="Enter API key"
                            className="bg-zinc-800 border-zinc-700 rounded-r-none text-xs"
                          />
                          <Button
                            type="button"
                            variant="outline"
                            className="rounded-l-none border-l-0 bg-zinc-800 border-zinc-700 h-8"
                            onClick={() => toggleApiKeyVisibility("search")}
                          >
                            {visibleApiKeys.search ? <EyeOff size={14} /> : <Eye size={14} />}
                          </Button>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Email Agent */}
                  <div className="p-3 border border-zinc-700 rounded-lg">
                    <div className="flex items-center space-x-2 mb-2">
                      <Mail className="w-4 h-4 text-purple-400" />
                      <input
                        type="checkbox"
                        id="email-agent"
                        className="w-4 h-4 text-blue-600 bg-zinc-700 border-zinc-600 rounded focus:ring-blue-500 focus:ring-2"
                      />
                      <label htmlFor="email-agent" className="text-sm font-medium">
                        Email Agent
                      </label>
                    </div>

                    <div className="space-y-3 mt-3">
                      <div>
                        <Label htmlFor="email-provider" className="text-xs">
                          Provider
                        </Label>
                        <Select defaultValue="anthropic">
                          <SelectTrigger className="bg-zinc-800 border-zinc-700 text-xs mt-1">
                            <SelectValue placeholder="Select Provider" />
                          </SelectTrigger>
                          <SelectContent className="bg-zinc-800 border-zinc-700">
                            <SelectItem value="anthropic">Anthropic</SelectItem>
                            <SelectItem value="openai">OpenAI</SelectItem>
                            <SelectItem value="ollama">Ollama</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>

                      <div>
                        <Label htmlFor="email-model" className="text-xs">
                          Model
                        </Label>
                        <Select defaultValue="claude-3-sonnet">
                          <SelectTrigger className="bg-zinc-800 border-zinc-700 text-xs mt-1">
                            <SelectValue placeholder="Select Model" />
                          </SelectTrigger>
                          <SelectContent className="bg-zinc-800 border-zinc-700">
                            <SelectItem value="claude-3-sonnet">Claude 3 Sonnet</SelectItem>
                            <SelectItem value="claude-3-opus">Claude 3 Opus</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>

                      <div>
                        <Label htmlFor="email-api-key" className="text-xs">
                          API Key
                        </Label>
                        <div className="flex mt-1">
                          <Input
                            id="email-api-key"
                            type={visibleApiKeys.email ? "text" : "password"}
                            placeholder="Enter API key"
                            className="bg-zinc-800 border-zinc-700 rounded-r-none text-xs"
                          />
                          <Button
                            type="button"
                            variant="outline"
                            className="rounded-l-none border-l-0 bg-zinc-800 border-zinc-700 h-8"
                            onClick={() => toggleApiKeyVisibility("email")}
                          >
                            {visibleApiKeys.email ? <EyeOff size={14} /> : <Eye size={14} />}
                          </Button>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Report Agent */}
                  <div className="p-3 border border-zinc-700 rounded-lg">
                    <div className="flex items-center space-x-2 mb-2">
                      <FileText className="w-4 h-4 text-orange-400" />
                      <input
                        type="checkbox"
                        id="report-agent"
                        defaultChecked={true}
                        className="w-4 h-4 text-blue-600 bg-zinc-700 border-zinc-600 rounded focus:ring-blue-500 focus:ring-2"
                      />
                      <label htmlFor="report-agent" className="text-sm font-medium">
                        Report Agent
                      </label>
                    </div>

                    <div className="space-y-3 mt-3">
                      <div>
                        <Label htmlFor="report-provider" className="text-xs">
                          Provider
                        </Label>
                        <Select defaultValue="anthropic">
                          <SelectTrigger className="bg-zinc-800 border-zinc-700 text-xs mt-1">
                            <SelectValue placeholder="Select Provider" />
                          </SelectTrigger>
                          <SelectContent className="bg-zinc-800 border-zinc-700">
                            <SelectItem value="anthropic">Anthropic</SelectItem>
                            <SelectItem value="openai">OpenAI</SelectItem>
                            <SelectItem value="deepseek">DeepSeek</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>

                      <div>
                        <Label htmlFor="report-model" className="text-xs">
                          Model
                        </Label>
                        <Select defaultValue="claude-3-opus">
                          <SelectTrigger className="bg-zinc-800 border-zinc-700 text-xs mt-1">
                            <SelectValue placeholder="Select Model" />
                          </SelectTrigger>
                          <SelectContent className="bg-zinc-800 border-zinc-700">
                            <SelectItem value="claude-3-opus">Claude 3 Opus</SelectItem>
                            <SelectItem value="claude-3-sonnet">Claude 3 Sonnet</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>

                      <div>
                        <Label htmlFor="report-api-key" className="text-xs">
                          API Key
                        </Label>
                        <div className="flex mt-1">
                          <Input
                            id="report-api-key"
                            type={visibleApiKeys.report ? "text" : "password"}
                            placeholder="Enter API key"
                            className="bg-zinc-800 border-zinc-700 rounded-r-none text-xs"
                          />
                          <Button
                            type="button"
                            variant="outline"
                            className="rounded-l-none border-l-0 bg-zinc-800 border-zinc-700 h-8"
                            onClick={() => toggleApiKeyVisibility("report")}
                          >
                            {visibleApiKeys.report ? <EyeOff size={14} /> : <Eye size={14} />}
                          </Button>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Additional agents (collapsed by default) */}
                  <Accordion type="single" collapsible className="border-none">
                    <AccordionItem value="more-agents" className="border-none">
                      <AccordionTrigger className="py-1 text-sm text-zinc-400">Show more agents</AccordionTrigger>
                      <AccordionContent>
                        <div className="space-y-4">
                          {/* Data Analysis Agent */}
                          <div className="p-3 border border-zinc-700 rounded-lg">
                            <div className="flex items-center space-x-2 mb-2">
                              <BarChart3 className="w-4 h-4 text-cyan-400" />
                              <input
                                type="checkbox"
                                id="data-agent"
                                className="w-4 h-4 text-blue-600 bg-zinc-700 border-zinc-600 rounded focus:ring-blue-500 focus:ring-2"
                              />
                              <label htmlFor="data-agent" className="text-sm font-medium">
                                Data Analysis Agent
                              </label>
                            </div>

                            <div className="space-y-3 mt-3">
                              <div>
                                <Label htmlFor="data-provider" className="text-xs">
                                  Provider
                                </Label>
                                <Select defaultValue="deepseek">
                                  <SelectTrigger className="bg-zinc-800 border-zinc-700 text-xs mt-1">
                                    <SelectValue placeholder="Select Provider" />
                                  </SelectTrigger>
                                  <SelectContent className="bg-zinc-800 border-zinc-700">
                                    <SelectItem value="deepseek">DeepSeek</SelectItem>
                                    <SelectItem value="openai">OpenAI</SelectItem>
                                    <SelectItem value="ollama">Ollama</SelectItem>
                                  </SelectContent>
                                </Select>
                              </div>

                              <div>
                                <Label htmlFor="data-model" className="text-xs">
                                  Model
                                </Label>
                                <Select defaultValue="deepseek-v3">
                                  <SelectTrigger className="bg-zinc-800 border-zinc-700 text-xs mt-1">
                                    <SelectValue placeholder="Select Model" />
                                  </SelectTrigger>
                                  <SelectContent className="bg-zinc-800 border-zinc-700">
                                    <SelectItem value="deepseek-v3">DeepSeek V3</SelectItem>
                                    <SelectItem value="deepseek-math">DeepSeek Math</SelectItem>
                                  </SelectContent>
                                </Select>
                              </div>

                              <div>
                                <Label htmlFor="data-api-key" className="text-xs">
                                  API Key
                                </Label>
                                <div className="flex mt-1">
                                  <Input
                                    id="data-api-key"
                                    type={visibleApiKeys.data ? "text" : "password"}
                                    placeholder="Enter API key"
                                    className="bg-zinc-800 border-zinc-700 rounded-r-none text-xs"
                                  />
                                  <Button
                                    type="button"
                                    variant="outline"
                                    className="rounded-l-none border-l-0 bg-zinc-800 border-zinc-700 h-8"
                                    onClick={() => toggleApiKeyVisibility("data")}
                                  >
                                    {visibleApiKeys.data ? <EyeOff size={14} /> : <Eye size={14} />}
                                  </Button>
                                </div>
                              </div>
                            </div>
                          </div>

                          {/* Web Scraping Agent */}
                          <div className="p-3 border border-zinc-700 rounded-lg">
                            <div className="flex items-center space-x-2 mb-2">
                              <Globe className="w-4 h-4 text-yellow-400" />
                              <input
                                type="checkbox"
                                id="web-agent"
                                className="w-4 h-4 text-blue-600 bg-zinc-700 border-zinc-600 rounded focus:ring-blue-500 focus:ring-2"
                              />
                              <label htmlFor="web-agent" className="text-sm font-medium">
                                Web Scraping Agent
                              </label>
                            </div>

                            <div className="space-y-3 mt-3">
                              <div>
                                <Label htmlFor="web-provider" className="text-xs">
                                  Provider
                                </Label>
                                <Select defaultValue="ollama">
                                  <SelectTrigger className="bg-zinc-800 border-zinc-700 text-xs mt-1">
                                    <SelectValue placeholder="Select Provider" />
                                  </SelectTrigger>
                                  <SelectContent className="bg-zinc-800 border-zinc-700">
                                    <SelectItem value="ollama">Ollama</SelectItem>
                                    <SelectItem value="openai">OpenAI</SelectItem>
                                    <SelectItem value="deepseek">DeepSeek</SelectItem>
                                  </SelectContent>
                                </Select>
                              </div>

                              <div>
                                <Label htmlFor="web-model" className="text-xs">
                                  Model
                                </Label>
                                <Select defaultValue="llama3">
                                  <SelectTrigger className="bg-zinc-800 border-zinc-700 text-xs mt-1">
                                    <SelectValue placeholder="Select Model" />
                                  </SelectTrigger>
                                  <SelectContent className="bg-zinc-800 border-zinc-700">
                                    <SelectItem value="llama3">Llama 3</SelectItem>
                                    <SelectItem value="mistral">Mistral</SelectItem>
                                  </SelectContent>
                                </Select>
                              </div>

                              <div>
                                <Label htmlFor="web-api-key" className="text-xs">
                                  API Key
                                </Label>
                                <div className="flex mt-1">
                                  <Input
                                    id="web-api-key"
                                    type={visibleApiKeys.web ? "text" : "password"}
                                    placeholder="Enter API key or local URL"
                                    className="bg-zinc-800 border-zinc-700 rounded-r-none text-xs"
                                  />
                                  <Button
                                    type="button"
                                    variant="outline"
                                    className="rounded-l-none border-l-0 bg-zinc-800 border-zinc-700 h-8"
                                    onClick={() => toggleApiKeyVisibility("web")}
                                  >
                                    {visibleApiKeys.web ? <EyeOff size={14} /> : <Eye size={14} />}
                                  </Button>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </AccordionContent>
                    </AccordionItem>
                  </Accordion>
                </div>
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="settings" className="border-zinc-800">
              <AccordionTrigger className="hover:bg-zinc-800 px-3 py-2 rounded-md">Global Settings</AccordionTrigger>
              <AccordionContent className="px-3 py-2">
                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="temperature">Default Temperature</Label>
                    <div className="flex items-center gap-2">
                      <Input
                        id="temperature"
                        type="range"
                        min="0"
                        max="1"
                        step="0.1"
                        defaultValue="0.7"
                        className="bg-zinc-800 border-zinc-700"
                      />
                      <span className="text-sm">0.7</span>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="max-tokens">Max Tokens</Label>
                    <Input id="max-tokens" type="number" defaultValue="4000" className="bg-zinc-800 border-zinc-700" />
                  </div>
                </div>
              </AccordionContent>
            </AccordionItem>
          </Accordion>
        </div>
      </ScrollArea>
      <div className="p-4 border-t border-zinc-800">
        <Button className="w-full bg-zinc-700 hover:bg-zinc-600">Apply Configuration</Button>
      </div>
    </div>
  )
}
