from openai import OpenAI

client = OpenAI()

"""
https://platform.openai.com/docs/guides/conversation-state?api-mode=responses
"""

# ---------------------------------
# Manual conversation state
# ---------------------------------

response = client.responses.create(
    model="gpt-4.1-mini",
    input=[
        {"role": "user", "content": "knock knock"},
        {"role": "assistant", "content": "who's there?"},
        {"role": "user", "content": "orange"},
    ],
)

print(response.output_text)


# ---------------------------------
# Dynamic conversation state
# ---------------------------------

history = [{"role": "user", "content": "tell me a joke"}]
response = client.responses.create(model="gpt-4.1-mini", input=history, store=False)
print(response.output_text)

# Add the response to the conversation
history += [
    {"role": output.role, "content": output.content} for output in response.output
]

history.append({"role": "user", "content": "tell me another"})
second_response = client.responses.create(
    model="gpt-4.1-mini", input=history, store=False
)
print(second_response.output_text)

# ---------------------------------
# OpenAI APIs for conversation state (default is to store)
# ---------------------------------

response = client.responses.create(
    model="gpt-4.1-mini",
    input="Tell me a joke",
)
print(response.output_text)

second_response = client.responses.create(
    model="gpt-4.1-mini",
    previous_response_id=response.id,
    input=[{"role": "user", "content": "explain why this is funny."}],
)
print(second_response.output_text)
