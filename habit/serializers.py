from rest_framework import serializers

from habit.models import Habits
from habit.validators import validate_pleasant_habit, validate_one_field_only, lead_time, period_habit


class HabitsSerializer(serializers.ModelSerializer):
    # action = serializers.CharField(validators=[unique_habit_name_for_user])
    time_to_action = serializers.TimeField(validators=[lead_time])
    period = serializers.IntegerField(validators=[period_habit])

    class Meta:
        model = Habits
        fields = "__all__"

    # def validate_name(self, value):
    #     owner = self.context['request'].user
    #     unique_habit_name_for_user(value, owner)
    #     return value


    def validate(self, attrs):
        print(attrs)
        addition_habit = attrs.get('addition_habit')
        award = attrs.get('award')
        validate_pleasant_habit(addition_habit)
        validate_one_field_only(addition_habit, award)

        return attrs




class HabitsModerationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habits
        fields = ['is_published']  # Указываем только поле, которое может быть изменено

    def update(self, instance, validated_data):
        # Обновляем только поле is_published
        instance.is_published = validated_data.get('is_published', instance.is_published)
        instance.save()
        return instance


