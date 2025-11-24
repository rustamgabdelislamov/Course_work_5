import json
from datetime import timedelta, datetime
import requests
from celery import shared_task
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from habit.models import Habits
from config import settings


@shared_task
def create_periodic_task():
    habits = Habits.objects.all()
    for habit in habits:
        if not PeriodicTask.objects.filter(name=f"Send message {habit.owner.tg_chat_id} {habit.pk}").exists():
            print(f"Задача добавлена {habit.action}")
            schedule, created = IntervalSchedule.objects.get_or_create(
                every=habit.period,
                period=IntervalSchedule.DAYS,
            )
            text = f"я буду {habit.action} в {habit.time} в {habit.place}"
            PeriodicTask.objects.create(
                interval=schedule,
                name=f"Send message {habit.owner.tg_chat_id} {habit.pk}",
                task='users.tasks.send_message',
                args=json.dumps([text, habit.owner.tg_chat_id]),
                start_time=str(datetime.now().date()) + " " + str(habit.time)
            )

@shared_task
def send_message(text, tg_chat_id):
    params = {
        'text': text,
        'chat_id': tg_chat_id
    }
    requests.get(f'{settings.TELEGRAM_URL}{settings.BOT_TOKEN}/sendMessage', params=params).json()
