from aiogram import F
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery
from aiogram.types import Message
from aiogram3_di import Depends

from typing import Annotated

from app.services.start import StartService

router = Router(name=__name__)


@router.message(CommandStart())
async def start_command(
        message: Message,
        service: Annotated[
            StartService, Depends(StartService.init)]
):
    return await service.handle_start_command(
        message
    )
