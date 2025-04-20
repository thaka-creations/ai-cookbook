"""
Orchestration is a workflow pattern where a central LLM coordinates multiple
specialized LLMs or components to accomplish complex tasks.

Key benefits:
1. Task decomposition - Break complex problems into manageable subtasks
2. Specialized handling - Each component focuses on specific aspects
3. Dynamic coordination - Adapt workflow based on intermediate results
4. Quality control - Validate and refine results at each step
5. Resource optimization - Only invoke needed components

Common use cases:
- Multi-step content generation
- Complex data analysis pipelines
- Automated research workflows
- Multi-agent conversations
- Document processing pipelines

The orchestrator LLM acts as a conductor, determining the sequence of
operations and coordinating the flow of information between components.
"""

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
# Step 1: Define the data models for orchestration
# ----------------------------------


class Task(BaseModel):
    """Individual task in the workflow"""

    task_id: str = Field(description="Unique identifier for the task")
    description: str = Field(description="Description of what needs to be done")
    dependencies: List[str] = Field(description="IDs of tasks that must complete first")
    status: str = Field(description="Current status of the task")
    result: Optional[str] = Field(description="Output from the task if completed")


class WorkflowPlan(BaseModel):
    """Overall plan for executing the workflow"""

    workflow_id: str = Field(description="Unique identifier for the workflow")
    tasks: List[Task] = Field(description="List of tasks to be executed")
    current_stage: str = Field(description="Current stage of workflow execution")
    start_time: datetime = Field(description="When the workflow started")
    completion_time: Optional[datetime] = Field(
        description="When the workflow finished"
    )


class WorkflowResult(BaseModel):
    """Final results from the workflow"""

    workflow_id: str = Field(description="ID of the completed workflow")
    success: bool = Field(description="Whether the workflow completed successfully")
    results: dict = Field(description="Combined results from all tasks")
    execution_time_ms: int = Field(description="Total execution time in milliseconds")
    error_message: Optional[str] = Field(description="Error message if workflow failed")


# ----------------------------------
# Step 2: Define the orchestration functions
# ----------------------------------


def create_workflow_plan(objective: str) -> WorkflowPlan:
    """Have the orchestrator LLM break down the objective into tasks"""
    logger.info(f"Creating workflow plan for: {objective}")

    response = client.responses.parse(
        model=model,
        instructions="""
        Break down this objective into a series of discrete tasks.
        Identify dependencies between tasks and create a workflow plan.
        """,
        input=[{"role": "user", "content": objective}],
        text_format=WorkflowPlan,
    )

    plan = response.output[0].content[0].parsed
    logger.info(f"Created workflow plan with {len(plan.tasks)} tasks")
    return plan


def execute_task(task: Task) -> str:
    """Execute a single task in the workflow"""
    logger.info(f"Executing task: {task.task_id}")

    # Simulate task execution with appropriate LLM call
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Execute the following task:"},
            {"role": "user", "content": task.description},
        ],
    )

    result = response.choices[0].message.content
    logger.info(f"Task {task.task_id} completed")
    return result


def orchestrate_workflow(objective: str) -> WorkflowResult:
    """Main orchestration function"""
    start_time = datetime.now()
    logger.info("Starting workflow orchestration")

    try:
        # Create the workflow plan
        plan = create_workflow_plan(objective)
        results = {}

        # Execute tasks in dependency order
        while not all(task.status == "completed" for task in plan.tasks):
            for task in plan.tasks:
                if task.status != "completed":
                    # Check if dependencies are met
                    deps_completed = all(dep in results for dep in task.dependencies)

                    if deps_completed:
                        task.result = execute_task(task)
                        results[task.task_id] = task.result
                        task.status = "completed"

        # Calculate execution time
        execution_time = int((datetime.now() - start_time).total_seconds() * 1000)

        return WorkflowResult(
            workflow_id=plan.workflow_id,
            success=True,
            results=results,
            execution_time_ms=execution_time,
            error_message=None,
        )

    except Exception as e:
        logger.error(f"Workflow failed: {str(e)}")
        return WorkflowResult(
            workflow_id="failed",
            success=False,
            results={},
            execution_time_ms=0,
            error_message=str(e),
        )


# ----------------------------------
# Step 3: Test the orchestration workflow
# ----------------------------------


def main():
    # Test with a complex objective
    objective = """
    Analyze a technical article, extract the key points, generate a summary,
    and create social media posts to share the insights.
    """

    result = orchestrate_workflow(objective)

    if result.success:
        logger.info(f"Workflow completed in {result.execution_time_ms}ms")
        for task_id, task_result in result.results.items():
            logger.info(f"Task {task_id} result: {task_result[:100]}...")
    else:
        logger.error(f"Workflow failed: {result.error_message}")


if __name__ == "__main__":
    main()
