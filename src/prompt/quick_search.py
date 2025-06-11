import datetime

def quick_search_prompt(query, data):
    return f"""
        Today is {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.

        # Task Overview

        You have been presented with the following question:
        > {query}

        # Reference Material

        Below is a list of the most recent and relevant information available:
        {data}

        # Instructions

        1. Evaluate the relevance of the provided data to the question. If the data is not relevant, you may disregard it.
        2. If the data is useful, please integrate it thoughtfully into your response.
        3. When citing sources, use APA-style citations *and* format each citation as a clickable Markdown link. For example:
           - Correct format: (Author, Year) [Title](URL)
           - Do NOT use plain URLs or parentheses without links.
        4. Use Markdown links to wrap citations so users can click the link and reach the web source directly.
        5. Write your response in a clear, professional, and well-structured manner.
        6. The response should be approximately 500 words.
        7. Use Markdown formatting with:
            # for main titles
            ## for subtitles
        8. Use appropriate headings for other sections as needed.
        9. You must include inline citations in APA format with clickable Markdown URLs.
        10. Include only relevant content; exclude anything irrelevant.

        Please ensure your response is informative, concise, and easy to read.
    """