# OpenAI API Introduction

This example demonstrates basic usage of the OpenAI API to generate text completions and chat conversations.

## Key Concepts

- Making requests to the OpenAI API
- Handling API responses and errors
- Effective prompt engineering
- Working with different message types
- Managing conversation context

## Create chat completion
Create a model response for the given chat conversation. Can be text generation, vision and audio

### Request Body
#### Messages
A list of messages comprising the conversation so far. Depending on the model you use, different message types (modalities) are supported, like text, images and audio

##### **Developer** message
Developer-provided instructions that the model should follow, regardless of messages sent by the user. With o1 models and newer, **developer** messages replace the previous **system** messages.

The message contains:
- Content: The actual instructions or guidance for the model
- Role: Set as "developer" to identify this as a developer message
- Name (optional): A unique identifier to distinguish between different participants with the same role

##### **System** message
Same as developer message above

##### **User** message
Messages sent by an end user, containing prompts or additional context information

The message contains:
- Content: The actual instructions or guidance for the model
- Role: The role of the messages author, in this case **user**
- Name (optional): A unique identifier to distinguish between different participants with the same role

##### **Assistant message** message
Messages sent by the model in response to user messages

The message contains:
- Content: The model's response to the user's message
- Role: The role of the message's author, in this case **assistant**
- Name (optional): A unique identifier to distinguish between different participants with the same role
- Function call (optional): Details about a function call made by the model. Deprecated and replaced by **tool_calls**
- Tool calls (optional): Details about tool calls made by the model
- Audio (optional): Data about a previous audio response from the model
- Refusal: The refusal message by the assistant

#### Model <span style="color: red">(Required)</span>

## Streaming
Stream partial progress of model responses as they are generated. This allows for:
- Real-time display of responses
- Faster perceived response time
- Lower memory usage for long responses

See [02-streaming.py](02-streaming.py) for an example of streaming chat completions.
