
import { useState, useEffect } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Eye, ArrowLeft, ExternalLink, Calendar, Globe } from "lucide-react";
import { Link } from "react-router-dom";
import { useToast } from "@/hooks/use-toast";

interface NewsItem {
  snippet: string;
  title: string;
  link: string;
  date: string;
  source: string;
}

const News = () => {
  const [news, setNews] = useState<NewsItem[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState("technology");
  const { toast } = useToast();

  const categories = [
    { id: "technology", label: "Tech & Science" },
    { id: "finance", label: "Finance" },
    { id: "entertainment", label: "Entertainment" },
    { id: "sports", label: "Sports" },
    { id: "world", label: "World" },
    { id: "health", label: "Health" }
  ];

  const fetchNews = async (category: string) => {
    setIsLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/news/${category}`);
      if (response.ok) {
        const data = await response.json();
        setNews(data.news || []);
      } else {
        throw new Error("Failed to fetch news");
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to fetch news. Please try again.",
        variant: "destructive",
      });
      setNews([]);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchNews(selectedCategory);
  }, [selectedCategory]);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric',
      year: 'numeric'
    });
  };

  const truncateText = (text: string, maxLength: number) => {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + "...";
  };

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-6">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-6">
            <Link to="/">
              <Button variant="ghost" size="sm" className="text-muted-foreground hover:text-foreground">
                <ArrowLeft className="h-4 w-4 mr-2" />
                Back to Chat
              </Button>
            </Link>
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-xl bg-primary/10 border border-primary/20">
                <Eye className="h-5 w-5 text-primary" />
              </div>
              <h1 className="text-2xl font-light gradient-text">Discover</h1>
            </div>
          </div>
        </div>

        {/* Category Navigation */}
        <div className="flex flex-wrap gap-2 mb-8 justify-center">
          {categories.map((category) => (
            <Button
              key={category.id}
              variant={selectedCategory === category.id ? "default" : "ghost"}
              size="sm"
              onClick={() => setSelectedCategory(category.id)}
              className={`rounded-full px-6 ${
                selectedCategory === category.id
                  ? "bg-primary text-primary-foreground"
                  : "text-muted-foreground hover:text-foreground hover:bg-muted"
              }`}
            >
              {category.label}
            </Button>
          ))}
        </div>

        {/* News Grid */}
        <div className="max-w-6xl mx-auto">
          {isLoading ? (
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {Array.from({ length: 6 }).map((_, i) => (
                <Card key={i} className="glass-card border-0 animate-pulse">
                  <CardContent className="p-6">
                    <div className="space-y-4">
                      <div className="h-4 bg-muted rounded w-3/4"></div>
                      <div className="h-4 bg-muted rounded w-1/2"></div>
                      <div className="space-y-2">
                        <div className="h-3 bg-muted rounded"></div>
                        <div className="h-3 bg-muted rounded w-5/6"></div>
                        <div className="h-3 bg-muted rounded w-4/6"></div>
                      </div>
                      <div className="flex justify-between items-center">
                        <div className="h-3 bg-muted rounded w-1/4"></div>
                        <div className="h-3 bg-muted rounded w-1/3"></div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : news.length === 0 ? (
            <div className="text-center py-12">
              <div className="w-12 h-12 rounded-full bg-muted/50 flex items-center justify-center mx-auto mb-4">
                <Globe className="h-6 w-6 text-muted-foreground" />
              </div>
              <h3 className="text-lg font-medium text-foreground mb-2">No news found</h3>
              <p className="text-muted-foreground">Try selecting a different category</p>
            </div>
          ) : (
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {news.map((item, index) => (
                <Card 
                  key={index} 
                  className="glass-card border-0 hover:shadow-lg transition-all duration-300 cursor-pointer group"
                  onClick={() => window.open(item.link, '_blank')}
                >
                  <CardContent className="p-6">
                    <div className="space-y-4">
                      <h3 className="font-semibold text-foreground text-lg leading-tight group-hover:text-primary transition-colors">
                        {truncateText(item.title, 80)}
                      </h3>
                      
                      <p className="text-muted-foreground text-sm leading-relaxed">
                        {truncateText(item.snippet, 150)}
                      </p>
                      
                      <div className="flex items-center justify-between pt-4 border-t border-border/20">
                        <div className="flex items-center gap-3 text-xs text-muted-foreground">
                          <Badge variant="secondary" className="text-xs">
                            {item.source}
                          </Badge>
                          <div className="flex items-center gap-1">
                            <Calendar className="h-3 w-3" />
                            {formatDate(item.date)}
                          </div>
                        </div>
                        <ExternalLink className="h-4 w-4 text-muted-foreground group-hover:text-primary transition-colors" />
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default News;
