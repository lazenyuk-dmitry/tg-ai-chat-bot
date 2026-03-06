import time
import asyncio
from datetime import timedelta
from aiohttp import web
from app.config import settings
from app.utils.logger import logger
from app.health.types import HealthStatus
from app.bot.service import BotService
from app.db.service import DatabaseService

class HealthServer():
    start_time = None

    def __init__(self, bot: BotService, db: DatabaseService):
        self.bot = bot
        self.db = db

        self.check_timeout = 15
        self.cache_ttl = 30
        self.cached_status = HealthStatus()
        self.last_check_time = 0

    async def async_check(self):
        self.cached_status = HealthStatus()

        try:
            async with asyncio.timeout(self.check_timeout):
                bot_task = asyncio.create_task(self.bot.is_healthy())
                db_task = asyncio.create_task(self.db.is_healthy())
                bot_healthy, db_healthy = await asyncio.gather(bot_task, db_task)
                self.cached_status.bot = bot_healthy
                self.cached_status.db = db_healthy

        except TimeoutError:
            self.cached_status.error = "Timeout Error"
        except Exception as e:
            self.cached_status.error = str(e)

    async def health_check(self, request):
        current_time = time.time()

        if (current_time - self.last_check_time) > self.cache_ttl:
            await self.async_check()
            self.last_check_time = current_time

        bot_healthy = self.cached_status.bot
        db_healthy = self.cached_status.db
        error = self.cached_status.error

        return self.send_status(bot_healthy=bot_healthy, db_healthy=db_healthy, err=error)

    def send_status(self, bot_healthy=False, db_healthy=False, err=None):
        check_list = {"bot": bot_healthy, "db": db_healthy}
        all_healthy = all(check_list.values())

        uptime_readable = str(timedelta(seconds=int(time.time() - self.start_time)))

        data = {
            "status": "ok" if all_healthy else "error",
            "uptime": uptime_readable,
            "checks": {
                key: "healthy" if is_ok else "unhealthy"
                for key, is_ok in check_list.items()
            },
            "error": str(err)
        }
        return web.json_response(data, status=200 if all_healthy else 500)

    async def setup(self) -> web.AppRunner:
        self.start_time = time.time()
        web_app = web.Application()
        web_runner = web.AppRunner(web_app)
        web_app.router.add_get("/healthy", self.health_check)
        await web_runner.setup()
        return web_runner

    async def start(self) -> None:
        port = settings.health_port
        runner = await self.setup()
        site = web.TCPSite(runner, "0.0.0.0", port)
        await site.start()
        logger.info("🚀 Health Check run on port %s", port)
