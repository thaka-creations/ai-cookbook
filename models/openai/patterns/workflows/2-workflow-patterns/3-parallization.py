"""
Parallelization is a workflow pattern where multiple LLM calls are executed
concurrently rather than sequentially to improve performance.

Key benefits:
1. Reduced latency - Multiple operations execute simultaneously
2. Better resource utilization - Parallel processing of independent tasks
3. Improved scalability - Can handle more requests in same time window
4. Cost effective - Faster total processing time for batch operations

Common use cases:
- Batch processing multiple documents
- Concurrent analysis of different aspects of same input
- Parallel validation of multiple fields
- Simultaneous translation to multiple languages
- Processing multiple user requests

The pattern works best when tasks are independent and don't require
sequential dependencies. Care must be taken to handle rate limits
and manage computational resources.
"""

import asyncio
import logging
from typing import List, Optional
from datetime import datetime

from openai import OpenAI
from pydantic import BaseModel, Field

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

client = OpenAI()
model = "gpt-4.1-mini"


# ----------------------------------
# Step 1: Define the data models for parallel processing
# ----------------------------------


class DocumentAnalysis(BaseModel):
    # Analysis results for a single document
    document_id: str = Field(description="Unique identifier for the document")
    sentiment_score: float = Field(description="Sentiment score from -1 to 1")
    key_topics: List[str] = Field(description="Main topics identified")
    summary: str = Field(description="Brief summary of the document")
    language: str = Field(description="Detected language of the document")


class BatchAnalysisResult(BaseModel):
    # Combined results from parallel document analysis
    total_documents: int = Field(description="Total number of documents processed")
    average_sentiment: float = Field(
        description="Average sentiment across all documents"
    )
    common_topics: List[str] = Field(
        description="Topics appearing in multiple documents"
    )
    analysis_duration_ms: int = Field(
        description="Total processing time in milliseconds"
    )
    results: List[DocumentAnalysis] = Field(description="Individual document results")


# ----------------------------------
# Step 2: Define the parallel processing functions
# ----------------------------------


async def analyze_document(document_id: str, text: str) -> DocumentAnalysis:
    """Analyze a single document asynchronously"""
    logger.info(f"Analyzing document {document_id}")

    # Simulate processing time
    await asyncio.sleep(random.uniform(0.5, 1.5))

    # Generate random results
    sentiment_score = random.uniform(-1, 1)
    key_topics = random.sample(
        ["AI", "Machine Learning", "Data Science", "Blockchain", "Quantum Computing"],
        random.randint(1, 3),
    )

    summary = f"This document discusses {', '.join(key_topics)} and has a sentiment score of {sentiment_score:.2f}"

    return DocumentAnalysis(
        document_id=document_id,
        sentiment_score=sentiment_score,
        key_topics=key_topics,
        summary=summary,
        language="en",
    )


async def analyze_batch(documents: List[str]) -> BatchAnalysisResult:
    """Analyze a batch of documents in parallel"""
    start_time = datetime.now()
    logger.info(f"Starting batch analysis of {len(documents)} documents")

    # Create a list of tasks to run in parallel
    tasks = [analyze_document(str(i), doc) for i, doc in enumerate(documents)]

    # Run all tasks concurrently
    results = await asyncio.gather(*tasks)

    # Combine results into a single response
    total_documents = len(results)
    average_sentiment = (
        sum(result.sentiment_score for result in results) / total_documents
    )
    common_topics = set.intersection(*[set(result.key_topics) for result in results])

    # Calculate total processing time
    analysis_duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)

    return BatchAnalysisResult(
        total_documents=total_documents,
        average_sentiment=average_sentiment,
        common_topics=list(common_topics),
        analysis_duration_ms=analysis_duration_ms,
        results=results,
    )


# ----------------------------------
# Step 3: Test the parallel processing workflow
# ----------------------------------


async def main():
    # Generate sample documents
    documents = [
        "The latest trends in AI and machine learning",
        "Blockchain technology: Past, present, and future",
        "Quantum computing: A beginner's guide",
        "Data science in healthcare: Insights from recent studies",
        "The impact of AI on modern society",
    ]

    # Run the parallel analysis
    result = await analyze_batch(documents)

    # Print the results
    logger.info(f"Batch analysis completed in {result.analysis_duration_ms}ms")
    logger.info(f"Total documents processed: {result.total_documents}")
    logger.info(f"Average sentiment: {result.average_sentiment:.2f}")
    logger.info(f"Common topics: {', '.join(result.common_topics)}")

    # Print individual document results
    for doc in result.results:
        logger.info(f"Document {doc.document_id}:")
        logger.info(f"  Sentiment: {doc.sentiment_score:.2f}")
        logger.info(f"  Topics: {', '.join(doc.key_topics)}")
        logger.info(f"  Summary: {doc.summary}")


if __name__ == "__main__":
    import random
    import nest_asyncio

    nest_asyncio.apply()
    asyncio.run(main())
