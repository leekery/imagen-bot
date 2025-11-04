# middlewares/whitelist_guard.py
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Dict, Any, Awaitable
from whitelist import Whitelist

class WhitelistGuard(BaseMiddleware):
    def __init__(self, wl: Whitelist, denied_text: str = "Доступ ограничен. Напишите администратору."):
        super().__init__()
        self.wl = wl
        self.denied_text = denied_text

    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        user = event.from_user if hasattr(event, "from_user") else None
        if user and self.wl.is_allowed(user.id):
            return await handler(event, data)
        # мягкий отказ
        if isinstance(event, Message):
            await event.answer(self.denied_text)
        elif isinstance(event, CallbackQuery):
            await event.answer(self.denied_text, show_alert=True)
        return
