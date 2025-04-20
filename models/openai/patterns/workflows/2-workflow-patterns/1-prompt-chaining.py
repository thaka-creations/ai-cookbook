import logging
from datetime import datetime
from typing import Optional

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
# Step 1: Define the data models for each stage
# ----------------------------------


class EventExtraction(BaseModel):
    # First LLM call: Extract basic event information
    description: str = Field(description="Raw description of the event")
    is_calendar_event: bool = Field(
        description="Whether this text describes a calendar event"
    )
    confidence_score: float = Field(description="Confidence score between 0 and 1")


class EventDetails(BaseModel):
    # Second LLM call: Extract detailed event information
    name: str = Field(description="Name of the event")
    date: str = Field(
        description="Date and time of the event. Use ISO 8601 to format this value."
    )
    duration_minutes: int = Field(description="Expected duration in minutes")
    participants: list[str] = Field(description="List of participants")


class EventConfirmation(BaseModel):
    # Third LLM call: Confirm event details
    confirmation_message: str = Field(
        description="Natural language confirmation message"
    )
    calendar_link: Optional[str] = Field(
        description="Generated calendar link if applicable"
    )


# ----------------------------------
# Step 2: Define the functions
# ----------------------------------


def extract_event_info(user_input: str) -> EventExtraction:
    # First LLM call to determine if input is a calendar event
    logger.info("Starting event extration analysis")
    logger.debug(f"Input text: {user_input}")

    today = datetime.now()
    date_context = f"Today is {today.strftime('%A, %B %d, %Y')}."

    response = client.responses.parse(
        model=model,
        instructions=f"{date_context} Analyze if the text describes a calendar event.",
        input=[
            {
                "role": "user",
                "content": user_input,
            }
        ],
        text_format=EventExtraction,
    )

    result = response.output[0].content[0].parsed
    logger.info(
        f"Extraction complete - Is calendar event: {result.is_calendar_event}, Confidence: {result.confidence_score:.2f}"
    )
    return result


def parse_event_details(description: str) -> EventDetails:
    # Second LLM call to extract detailed event information
    logger.info("Starting event details extraction")

    today = datetime.now()
    date_context = f"Today is {today.strftime('%A, %B %d, %Y')}."

    response = client.responses.parse(
        model=model,
        instructions=f"{date_context} Extract detailed event information. When dates reference 'next Tuesday' or similar relative dates, use this current date as reference.",
        input=[
            {
                "role": "user",
                "content": description,
            }
        ],
        text_format=EventDetails,
    )

    result = response.output[0].content[0].parsed
    logger.info(
        f"Parsed event details - Name: {result.name}, Date: {result.date}, Duration: {result.duration_minutes}min"
    )
    logger.debug(f"Participants: {', '.join(result.participants)}")
    return result


def generate_confirmation(event_details: EventDetails) -> EventConfirmation:
    # Third LLM call to generate confirmation message
    logger.info("Generating confirmation message")

    response = client.responses.parse(
        model=model,
        instructions="Generate a natural confirmation message for the event. Sign of with your name; Susie",
        input=[
            {
                "role": "user",
                "content": str(event_details.model_dump()),
            }
        ],
        text_format=EventConfirmation,
    )

    result = response.output[0].content[0].parsed
    logger.info("Confirmation message generated successfully")
    return result


# ----------------------------------
# Step 3: Chain the functions together
# ----------------------------------


def process_calendar_request(user_input: str) -> Optional[EventConfirmation]:
    # Main function implementing the prompt chain with gate check
    # logger.info("Processing calendar request")
    # logger.debug(f"User input: {user_input}")

    # First LLM call: Extract basic info
    initial_extraction = extract_event_info(user_input)

    # Gate check: verify if it's a calendar event with sufficient confidence
    if (not initial_extraction.is_calendar_event) or (
        initial_extraction.confidence_score < 0.7
    ):
        logger.warning(
            f"Gate check failed - is_calendar_event: {initial_extraction.is_calendar_event}, confidence: {initial_extraction.confidence_score:.2f}"
        )
        return None

    logger.info("Gate check passed, proceeding with event processing")

    # Second LLM call: Get detailed event info
    event_details = parse_event_details(initial_extraction.description)

    # Third LLM call: Get detailed event information
    confirmation = generate_confirmation(event_details)

    logger.info("Calendar request processing completed successfully")
    return confirmation


# ----------------------------------
# Step 4: Test the workflow
# ----------------------------------

if __name__ == "__main__":
    # Test with a sample user input
    user_input = "Let's schedule a 1h team meeting next Tuesday at 2pm with Alice and Bob to discuss the project roadmap."
    result = process_calendar_request(user_input)
    if result:
        print(f"Confirmation: {result.confirmation_message}")
        if result.calendar_link:
            print(f"Calendar link: {result.calendar_link}")
    else:
        print("This doesn't appear to be a calendar event request.")
