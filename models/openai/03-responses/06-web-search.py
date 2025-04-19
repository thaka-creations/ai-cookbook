from openai import OpenAI

client = OpenAI()

# --------------------------------
# Basic web search
# --------------------------------

response = client.responses.create(
    model="gpt-4.1-mini",
    tools=[{"type": "web_search_preview"}],
    input="What are the best restaurant in Ruaka?",
)

print(response.output_text)
