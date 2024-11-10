from aiogram import F
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery
from aiogram.types import Message
from aiogram3_di import Depends

from typing import Annotated

from app.services.auction import AuctionService

router = Router(name=__name__)


@router.message(F.text.startswith("https://zakupki.mos.ru/auction/"))
async def auction_analyze(
        message: Message,
        service: Annotated[
            AuctionService, Depends(AuctionService.init)]
):
    url = message.text
    return await service.handle_auction_analyze_create(
        message,
        url
    )
