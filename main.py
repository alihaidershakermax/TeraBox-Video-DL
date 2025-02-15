import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import os
from datetime import datetime, timedelta

# ✅ ضع توكن البوت هنا
TOKEN = "7817440343:AAFEAXnRaRxv3STLGx5N9_8kBasy4fvvFLw"

# ✅ ضع معرف المسؤول (ID الخاص بك) لمنع المستخدمين العاديين من تعديل الأسماء
ADMIN_ID = 960173511 # استبدل هذا بـ Telegram ID الخاص بك

# ✅ اسم الملف الذي سيتم تخزين الأسماء فيه
FILE_NAME = "students.txt"

# ✅ معرف القناة الخاصة
CHANNEL_ID = -1002475274978  # استبدل هذا بمعرف القناة الخاصة

# ✅ إعداد البوت
bot = Bot(token=TOKEN)
dp = Dispatcher()

# ✅ تفعيل تسجيل الأخطاء
logging.basicConfig(level=logging.INFO)

# 📌 تخزين آخر رسالة تم التحقق منها
last_checked_message_id = None

# 📌 إنشاء ملف الأسماء تلقائيًا عند بدء التشغيل إذا لم يكن موجودًا
def ensure_file_exists():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            file.write("")  # إنشاء ملف فارغ

# 📌 تحميل الأسماء من الملف النصي
def load_names():
    ensure_file_exists()
    with open(FILE_NAME, "r", encoding="utf-8") as file:
        return [line.strip().lower() for line in file.readlines() if line.strip()]

# 📌 حفظ الأسماء في الملف النصي
def save_names(names_list):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        file.write("\n".join(names_list))

# 📌 استقبال الاسم الثلاثي من المستخدم
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("مرحبًا! الرجاء إرسال اسمك الثلاثي كما هو في السجلات الجامعية للتحقق من تسجيلك:")

# 📌 التحقق من الاسم الثلاثي في الملف النصي
@dp.message()
async def check_name(message: types.Message):
    name_to_check = message.text.strip().lower()
    names_list = load_names()

    # ✅ التحقق من أن الاسم يحتوي على 3 كلمات على الأقل
    if len(name_to_check.split()) < 3:
        await message.answer("⚠️ يجب إدخال الاسم الثلاثي كاملًا.")
        return

    if name_to_check in names_list:
        await message.answer("✅ تم العثور على اسمك في القائمة! أنت مسجل في النظام.")
    else:
        await message.answer("❌ عذرًا، لم يتم العثور على اسمك في القائمة.")

# 📌 التحقق من القناة الخاصة كل 5 ثوانٍ
async def check_channel_periodically():
    global last_checked_message_id

    while True:
        try:
            # ✅ الحصول على آخر رسالة في القناة
            messages = await bot.get_chat_history(chat_id=CHANNEL_ID, limit=10)  # الحصول على آخر 10 رسائل
            if messages:
                for message in messages:
                    # ✅ التحقق من أن الرسالة جديدة
                    if last_checked_message_id is None or message.message_id > last_checked_message_id:
                        last_checked_message_id = message.message_id

                        # ✅ استخراج الأسماء من الرسالة
                        names_in_message = message.text.splitlines()
                        names_list = load_names()
                        new_names = []

                        for name in names_in_message:
                            name = name.strip().lower()
                            if name and name not in names_list:
                                names_list.append(name)
                                new_names.append(name)

                        # ✅ حفظ الأسماء الجديدة
                        if new_names:
                            save_names(names_list)
                            await bot.send_message(
                                chat_id=ADMIN_ID,
                                text=f"✅ تمت إضافة الأسماء التالية تلقائيًا:\n{', '.join(new_names)}"
                            )

        except Exception as e:
            logging.error(f"حدث خطأ أثناء التحقق من القناة: {e}")

        # ✅ الانتظار لمدة 5 ثوانٍ قبل التحقق مرة أخرى
        await asyncio.sleep(5)

# ✅ تشغيل البوت
async def main():
    ensure_file_exists()  # إنشاء الملف تلقائيًا عند بدء التشغيل
    asyncio.create_task(check_channel_periodically())  # بدء التحقق الدوري
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
