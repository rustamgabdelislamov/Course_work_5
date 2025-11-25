from datetime import timedelta, time
from rest_framework.exceptions import ValidationError


def validate_pleasant_habit(addition_habit):
    if addition_habit and not addition_habit.reward_action:
        # проверяет что если поле addition_habit заполнено и не
        # выбрана связанная привычка то вызывает исключение
        raise ValidationError(
            "В связанные привычки могут попадать только привычки с признаком приятной привычки."
        )


def validate_one_field_only(addition_habit, award):
    if addition_habit and award:
        raise ValidationError(
            "Заполните только одно из полей , либо связанную привычку, либо вознаграждение"
        )


def lead_time(time_to_action):
    if isinstance(time_to_action, time):
        # Преобразуем время в timedelta
        time_as_timedelta = timedelta(
            hours=time_to_action.hour,
            minutes=time_to_action.minute,
            seconds=time_to_action.second,
        )

        # Сравниваем с 2 минутами
        if time_as_timedelta > timedelta(minutes=2):
            raise ValidationError("Время выполнения не может быть более 2 минут.")
    else:
        raise ValidationError("Время выполнения должно быть корректным временем.")


def period_habit(period):
    if not isinstance(period, int):
        raise ValidationError("Время периода должно быть числом")
    if period > 1:
        raise ValidationError("Привычка должна повторятся раз в неделю")


# def unique_habit_name_for_user(action, owner):
#     if Habits.objects.filter(action=action, owner=owner).exists():
#         raise ValidationError(f'У вас уже есть привычка с именем "{action}".')
