from openai import OpenAI

client = OpenAI()

# https://platform.openai.com/docs/api-reference/responses

# ---------------------------------
# Basic text example with the chat completions API
# ---------------------------------

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {
            "role": "user",
            "content": "Write a one-sentence bedtime story about a unicorn",
        }
    ],
)

print(response.choices[0].message.content)
