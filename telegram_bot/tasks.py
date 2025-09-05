from asgiref.sync import sync_to_async
from celery import shared_task
from django.conf import settings
from django.core.cache import cache
from django.utils.timezone import now
from telegram import Bot

from habits.models import Habit

LOCK_KEY = "send_reminders_lock"


@shared_task
def send_reminders():
    got = cache.add(LOCK_KEY, "1", timeout=55)
    if not got:
        return
    try:
        pass
    finally:
        cache.delete(LOCK_KEY)


async def _send_reminders_async() -> None:
    bot = Bot(token=settings.TELEGRAM_TOKEN)

    queryset = Habit.objects.filter(
        time__hour=now().hour,
        time__minute=now().minute,
    )
    habits = await sync_to_async(list)(queryset)

    for habit in habits:
        telegram_id = getattr(habit.user, "telegram_id", None)
        if telegram_id:
            message = f"⏰ Пора выполнить привычку: {habit.action} в {habit.place}"
            try:
                await bot.send_message(chat_id=telegram_id, text=message)
            except Exception as e:
                print(f"Ошибка при отправке Telegram: {e}")

    try:
        await bot.shutdown()
    except Exception:
        pass
