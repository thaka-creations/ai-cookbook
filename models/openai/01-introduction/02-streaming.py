# This code demonstrates streaming chat completions from the OpenAI API
# We create a streaming chat completion request with:
# - The GPT-4 model
# - A simple user message
# - stream=True to enable streaming
# The response comes back in chunks that we can process one at a time

from openai import OpenAI

client = OpenAI()

stream = client.chat.completions.create(
    model="gpt-4.1",
    messages=[{"role": "user", "content": "Hello, how are you?"}],
    stream=True,
)

for chunk in stream:
    # If the chunk has content, print it
    # The content is a delta, which means it's a change to the previous content
    # So we need to accumulate the content as we get the chunks
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
