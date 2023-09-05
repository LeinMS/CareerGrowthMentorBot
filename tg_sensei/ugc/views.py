# from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

import telebot
from telebot import types
import logging
from ugc.db_func import ProfileInterface, MessageInterface
from ugc.models import UserPrompt
from ugc.langchain_openai import get_conversation
from django.conf import settings
from ugc.questionaire import Questionare
from ugc.Templates import default_user_template


# Настроить логирование для вывода в stdout
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s')
logger = logging.getLogger(__name__)
logger.info("This message will be sent to CloudWatch Logs if ECS is configured with awslogs driver.")

bot = telebot.TeleBot(settings.TOKEN)
# print(bot)


@bot.message_handler(commands=['start'])
def to_greet(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item1 = types.KeyboardButton("Sure!")
    item2 = types.KeyboardButton("No, let's chat")
    markup.add(item1, item2)
    txt = "Do you want to answer some questions? This will help me to more consciously carry on the conversation."
    bot.send_message(message.chat.id, txt, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Sure!")
def questionnaire(message):
    q = Questionare(bot, message)
    q.ask_next_question()


@bot.message_handler()
def get_bot_message(message):
    chat_id = message.chat.id
    text = message.text or ""
    bot.send_chat_action(chat_id, 'typing')

    # Проверка наличия user_prompt для данного пользователя
    p = ProfileInterface.get_or_create_profile(external_id=message.chat.id,
                                               name=message.from_user.username)
    try:
        user_prompt_obj = UserPrompt.objects.filter(profile=p).latest('created_at')
        user_custom_prompt = user_prompt_obj.prompt

    except UserPrompt.DoesNotExist:
        user_custom_prompt = default_user_template

    conversation = get_conversation(user_custom_prompt, p)

    bot_answer_text = f'{conversation.predict(input=message.text)}'
    bot.send_message(chat_id, bot_answer_text)

    MessageInterface.create_message(profile=p, user_text=text, bot_answer=bot_answer_text)
    logger.info(f"Message processed for user {message.from_user.username}")


@method_decorator(csrf_exempt, name='dispatch')
class TelegramBotView(View):

    def post(self, request, *args, **kwargs):
        try:
            json_str = request.body.decode('UTF-8')
            update = telebot.types.Update.de_json(json_str)
            bot.process_new_updates([update])
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            logger.error(f"Error processing update: {e}", exc_info=True)
            return JsonResponse({'status': 'error', 'message': str(e)})


