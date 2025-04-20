import requests
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()


# ----------------------------------
# Define the tool (function) that we want to call
# ----------------------------------


def get_weather(latitude, longitude):
    """This is a publically available API that returns the weather for a given location."""
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    )
    data = response.json()
    print("data", data)
    return data["current"]


# ----------------------------------
# Call the model
# ----------------------------------


tools = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "Get the weather for a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "latitude": {"type": "number"},
                "longitude": {"type": "number"},
            },
            "required": ["latitude", "longitude"],
            "additionalProperties": False,
        },
        "strict": True,
    }
]

messages = [
    {"role": "system", "content": "You are a helpful weather assistant."},
    {"role": "user", "content": "What's the weather like in Ruiru today?"},
]

response = client.responses.create(
    model="gpt-4.1-mini",
    input=messages,
    tools=tools,
)

print(response.output_text)
print(response.model_dump_json(indent=2))
