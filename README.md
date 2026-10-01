<div align="center">

<img src="logo.svg" width="120" alt="Super JinX">

# 🛡️ Super JinX Panel

**پنل نمایندگی رایگان و ضدسانسور، بر پایه‌ی پاسارگاد · نصب خودکار روی Railway**

![Free](https://img.shields.io/badge/Price-Free-37e66f?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-5.0.0-20a4ff?style=for-the-badge)
![Railway](https://img.shields.io/badge/Deploy-Railway-0B0D0E?style=for-the-badge&logo=railway&logoColor=white)
![PasarGuard](https://img.shields.io/badge/Based%20on-PasarGuard-1e3a8a?style=for-the-badge)
![Xray](https://img.shields.io/badge/Core-Xray-7c4dff?style=for-the-badge)

### 📣 [کانال رسمی جینکس | 𝙎𝙪𝙥𝙚𝙧 𝗝𝗶𝗻𝗫](https://t.me/+WvKFv0lU_i5lNGE0)

</div>

---

## 📋 فهرست

- 📖 [معرفی](#-معرفی)
  - 🤔 [چرا Super JinX؟](#-چرا-super-jinx)
  - ✨ [امکانات](#-امکانات)
- 🚀 [نصب](#-نصب)
- 🔐 [ورود](#-ورود)
- 🔗 [لینک اشتراک و کانفیگ‌ها](#-لینک-اشتراک-و-کانفیگها)
- 👥 [پنل نمایندگی](#-پنل-نمایندگی)
- 📚 [مستندات](#-مستندات)
- 💬 [پشتیبانی](#-پشتیبانی)

---

# 📖 معرفی

> **Super JinX چیه؟**

Super JinX یه نسخه‌ی آماده و بهینه‌شده از پنل **پاسارگاد** برای Railway هست. پنل، هسته‌ی **Xray** و **nginx** همه داخل یه سرویس اجرا میشن. با اولین Deploy همه چیز خودکار ساخته میشه و لازم نیست حتی یه تنظیم دستی انجام بدی.

---

## 🤔 چرا Super JinX؟

> **ساده، سریع، بی‌دردسر**

پنل‌های معمولی رو باید روی VPS نصب کنی، اینباند بسازی، هاست تنظیم کنی، گروه درست کنی و کلی کار دیگه. توی Super JinX فقط ریپو رو به Railway وصل می‌کنی و بعد از چند دقیقه یه پنل نمایندگی کامل با ۵ کانفیگ آماده تحویل می‌گیری.

---

### ✨ امکانات

**🌐 پنل و API**
- داشبورد کامل پاسارگاد (فارسی)
- REST API کامل
- همه چیز در **یک سرویس** روی پورت 8080، بدون نصب نود جدا

**⚡ کانفیگ‌ها**
- **۵ کانفیگ VLESS + WebSocket + TLS** روی پورت 443
- `alpn=http/1.1` برای بهترین سازگاری با Railway
- **Early Data (`ed=2560`)**: یه رفت‌وبرگشت کمتر در هر اتصال، یعنی پینگ کمتر
- هر کانفیگ مسیر، اثرانگشت TLS (Chrome، Firefox، Safari، Edge، iOS) و اسم مخصوص خودش رو داره
- کاربری که بدون گروه ساخته بشه، **خودکار** هر ۵ کانفیگ رو می‌گیره

**👥 مدیریت کاربر و نمایندگی**
- نقش آماده‌ی **«نماینده»** با سهمیه‌ی حجم
- هر نماینده فقط کاربرهای خودش رو می‌بینه
- قالب‌های فروش آماده: 10، 30، 50، 100 گیگ (۳۰ روزه)، 200 گیگ (۶۰ روزه) و نامحدود
- محدودیت حجم و تاریخ انقضا

**🔗 اشتراک**
- صفحه‌ی ساب اختصاصی جینکس با حلقه‌ی مصرف، حجم باقی‌مانده، روزهای باقی‌مانده و تاریخ انقضا به تقویم شمسی
- **QR داخلی** (بدون سرویس بیرونی) با امکان ذخیره‌ی عکس
- اتصال با یک لمس برای **V2Box، v2rayNG، Hiddify، Streisand، Happ و NekoBox**
- سازگار با V2ray، Clash، ClashMeta و sing-box

**🛠️ پایداری**
- خودترمیم: با هر ری‌استارت همه چیز چک و اصلاح میشه
- Health Check داخلی برای nginx و پنل
- همه‌ی پورت‌های داخلی فقط روی `127.0.0.1`

---

# 🚀 نصب

> **نصب سریع**: حدود ۵ دقیقه

1. همه‌ی فایل‌ها رو یکجا داخل یه ریپوی **GitHub** آپلود کن (**Add file ← Upload files**). پوشه نداره.
2. در [Railway](https://railway.com) بزن **New Project ← Deploy from GitHub repo** و ریپو رو انتخاب کن.
3. **Settings ← Networking ← Generate Domain** و پورت رو **`8080`** بذار.
4. یه **Volume** با مسیر **`/var/lib/pasarguard`** وصل کن.
5. **Region** رو بذار روی **EU West (Amsterdam)** تا پینگ کمتر بشه.
6. یک بار **Redeploy** کن. 🎉

📖 راهنمای کامل تصویری: [INSTALL.md](INSTALL.md)

---

# 🔐 ورود

| | آدرس | نام کاربری | رمز |
|---|---|---|---|
| 👑 مالک | `https://YOUR-DOMAIN/dashboard/` | `admin` | `admin` |
| 🤝 نماینده‌ی نمونه (۵۰ گیگ) | `https://YOUR-DOMAIN/dashboard/` | `reseller` | `reseller` |

> رمز مالک همیشه `admin` هست و با هر ری‌استارت دوباره روی همین تنظیم میشه.

---

# 🔗 لینک اشتراک و کانفیگ‌ها

```
https://YOUR-DOMAIN/sub/<token>
```

| # | اسم | مسیر | اثرانگشت |
|---|---|---|---|
| 1 | 🚀 Turbo | `/ws/…` | chrome |
| 2 | ⚡ Flash | `/stream/…` | firefox |
| 3 | 🔥 Fire | `/live/…` | safari |
| 4 | 💎 Diamond | `/gw/…` | edge |
| 5 | 🌙 Night | `/cdn/…` | ios |

نمونه:

```
vless://<uuid>@YOUR-DOMAIN:443?type=ws&path=%2Fws%2F<id>%3Fed%3D2560&security=tls&sni=YOUR-DOMAIN&host=YOUR-DOMAIN&alpn=http%2F1.1&fp=chrome&encryption=none#🚀 Turbo | جینکس
```

---

# 👥 پنل نمایندگی

1. با `admin` وارد شو ← **مدیران ← افزودن مدیر**
2. نقش: **نماینده** · سهمیه‌ی حجم: مثلاً **50 GB**
3. ذخیره کن و یوزر و رمز رو به نماینده بده

**ساخت کاربر:** **کاربران ← ساخت کاربر ←** یه قالب انتخاب کن ← ذخیره. هر ۵ کانفیگ خودکار وصل میشن.

---

# 📚 مستندات

| | |
|---|---|
| 🚀 [INSTALL.md](INSTALL.md) | نصب قدم‌به‌قدم |
| ❓ [FAQ.md](FAQ.md) | پینگ قرمز، تغییر رمز، نماینده و... |
| 🩺 [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | حل خطاهای Railway |
| 📝 [CHANGELOG.md](CHANGELOG.md) | تغییرات هر نسخه |
| 🔒 [SECURITY.md](SECURITY.md) | نکات امنیتی |
| ⚙️ [env.example](env.example) | متغیرهای اختیاری |

---

# 💬 پشتیبانی

<div align="center">

### 📣 [عضویت در کانال جینکس | 𝙎𝙪𝙥𝙚𝙧 𝗝𝗶𝗻𝗫](https://t.me/+WvKFv0lU_i5lNGE0)

آپدیت‌ها · آموزش‌ها · پشتیبانی

⭐ اگه به کارت اومد، به ریپو **Star** بده

---

ساخته‌شده با ❤️ برای اینترنت آزاد، توسط تیم **جینکس** با کمک **ClickUp Brain** 🧠

بر پایه‌ی [PasarGuard](https://github.com/PasarGuard/panel) · مجوز [AGPL-3.0](https://github.com/PasarGuard/panel/blob/main/LICENSE)

</div>
