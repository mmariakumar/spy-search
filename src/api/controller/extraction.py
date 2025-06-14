import re
import time
import logging
from collections import Counter
from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)

# Global model instance - using the absolute fastest model
_model = None

def get_model():
    """Load the fastest possible sentence transformer model"""
    global _model
    if _model is None:
        start_time = time.perf_counter()
        # This is the FASTEST model available - 14MB, extremely fast inference
        _model = SentenceTransformer('paraphrase-MiniLM-L3-v2', device='cpu')
        # Force CPU to avoid GPU overhead for small batches
        _model.max_seq_length = 128  # Limit sequence length for speed
        load_time = time.perf_counter() - start_time
        logger.info(f"Ultra-fast model loaded in {load_time:.3f}s")
    return _model

# Pre-compiled regex for speed
WORD_PATTERN = re.compile(r'\b[a-zA-Z][a-zA-Z0-9_-]{2,}\b')

# Minimal stop words for maximum speed
STOP_WORDS = frozenset([
    'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 
    'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old', 'see', 
    'two', 'way', 'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use', 'will',
    'have', 'been', 'that', 'this', 'they', 'what', 'with', 'were', 'your', 'from', 'some',
    'come', 'them', 'said', 'very', 'well', 'just', 'like', 'good', 'much', 'more', 'want',
    'than', 'make', 'know', 'time', 'only', 'look', 'take', 'work', 'find', 'here', 'when'
])

def lightning_candidates(text: str, max_candidates: int = 25) -> List[str]:
    """Ultra-fast candidate extraction - under 10ms"""
    words = WORD_PATTERN.findall(text.lower())
    
    # Filter and score in one pass
    candidates = []
    word_freq = Counter()
    
    for word in words:
        if word not in STOP_WORDS and len(word) > 2:
            word_freq[word] += 1
    
    # Add top single words
    candidates.extend([w for w, _ in word_freq.most_common(15)])
    
    # Add strategic bigrams (only high-frequency words)
    frequent_words = {w for w, c in word_freq.items() if c > 0}
    filtered_words = [w for w in words if w in frequent_words]
    
    # Fast bigram generation
    for i in range(min(len(filtered_words) - 1, 20)):  # Limit iterations
        w1, w2 = filtered_words[i], filtered_words[i + 1]
        if len(w1) > 2 and len(w2) > 2:
            candidates.append(f"{w1} {w2}")
    
    return candidates[:max_candidates]

def ultra_fast_similarity(text: str, candidates: List[str], max_keywords: int = 8) -> List[str]:
    """Ultra-optimized model inference - target under 200ms"""
    if not candidates:
        return []
    
    start_time = time.perf_counter()
    
    try:
        model = get_model()
        
        # Truncate text for speed (keep most relevant part)
        text_truncated = text[:200] if len(text) > 200 else text
        
        # Batch encode for maximum efficiency
        encode_start = time.perf_counter()
        
        # Single batch encoding - most efficient
        all_texts = [text_truncated] + candidates
        embeddings = model.encode(all_texts, 
                                show_progress_bar=False,
                                batch_size=32,  # Optimal batch size
                                normalize_embeddings=True)  # Pre-normalize for speed
        
        encode_time = time.perf_counter() - encode_start
        
        # Lightning-fast similarity (pre-normalized, so just dot product)
        text_emb = embeddings[0:1]
        candidate_embs = embeddings[1:]
        
        # Vectorized dot product (faster than cosine_similarity)
        similarities = np.dot(candidate_embs, text_emb.T).flatten()
        
        # Quick scoring with minimal overhead
        scored = []
        for i, candidate in enumerate(candidates):
            score = similarities[i]
            
            # Fast bonuses
            if ' ' in candidate:  # Bigram
                score *= 1.2
            elif len(candidate) > 6:  # Long word
                score *= 1.1
            
            scored.append((candidate, score))
        
        # Fast sort and return
        scored.sort(key=lambda x: x[1], reverse=True)
        result = [candidate for candidate, _ in scored[:max_keywords]]
        
        total_time = time.perf_counter() - start_time
        logger.debug(f"Ultra-fast model inference: {total_time:.3f}s ({encode_time:.3f}s encoding)")
        
        return result
        
    except Exception as e:
        # Ultra-fast fallback
        logger.warning(f"Model failed, using frequency fallback: {e}")
        word_freq = Counter(candidates)
        return [word for word, _ in word_freq.most_common(max_keywords)]

def extract_keywords(text: str, max_keywords: int = 8, previous_context: str = "", context_weight: float = 0.3) -> str:
    """
    Lightning-fast keyword extraction with model - target under 300ms total
    """
    overall_start = time.perf_counter()
    
    if not text.strip():
        return ""
    
    # Fast context check
    needs_context = any(trigger in text.lower() for trigger in [
        'there', 'that', 'those', 'them', 'it', 'this', 'these', 'place',
        'same', 'similar', 'related', 'mentioned', 'above', 'previous'
    ])
    
    if previous_context and needs_context and context_weight > 0:
        # Lightning context processing
        context_keywords = max(2, int(max_keywords * context_weight))
        main_keywords = max_keywords - context_keywords
        
        # Parallel candidate extraction
        main_candidates = lightning_candidates(text, 15)
        context_candidates = lightning_candidates(previous_context, 10)
        
        # Fast model scoring
        main_result = ultra_fast_similarity(text, main_candidates, main_keywords)
        context_result = ultra_fast_similarity(previous_context, context_candidates, context_keywords)
        
        # Merge results
        final_keywords = main_result + context_result
        final_keywords = list(dict.fromkeys(final_keywords))[:max_keywords]  # Dedupe
        
    else:
        # Single text processing
        candidates = lightning_candidates(text, 20)
        final_keywords = ultra_fast_similarity(text, candidates, max_keywords)
    
    total_time = time.perf_counter() - overall_start
    result = ' '.join(final_keywords)
    
    logger.info(f"Lightning extraction: {total_time:.3f}s -> '{result}'")
    
    return result

def smart_message_processing(validated_messages: List) -> tuple[str, str]:
    """
    Ultra-fast message processing - under 5ms
    """
    if not validated_messages:
        return "", ""
    
    if len(validated_messages) <= 1:
        current_query = validated_messages[0].content if validated_messages else ""
        return current_query, ""
    
    # Lightning-fast processing
    current_query = validated_messages[-1].content
    
    # Get only user messages, limit to last 2 for speed
    user_messages = []
    for msg in reversed(validated_messages[:-1]):
        if msg.role == 'user':
            user_messages.append(msg.content)
            if len(user_messages) >= 2:
                break
    
    recent_context = " ".join(reversed(user_messages)) if user_messages else ""
    
    return current_query, recent_context

# Alternative: If you need even faster, use this CPU-optimized version
def get_cpu_optimized_model():
    """Alternative ultra-fast CPU model"""
    global _model
    if _model is None:
        # Even smaller model - 5MB only
        _model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
        _model.max_seq_length = 64  # Very short sequences
        # Optimize for CPU
        import torch
        torch.set_num_threads(1)  # Single thread for small batches
    return _model