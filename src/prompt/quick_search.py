import datetime

def quick_search_prompt(query, data):
    return f"""
# Search Result Summary
**Timestamp:** {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## User Query
> {query}

---

## Browser-Simulated Response

Based on the content retrieved, here is the concise and relevant information related to your query:

{data}

---

## Instructions for Response

1. **Act as a Browser**: Provide a direct, clear summary or answer as if presenting a webpage snippet or search preview.
2. **Relevance is Key**: Use only relevant information from the retrieved content to answer the query.
3. **Professional & Concise**: Write in a clear, professional tone with no unnecessary filler.
4. **Use APA-style Inline Citations**, formatted as clickable Markdown links:
   - Correct: (Author, Year) [Source Title](https://example.com)
5. **Formatting**:
   - Use Markdown headers (#, ##) for structure.
   - Use lists or tables only if they improve clarity.
6. **Length Guidance**:
   - Keep answers brief for trivial/simple queries (~50-400 words).
   - Expand only if the query demands complex explanation (~400-600 words).
7. **Output Style**:
   - Summarize first.
   - Then provide more detailed information if needed.
   - Maintain a professional, user-friendly tone throughout.

---

**Example Output**:

# Example Domain Summary

This domain is intended for use in illustrative examples within documents. You may use it freely without prior permission or coordination (Example Domain, n.d.) [Example Domain](https://example.com).

---

Your final response should simulate what a user would see if they searched the query and browsed to the page — concise, relevant, and informative.
"""