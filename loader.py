from dotenv import load_dotenv  # type: ignore
import os
from typing import Final


class Settings:
    def __init__(self) -> None:
        load_dotenv()
        token = os.getenv("TOKEN")
        if not token:
            raise RuntimeError(
                "Не найден TOKEN. Создай файл .env рядом с проектом и добавь строку:\n"
                "TOKEN=ваш_токен_бота"
            )
        self._token: Final[str] = token

    @property
    def token(self) -> str:
        return self._token


settings = Settings()
TOKEN: str = settings.token
