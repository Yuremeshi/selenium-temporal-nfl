from datetime import timedelta
from temporalio import workflow

@workflow.defn
class ScrapingWorkflow:
    @workflow.run
    async def run(self) -> str:
        await workflow.execute_activity(
            "selenium_scraper",
            start_to_close_timeout=timedelta(minutes=10),
        )

        await workflow.execute_activity(
            "postgres",
            start_to_close_timeout=timedelta(minutes=10),
        )
        return 'Stats scraped'
