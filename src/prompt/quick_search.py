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

        - Evaluate the relevance of the provided data to the question. If the data is not relevant, you may disregard it.
        - If the data is useful, please integrate it thoughtfully into your response.
        - Include APA-style citations with URLs for any referenced information.
        - Write your response in a clear, professional, and well-structured manner.
        - The response should be approximately 500 words.
        - Use Markdown formatting with:
        - `#` for main titles
        - `##` for subtitles
        - Appropriate headings for other sections as needed
        - You must include the inline reference with APA format. 
        - Just include relevant content ! Don't include anything irrelvant ! 

        Please ensure your response is informative, concise, and easy to read.
    """