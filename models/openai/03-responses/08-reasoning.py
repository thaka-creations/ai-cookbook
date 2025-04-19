from openai import OpenAI

client = OpenAI()

# --------------------------------
# Create a reasoning tool
# --------------------------------
prompt = """
Write a bash script that takes a matrix represented as a string with 
format '[1,2],[3,4],[5,6]' and prints the transpose in the same format.
"""

response = client.responses.create(
    model="o3-mini",
    reasoning={"effort": "medium"},
    input=[{"role": "user", "content": prompt}],
)

print(response.output_text)
