"""Настройки: всё, что отличается от машины к машине, — в .env, а не в коде.

В коде остаются только значения по умолчанию. Пароли и токены в коде
не появляются вовсе: код уходит в git, а .env — нет.
"""

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    data_dir: Path
    log_file: Path
    # repr=False: токен не печатается, даже если напечатать настройки целиком
    telegram_token: str = field(repr=False)


def load_settings() -> Settings:
    load_dotenv(ROOT / ".env")
    return Settings(
        # ROOT / "data" — относительный путь от корня проекта; абсолютный путь в .env его заменит
        data_dir=ROOT / os.getenv("PRIME_DATA_DIR", "data"),
        log_file=ROOT / "logs" / "prime.log",
        telegram_token=os.getenv("TELEGRAM_TOKEN", ""),
    )
