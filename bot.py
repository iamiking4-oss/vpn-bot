import sqlite3

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# =====================
# تنظیمات
# =====================

TOKEN = "8938101725:AAFIkOoi23yM-NpgXhB5B8ucvRkSnO1XjVg"
ADMIN_ID = 8302899485

SUPPORT = "@nzdik_nya"
CARD = "بنام زارعی 5892101706171671"

# =====================
# دیتابیس
# =====================

db = sqlite3.connect(
    "users.db",
    check_same_thread=False
)

cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY
)
""")

db.commit()


def save_user(user_id):
    cursor.execute(
        "INSERT OR IGNORE INTO users VALUES(?)",
        (user_id,)
    )
    db.commit()


# =====================
# استارت
# =====================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    save_user(
        update.effective_user.id
    )

    keyboard = [

        [
            InlineKeyboardButton(
                "🛒 خرید اشتراک",
                callback_data="buy"
            )
        ],

        [
            InlineKeyboardButton(
                "💰 قیمت ها",
                callback_data="price"
            )
        ],

        [
            InlineKeyboardButton(
                "📞 پشتیبانی",
                callback_data="support"
            )
        ]

    ]

    await update.message.reply_text(
        "🌐 به فروشگاه VPN خوش آمدید",
        reply_markup=
        InlineKeyboardMarkup(
            keyboard
        )
    )


# =====================
# دکمه ها
# =====================

async def button(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    if query.data == "buy":

        keyboard = [

            [
                InlineKeyboardButton(
                    "🔥 یک ماهه | 100 هزار",
                    callback_data="plan1"
                )
            ],

            [
                InlineKeyboardButton(
                    "⚡ سه ماهه | 250 هزار",
                    callback_data="plan3"
                )
            ],

            [
                InlineKeyboardButton(
                    "💎 شش ماهه | 450 هزار",
                    callback_data="plan6"
                )
            ]

        ]

        await query.message.reply_text(
            "پلن مورد نظر را انتخاب کنید:",
            reply_markup=
            InlineKeyboardMarkup(
                keyboard
            )
        )

    elif query.data == "price":

        await query.message.reply_text(
            "💰 قیمت ها\n\n"
            "🔥 یک ماهه : 100 هزار تومان\n"
            "⚡ سه ماهه : 250 هزار تومان\n"
            "💎 شش ماهه : 450 هزار تومان"
        )

    elif query.data == "support":

        await query.message.reply_text(
            f"📞 پشتیبانی:\n{SUPPORT}"
        )

    elif query.data == "plan1":

        await query.message.reply_text(
            f"🔥 اشتراک یک ماهه\n\n"
            f"💵 مبلغ: 100 هزار تومان\n\n"
            f"شماره کارت:\n{CARD}\n\n"
            "بعد از پرداخت، عکس رسید را ارسال کنید."
        )

    elif query.data == "plan3":

        await query.message.reply_text(
            f"⚡ اشتراک سه ماهه\n\n"
            f"💵 مبلغ: 250 هزار تومان\n\n"
            f"شماره کارت:\n{CARD}\n\n"
            "بعد از پرداخت، عکس رسید را ارسال کنید."
        )

    elif query.data == "plan6":

        await query.message.reply_text(
            f"💎 اشتراک شش ماهه\n\n"
            f"💵 مبلغ: 450 هزار تومان\n\n"
            f"شماره کارت:\n{CARD}\n\n"
            "بعد از پرداخت، عکس رسید را ارسال کنید."
        )


# =====================
# دریافت رسید
# =====================

async def receipt(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    text = (
        "💳 رسید جدید\n\n"
        f"👤 نام: {user.first_name}\n"
        f"🆔 آیدی: {user.id}\n\n"
        f"/send {user.id}"
    )

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=
        update.message.photo[-1].file_id,
        caption=text
    )

    await update.message.reply_text(
        "✅ رسید شما ارسال شد."
    )


# =====================
# ارسال کانفیگ
# =====================

async def send_vpn(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if update.effective_user.id != ADMIN_ID:

        return

    if len(context.args) < 2:

        await update.message.reply_text(
            "فرمت:\n"
            "/send userid config"
        )

        return

    try:

        user_id = int(
            context.args[0]
        )

        config = " ".join(
            context.args[1:]
        )

        await context.bot.send_message(
            chat_id=user_id,
            text=
            "🔐 اشتراک شما فعال شد\n\n"
            + config
        )

        await update.message.reply_text(
            "✅ کانفیگ ارسال شد."
        )

    except Exception as e:

        await update.message.reply_text(
            f"❌ خطا:\n{e}"
        )


# =====================
# آمار
# =====================

async def stats(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if update.effective_user.id != ADMIN_ID:
        return

    cursor.execute(
        "SELECT COUNT(*) FROM users"
    )

    count = cursor.fetchone()[0]

    await update.message.reply_text(
        f"👥 تعداد کاربران:\n{count}"
    )


# =====================
# اجرا
# =====================

def main():

    app = (
        Application
        .builder()
        .token(TOKEN)
        .build()
    )

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
        CommandHandler(
            "send",
            send_vpn
        )
    )

    app.add_handler(
        CommandHandler(
            "stats",
            stats
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            button
        )
    )

    app.add_handler(
        MessageHandler(
            filters.PHOTO,
            receipt
        )
    )

    print(
        "Bot Started..."
    )

    app.run_polling()


if __name__ == "__main__":
    main()
