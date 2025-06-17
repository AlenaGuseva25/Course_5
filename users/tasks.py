import telegram
from celery import shared_task
from django.utils import timezone
from telegram.error import TelegramError

from config.settings import TG_BOT_TOKEN
from habits.models import Habit


@shared_task
def send_telegram_message(chat_id):
    '''Отправка напоминания в Telegram'''
    try:
        bot = telegram.Bot(token=TG_BOT_TOKEN)
        now = timezone.now()

        habits_to_remind = Habit.objects.filter(
            last_reminder__lte=now - timezone.timedelta(days=1),
            time__hour=now.hour,
            time__minute=now.minute
        )

        for habit in habits_to_remind:
            message = f" Напоминание: {habit.action} в {habit.time.strftime('%H:%M')}"
            bot.send_message(chat_id=chat_id, text=message)
            habit.last_reminder = now
            habit.save(update_fields=['last_reminder'])

    except TelegramError as e:
        print(f"Telegram API error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")