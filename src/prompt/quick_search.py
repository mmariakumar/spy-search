import datetime


def quick_search_prompt(query, data):
    return f"""
    ## Timestamp
    {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

    ## Task

    Respond to the following question:
    > {query}

    ## Reference Material

    The following information has been retrieved for your use:
    {data}

    ## Instructions

    1. **Assess Relevance**: Review the reference material and disregard any irrelevant data.
    2. **Integrate Thoughtfully**: Use only relevant and accurate data to support your response.
    3. **Use APA-style Inline Citations**:
       - Format citations as clickable Markdown links inside parentheses.
       - Correct: (Author, 20xx) [Source Title](https://example.com)
       - Incorrect: [(Author, 20xx) Source Title][https://example.com]
    4. **Formatting Requirements**:
       - Use `#` for the main title
       - Use `##` for section headings
       - Apply standard Markdown for clarity (lists, bold, etc.)
    5. **Be Concise and Professional**:
       - Avoid unnecessary filler or unrelated content.
       - Present information clearly and with a professional tone.
    6. **Use Tables If Appropriate**: Include tables only when they enhance clarity or comprehension.
    7. **Length Guidelines**:
       - Trivial questions: ~50-100 words
       - Simple questions: ~200-400 words
       - Complex questions: ~400-600 words
    8. **Steps for complex**
       - Summary with links 
       - More deatils infomation 
       - write like professional

    Ensure the final response is informative, well-structured, and easy to read.
    """
