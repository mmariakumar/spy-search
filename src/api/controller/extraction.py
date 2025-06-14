import re
from collections import Counter
from typing import List

def extract_keywords(text: str, max_keywords: int = 8, previous_context: str = "", context_weight: float = 0.3) -> str:
    """
    Ultra-fast keyword extraction with smart context weighting
    Prioritizes recent queries while maintaining context awareness
    """
    
    # Pre-compiled regex for maximum speed
    word_pattern = re.compile(r'\b[a-zA-Z][a-zA-Z0-9_-]{2,}\b')
    
    # Minimal stop words set for speed
    stop_words = frozenset([
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of',
        'with', 'by', 'from', 'about', 'into', 'through', 'during', 'before',
        'after', 'above', 'below', 'can', 'could', 'should', 'would', 'will',
        'have', 'has', 'had', 'be', 'been', 'being', 'am', 'are', 'was', 'were',
        'do', 'does', 'did', 'get', 'got', 'give', 'take', 'make', 'come', 'go',
        'see', 'know', 'think', 'say', 'tell', 'ask', 'work', 'try', 'use',
        'find', 'help', 'show', 'play', 'move', 'live', 'feel', 'seem', 'hear',
        'what', 'how', 'when', 'where', 'why', 'who', 'which', 'that', 'this',
        'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me',
        'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our',
        'their', 'like', 'just', 'want', 'need', 'very', 'much', 'many', 'more',
        'most', 'some', 'any', 'all', 'so', 'than', 'too', 'way', 'well', 'good',
        'new', 'old', 'long', 'right', 'big', 'small', 'large', 'great', 'high',
        'low', 'own', 'same', 'different', 'every', 'each', 'other', 'another',
        'such', 'only', 'first', 'last', 'next', 'few', 'little', 'much', 'many',
        'there', 'here', 'then', 'now', 'today', 'yesterday', 'tomorrow'
    ])
    
    # High-value domain terms
    boosters = frozenset([
        'api', 'app', 'car', 'health', 'doctor', 'bank', 'money', 'house', 'school',
        'job', 'travel', 'food', 'movie', 'game', 'phone', 'computer', 'software',
        'business', 'service', 'price', 'buy', 'sell', 'search', 'website', 'online',
        'digital', 'tech', 'data', 'system', 'network', 'security', 'finance',
        'legal', 'medical', 'education', 'news', 'social', 'media', 'market',
        'company', 'product', 'review', 'guide', 'tips', 'best', 'top', 'how',
        'tutorial', 'solution', 'problem', 'issue', 'fix', 'repair', 'install',
        'setup', 'config', 'update', 'upgrade', 'download', 'free', 'premium',
        'restaurant', 'hotel', 'flight', 'booking', 'recipe', 'ingredients',
        'streaming', 'video', 'music', 'podcast', 'course', 'training'
    ])
    
    # Context reference words that should pull from previous context
    context_triggers = frozenset([
        'there', 'that', 'those', 'them', 'it', 'this', 'these', 'place', 'location',
        'same', 'similar', 'related', 'mentioned', 'above', 'previous', 'earlier'
    ])
    
    word_scores = Counter()
    
    # Process main text with HIGH priority (weight 4-6x)
    text_lower = text.lower()
    words = word_pattern.findall(text_lower)
    
    # Check if we need context (contains reference words)
    needs_context = any(trigger in text_lower for trigger in context_triggers)
    
    for word in words:
        if word not in stop_words:
            # PRIMARY QUERY gets maximum weight
            score = 4  # Base score for current query
            if word in boosters:
                score = 6  # High boost for current query boosters
            elif len(word) > 6:
                score = 5  # Length bonus for current query
            word_scores[word] += score
    
    # Process context with LOWER priority only if needed
    if previous_context and needs_context and context_weight > 0:
        context_lower = previous_context.lower()
        context_words = word_pattern.findall(context_lower)
        
        for word in context_words:
            if word not in stop_words:
                # CONTEXT gets much lower weight
                score = max(1, int(context_weight * 2))  # Much lower base score
                if word in boosters:
                    score = max(2, int(context_weight * 3))  # Lower boost
                elif len(word) > 6:
                    score = max(1, int(context_weight * 2))  # Lower length bonus
                word_scores[word] += score
    
    # Extract bigrams ONLY from main text for speed and relevance
    if len(word_scores) < max_keywords * 2:
        for i in range(len(words) - 1):
            w1, w2 = words[i], words[i + 1]
            if (w1 not in stop_words and w2 not in stop_words and 
                len(w1) > 2 and len(w2) > 2):
                bigram = f"{w1} {w2}"
                score = 5  # High score for current query bigrams
                if w1 in boosters or w2 in boosters:
                    score = 7  # Maximum score for boosted bigrams
                word_scores[bigram] += score
    
    # Get top keywords - current query terms will dominate due to higher scores
    top_terms = [word for word, count in word_scores.most_common(max_keywords)]
    
    return ' '.join(top_terms)


def smart_message_processing(validated_messages: List) -> tuple[str, str]:
    """
    Ultra-fast message processing that prioritizes recent context
    Returns: (current_query, relevant_context)
    """
    if len(validated_messages) <= 1:
        current_query = validated_messages[0].content if validated_messages else ""
        return current_query, ""
    
    # Get current query (most recent)
    current_query = validated_messages[-1].content
    
    # Get only last 2-3 user messages for context (not all history)
    user_messages = [msg.content for msg in validated_messages[:-1] if msg.role == 'user']
    
    # Only use last 2 messages as context for speed and relevance
    recent_context = " ".join(user_messages[-2:]) if user_messages else ""
    
    return current_query, recent_context
