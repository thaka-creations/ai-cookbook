from openai import OpenAI

client = OpenAI()

tools = [
    {
        "type": "function",
        "name": "send_email",
        "description": "Send an email to a given recipient with a subject and message.",
        "parameters": {
            "type": "object",
            "properties": {
                "to": {"type": "string", "description": "The recipient email address."},
                "subject": {"type": "string", "description": "Email subject line."},
                "body": {"type": "string", "description": "Body of the email message."},
            },
            "required": ["to", "subject", "body"],
            "additionalProperties": False,
        },
    }
]

response = client.responses.create(
    model="gpt-4.1-mini",
    tools=tools,
    tool_choice="auto",
    input="Can you send an email to thakacreations@gmail.com saying hi?",
)

print(response.output)
print(response.output[0].model_dump_json(indent=2))
