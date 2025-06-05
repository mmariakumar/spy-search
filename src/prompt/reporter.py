def report_prompt(query, data):
    return f"""
    You are provided with the following dataset:

    {data}

    Please carefully analyze the data and answer the following query if the data is relevant:

    Query: {query}

    Requirements:
    - Provide a clear, detailed, and high-quality response.
    - Always include citations referencing the relevant parts of the data.
    - If the data is insufficient or irrelevant to answer the query, state so explicitly.
    - Use professional and precise language.

    Generate the response accordingly.
"""