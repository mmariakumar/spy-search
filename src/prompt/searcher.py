def search_plan(task: str, todo: list[str], k: int = 6 , search_engine:list[str]=["google" , "arxiv" , "google_news"]) -> str:
    step_left = k - len(todo) 
    return f"""
        You are an expert planner for search tasks. Your current assignment is to search and gather information on the following topic:

        {task}


        Below is the existing todo list of tasks completed so far:

        {todo}

        You have access to the following tools:

        - **url_search**:  
        Use search engines such as Google, arXiv, Google News, etc., to find relevant URLs for further investigation.  
        *Note:* You only need to provide the search keyword, not the specific site.  
        This tool returns a list of URLs and page descriptions — it does **not** return page content.
        You are given the following search engine:
            {search_engine}

        - **page_content**:  
        Summarize the content and key information from the given pages.  
        This tool should be used **only after** performing `url_search` to obtain URLs to summarize.
        You don't need to answer search_engine for this function.

        ---

        Instructions:

        - Generate new tasks only if you believe the existing summaries in the todo list are insufficient for a thorough answer.
        - You have {step_left} remaining tasks allowed; do **not** exceed this limit.
        - Avoid using all remaining steps at once unless absolutely necessary.
        - The planning step will be invoked repeatedly as new content is added; base your next steps on the current todo list.
        - If no steps remain, do **not** perform any extra tasks — plan carefully when and what to do.
        - Prioritize executing the right tasks at the right time to maximize efficiency.
        - After search url you will not get any content, so in your plan if you want content please use other methods after calling get_url function
        
        Please respond strictly using the following JSON format:

        ```json
        [
            {{
                "tool": "<TOOL_NAME>",
                "keyword": "<SEARCH_KEYWORD>",
                "search_engine":<EXPECTED SEARCH PAGE>
                "content": "<EMPTY>"
            }}
        ]
        ```
    """