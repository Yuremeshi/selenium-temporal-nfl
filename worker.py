import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from workflows import ScrapingWorkflow
from activities import selenium_scraper, postgres

async def main():
    client = await Client.connect("localhost:7233")

    print("Starting worker")

    worker = Worker(
        client,
        task_queue="scraping-task-queue",
        workflows=[ScrapingWorkflow],
        activities=[selenium_scraper, postgres],
    )

    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
