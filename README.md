# Sadsod Shoes — نسخة جاهزة للنشر (Deploy)

✅ عربي (RTL) — ✅ الجزائر فقط — ✅ الدفع عند الاستلام  
✅ لوحة تحكم كاملة + طلبات + شحن (ولاية/دائرة) + تتبع

---

## 1) تشغيل محلي بسرعة (SQLite)
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt
python app/app.py
```
افتح: http://127.0.0.1:5000  
لوحة التحكم: http://127.0.0.1:5000/admin  
بيانات الدخول: admin / admin123

---

## 2) تشغيل بقاعدة بيانات PostgreSQL عبر Docker (أفضل للنشر)
تحتاج Docker Desktop ثم:
```bash
docker compose up --build
```
افتح: http://127.0.0.1:5000

---

## 3) النشر على استضافة (Render / Railway / VPS)
### A) Render / Railway
- اربط الريبو
- ضع **Start Command**:
`gunicorn -w 2 -b 0.0.0.0:$PORT wsgi:app`
- فعّل متغيرات البيئة:
  - `SADSOD_SECRET` قيمة قوية
  - `DATABASE_URL` (الاستضافة تعطيه لك)

### B) VPS (Ubuntu)
```bash
pip install -r requirements.txt
export SADSOD_SECRET="StrongSecret"
export DATABASE_URL="postgresql://user:pass@host:5432/db"
gunicorn -w 2 -b 0.0.0.0:5000 wsgi:app
```

---

## ملاحظات
- عند أول تشغيل، يتم إنشاء الجداول تلقائياً + إدخال منتجات تجريبية + أسعار توصيل افتراضية.
- يمكنك تعديل أسعار التوصيل من لوحة التحكم (الشحن).
- الدوائر تُضاف من لوحة التحكم (قسم الدوائر) ثم تظهر تلقائياً في Checkout.
