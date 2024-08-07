import asyncio
from temporalio.client import Client
from workflows import ScrapingWorkflow

async def start_workflow():
    client = await Client.connect("localhost:7233")

    result = await client.execute_workflow(
        ScrapingWorkflow.run,
        id="scraping-workflow-id",
        task_queue="scraping-task-queue",
    )
    print(f"Scraping result: {result}")

if __name__ == "__main__":
    asyncio.run(start_workflow())
