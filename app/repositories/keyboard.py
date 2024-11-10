from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.schemas.user import UserSchema
from app.schemas.action_callback import Action, CriteriaActionCallback


class KeyboardRepository:
    false_symbol = '❌'
    true_symbol = '✅'

    @classmethod
    def settings_keyboard(
            cls,
            user: UserSchema
    ):
        builder = InlineKeyboardBuilder()
        for crit_name, translated in zip(user.criteria.model_dump().keys(), user.criteria.translated_dict().items()):
            builder.button(
                text=f'{[cls.false_symbol, cls.true_symbol][int(translated[1])]} {translated[0]}',
                callback_data=CriteriaActionCallback(
                    action=Action.settings.action_name,
                    criteria_name=crit_name
                )
            )
        builder.adjust(1)
        return builder.as_markup()
