import time
from datetime import timedelta
from aiohttp import web
from app.config import settings
from app.utils.logger import logger
from app.bot.service import BotService

class HealthServer():
    start_time = None

    def __init__(self, bot: BotService):
        self.bot = bot

    async def health_check(self, request):
        bot_healthy = await self.bot.is_healthy()
        check_list = {"bot": bot_healthy}
        all_healthy = all(check_list.values())


        uptime_readable = str(timedelta(seconds=int(time.time() - self.start_time)))

        data = {
            "status": "ok" if all_healthy else "error",
            "uptime": uptime_readable,
            "checks": {
                key: "healthy" if is_ok else "unhealthy"
                for key, is_ok in check_list.items()
            }
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
