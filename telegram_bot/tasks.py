import asyncio

from celery import shared_task
from django.conf import settings
from django.utils.timezone import now
from telegram import Bot

from habits.models import Habit


@shared_task
def send_reminders() -> None:
    asyncio.run(_send_reminders_async())


async def _send_reminders_async() -> None:
    bot = Bot(token=settings.TELEGRAM_TOKEN)

    habits = Habit.objects.filter(time__hour=now().hour, time__minute=now().minute)

    for habit in habits:
        if hasattr(habit.user, "telegram_id") and habit.user.telegram_id:
            message = f"⏰ Пора выполнить привычку: {habit.action} в {habit.place}"
            try:
                await bot.send_message(chat_id=habit.user.telegram_id, text=message)
            except Exception as e:
                print(f"Ошибка при отправке Telegram: {e}")
