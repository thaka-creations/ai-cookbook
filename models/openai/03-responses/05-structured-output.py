import json
from openai import OpenAI
from typing import List
from pydantic import BaseModel

client = OpenAI()

# --------------------------------
# Using a JSON Schema
# --------------------------------


response = client.responses.create(
    model="gpt-4.1-mini",
    input=[
        {"role": "system", "content": "Extract the event information."},
        {
            "role": "user",
            "content": "Alice and Bob are going to a science fair on Friday.",
        },
    ],
    text={
        "format": {
            "type": "json_schema",
            "name": "calendar_event",
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "date": {"type": "string"},
                    "participants": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["name", "date", "participants"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
)

event = json.loads(response.output_text)
print(event)


class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: List[str]


response = client.responses.parse(
    model="gpt-4.1-mini",
    input="Alice and Bob are going to a science fair on Friday",
    instructions="Extract the event information",
    text_format=CalendarEvent,
)

response_model = response.output[0].content[0].parsed
print(response_model)
print(response_model.model_dump_json(indent=2))
