from openai import OpenAI

client = OpenAI()

"""
Model spec: https://model-spec.openai.com/2025-02-12.html
Dashboard: https://platform.openai.com/logs?api=responses
"""

# ---------------------------------
# Introduction instructions
# ---------------------------------

"""
Inputs can now be a single string or a list of messages.
The list of roles can now be:
- system
- developer
- user
- assistant
"""

response = client.responses.create(
    model="gpt-4.1-mini",
    instructions="Talk like a pirate",
    input="Are semicolons optional in Javascript?",
)
print(response.output_text)


# ---------------------------------
# The chain of command (hierarchical instructions)
# ---------------------------------

response = client.responses.create(
    model="gpt-4.1-mini",
    input=[
        {"role": "system", "content": "Talk like a pirate."},
        {"role": "developer", "content": "don't talk like a pirate."},
        {"role": "user", "content": "Are semicolons optional in Javascript?"},
    ],
)
print(response.output_text)

response = client.responses.create(
    model="gpt-4.1-mini",
    input=[
        {"role": "system", "content": "Don't talk like a pirate."},
        {"role": "developer", "content": "Talk like a pirate."},
        {"role": "user", "content": "Are semicolons optional in Javascript?"},
    ],
)
print(response.output_text)
