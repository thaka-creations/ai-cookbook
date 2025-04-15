import json

from openai import OpenAI

client = OpenAI()


def send_reply(message: str):
    print(f"Sending reply: {message}")


# --------------------------------
# Structured output example using function calling
# --------------------------------

query = "Hi there, I have a question about my bill. Can you help me?"

function_name = "chat"

tools = [
    {
        "type": "function",
        "function": {
            "name": function_name,
            "description": "Function to respond to a customer query",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "Your reply that we send to the customer",
                    },
                    "category": {
                        "type": "string",
                        "enum": ["general", "order", "billing"],
                        "description": "Category of the ticket",
                    },
                },
                "required": ["content", "category"],
            },
        },
    }
]

messages = [
    {
        "role": "system",
        "content": """
        You're a helpful customer care assistant that can classify incoming messages and create a response.
        """,
    },
    {"role": "user", "content": query},
]


response = client.chat.completions.create(
    model="gpt-4.1",
    messages=messages,
    tools=tools,
    tool_choice={"type": "function", "function": {"name": function_name}},
)

tool_call = response.choices[0].message.tool_calls[0]
type(tool_call)

function_args = json.loads(tool_call.function.arguments)
type(function_args)

print(function_args["category"])
send_reply(function_args["content"])

# --------------------------------
# Chaning the schema, resulting in an error
# --------------------------------
