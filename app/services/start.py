from aiogram.types import Message
from typing import Annotated
from aiogram3_di import Depends

from app.repositories.user import UserRepository
from app.repositories.keyboard import KeyboardRepository
from app.schemas.user import UserSchema, CheckCriteriaSchema
from app.schemas.message import TextMessage
from app.handlers.utils import bot_route, build_aiogram_method


class StartService:
    def __init__(
            self,
            user_repository: UserRepository,
            keyboard_repository: KeyboardRepository
    ):
        self.user_repository = user_repository
        self.keyboard_repository = keyboard_repository

    @classmethod
    def init(
            cls,
            user_repository: Annotated[
                UserRepository, Depends(UserRepository)],
            keyboard_repository: Annotated[
                KeyboardRepository, Depends(KeyboardRepository)],
    ):
        return cls(user_repository=user_repository, keyboard_repository=keyboard_repository)

    @bot_route()
    async def handle_start_command(self, message: Message):
        user_model = self.user_repository.store(message.from_user.id)
        markup = self.keyboard_repository.settings_keyboard(user_model)
        response = TextMessage(text="Настройки", reply_markup=markup)
        return build_aiogram_method(message.from_user.id, response)
