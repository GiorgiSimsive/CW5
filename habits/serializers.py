from typing import Any

from rest_framework import serializers

from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ["user"]

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        reward = data.get("reward")
        linked_habit = data.get("linked_habit")
        is_pleasant = data.get("is_pleasant", False)
        execution_time = data.get("execution_time", 0)
        periodicity = data.get("periodicity", 1)

        if reward and linked_habit:
            raise serializers.ValidationError("Укажите только reward или linked_habit, не оба.")
        if execution_time > 120:
            raise serializers.ValidationError("execution_time не должен превышать 120 секунд.")
        if linked_habit and not linked_habit.is_pleasant:
            raise serializers.ValidationError("Связанная привычка должна быть is_pleasant=True.")
        if is_pleasant and (reward or linked_habit):
            raise serializers.ValidationError("У приятной привычки не может быть reward или linked_habit.")
        if periodicity > 7:
            raise serializers.ValidationError("periodicity должен быть ≤ 7 (раз в неделю или чаще).")

        return data
