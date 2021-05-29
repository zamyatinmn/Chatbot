from datetime import datetime
import random
import nltk
import pytz
import sklearn
import json

# time = datetime.now(pytz.timezone('Europe/Moscow'))
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

with open('BOT_CONFIG.json', 'r', encoding="utf8") as f:
    BOT_CONFIG = json.load(f)


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


X = []
y = []
for intent in BOT_CONFIG['intents']:
    X += BOT_CONFIG['intents'][intent]['examples']
    y += [intent] * len(BOT_CONFIG['intents'][intent]['examples'])

print(len(X), len(y))


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
print(len(X_train), len(X_test))


# vectorizer = sklearn.feature_extraction.text.CountVectorizer(analyzer='char', ngram_range=(1, 2), min_df=1,
#                                                              preprocessor=clean)

vectorizer = sklearn.feature_extraction.text.TfidfVectorizer(analyzer='char_wb', ngram_range=(1,3))

vectorizer.fit(X_train)

X_train_vectorized = vectorizer.transform(X_train)
X_test_vectorized = vectorizer.transform(X_test)

classifier = RandomForestClassifier()
classifier.fit(X_train_vectorized, y_train)

# classifier.predict(vectorizer.transform(['привет']))

print(classifier.score(X_test_vectorized, y_test))



def get_intent_by_ml(text):
    return classifier.predict(vectorizer.transform([text]))[0]

def bot(ml, question):
    if ml:
        intent = get_intent_by_ml(question)
    else:
        intent = get_intent(question)

    if intent != 'Не удалось определить интент':
        return random.choice(BOT_CONFIG['intents'][intent]['responses'])
    else:
        return random.choice(BOT_CONFIG['failure_phrases'])

# $ pip install python-telegram-bot --upgrade

import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, _: CallbackContext) -> None:
    """Echo the user message."""
    ml = True
    update.message.reply_text(bot(ml, update.message.text))


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

main()