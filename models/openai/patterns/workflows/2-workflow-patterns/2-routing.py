"""
Routing is a workflow pattern where the LLM acts as a router or dispatcher,
determining which path or function should handle a given input.

Key benefits:
1. Modular design - Each handler focuses on a specific task
2. Maintainability - Easy to add/modify handlers without changing core logic
3. Flexibility - LLM can make intelligent routing decisions based on context
4. Error reduction - Specialized handlers are more reliable than one-size-fits-all

Common use cases:
- Customer support routing to appropriate department
- Content moderation with different policies per content type
- Multi-language processing with language-specific handlers
- Task delegation in automated workflows
- API endpoint routing based on natural language requests

The LLM analyzes the input and routes it to the most appropriate handler,
rather than trying to handle everything itself.
"""

import logging
from typing import Literal, Optional

from openai import OpenAI
from pydantic import BaseModel, Field

# set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

client = OpenAI()
model = "gpt-4.1-mini"


# ----------------------------------
# Step 1: Define the data models for routing and responses
# ----------------------------------
class CalendarRequestType(BaseModel):
    # Router LLM call: Detetmine the type of calendar request
    request_type: Literal["new_event", "modify_event", "other"] = Field(
        description="Type of calendar request being made"
    )
    confidence_score: float = Field(description="Confidence score between 0 and 1")
    description: str = Field(description="Cleaned description of the request")


class NewEventDetails(BaseModel):
    # Details for creating a new event
    name: str = Field(description="Name of the event")
    date: str = Field(description="Date and time of the event (ISO 8601)")
    duration_minutes: int = Field(description="Duration in minutes")
    participants: list[str] = Field(description="List of participants")


class Change(BaseModel):
    """Details for changing an existing event"""

    field: str = Field(description="Field to change")
    new_value: str = Field(description="New value for the field")


class ModifyEventDetails(BaseModel):
    """Details for modifying an existing event"""

    event_identifier: str = Field(
        description="Description to identify the existing event"
    )
    changes: list[Change] = Field(description="List of changes to make")
    participants_to_add: list[str] = Field(description="New participants to add")
    participants_to_remove: list[str] = Field(description="Participants to remove")


class CalendarResponse(BaseModel):
    """Final response format"""

    success: bool = Field(description="Whether the operation was successful")
    message: str = Field(description="User-friendly response message")
    calendar_link: Optional[str] = Field(description="Calendar link if applicable")


# ----------------------------------
# Step 2: Define the functions and the routing logic
# ----------------------------------
def route_calendar_request(user_input: str) -> CalendarRequestType:
    # Router LLM call to determine the type of calendar request
    logger.info("Routing calendar request")
    logger.debug(f"User input: {user_input}")

    response = client.responses.parse(
        model=model,
        instructions="""
        Determine if this is a request to create a new calendar event or modify an existing one.
        """,
        input=[{"role": "user", "content": user_input}],
        text_format=CalendarRequestType,
    )

    result = response.output[0].content[0].parsed
    logger.info(
        f"Request routed as: {result.request_type} with confidence: {result.confidence_score}"
    )
    return result


def handle_new_event(description: str) -> CalendarResponse:
    # Handler LLM call: Create a new event
    logger.info("Processing new event request")

    # Get event details
    response = client.responses.parse(
        model=model,
        instructions="""
        Extract details for creating a new calendar event.
        """,
        input=[{"role": "user", "content": description}],
        text_format=NewEventDetails,
    )

    result = response.output[0].content[0].parsed
    logger.info(f"New event: {result.model_dump_json(indent=2)}")

    # generate response
    return CalendarResponse(
        success=True,
        message=f"Created new event '{result.name}' for {result.date} with {', '.join(result.participants)}",
        calendar_link=f"calendar://new?event={result.name}",
    )


def handle_modify_event(description: str) -> CalendarResponse:
    # Handler LLM call: Modify an existing event
    logger.info("Processing modify event request")

    # Get modification details
    response = client.responses.parse(
        model=model,
        instructions="""
        Extract details for modifying an existing calendar event.
        """,
        input=[{"role": "user", "content": description}],
        text_format=ModifyEventDetails,
    )

    result = response.output[0].content[0].parsed
    logger.info(f"Modify event: {result.model_dump_json(indent=2)}")

    # generate response
    return CalendarResponse(
        success=True,
        message=f"Modified event '{result.event_identifier}' with the requested changes",
        calendar_link=f"calendar://modify?event={result.event_identifier}",
    )


def process_calendar_request(user_input: str) -> Optional[CalendarResponse]:
    # Main function implementing the routing and handling logic
    logger.info("Processing calendar request")
    logger.debug(f"User input: {user_input}")

    # Route the request
    route_result = route_calendar_request(user_input)

    # Check confidence threshold
    if route_result.confidence_score < 0.7:
        logger.warning(f"Low confidence score: {route_result.confidence_score}")
        return None

    # Handle the request based on the route result
    if route_result.request_type == "new_event":
        return handle_new_event(route_result.description)
    elif route_result.request_type == "modify_event":
        return handle_modify_event(route_result.description)
    else:
        logger.warning(f"Unhandled request type: {route_result.request_type}")
        return None


# ----------------------------------
# Step 3: Test the workflow with new event
# ----------------------------------
new_event_input = "Let's schedule a team meeting next Tuesday at 2pm with Alice and Bob"
result = process_calendar_request(new_event_input)
if result:
    print(f"Response: {result.message}")


# --------------------------------------------------------------
# Step 4: Test with modify event
# --------------------------------------------------------------

modify_event_input = (
    "Can you move the team meeting with Alice and Bob to Wednesday at 3pm instead?"
)
result = process_calendar_request(modify_event_input)
if result:
    print(f"Response: {result.message}")


# --------------------------------------------------------------
# Step 5: Test with invalid request
# --------------------------------------------------------------

invalid_input = "What's the weather like today?"
result = process_calendar_request(invalid_input)
if not result:
    print("Request not recognized as a calendar operation")
