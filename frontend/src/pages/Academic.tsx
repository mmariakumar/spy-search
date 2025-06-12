
import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Search, GraduationCap, Send } from "lucide-react";
import { Link } from "react-router-dom";
import { useToast } from "@/hooks/use-toast";

const Academic = () => {
  const [query, setQuery] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [response, setResponse] = useState("");
  const { toast } = useToast();

  const handleSearch = async () => {
    if (!query.trim()) return;
    
    setIsLoading(true);
    setResponse("");
    
    try {
      const formData = new FormData();
      formData.append('messages', JSON.stringify([{ role: 'user', content: query }]));
      
      const res = await fetch(`http://localhost:8000/stream_completion_academic/${encodeURIComponent(query)}`, {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        throw new Error(`Server error: ${res.status}`);
      }

      const reader = res.body?.getReader();
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
        setResponse(accumulatedContent);
      }

    } catch (error) {
      toast({
        title: "Search Failed",
        description: "Failed to search academic content. Please try again.",
        variant: "destructive",
      });
      console.error('Academic search error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-6">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <Link to="/" className="flex items-center gap-3">
            <div className="p-2 rounded-xl bg-primary/10 border border-primary/20">
              <GraduationCap className="h-5 w-5 text-primary" />
            </div>
            <h1 className="text-xl font-light gradient-text">Academic Search</h1>
          </Link>
          <div className="flex gap-4">
            <Link to="/news">
              <Button variant="ghost" size="sm" className="text-muted-foreground hover:text-foreground">
                Discover
              </Button>
            </Link>
            <Link to="/">
              <Button variant="ghost" size="sm" className="text-muted-foreground hover:text-foreground">
                Home
              </Button>
            </Link>
          </div>
        </div>

        {/* Main Content */}
        <div className="max-w-4xl mx-auto">
          {/* Search Section */}
          <div className="text-center mb-12">
            <div className="flex items-center justify-center gap-3 mb-4">
              <GraduationCap className="h-8 w-8 text-primary" />
              <h2 className="text-3xl font-light text-foreground">Academic Research</h2>
            </div>
            <p className="text-lg text-muted-foreground font-light max-w-2xl mx-auto mb-8">
              Explore academic papers, journals, and research content
            </p>
            
            {/* Search Input */}
            <div className="flex gap-2 max-w-2xl mx-auto mb-8">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Search academic content..."
                  className="pl-10 pr-4 py-3 text-base"
                  onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                />
              </div>
              <Button 
                onClick={handleSearch} 
                disabled={!query.trim() || isLoading}
                className="px-6"
              >
                <Send className="h-4 w-4 mr-2" />
                Search
              </Button>
            </div>

            {/* Categories */}
            <div className="flex flex-wrap gap-3 justify-center">
              {[
                "Health", 
                "Law", 
                "Technology", 
                "Science", 
                "Humanities"
              ].map((category) => (
                <Button
                  key={category}
                  variant="ghost"
                  size="sm"
                  onClick={() => setQuery(`Research papers about ${category.toLowerCase()}`)}
                  className="rounded-full border border-border/40 text-muted-foreground hover:text-foreground hover:bg-muted/50"
                >
                  {category}
                </Button>
              ))}
            </div>
          </div>

          {/* Results Section */}
          {(response || isLoading) && (
            <Card className="glass-card border-0">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <GraduationCap className="h-5 w-5" />
                  Academic Research Results
                </CardTitle>
              </CardHeader>
              <CardContent>
                {isLoading ? (
                  <div className="flex items-center justify-center py-8">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
                    <span className="ml-3 text-muted-foreground">Searching academic content...</span>
                  </div>
                ) : (
                  <div className="prose prose-sm max-w-none">
                    <pre className="whitespace-pre-wrap text-sm">{response}</pre>
                  </div>
                )}
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};

export default Academic;
