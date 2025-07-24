import asyncio
import logging

from aiogram import Bot, Dispatcher

import config
from app.main_handlers import router
from app.admin_handlers import admin_router
from app.database import init_db

main_bot = Bot(config.TOKEN_MAIN_BOT)
admin_bot = Bot(config.TOKEN_ADMIN_BOT)

dp = Dispatcher()
admin_dp = Dispatcher()

async def main():
    init_db()
    dp.include_router(router)
    admin_dp.include_router(admin_router)

    await asyncio.gather(dp.start_polling(main_bot), admin_dp.start_polling(admin_bot))

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped!')