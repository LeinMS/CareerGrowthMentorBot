from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Profile(models.Model):
    external_id = models.PositiveIntegerField(verbose_name="User ID in social network",
                                              unique=True)

    name = models.CharField(verbose_name="User name",
                            max_length=255)  # max_length based on typical name lengths

    is_active = models.BooleanField(default=True,
                                    verbose_name="is Active")

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


class DeviceLocation(models.Model):
    profile = models.ForeignKey(
        to='ugc.Profile',
        verbose_name='Profile',
        on_delete=models.PROTECT,
    )

    DEVICE_CHOICES = (('mobile', 'Mobile'), ('desktop', 'Desktop'))
    device_type = models.CharField(
        verbose_name='Device Type',
        max_length=10,
        choices=DEVICE_CHOICES,
        default='mobile',
        null=True,
        blank=True
    )

    latitude = models.FloatField(
        verbose_name='Latitude',
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        verbose_name='Longitude',
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        null=True,
        blank=True
    )

    timezone = models.CharField(
        verbose_name='Timezone',
        max_length=100,
        blank=True,
        null=True
    )

    UTC_CHOICES = [(i, str(i)) for i in range(-12, 13)]
    utc_offset = models.SmallIntegerField(
        verbose_name='UTC Offset',
        choices=UTC_CHOICES,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        verbose_name='Get timezone time',
        auto_now_add=True,
    )

    def __str__(self):
        return f'DeviceLocation {self.pk} for {self.profile}'

    class Meta:
        verbose_name = "DeviceLocation"
        verbose_name_plural = "DeviceLocations"