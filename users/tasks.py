import telegram
from celery import shared_task
from django.utils import timezone

from config.settings import TG_BOT_TOKEN
from habits.models import Habit


@shared_task
def send_telegram_reminders():
    '''Отправка напоминаний в Telegram'''
    try:
        bot = telegram.Bot(token=TG_BOT_TOKEN)
        now = timezone.now()

        habits_to_remind = Habit.objects.filter(
            time__hour=now.hour,
            time__minute=now.minute,
            last_remember__lt=now.replace(hour=0, minute=0, second=0)
        )

        for habit in habits_to_remind:
            if habit.owner.tg_id:
                message = f"⏰ Напоминание: {habit.action} в {habit.place} в {habit.time.strftime('%H:%M')}"
                bot.send_message(chat_id=habit.owner.tg_id, text=message)
                habit.last_remember = now
                habit.save()

    except Exception as e:
        print(f"Ошибка отправки напоминаний: {e}")
