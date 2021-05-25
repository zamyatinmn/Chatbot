from datetime import datetime
import random
import nltk
import pytz

time = datetime.now(pytz.timezone('Europe/Moscow'))

BOT_CONFIG = {'intents': {
    'hello': {
        'examples': ['Привет!', 'Хай', 'Прив', 'йо', 'ку', 'Здаров'],
        'responses': ['Здравствуйте!', 'Добрый день!', 'И Вам привет']
    },
    'bye': {
        'examples': ['Пока', 'Увидимся', 'До скорого свидания', 'бб'],
        'responses': ['Прощайте', 'Рад был Вас слышать', 'Приходите еще']
    },
    'time': {
        'examples': ['Который час?', 'Сколько время?', 'Подскажи время', 'время'],
        'responses': ['Сейчас %d часов %d минут и %d секунд по Московскому времени' % (time.hour, time.minute,
                                                                                       time.second)]
    },
    'support': {
        'examples': ['Что делать', 'я устал', 'У меня ничего не получается'],
        'responses': ['У тебя все получится', 'Ты молодец!', 'Ты со всем справишься', 'Ты крутой!']
    },
    'joke': {
        'examples': ['Расскажи анекдот', 'Расскажи шутку', 'Развесели меня'],
        'responses': ['Есть только две бесконечные вещи: Вселенная и дебаг. Хотя на счет вселенной я не уверен.',
                      'Решение сложной задачи поручайте ленивому сотруднику: он найдет более легкий путь.',
                      'Услышал от коллеги питонщика: Работа - не волк. Работа - питон.',
                      'Иногда надо рассмешить людей, чтобы отвлечь их от желания вас повесить.',
                      'Дружба между человеком и компьютером возможна. Правда, от нее появляются программы.']
    },
    'answer': {
        'examples': ['Дай ответ на главный вопрос жизни, вселенной и всего такого', 'что есть бог',
                     'В чем смысл жизни?'],
        'responses': ['42']
    }
}}


def clean(text):
    clean_text = ''
    for ch in text.lower():
        if ch in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя ':
            clean_text += ch
    return clean_text


def compare(s1, s2):
    return nltk.edit_distance(s1, s2) / ((len(s1) + len(s2)) / 2) < 0.4


def get_intent(question):
    for intent in BOT_CONFIG['intents']:
        for example in BOT_CONFIG['intents'][intent]['examples']:
            if compare(clean(example), clean(question)):
                return intent
    return 'Не удалось определить интент'


def bot():
    question = input()
    intent = get_intent(question)
    if intent != 'Не удалось определить интент':
        print(random.choice(BOT_CONFIG['intents'][intent]['responses']))
    else:
        print(intent)


while True:
    bot()
