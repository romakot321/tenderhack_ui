import asyncio
import secrets

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.methods import TelegramMethod
from aiogram.methods.base import TelegramType
from aiogram.types import InputFile
from aiogram3_di import setup_di
from aiohttp import MultipartWriter
from loguru import logger
import os

from app import handlers


def _setup_dispatcher(dispatcher: Dispatcher):
    dispatcher.include_routers(handlers.start.router)
    dispatcher.include_routers(handlers.settings.router)
    dispatcher.include_routers(handlers.auction.router)
    setup_di(dispatcher)


async def run_polling():
    global bot, dispatcher
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dispatcher = Dispatcher()
    _setup_dispatcher(dispatcher)

    await bot.delete_webhook()
    logger.info("Bot started")
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(run_polling())
