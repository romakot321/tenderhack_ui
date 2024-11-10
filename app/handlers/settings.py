from typing import Annotated

from aiogram import F
from aiogram import Router, Bot
from aiogram.types import CallbackQuery
from aiogram3_di import Depends

from app.services.settings import SettingsService
from app.schemas.action_callback import Action
from app.schemas.action_callback import ActionCallback
from app.schemas.action_callback import CriteriaActionCallback

router = Router(name=__name__)


@router.callback_query(
    CriteriaActionCallback.filter(
        F.action == Action.settings.action_name
    )
)
async def settings_callback(
        query: CallbackQuery,
        callback_data: CriteriaActionCallback,
        settings_service: Annotated[
            SettingsService, Depends(SettingsService.init)]
):
    print(query)
    return await settings_service.handle_criteria_callback(query, callback_data)

