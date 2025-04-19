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

# --------------------------------
# Basic web search with location
# --------------------------------

response = client.responses.create(
    model="gpt-4.1-mini",
    tools=[
        {
            "type": "web_search_preview",
            "user_location": {
                "type": "approximate",
                "country": "KE",
                "city": "Nairobi",
            },
        }
    ],
    input="What are the best restaurant in Ruaka?",
)

print(response.output_text)
response.output[1].content[0].annotations
response.output[1].content[0].annotations[0].url
