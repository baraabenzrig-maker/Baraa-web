# SocialApp - منصة اجتماعية

مشروع يجمع ميزات من فيسبوك وإنستغرام وواتساب وزوم.

## الميزات الحالية
- تسجيل الدخول والتسجيل
- المنشورات مع الإعجاب والتعليقات
- المجموعات
- القصص
- غرفة الانتظار
- دردشة فورية (WebSocket)
- لوحة آدمن أساسية
- بث مباشر (يمكن توسيعه)

## التشغيل محلياً
```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

افتح: http://127.0.0.1:8000/docs

## النشر على Render
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
- 
