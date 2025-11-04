# whitelist.py
from __future__ import annotations

import json
import os
import tempfile
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Whitelist:
    """
    Класс для работы с whitelist.json.
    Формат файла:
    {
      "admins": [ {"id": 1320319316} ],
      "users":  [ {"id": 6165946917} ],
      "allow_unknown": false
    }
    """
    path: str
    admins: List[int] = field(default_factory=list)
    users: List[int] = field(default_factory=list)
    allow_unknown: bool = False

    # ---------- Загрузка/сохранение ----------

    @classmethod
    def load(cls, path: str) -> "Whitelist":
        if not os.path.exists(path):
            # если файла нет — создаём пустую структуру в памяти
            return cls(path=path)

        with open(path, "r", encoding="utf-8") as f:
            raw: Dict[str, Any] = json.load(f)

        admins = _extract_ids(raw.get("admins", []))
        users = _extract_ids(raw.get("users", []))
        allow_unknown = bool(raw.get("allow_unknown", False))

        # удалим дубли
        admins = _unique(admins)
        users = _unique(users)

        return cls(path=path, admins=admins, users=users, allow_unknown=allow_unknown)

    def save(self) -> None:
        """Атомарная запись JSON, чтобы не побить файл при падении."""
        data = {
            "admins": [{"id": i} for i in _unique(self.admins)],
            "users": [{"id": i} for i in _unique(self.users)],
            "allow_unknown": bool(self.allow_unknown),
        }
        dir_name = os.path.dirname(os.path.abspath(self.path)) or "."
        os.makedirs(dir_name, exist_ok=True)

        with tempfile.NamedTemporaryFile("w", delete=False, dir=dir_name, encoding="utf-8") as tmp:
            json.dump(data, tmp, ensure_ascii=False, indent=2)
            tmp.flush()
            os.fsync(tmp.fileno())
            tmp_name = tmp.name

        os.replace(tmp_name, self.path)

    # ---------- Проверки доступа ----------

    def is_admin(self, user_id: Optional[int]) -> bool:
        return user_id is not None and user_id in self.admins

    def is_user(self, user_id: Optional[int]) -> bool:
        return user_id is not None and user_id in self.users

    def is_allowed(self, user_id: Optional[int]) -> bool:
        """Разрешён ли доступ пользователю с таким ID."""
        if user_id is None:
            return bool(self.allow_unknown)
        if self.is_admin(user_id):
            return True
        if self.is_user(user_id):
            return True
        return bool(self.allow_unknown)

    # ---------- Модификация списков ----------

    def add_admin(self, user_id: int) -> None:
        if user_id not in self.admins:
            self.admins.append(user_id)

    def add_user(self, user_id: int) -> None:
        if user_id not in self.users:
            self.users.append(user_id)

    def remove_admin(self, user_id: int) -> None:
        self.admins = [i for i in self.admins if i != user_id]

    def remove_user(self, user_id: int) -> None:
        self.users = [i for i in self.users if i != user_id]

    def set_allow_unknown(self, value: bool) -> None:
        self.allow_unknown = bool(value)

    # ---------- Утилиты для удобства ----------

    def to_dict(self) -> Dict[str, Any]:
        """Если надо быстро отдать текущее состояние (например, в /debug)."""
        return {
            "admins": [{"id": i} for i in sorted(self.admins)],
            "users": [{"id": i} for i in sorted(self.users)],
            "allow_unknown": self.allow_unknown,
        }

    def __len__(self) -> int:
        """Сколько уникальных ID всего (admins + users)."""
        return len(set(self.admins) | set(self.users))


# ===== Вспомогательные функции (приватные) =====

def _extract_ids(items: Any) -> List[int]:
    """
    Приводит список admin/user к [int, ...]
    Поддерживает:
      - [{"id": 123}, {"id": 456}]
      - [123, 456]
    Остальное игнорируется.
    """
    result: List[int] = []
    if not isinstance(items, list):
        return result
    for x in items:
        if isinstance(x, int):
            result.append(x)
        elif isinstance(x, dict) and "id" in x and isinstance(x["id"], int):
            result.append(x["id"])
    return result


def _unique(ids: List[int]) -> List[int]:
    """Убирает дубли, сохраняет порядок первой встречи."""
    seen = set()
    out: List[int] = []
    for i in ids:
        if i not in seen:
            seen.add(i)
            out.append(i)
    return out
