import json
from openai import OpenAI
from pydantic import BaseModel, Field

client = OpenAI()


# ----------------------------------
# Define the knowledge base retrieval tool
# ----------------------------------


def search_knowledge_base(query: str) -> list[dict]:
    """
    Load the whole knowledge base from the JSON file.
    (This is a mock function for demonstration purposes, we don't search)
    """
    with open("kb.json", "r") as f:
        return json.load(f)


# ----------------------------------
# Step 1: Call model with search_knowledge_base tool defined
# ----------------------------------

tools = [
    {
        "type": "function",
        "name": "search_knowledge_base",
        "description": "Get the answer to the user's question from the knowledge base.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The query to search the knowledge base with",
                }
            },
            "required": ["query"],
            "additionalProperties": False,
        },
        "strict": True,
    }
]

messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant that answers questions from the knowledge base about our e-commerce store.",
    },
    {"role": "user", "content": "What is the return policy?"},
]

response = client.responses.create(
    model="gpt-4.1-mini",
    input=messages,
    tools=tools,
)

# ----------------------------------
# Step 2: Execute the tool call
# ----------------------------------

tool_call = response.output[0]
args = json.loads(tool_call.arguments)
results = search_knowledge_base(args["query"])
print("results", results)

# ----------------------------------
# Step 3: Supply the results and call the model again
# ----------------------------------


class KBResponse(BaseModel):
    answer: str = Field(description="The answer to the user's question.")
    source: int = Field(description="The record id of the answer")


messages.append(tool_call)
messages.append(
    {
        "type": "function_call_output",
        "call_id": tool_call.call_id,
        "output": str(results),
    }
)

response_2 = client.responses.parse(
    model="gpt-4.1-mini",
    input=messages,
    tools=tools,
    text_format=KBResponse,
)

print(response_2.output_text)
