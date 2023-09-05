from ugc.models import Profile, Message, UserPrompt


class ProfileInterface:
    '''Interface for Profile operations.'''

    @staticmethod
    def get_or_create_profile(external_id, name):
        '''создает или возвращает профиль на основе внешнего ID и имени.'''
        profile, created = Profile.objects.get_or_create(
            external_id=external_id,
            defaults={'name': name}
        )
        return profile

    @staticmethod
    def get_profile_by_external_id(external_id):
        '''возвращает профиль по внешнему ID или None, если профиль не найден'''
        try:
            return Profile.objects.get(external_id=external_id)
        except Profile.DoesNotExist:
            return None

    @staticmethod
    def update_profile_name(external_id, new_name):
        '''обновляет имя профиля по его внешнему ID'''
        try:
            profile = Profile.objects.get(external_id=external_id)
            profile.name = new_name
            profile.save()
            return profile
        except Profile.DoesNotExist:
            return None

    @staticmethod
    def delete_profile(external_id):
        '''удаляет профиль по его внешнему ID'''
        try:
            profile = Profile.objects.get(external_id=external_id)
            profile.delete()
            return True
        except Profile.DoesNotExist:
            return False


class MessageInterface:
    '''Interface for Message operations.'''

    @staticmethod
    def create_message(profile, user_text, bot_answer=""):
        '''Создает новое сообщение в базе данных.'''
        message = Message(profile=profile, user_text=user_text, bot_answer=bot_answer)
        message.save()
        return message

    @staticmethod
    def get_last_n_entries(profile, n=3):
        '''Возвращает последние n сообщений для указанного профиля.'''
        return Message.objects.filter(profile=profile).order_by('-created_at')[:n]

    @staticmethod
    def get_message_by_id(message_id):
        '''Возвращает сообщение по его ID или None, если сообщение не найдено.'''
        try:
            return Message.objects.get(pk=message_id)
        except Message.DoesNotExist:
            return None

    @staticmethod
    def get_messages_by_profile(profile):
        '''Возвращает все сообщения для указанного профиля.'''
        return Message.objects.filter(profile=profile)

    @staticmethod
    def update_message(message_id, user_text=None, bot_answer=None):
        '''Обновляет содержание сообщения по его ID.'''
        try:
            message = Message.objects.get(pk=message_id)
            if user_text is not None:
                message.user_text = user_text
            if bot_answer is not None:
                message.bot_answer = bot_answer
            message.save()
            return message
        except Message.DoesNotExist:
            return None

    @staticmethod
    def delete_message(message_id):
        '''Удаляет сообщение по его ID.'''
        try:
            message = Message.objects.get(pk=message_id)
            message.delete()
            return True
        except Message.DoesNotExist:
            return False


class UserPromptInterface:
    '''Interface for UserPrompt operations.'''

    @staticmethod
    def create_user_prompt(profile, prompt):
        '''Создает новый пользовательский запрос в базе данных.'''
        if isinstance(prompt, str):
            user_prompt = UserPrompt(profile=profile, prompt=prompt)
            user_prompt.save()
            return user_prompt
        else:
            print('Prompt is not text format!')

    @staticmethod
    def get_prompt_by_id(prompt_id):
        '''Возвращает пользовательский запрос по его ID или None, если запрос не найден.'''
        try:
            return UserPrompt.objects.get(pk=prompt_id)
        except UserPrompt.DoesNotExist:
            return None

    @staticmethod
    def get_prompts_by_profile(profile):
        '''Возвращает все пользовательские запросы для указанного профиля.'''
        return UserPrompt.objects.filter(profile=profile)

    @staticmethod
    def update_prompt(prompt_id, new_prompt):
        '''Обновляет содержание пользовательского запроса по его ID.'''
        try:
            user_prompt = UserPrompt.objects.get(pk=prompt_id)
            user_prompt.prompt = new_prompt
            user_prompt.save()
            return user_prompt
        except UserPrompt.DoesNotExist:
            return None

    @staticmethod
    def delete_prompt(prompt_id):
        '''Удаляет пользовательский запрос по его ID.'''
        try:
            user_prompt = UserPrompt.objects.get(pk=prompt_id)
            user_prompt.delete()
            return True
        except UserPrompt.DoesNotExist:
            return False