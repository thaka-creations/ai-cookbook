# OpenAI API Introduction

This example demonstrates basic usage of the OpenAI API to generate text completions.

## Key Concepts

- Making requests to the OpenAI API
- Handling API responses
- Basic prompt engineering
- Error handling

## Setup

1. Install dependencies:


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
