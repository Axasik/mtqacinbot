import os
import telebot
from telebot import types

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "Բարև ❤️\n\n"
        "Այստեղ կարող ես անանուն ուղարկել քո միտքը, զգացողությունը կամ խոսքը։\n\n"
        "Պարզապես գրիր այն հաջորդ հաղորդագրությամբ։"
    )


@bot.message_handler(content_types=["text"])
def receive_message(message):
    if message.text.startswith("/"):
        return

    text = message.text.strip()

    if not text:
        return

    keyboard = types.InlineKeyboardMarkup()
    publish_button = types.InlineKeyboardButton(
        "✅ Հրապարակել",
        callback_data="publish"
    )
    delete_button = types.InlineKeyboardButton(
        "❌ Ջնջել",
        callback_data="delete"
    )

    keyboard.add(publish_button, delete_button)

    bot.send_message(
        ADMIN_ID,
        "💭 Նոր անանուն միտք․\n\n"
        f"«{text}»",
        reply_markup=keyboard
    )

    bot.send_message(
        message.chat.id,
        "Շնորհակալություն ❤️\n"
        "Քո միտքը ուղարկվել է ստուգման։"
    )


@bot.callback_query_handler(func=lambda call: call.data in ["publish", "delete"])
def handle_button(call):

    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(
            call.id,
            "Դուք չունեք թույլտվություն։",
            show_alert=True
        )
        return

    if call.data == "delete":
        bot.edit_message_text(
            "❌ Միտքը ջնջվել է։",
            call.message.chat.id,
            call.message.message_id
        )
        bot.answer_callback_query(call.id)
        return

    original_text = call.message.text

    if "«" in original_text and "»" in original_text:
        thought = original_text.split("«", 1)[1].rsplit("»", 1)[0]
    else:
        thought = original_text

    bot.send_message(
        CHANNEL_ID,
        f"💭 «{thought}»"
    )

    bot.edit_message_text(
        "✅ Միտքը հրապարակվեց ալիքում։",
        call.message.chat.id,
        call.message.message_id
    )

    bot.answer_callback_query(call.id)


print("🤖 Bot is running...")

bot.infinity_polling(skip_pending=True)
