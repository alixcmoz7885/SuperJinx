# 🚀 نصب Super JinX روی Railway

## پیش‌نیاز
- اکانت [GitHub](https://github.com)
- اکانت [Railway](https://railway.com)

## مراحل
1. **ریپو:** همه‌ی فایل‌ها رو یکجا داخل یه ریپوی جدید GitHub آپلود کن (Add file ← Upload files). هیچ پوشه‌ای لازم نیست.
2. **Deploy:** در Railway بزن **New Project ← Deploy from GitHub repo** و ریپو رو انتخاب کن.
3. **دامنه:** **Settings ← Networking ← Generate Domain** و پورت رو **8080** بذار.
4. **Volume:** روی سرویس راست‌کلیک کن ← **Attach Volume** و مسیر رو **`/var/lib/pasarguard`** بذار.
5. **Region:** **Settings ← Deploy ← Region ← EU West (Amsterdam)**.
6. **Redeploy:** یک بار از تب Deployments بزن Redeploy.

## بعد از نصب
- پنل: `https://YOUR-DOMAIN/dashboard/` با `admin` / `admin`
- در Deploy Logs باید خط `[bootstrap] DONE` رو ببینی.

## ساخت کاربر
**کاربران ← ساخت کاربر**، یه قالب حجم انتخاب کن (مثلاً 30GB - 30 روز) و ذخیره کن. ۵ کانفیگ خودکار بهش وصل میشه، حتی اگه گروه رو انتخاب نکنی.
