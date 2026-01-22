import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

QUESTIONS = [
    {
        "q": "1) Iqtisodiy nazariyaning qaysi oqimida savdo-sotiq va asosan tashqi savdo barcha boyliklarning manbai deb hisoblanadi?",
        "options": ["Merkantilizm", "Fiziokratlar", "Klassik burjua iqtisodiy maktabi", "Marjinalizm"],
        "answer": 0
    },
    {
        "q": "2) Hozirgi zamon iqtisodiy nazariyasining qaysi oqimida iqtisodiy o‘sishni ta'minlashning va tartibga solishning asosiy vositasi pul deb hisoblanadi?",
        "options": ["Keynschilar", "Monetarizm", "Institutsionalizm", "Liberalizm"],
        "answer": 1
    },
]

def keyboard(options):
    letters = ["A", "B", "C", "D"]
    buttons = []
    for i, opt in enumerate(options):
        buttons.append([InlineKeyboardButton(f"{letters[i]}) {opt}", callback_data=str(i))])
    return InlineKeyboardMarkup(buttons)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom 😊\nTestni boshlash uchun /quiz yozing ✅")

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["i"] = 0
    context.user_data["score"] = 0
    q = QUESTIONS[0]
    await update.message.reply_text(q["q"], reply_markup=keyboard(q["options"]))

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    i = context.user_data.get("i", 0)
    score = context.user_data.get("score", 0)

    selected = int(query.data)
    correct = QUESTIONS[i]["answer"]

    if selected == correct:
        score += 1
        await query.edit_message_text("✅ To‘g‘ri!")
    else:
        await query.edit_message_text(f"❌ Xato! To‘g‘ri javob: {['A','B','C','D'][correct]}")

    context.user_data["score"] = score
    i += 1
    context.user_data["i"] = i

    if i >= len(QUESTIONS):
        await query.message.reply_text(f"🎯 Tugadi!\n✅ To‘g‘ri: {score}\n❌ Xato: {len(QUESTIONS)-score}")
        await query.message.reply_text("Yana boshlash: /quiz ✅")
    else:
        q = QUESTIONS[i]
        await query.message.reply_text(q["q"], reply_markup=keyboard(q["options"]))

def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN topilmadi! Render ichida Environment Variables ga qo‘ying.")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("quiz", quiz))
    app.add_handler(CallbackQueryHandler(handle))

    print("✅ Bot ishlayapti...")
    app.run_polling()

if name == "main":
    main()
