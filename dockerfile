# استخدم صورة Python الرسمية كصورة أساسية
FROM python:3.9-slim-buster

# قم بتعيين دليل العمل داخل الحاوية
WORKDIR /app

# انسخ ملفات الاعتماديات (requirements.txt) إذا كانت موجودة
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# انسخ باقي ملفات المشروع إلى دليل العمل
COPY . .

# قم بتعيين متغيرات البيئة (إذا كنت تستخدمها)
ENV TOKEN="7817440343:AAFEAXnRaRxv3STLGx5N9_8kBasy4fvvFLw"
ENV ADMIN_ID=960173511
ENV CHANNEL_ID=-1002475274978
ENV FILE_NAME="students.txt"

# قم بتشغيل البوت
CMD ["python", "main.py"]
