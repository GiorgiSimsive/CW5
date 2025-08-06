from celery import shared_task
from telegram import Bot
from django.conf import settings
from habits.models import Habit
from django.utils.timezone import now
import asyncio

@shared_task
def send_reminders():
    asyncio.run(_send_reminders_async())


async def _send_reminders_async():
    bot = Bot(token=settings.TELEGRAM_TOKEN)

    habits = Habit.objects.filter(time__hour=now().hour, time__minute=now().minute)

    for habit in habits:
        if hasattr(habit.user, 'telegram_id') and habit.user.telegram_id:
            message = f"⏰ Пора выполнить привычку: {habit.action} в {habit.place}"
            try:
                await bot.send_message(chat_id=habit.user.telegram_id, text=message)
            except Exception as e:
                print(f"Ошибка при отправке Telegram: {e}")
