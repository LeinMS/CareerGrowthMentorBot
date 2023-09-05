from django.db import models


class Profile(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name="User ID in social network",
        unique=True,)

    name = models.TextField(verbose_name="User name",)

    # возврат человекочитаемого описания
    def __str__(self):
        return f'#{self.external_id} {self.name}'


    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"


class Message(models.Model):
    profile = models.ForeignKey(
        to='ugc.Profile',
        verbose_name='Profile',
        on_delete=models.PROTECT,
    )
    user_text = models.TextField(
        verbose_name='Users text',
        blank=True,
    )
    bot_answer = models.TextField(
        verbose_name='Bot answer',
        blank=True
    )
    created_at = models.DateTimeField(
        verbose_name='Get message time',
        auto_now_add=True,
    )
    # возврат человекочитаемого описания
    def __str__(self):
        return f'Message {self.pk} {self.profile}'

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"


class UserPrompt(models.Model):
    profile = models.ForeignKey(
        to='ugc.Profile',
        verbose_name='Profile',
        on_delete=models.PROTECT,
    )

    prompt = models.TextField(
        verbose_name='Text',
        blank=True
    )
    created_at = models.DateTimeField(
        verbose_name='Get prompt time',
        auto_now_add=True,
    )

    # возврат человекочитаемого описания
    def __str__(self):
        return f'UserPrompt {self.pk} {self.profile}'

    class Meta:
        verbose_name = "UserPrompt"
        verbose_name_plural = "UserPrompts"

