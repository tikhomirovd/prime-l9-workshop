"""Командная строка: uv run prime report --date 2026-08-24.

Здесь только разбор аргументов. Считает report.py, данные даёт data.py.
"""

import argparse
from datetime import date

from prime import report


def main() -> None:
    parser = argparse.ArgumentParser(prog="prime", description="Мониторинг подписки ПРАЙМ")
    commands = parser.add_subparsers(dest="command", required=True)

    report_cmd = commands.add_parser("report", help="отчёт за одну дату")
    report_cmd.add_argument(
        "--date", type=date.fromisoformat, required=True, help="дата отчёта, ГГГГ-ММ-ДД"
    )

    args = parser.parse_args()
    if args.command == "report":
        print(report.format_report(report.build_day(args.date)))
