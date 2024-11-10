from aiogram.types import Message
from typing import Annotated
from aiogram3_di import Depends

from app.repositories.user import UserRepository
from app.repositories.keyboard import KeyboardRepository
from app.schemas.user import UserSchema, CheckCriteriaSchema
from app.schemas.action_callback import CriteriaActionCallback
from app.schemas.message import TextMessage
from app.handlers.utils import bot_route, build_aiogram_method


class SettingsService:
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

    def _make_user_model(self, telegram_id: int):
        return UserSchema(telegram_id=telegram_id, criteria=CheckCriteriaSchema())

    @bot_route()
    async def handle_criteria_callback(self, query, callback_data: CriteriaActionCallback):
        user_model = self.user_repository.get(query.from_user.id)
        if user_model is None:
            return query.answer("Пользователь не найден")
        print(callback_data)
        user_model = self.user_repository.toggle_criteria(query.from_user.id, callback_data.criteria_name)
        markup = self.keyboard_repository.settings_keyboard(user_model)
        response = TextMessage(text="Настройки", reply_markup=markup, message_id=query.message.message_id)
        return build_aiogram_method(query.from_user.id, response, use_edit=True)
