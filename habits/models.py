from datetime import timedelta
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework.exceptions import ValidationError
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Habit(models.Model):
    '''Модель привычки'''

    PERIODICITY_CHOICES = [
        (1, "ежедневно"),
        (2, "через день"),
        (3, "раз в 3 дня"),
        (4, "раз в 4 дня"),
        (5, "раз в 5 дней"),
        (6, "раз в 6 дней"),
        (7, "еженедельно"),
    ]

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='habits', verbose_name="Пользователь")

    place = models.CharField(
        max_length=160, null=True, verbose_name='Место где выполняется привычка'
    )

    time = models.TimeField(
        null=True, verbose_name='время', help_text='в формате чч:мм',
    )

    action = models.CharField(max_length=160, verbose_name='Привычка')

    pleasantness = models.BooleanField(default=False, help_text='Признак приятной привычки')

    sheaf = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, verbose_name='Связанная привычка'
    )
    periodicity = models.PositiveSmallIntegerField(
        choices=PERIODICITY_CHOICES,
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        help_text='Периодичность: 1-ежедневно, 7-еженедельно',
    )
    reward = models.TextField(null=True, blank=True, verbose_name='Вознаграждение за выполненную привычку')
    time_to_complete = models.DurationField(
        null=True, blank=True,
        validators=[MaxValueValidator(limit_value=timedelta(minutes=2))],
        help_text='Формат: ЧЧ:ММ:СС (например, 00:01:00 — 1 минута)'
    )
    is_public = models.BooleanField(default=False, verbose_name='Признак публичности')
    last_remember = models.DateTimeField(
        verbose_name='Последнее напоминание',
        null=True,
        blank=True,
        help_text='Когда в последний раз было отправлено напоминание',
    )

    def clean(self):
        '''Проверка заданных полей'''
        if self.pleasantness and (self.reward or self.sheaf):
            raise ValidationError(
                'Приятная привычка не должна иметь вознаграждения'
            )
        if not self.pleasantness and self.reward and self.sheaf:
            raise ValidationError(
                'Необходимо указать либо вознаграждение, либо связанную привычку'
            )

    @property
    def is_visible(self):
        '''Проверка видно ли привычку другим'''
        return self.is_public

    def __str__(self):
        return f'{self.owner}, {self.action}'

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'