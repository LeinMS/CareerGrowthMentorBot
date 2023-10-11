from telebot import types
from ugc.db_func import ProfileInterface, UserPromptInterface, DeviceLocationInterface
from timezonefinder import TimezoneFinder
import pytz
from datetime import datetime
from ugc.langchain_openai import get_conversation
from ugc.Templates import default_user_template
from ugc.models import UserPrompt

class Questionare:

    def __init__(self, bot, message):
        self.bot = bot
        self.chat_id = message.chat.id
        self.current_question_idx = 0
        self.message = message
        self.QUESTIONS = [
            {
                'key': 'q1',
                'text': "What is your name?",
                'characteristic': 'Name',
                'options': None
            },
            {
                'key': 'q2',
                'text': "You find a lamp with a genie who grants you a wish to try any job for a day. What would it be?",
                'characteristic': 'Career interests',
                'options': [
                    ("Artist in a creative studio", "Creative industries"),
                    ("CEO of a large company", "Corporate, leadership roles"),
                    ("Scientist in a research lab", "Science, research roles"),
                    ("Chef in a high-end restaurant", "Culinary, hospitality roles")
                ]
            },
            {
                'key': 'q3',
                'text': "You're learning to play a new instrument. How would you prefer to learn?",
                'characteristic': 'Learning Style',
                'options': [
                    ("Watching YouTube tutorials", "Visual and auditory learning"),
                    ("Reading a how-to book", "Reading/writing learning"),
                    ("Taking a hands-on workshop", "Kinesthetic learning"),
                    ("Having one-on-one lessons", "Personalized Instruction Learning")
                ]
            },
            {
                'key': 'q4',
                'text': "You're planning a dream vacation. What's the first thing you do?",
                'characteristic': 'Problem-solving approach',
                'options': [
                    ("Make a detailed itinerary", "Methodical, structured planning"),
                    ("Research the local culture and history", "Analytical, exploratory planning"),
                    ("Ask friends for recommendations", "Social, collaborative planning"),
                    ("Just pack and go!", "Spontaneous, flexible planning")
                ]
            },
            {
                'key': 'q5',
                'text': "You find a treasure chest but it's locked. What's your approach?",
                'characteristic': 'Problem-solving approach',
                'options': [
                    ("Look for the key", "Methodical problem-solving"),
                    ("Try to pick the lock", "Innovative problem-solving"),
                    ("Look for clues in the surroundings", "Analytical problem-solving"),
                    ("Try to break it open", "Action-oriented problem-solving")
                ]
            },
            {
                'key': 'q6',
                'text': "You're stuck on a difficult task at work. What do you do?",
                'characteristic': 'Problem-solving approach',
                'options': [
                    ("Ask a colleague for help", "Collaborative problem-solving"),
                    ("Take a break and come back later", "Reflective problem-solving"),
                    ("Keep trying different approaches", "Persistent problem-solving"),
                    ("Research online for solutions", "Research-oriented problem-solving")
                ]
            },
            {
                'key': 'q7',
                'text': "At a networking event, you prefer to…",
                'characteristic': 'Communication Style',
                'options': [
                    ("Meet as many people as possible", "Extroverted communication"),
                    ("Have deep conversations with a few people", "Introverted communication"),
                    ("Listen more than talk", "Listener communication"),
                    ("Stick to people you already know", "Familiar communication")
                ]
            },
            {
                'key': 'q8',
                'text': "You have to choose between a high-paying job you don't like and a lower-paying job you love. What would you pick?",
                'characteristic': 'Values and motivations',
                'options': [
                    ("High-paying job", "Financial stability"),
                    ("Lower-paying job", "Intrinsic satisfaction"),
                    ("Negotiate the pay at the job I love", "Balanced"),
                    ("Take the high-paying job but continue looking", "Financial stability, ambition")
                ]
            },
            {
                'key': 'q9',
                'text': "When you feel stressed or overwhelmed, you usually…",
                'characteristic': 'Stress management',
                'options': [
                    ("Go for a run or workout", "Physical stress management"),
                    ("Meditate or practice mindfulness", "Mindful stress management"),
                    ("Talk to a friend or loved one", "Social stress management"),
                    ("Immerse yourself in a hobby or activity you love", "Personal-interest stress management")
                ]
            },
            {
                'key': 'q10',
                'text': "How do you feel about public speaking?",
                'characteristic': 'Values and motivations',
                'options': [
                    ("Love it!", "Confidence, extraversion, leadership"),
                    ("It's okay", "Balanced perspective, adaptability"),
                    ("Not a fan but can manage", "Resilience, willingness to step out of comfort zone"),
                    ("Avoid it at all costs", "Introversion, preference for one-on-one or written communication")
                ]
            },
            {
                'key': 'q11',
                'text': "You come across a problem you can't solve immediately. How do you react?",
                'characteristic': 'Problem-solving approach',
                'options': [
                    ("Feel motivated to find a solution", "Persistent problem-solving but determined"),
                    ("Feel frustrated but determined", "Resilient yet emotionally aware"),
                    ("Seek help from others", "Collaborative problem-solving"),
                    ("Feel anxious and stressed", "Reflective problem-solving")
                ]
            },
            {
                'key': 'q12',
                'text': "If you had a free hour each day, how would you spend it?",
                'characteristic': 'Learning Style',
                'options': [
                    ("Learn something new", "Intellectual curiosity"),
                    ("Help someone in need", "Altruistic learning"),
                    ("Relax and recharge", "Restful learning"),
                    ("Work on personal projects", "Project-based learning")
                ]
            },
            {
                'key': 'q13',
                'text': "When discussing an important topic with someone, you prefer to…",
                'characteristic': 'Communication Style',
                'options': [
                    ("Have a face-to-face conversation", "Personal communication"),
                    ("Send a detailed email", "Written communication"),
                    ("Talk over the phone", "Auditory communication"),
                    ("Discuss in a group setting", "Collaborative communication")
                ]
            },
            {
                'key': 'q14',
                'text': "You've been given a complex task at work. Your approach is to…",
                'characteristic': 'Problem-solving approach',
                'options': [
                    ("Dive in headfirst", "Persistent problem-solving"),
                    ("Make a detailed plan", "Research-oriented problem-solving"),
                    ("Collaborate with others", "Collaborative problem-solving"),
                    ("Research and gather information first", "Research-oriented problem-solving")
                ]
            },
            {
                'key': 'q15',
                'text': "In terms of career success, what's most important to you?",
                'characteristic': 'Values and motivations',
                'options': [
                    ("Making a positive impact", "Altruism, contribution"),
                    ("Financial stability", "Financial security"),
                    ("Personal satisfaction", "Intrinsic satisfaction"),
                    ("Recognition and prestige", "Ambition, extrinsic motivation")
                ]
            },
            {
                'key': 'q16',
                'text': "From which type of application are you communicating?",
                'characteristic': None,
                'options': [("Desktop", "Desktop"), ("Mobile", "Mobile")]
            }
        ]

        self.prompt = {
            'Name': None,
            'Career interests': [],
            'Learning Style': [],
            'Problem-solving approach': [],
            'Communication Style': [],
            'Values and motivations': [],
            'Stress management': [],
        }
        self.question_data = {q['key']: [] for q in self.QUESTIONS}

    def ask_next_question(self):
        """ Next question or stop """
        if self.current_question_idx < len(self.QUESTIONS):
            question = self.QUESTIONS[self.current_question_idx]
            markup = None
            if question['options']:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                buttons = [types.KeyboardButton(text) for text, _ in question['options']]
                markup.add(*buttons)
            msg = self.bot.send_message(self.chat_id,
                                        question['text'],
                                        reply_markup=markup)

            self.bot.register_next_step_handler(msg, self.handle_answer)

        else:
            remove_markup = types.ReplyKeyboardRemove()
            self.bot.send_message(self.chat_id,
                                  "Thank you for completing the questionnaire!",
                                  reply_markup=remove_markup)

            # Форматирование ответов и отправка их пользователю
            formatted_text = self.format_prompt()
            # save prompt
            self.save_user_prompt(formatted_text)
            # Бот отправляет первое сообщение
            # try:
            #     self.send_welcome_message_based_on_prompt(self.message)
            # except Exception as e:
            #     print(e)


    def handle_desktop(self, message):
        user_input = message.text

        if user_input == "Skip":
            utc_value = None

        else:
            utc_value = self.get_utf(message.text)

        profile = self.db_action(ProfileInterface.get_or_create_profile,
                                 external_id=message.chat.id,
                                 name=message.from_user.username)

        self.db_action(DeviceLocationInterface.set_device_type_desktop,
                       profile=profile,
                       utc_offset=utc_value)

        self.current_question_idx += 1
        self.ask_next_question()

    def handle_mobile_location_permission(self, message):
        if message.location:
            lat = message.location.latitude
            lng = message.location.longitude
            try:
                tf = TimezoneFinder()
                tz_name = tf.timezone_at(lng=lng,
                                         lat=lat)
                if not tz_name:
                    raise ValueError("Could not determine timezone")

                timezone = pytz.timezone(tz_name)
                utc_offset = timezone.utcoffset(datetime.utcnow()).total_seconds() / 3600

                # Get user profile or create if not exists
                profile = self.db_action(ProfileInterface.get_or_create_profile,
                                         external_id=message.chat.id,
                                         name=message.from_user.username)

                # Save to the DeviceLocation. Assuming there's a method like 'create_device_location'.
                # Modify as per your actual DB functions.
                self.db_action(DeviceLocationInterface.create_device_location,
                               profile=profile,
                               lat=lat,
                               lng=lng,
                               timezone=tz_name,
                               utc_offset=utc_offset)

                self.bot.send_message(self.chat_id, f"Your timezone is: {tz_name}, UTC+{int(utc_offset)}")
                self.current_question_idx += 1
                self.ask_next_question()

            except Exception as e:
                self.bot.send_message(self.chat_id, "Oops! Something went wrong. Please try again.")
                print(f"Error occurred while saving timezone: {e}")
                self.ask_next_question() # ПРОВЕРИТЬ ЭТО !!!!

        elif message.text == "No":
            # Optionally save NULL data or do nothing, then move to the next question
            self.current_question_idx += 1
            self.ask_next_question()
        else:
            self.bot.send_message(self.chat_id, "Please select a valid option.")
            self.ask_next_question()

    def handle_answer(self, message):
        question = self.QUESTIONS[self.current_question_idx]

        if question['key'] == 'q16':
            try:
                if message.text == "Desktop":
                    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
                    skip_button = types.KeyboardButton("Skip")
                    markup.add(skip_button)

                    msg = self.bot.send_message(self.chat_id,
                                                "Please input your timezone (e.g. +3 or -5 or etc) or press 'Skip'.",
                                                reply_markup=markup)
                    self.bot.send_message(self.chat_id,
                                          "If you don't know your own UTC then use [this site](https://time.is/en/UTC) to find out!",
                                          parse_mode="Markdown")

                    # Здесь мы регистрируем обработчик события, но не ждем его завершения
                    self.bot.register_next_step_handler(msg, self.handle_desktop)
                    return

                elif message.text == "Mobile":
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                    item1 = types.KeyboardButton("Yes!", request_location=True)
                    item2 = types.KeyboardButton("No")
                    markup.add(item1, item2)
                    txt = 'Would you like to share your location?'
                    msg = self.bot.send_message(message.chat.id, txt, reply_markup=markup)
                    self.bot.register_next_step_handler(msg, self.handle_mobile_location_permission)
                    return

            except Exception as e:
                self.bot.send_message(self.chat_id, "Oops! Something went wrong. Please try again.")
                print(f"just click on the button : {e}")
                self.ask_next_question() # ПРОВЕРИТЬ ЭТО !!!!

        if self.prompt['Name'] is None:
            user_input = message.text
            self.prompt['Name'] = user_input

        if question['options']:
            options_dict = dict(question['options'])

            if message.text in options_dict:
                self.question_data[question['key']].append(options_dict[message.text])
                self.current_question_idx += 1
                self.ask_next_question()
                self.prompt[question['characteristic']].append(options_dict[message.text])

            else:
                self.bot.send_message(self.chat_id, "Please select a valid option.")
                self.ask_next_question()
        else:
            self.question_data[question['key']].append(message.text)
            self.current_question_idx += 1
            self.ask_next_question()

    def format_prompt(self):
        formatted_text = ""
        for characteristic, values in self.prompt.items():
            # Если это имя, форматируем особым образом
            if characteristic == 'Name':
                formatted_text += f"{characteristic}: {values}.\n"
            else:
                # Если это список значений
                if isinstance(values, list):
                    formatted_text += f"{characteristic}: {', '.join(values)}\n"
                else:
                    formatted_text += f"{characteristic}: {values}.\n"
        return formatted_text

    def save_user_prompt(self, formatted_text):
        try:

            user_custom_prompt = formatted_text
            # self.bot.send_message(self.message.chat.id, "Attempting to save your prompt...")

            profile = self.db_action(ProfileInterface.get_or_create_profile,
                                     external_id=self.message.chat.id,
                                     name=self.message.from_user.username)

            self.db_action(UserPromptInterface.create_user_prompt,
                           profile=profile,
                           prompt=user_custom_prompt)

            # self.bot.send_message(self.message.chat.id, "Your prompt is saved successfully!")

        except Exception as e:
            self.bot.send_message(self.message.chat.id, "Oops! Something went wrong while saving your prompt. Please try again.")
            print(f"Error occurred while saving user prompt: {e}")

    def get_utf(self, value):
        # Если значение является строкой и начинается с "+", удаляем "+".
        if isinstance(value, str) and value.startswith("+"):
            value = value[1:]

        # Пытаемся преобразовать value в число
        try:
            num = int(value)
        except ValueError:
            self.bot.send_message(self.message.chat.id, "Oops! It seems you've entered an invalid input. Please provide a whole number.")
            return None

        if -12 <= num <= 12:
            return num
        else:
            self.bot.send_message(self.message.chat.id, "Sorry, the value you entered is out of range. Please provide a number between -12 and 12.")
            return None

    def db_action(self, func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            self.bot.send_message(self.chat_id,
                                  "Oops! An error occurred while accessing the database. Please try again.")
            print(f"Database Error: {e}")
            return None

    def send_welcome_message_based_on_prompt(self, message):
        # Получаем промпт пользователя
        chat_id = message.chat.id
        p = ProfileInterface.get_or_create_profile(external_id=chat_id,
                                                   name=message.from_user.username)
        try:
            user_prompt_obj = UserPrompt.objects.filter(profile=p).latest('created_at')
            user_custom_prompt = user_prompt_obj.prompt

        except UserPrompt.DoesNotExist:
            user_custom_prompt = default_user_template

        # Генерируем приветственное сообщение на основе промпта пользователя
        conversation = get_conversation(user_custom_prompt, p)
        welcome_text = f'{conversation.predict(input="Hello!")}'

        # Отправляем приветственное сообщение пользователю
        self.bot.send_message(chat_id, welcome_text)


