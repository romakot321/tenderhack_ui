from aiogram import types
from pydantic import BaseModel, ConfigDict, computed_field, Field


class Message(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    message_id: int | None = None  # Message_id has set by telegram


class TextMessage(Message):
    text: str
    reply_markup: types.InlineKeyboardMarkup | None = None
    parse_mode: str | None = None
