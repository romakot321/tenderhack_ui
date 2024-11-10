from aiogram.types import Message
from typing import Annotated
from aiogram3_di import Depends
from loguru import logger
import asyncio

from app.repositories.analyze_storage import AnalyzeStorageRepository
from app.repositories.analyze import AnalyzeRepository
from app.repositories.user import UserRepository
from app.repositories.keyboard import KeyboardRepository
from app.schemas.auction import AuctionSchema
from app.schemas.analyze import AnalyzeSchema
from app.schemas.message import TextMessage
from app.schemas.user import CheckCriteriaSchema
from app.handlers.utils import bot_route, build_aiogram_method, send_methods


class AuctionService:
    def __init__(
            self,
            analyze_storage_rep: AnalyzeStorageRepository,
            keyboard_repository: KeyboardRepository,
            analyze_repository: AnalyzeRepository,
            user_repository: UserRepository
    ):
        self.analyze_storage_rep = analyze_storage_rep
        self.keyboard_repository = keyboard_repository
        self.analyze_repository = analyze_repository
        self.user_repository = user_repository

    @classmethod
    def init(
            cls,
            analyze_storage_rep: Annotated[
                AnalyzeStorageRepository, Depends(AnalyzeStorageRepository)],
            keyboard_repository: Annotated[
                KeyboardRepository, Depends(KeyboardRepository)],
            analyze_repository: Annotated[
                AnalyzeRepository, Depends(AnalyzeRepository)],
            user_repository: Annotated[
                UserRepository, Depends(UserRepository)],
    ):
        return cls(
            analyze_storage_rep=analyze_storage_rep,
            keyboard_repository=keyboard_repository,
            analyze_repository=analyze_repository,
            user_repository=user_repository
        )

    async def _check_analyze_complete(self, url: str) -> TextMessage | None:
        analyze_model = self.analyze_storage_rep.get(url)
        if analyze_model is None:
            return
        analyze_model = await self.analyze_repository.check_auction_analyze(analyze_model.id)
        if analyze_model is None:
            return
        return TextMessage(text="Статус: " + str(analyze_model))

    async def _create_analyze(self, url: str, criteria: CheckCriteriaSchema) -> TextMessage:
        analyze_model = await self.analyze_repository.create_auction_analyze(url, criteria)
        self.analyze_storage_rep.store(analyze_model, url)
        return TextMessage(text=str(analyze_model))

    async def _wait_for_analyze_completion(self, chat_id: int, url: str, analyze_message_id: int):
        analyze_model = self.analyze_storage_rep.get(url)

        while True:
            analyze_model = await self.analyze_repository.check_auction_analyze(analyze_model.id)

            if analyze_model is not None and analyze_model.status:
                message = TextMessage(text=str(analyze_model), message_id=analyze_message_id)
                method = build_aiogram_method(chat_id, message, use_edit=True)
                return await send_methods(method)

            await asyncio.sleep(5)

    async def handle_auction_analyze_create(self, message: Message, url: str):
        create_response = None
        check_response = await self._check_analyze_complete(url)
        if check_response is None:
            user = self.user_repository.store(message.from_user.id)
            create_response = await self._create_analyze(url, user.criteria)

        method = build_aiogram_method(message.from_user.id, check_response or create_response)

        # For edit 'wait message', not sending new
        sended_message = (await send_methods(method))[0]
        if check_response is None:
            asyncio.create_task(self._wait_for_analyze_completion(message.from_user.id, url, sended_message.message_id))

        return sended_message

