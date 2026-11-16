"""Куда кладём результат: таблица out/daily.csv и отметка о последнем обработанном дне.

Два правила, без которых запуск по расписанию рано или поздно сломается:

1. Повторный запуск того же дня заменяет строку, а не дописывает вторую.
2. Файл сначала целиком пишется во временный и потом подменяет старый одной
   операцией. Если программа упадёт посреди записи, старый файл останется целым.
"""

import json
import os
from datetime import date
from pathlib import Path

import pandas as pd


def write_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)  # либо старый файл, либо новый — половины не бывает


def save_day(path: Path, row: dict) -> None:
    """Записать показатели дня. Строка за ту же дату отчёта заменяется."""
    table = pd.DataFrame([row])
    if path.exists():
        old = pd.read_csv(path)
        table = pd.concat([old[old["report_date"] != row["report_date"]], table])
    write_atomic(path, table.sort_values("report_date").to_csv(index=False))


def last_done(state_file: Path) -> date | None:
    """Последняя обработанная дата отчёта или None, если ещё ничего не было."""
    if not state_file.exists():
        return None
    return date.fromisoformat(json.loads(state_file.read_text())["last_done"])


def mark_done(state_file: Path, report_date: date) -> None:
    write_atomic(state_file, json.dumps({"last_done": report_date.isoformat()}))
