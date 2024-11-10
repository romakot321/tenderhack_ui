from enum import Enum
from aiogram.filters.callback_data import CallbackData
from pydantic import Field, AliasChoices


class Action(Enum):
    settings = dict(action_name='settings', screen_name='Настройки')

    def __init__(self, values):
        self.action_name = values.get('action_name')
        self.screen_name = values.get('screen_name')


class ActionCallback(CallbackData, prefix='action'):
    """
    :param action: str, action_name from Action enum
    """
    action: str

    @classmethod
    def copy(cls):
        return cls(**cls.__dict__)

    def replace(self, **values):
        """Return new object with replaced values"""
        new_state = self.__dict__ | values
        return self.__class__(**new_state)


class CriteriaActionCallback(ActionCallback, prefix='settings'):
    criteria_name: str = Field(validation_alias=AliasChoices('name', 'criteria_name'))

