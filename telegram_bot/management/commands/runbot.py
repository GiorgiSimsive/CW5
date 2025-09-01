from typing import Any

from django.core.management.base import BaseCommand

from telegram_bot.bot import run_bot


class Command(BaseCommand):
    help = "Run Telegram Bot"

    def handle(self, *args: Any, **options: Any) -> None:
        run_bot()
