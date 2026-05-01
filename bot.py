
import random
import string
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# --- كود الحل لمنصة Render (حطه هنا بالبداية) ---
app = Flask('')

@app.route('/')
def home():
 return "Bot is Running!"

def run():
    # سطر مهم عشان Render يلقى المنفذ وما يقفل البوت
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

# تشغيل الخادم الوهمي
keep_alive()
# --------------------------------------------

# التوكن وآيدي القسم
BOT_TOKEN = "8749223377:AAHXI2uTJX8EwXshLwMHa8Dc4zLLORPjxU8"
TOPIC_ID = 74

# بقية كودك (دالة generate_super_random_email) تبدأ من هنا...

def generate_super_random_email(word):
    # خيارات متنوعة للإضافات
    years = [str(i) for i in range(1985, 2015)]
    short_nums = [str(i) for i in range(1, 100)]
    cool_words = ["pro", "vip", "king", "live", "cool", "official", "boss", "user"]
    chars = string.ascii_lowercase # حروف عشوائية
    
    # قائمة بالأدوات اللي نستخدمها للربط
    separators = ["", ".", "_", "__"]
    
    # خلط المكونات: يختار بشكل عشوائي وش يضيف وكيف يربط
    mix_type = random.randint(1, 5)
    
    if mix_type == 1: # كلمة + سنة (مثال: word1995)
        res = f"{word}{random.choice(years)}"
    elif mix_type == 2: # كلمة + فاصل + رقمين (مثال: word_99)
        res = f"{word}{random.choice(separators)}{random.choice(short_nums)}"
    elif mix_type == 3: # كلمة + فاصل + كلمة ثانية (مثال: word.vip)
        res = f"{word}{random.choice(separators)}{random.choice(cool_words)}"
    elif mix_type == 4: # كلمة + حرفين عشوائية + رقم (مثال: wordax7)
        random_chars = ''.join(random.choices(chars, k=2))
        res = f"{word}{random_chars}{random.choice(short_nums)}"
    else: # خلطة معقدة (مثال: word_king88)
        res = f"{word}{random.choice(separators)}{random.choice(cool_words)}{random.choice(short_nums)}"
        
    return f"{res}@hotmail.com"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.message_thread_id == TOPIC_ID:
        word = update.message.text.strip()
        file_name = f"{word}_list.txt"
        
        with open(file_name, "w") as f:
            # ننتج 100 إيميل، كل واحد له نمط وخلطة مختلفة عن اللي قبله
            for _ in range(100):
                f.write(generate_super_random_email(word) + "\n")
        
        try:
            with open(file_name, "rb") as doc:
                await context.bot.send_document(
                    chat_id=update.effective_chat.id, 
                    document=doc,
                    message_thread_id=TOPIC_ID
                )
            os.remove(file_name)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("البوت شغال بنظام الخلط العشوائي.. جربه الآن!")
    app.run_polling()