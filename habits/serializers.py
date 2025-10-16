from datetime import timedelta

from rest_framework import serializers

from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = (
            'id',
            'action',
            'place',
            'pleasantness',
            'time',
            'related_habit',
            'periodicity',
            'reward',
            'time_to_complete',
            'is_public',
            'owner',
        )
        read_only_fields = ('owner',)

    def validate(self, data):
        '''Валидация привычек'''
        pleasantness = data.get('pleasantness', False)
        reward = data.get('reward')
        related_habit = data.get('related_habit')
        time_to_complete = data.get('time_to_complete')
        periodicity = data.get("periodicity", 1)
        is_public = data.get('is_public', False)
        if pleasantness:
            if reward:
                raise serializers.ValidationError(
                    'Приятная привычка не имеет вознаграждения'
                )
            if related_habit:
                raise serializers.ValidationError(
                    'Приятная привычка не может быть связана'
                )
            return data
        if reward and related_habit:
            raise serializers.ValidationError(
                'Нужно указать либо связанную привычку, либо вознаграждение, наличие сразу обоих недопустимо'
            )
        if related_habit is not None and not related_habit.pleasantness:
            raise serializers.ValidationError(
                'Связанная привычка должна быть приятной'
            )
        if time_to_complete and (time_to_complete > timedelta(minutes=2) or time_to_complete < timedelta(seconds=1)):
            raise serializers.ValidationError(
                'Время выполнения должно быть от 1 секунды до 2 минут'
            )
        if is_public and not pleasantness:
            if not reward and not related_habit:
                raise serializers.ValidationError(
                    'Публичная привычка должна иметь вознаграждение или связанную привычку'
                )
        return data

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class PublicHabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ['id', 'place', 'time', 'action', 'periodicity', 'time_to_complete']
