import os
from contextlib import asynccontextmanager
from typing import Annotated

from aiogram import F
from aiogram import Router, Bot
from aiogram import exceptions
from aiogram.methods import EditMessageText, EditMessageMedia, EditMessageReplyMarkup
from aiogram.methods import SendMessage, SendPhoto
from aiogram.types import CallbackQuery, Message
from aiogram3_di import Depends

from app.schemas.action_callback import Action
from app.schemas.action_callback import ActionCallback
from app.schemas.message import TextMessage, MediaMessage, MarkupMessage

router = Router(name=__name__)
_bot = Bot(os.getenv('BOT_TOKEN'))


__message_type_to_send_method: dict = {
    TextMessage: SendMessage,
    MediaMessage: SendPhoto,
}
__message_type_to_edit_method: dict = {
    TextMessage: EditMessageText,
    MediaMessage: EditMessageMedia,
    MarkupMessage: EditMessageReplyMarkup
}


def build_aiogram_method(
        telegram_id,
        message: TextMessage,
        use_edit: bool = False,
) -> SendMessage | None:
    """Return None if unknown message type"""
    if use_edit:
        method = __message_type_to_edit_method.get(type(message))
    else:
        method = __message_type_to_send_method.get(type(message))
    if method is None:
        raise ValueError("Unknown message type")
    return method(chat_id=telegram_id, **message.model_dump())


async def send_methods(*methods) -> list[dict]:
    responses = []
    for method in methods:
        try:
            responses.append(await _bot(method))
        except exceptions.TelegramForbiddenError:
            continue
    return responses


def bot_route():
    def method_sender_decorator(func):
        async def wrapper(*args, **kwargs):
            to_send = await func(*args, **kwargs)
            if not to_send:
                return
            if not isinstance(to_send, list):
                to_send = [to_send]

            message = kwargs.get('message')
            responses: list = await send_methods(*to_send)

            return responses

        return wrapper

    return method_sender_decorator
