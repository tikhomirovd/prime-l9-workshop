"""Командная строка: uv run prime report --date 2026-08-24 и uv run prime replay.

Здесь разбор аргументов, настройка журнала и перехват ошибок.
Считает report.py, данные даёт data.py.
"""

import argparse
import logging
import sys
from datetime import date
from pathlib import Path

from prime import config, replay, report

log = logging.getLogger("prime")


def setup_logging(log_file: Path) -> None:
    """Подробности — в файл. В терминал — только предупреждения и ошибки."""
    log_file.parent.mkdir(exist_ok=True)
    to_file = logging.FileHandler(log_file, encoding="utf-8")
    to_file.setLevel(logging.INFO)
    to_screen = logging.StreamHandler()
    to_screen.setLevel(logging.WARNING)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[to_file, to_screen],
    )


def main() -> None:
    parser = argparse.ArgumentParser(prog="prime", description="Мониторинг подписки ПРАЙМ")
    commands = parser.add_subparsers(dest="command", required=True)

    report_cmd = commands.add_parser("report", help="отчёт за одну дату")
    report_cmd.add_argument(
        "--date", type=date.fromisoformat, required=True, help="дата отчёта, ГГГГ-ММ-ДД"
    )

    replay_cmd = commands.add_parser("replay", help="обработать следующий день учебного времени")
    replay_cmd.add_argument(
        "--fail", action="store_true", help="учебный сбой посреди обработки дня"
    )

    args = parser.parse_args()
    settings = config.load_settings()
    setup_logging(settings.log_file)
    log.info("Запуск: prime %s", " ".join(sys.argv[1:]))
    log.info("Настройки: %s", settings)
    try:
        if args.command == "report":
            row = report.build_day(args.date, settings)
            if row is not None:
                print(report.format_report(row))
        elif args.command == "replay":
            done = replay.run_next_day(settings, fail=args.fail)
            if done is not None:
                print(f"Обработана дата отчёта {done:%d.%m.%Y}")
    except Exception:
        # Без этого ошибка улетит в терминал, которого у запуска по расписанию нет
        log.exception("Запуск упал")
        sys.exit(1)
    log.info("Готово")
