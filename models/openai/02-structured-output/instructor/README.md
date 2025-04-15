# Structured Output in LLM Applications
-----------------------------------
When working with the OpenAI API directly, you have two main options for obtaining structured output responses from GPT models. JSON mode and function calling. While both are powerful tools, they also have their limitations.
Understanding when to use each can enhance your workflow and give you more control over the output. 
After learning about these two methods, we'll dive into ["Instructor"]("https://github.com/daveebbelaar/openai-python-tutorial/tree/main/04%20Structured%20Output/Instructor") to gain even greater control over the output from OpenAI's models.
Instructor was covered in the great ["Pydantic is all you need"]("https://www.youtube.com/watch?v=yj-wSRJwrrc") talk by Jason Liu.


## Why Use JSON Output?
-----------------------
Using JSON output in your LLM applications provides more control and validation over the generated responses. It ensures that the output is always a valid JSON string, making it easier to parse and process the data in your application

## JSON Mode
------------
In **__JSON mode__**, the model generates outputs exclusively as valid JSON strings. However, you need to explicitly specify the desired JSON structure within the system prompt to guide the model towards the expected format.

Here's an example of using JSON mode:
```
query = "Hi there, I have a question about my bull. Can you help me?"

messages = [
    {
        "role": "system",
        "content": """
        You're a helpful customer care assistant that can classify incoming messages and create a response.
        Always response in the following JSON format: {"content" <response>, "category": <classification>}
        Available categories: 'general', 'order', 'billing'
        """,
    },
    {"role": "user", "content": query},
]

response = client.chat.completions.create(
    model="gpt-4.1",
    messages=messages,
    response_format={"type": "json_object"},
)

message = response.choices[0].message.content
type(message)

message_dict = json.loads(message)
type(message_dict)```

