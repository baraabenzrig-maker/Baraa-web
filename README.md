# SocialApp - دردشة + مكالمات فيديو

مشروع أولي يجمع بين الدردشة الفورية (مثل واتساب/ماسنجر) ومكالمات الفيديو (مثل زوم) باستخدام FastAPI.

## المميزات الحالية
- دردشة فورية جماعية باستخدام WebSocket
- واجهة بسيطة بالعربية
- جاهز للنشر على Render

## التشغيل محلياً

```bash
# إنشاء بيئة افتراضية
python -m venv venv
source venv/bin/activate   # على Linux/Mac
# أو
venv\\Scripts\\activate     # على Windows

# تثبيت المتطلبات
pip install -r requirements.txt

# تشغيل التطبيق
uvicorn app:app --reload
```

افتح المتصفح على: http://127.0.0.1:8000

## النشر على Render

1. ارفع المشروع على GitHub
2. في Render أنشئ Web Service جديد
3. اختر المستودع
4. الإعدادات:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
5. انشر

## الخطوات القادمة
- إضافة غرف دردشة
- إضافة مكالمات فيديو (WebRTC)
- نظام تسجيل دخول
- تغذية اجتماعية
- 
