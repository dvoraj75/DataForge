from apscheduler.schedulers.asyncio import AsyncIOScheduler


class DataForgeScheduler(AsyncIOScheduler):
    @classmethod
    def init_scheduler(cls) -> "DataForgeScheduler":
        return cls()
