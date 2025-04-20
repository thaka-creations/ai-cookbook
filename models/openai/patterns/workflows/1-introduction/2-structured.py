from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()


class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]


# ----------------------------------
# Call the model
# ----------------------------------

response = client.responses.parse(
    model="gpt-4.1-mini",
    instructions="Extract the event information",
    input=[
        {
            "role": "user",
            "content": "Alice and Bob are going to a science fair on Friday.",
        },
    ],
    text_format=CalendarEvent,
)

print(response.output_text)
print(response.model_dump_json(indent=2))
print(response.output[0].content[0].parsed)
print("name:", response.output[0].content[0].parsed.name)
print("date:", response.output[0].content[0].parsed.date)
print("participants:", response.output[0].content[0].parsed.participants)
