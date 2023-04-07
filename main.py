from collections import defaultdict

import telegram
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters


your_id: int = 0
gf_id: int = 0
allowed_users = [your_id, gf_id]
token: str = ""
proposal_photo_url: str = ""

stages = {
    1: "Начнём с простого: ищи в шкафу в прихожей.",
    2: "Тот, что грел, но не светил, теперь может светить и не греть.",
    3: "Ищи под той, что и светит, и греет.",
    4: "Из трёх частей, но един. Мал, но вмещает многие миры. Не разумен, но говорит. Не живой, но требует питания. "
       "Без ног, но стоит. Поезд не ждёт, но находится на станции.",
    5: "Оба живут там, где холодно. Еду берут там, где мокро. Ищи между ними.",
    6: "Они втроём эти строки создали: он придумал, они написали."
}

answers = {
    1: "шкаф",
    2: "искры",
    3: "феникс",
    4: "фортнайт",
    5: "коктейль",
    6: "2344",
}

user_stage = defaultdict(int)


def check_user(func):
    async def wrapper(update, context):
        if update.effective_user.id in allowed_users:
            await func(update, context)
    return wrapper


def get_greeting_text():
    return ("Приветствую! Чтобы дойти до финала, тебе нужно разгадать загадки. "
            "После того, как ты разгадаешь загадку, ты получишь следующую "
            "загадку или код для её получения (одно слово). Отправь код мне, чтобы "
            "перейти к следующей загадке.\n\n" + stages[1])


@check_user
async def start(update, context):
    chat_id = update.effective_chat.id
    user_stage[chat_id] = 1
    await update.message.reply_text(get_greeting_text())


@check_user
async def handle_message(update: telegram.Update, context):
    chat_id = update.effective_chat.id

    print(update.message.to_dict())
    message_text = update.message.text

    if user_stage[chat_id] == 0:
        user_stage[chat_id] = 1
        await context.bot.send_message(chat_id=chat_id, text=get_greeting_text())
        return
    elif user_stage[chat_id] > 6:
        await context.bot.send_message(chat_id=your_id, text=f'Она сказала "{message_text}"')
        return

    if message_text.lower().strip() == answers[user_stage[chat_id]].lower():
        user_stage[chat_id] += 1
        if user_stage[chat_id] == 7:
            await context.bot.send_photo(chat_id=chat_id, photo=proposal_photo_url, has_spoiler=True)
        else:
            await context.bot.send_message(chat_id=chat_id, text=stages[user_stage[chat_id]])
    else:
        await context.bot.send_message(chat_id=chat_id, text="Неверно :(\n\n" + stages[user_stage[chat_id]])


def main():
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    app.run_polling()


if __name__ == '__main__':
    main()
