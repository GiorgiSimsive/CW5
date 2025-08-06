from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from django.conf import settings
from django.contrib.auth.models import User
from users.models import Profile


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_id = update.effective_user.id
    username = update.effective_user.username

    try:
        user = User.objects.get(username=username)
        user.profile.telegram_id = tg_id
        user.profile.save()
        await context.bot.send_message(chat_id=tg_id, text="Telegram привязан!")
    except User.DoesNotExist:
        await context.bot.send_message(chat_id=tg_id, text="Пользователь не найден.")


def run_bot():
    app = ApplicationBuilder().token(settings.TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
