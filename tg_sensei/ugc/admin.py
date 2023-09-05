from django.contrib import admin

# Register your models here.
from .forms import ProfileForm
from .models import *


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'external_id',
                    'name')
    form = ProfileForm


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'profile',
                    'user_text',
                    'bot_answer',
                    'created_at')


@admin.register(UserPrompt)
class UserPromptAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'profile',
                    'prompt',
                    'created_at')

    # def get_queryset(self, request):
    #     return


