from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

from config import TOKEN, CONTACT_USERNAME

from flask import Flask
from threading import Thread
import os


WELCOME_TEXT = """
🔥 ברוכים הבאים!

החומר הכי טוב והכי איכותי, שירות מהיר ומחיר פגז!!! 💯

🚚 משלוחים לירושלים והמרכז בלבד
⏱️ התחייבות להגעה עד שעה
💵 תשלום במזומן לשליח

📲 בחרו את המוצר הרצוי מהתפריט.

👇 התחילו כאן:
"""


PRODUCTS = [
    {
        "name": "שאנל 1 גרם",
        "price": 300
    },
    {
        "name": "שאנל 2 גרם",
        "price": 650
    },
    {
        "name": "שאנל גבוהה 1 גרם",
        "price": 550
    },
    {
        "name": "בושם לבובו",
        "price": 350,
        "note": "מינימום הזמנה 5"
    }
]


def product_buttons():
    buttons = []

    for index, product in enumerate(PRODUCTS):
        text = f"🧴 {product['name']} - ₪{product['price']}"

        buttons.append([
            InlineKeyboardButton(
                text,
                callback_data=f"product_{index}"
            )
        ])

    return InlineKeyboardMarkup(buttons)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    with open("doctork.png", "rb") as photo:

        await update.message.reply_photo(
            photo=photo,
            caption=WELCOME_TEXT,
            reply_markup=product_buttons()
        )


async def product_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    index = int(query.data.split("_")[1])

    product = PRODUCTS[index]

    extra = ""

    if "note" in product:
        extra = f"\n📌 {product['note']}"

    text = (
        f"✅ בחרת: {product['name']}\n"
        f"💰 מחיר: ₪{product['price']}"
        f"{extra}\n\n"
        "😍 בחירה מצוינת!\n\n"
        "כדי להשלים את ההזמנה ולאמת את הפרטים,\n"
        "לחץ על הכפתור למטה ותועבר ישירות לשיחה פרטית איתי.\n\n"
        "🚚 לאחר האימות נוכל להמשיך בטיפול בהזמנה."
    )

    buttons = [
        [
            InlineKeyboardButton(
                "💬 מעבר לשיחה פרטית",
                url=f"https://t.me/{CONTACT_USERNAME}"
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 חזרה למוצרים",
                callback_data="back"
            )
        ]
    ]

    await query.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )


async def back(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
        WELCOME_TEXT,
        reply_markup=product_buttons()
    )


def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        CallbackQueryHandler(
            product_selected,
            pattern="^product_"
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            back,
            pattern="^back$"
        )
    )

    print("הבוט התחיל לעבוד!")

    app.run_polling()


web_app = Flask(__name__)


@web_app.route("/")
def home():
    return "Bot is running"


def run_web():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    Thread(target=run_web).start()
    main()