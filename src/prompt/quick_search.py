import datetime
def quick_search_prompt(query, data):
    return f"""
        Today is {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.

        You have been given the following question:
        {query}

        Below is a list of the latest relevant information:
        {data}

        If you determine that the provided data is not relevant to the question, you may disregard it. However, if the data is useful, please incorporate it into your response, including an APA-style citation with the linked URL.

        Please write your response in a clear, professional, and well-structured manner.
    """