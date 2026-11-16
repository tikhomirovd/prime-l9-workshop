"""Учебное время: каждый запуск обрабатывает следующий день истории.

Новых данных в базе ПРАЙМ не появляется, поэтому ежедневную работу
мы проигрываем: запуск по расписанию берёт день после последнего
обработанного. Пропущенные запуски дни не теряют — следующий запуск
начнёт с первого необработанного.
"""

import logging
from datetime import date, timedelta

from prime import report, results
from prime.config import Settings

log = logging.getLogger(__name__)


def run_next_day(settings: Settings, fail: bool = False) -> date | None:
    done = results.last_done(settings.state_file)
    report_date = settings.replay_start if done is None else done + timedelta(days=1)
    log.info("replay: дата отчёта %s, последняя обработанная %s", report_date, done)

    row = report.build_day(report_date, settings)
    if row is None:
        return None

    results.save_day(settings.out_dir / "daily.csv", row)
    if fail:
        # Учебный сбой ровно в худшем месте: строка уже записана, отметки о дне ещё нет
        raise RuntimeError("учебный сбой: результат записан, отметка о дне — нет")
    results.mark_done(settings.state_file, report_date)
    log.info("replay: %s обработан", report_date)
    return report_date
