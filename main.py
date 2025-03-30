''' comment
    Выполнить данную команду перед работой с проектом(Сразу после установки):

    Run this command before working with the project(Immediately after installation):


        pip install python-telegram-bot g4f diffusers transformers torch accelerate

'''


import g4f
import asyncio

from telegram import Update

from telegram.constants import ChatType

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes
from telegram.ext.filters import TEXT



def ai(user_input):
    reply = g4f.ChatCompletion.create (
        model = "gpt-4",
        messages = [
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    return reply



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Привет, Я neuro_bot_premium, как дела?")



async def handle_message(update: Update = None, context: ContextTypes.DEFAULT_TYPE = None) -> None:
    if update is None:
        user_message = input("Console \"User\": ")
        if user_message.lower() == "":
            print("Exit error...")

            return
        try:
            reply = ai(user_message)
            print("AI:", reply)
        except Exception as e:
            print(f"Ошибка при обработке запроса: {e}")
            await update.message.reply_text("ERROR... \n ")

        return

    user_message = update.message.text
    bot_username = context.bot.username
    chat_type = update.message.chat.type

    if chat_type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        if update.message.entities:
            for entity in update.message.entities:
                if entity.type == "mention" and f"@{bot_username}" in user_message:
                    try:
                        user_message = user_message.replace(f"@{bot_username}", "").strip()
                        reply = ai(user_message)
                        print("AI:", reply)
                        await update.message.reply_text(reply)
                    except Exception as e:
                        print(f"Ошибка при обработке запроса: {e}")
                        await update.message.reply_text("ERROR... \n ")

                    return

    elif chat_type == ChatType.PRIVATE:
        try:
            reply = ai(user_message)
            print("AI:", reply)
            await update.message.reply_text(reply)
        except Exception as e:
            print(f"Ошибка при обработке запроса: {e}")
            await update.message.reply_text("ERROR... \n ")



def main():
    telegram_token = "YOU_TELEGRAM_BOT_TOKEN"
    application = ApplicationBuilder().token(telegram_token).build()

    application.add_handler(CommandHandler("start", start))

    application.add_handler(MessageHandler(TEXT, handle_message))

    application.run_polling()



if __name__ == "__main__":
    while True:
        mode = input("Change: ").strip().lower()
        if mode == "con":
            print("Console run: ")
            while True:
                asyncio.run(handle_message())
        elif mode == "tg":
            main()
        else:
            print("ERROR...")
