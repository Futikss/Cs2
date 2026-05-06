# CS2 Bot — To'liq O'rnatish Qo'llanmasi
=====================================

## 1-QADAM: BotFather dan bot ochish

1. Telegramda @BotFather ni oching
2. /newbot yozing
3. Botga nom bering (masalan: CS2 Case Bot)
4. Username bering (masalan: cs2case_mybot) — oxiri "bot" tugashi kerak
5. BotFather sizga TOKEN beradi:
   Misol: 7123456789:AAF_abc123XYZ...
   → Bu tokenni saqlang!

6. Guruhga qo'shish uchun:
   /newbot → yaratilgan bot → Settings → Group Privacy → DISABLE qiling
   (Aks holda guruhda ishlamaydi)

---

## 2-QADAM: GitHub Pages ga webapp.html joylash (BEPUL)

1. github.com ga boring, ro'yxatdan o'ting
2. "New repository" bosing
3. Nom bering: cs2-webapp
4. Public tanlang → Create repository
5. "uploading an existing file" bosing
6. webapp.html faylini yuklang → Commit changes
7. Settings → Pages → Branch: main → Save
8. Sizga URL beriladi:
   https://SIZNING_USERNAME.github.io/cs2-webapp/webapp.html
   → Bu URL ni saqlang!

---

## 3-QADAM: Kompyuterda Python o'rnatish

Windows uchun:
1. python.org ga boring → Download → Python 3.11
2. O'rnatishda "Add to PATH" belgilang
3. CMD oching (Win+R → cmd)
4. Tekshiring: python --version

---

## 4-QADAM: Fayllarni sozlash

1. Masalan C:\cs2bot\ papka yarating
2. cs2_bot.py faylini shu papkaga qo'ying
3. webapp.html ni GitHub ga yuklagan bo'lsangiz u yerda qoladi

cs2_bot.py faylini Notepad++ yoki VS Code bilan oching:

   BOT_TOKEN  = "7123456789:AAF_abc123XYZ..."   ← BotFather tokeningiz
   WEBAPP_URL = "https://USERNAME.github.io/cs2-webapp/webapp.html"  ← GitHub URL

---

## 5-QADAM: Kutubxona o'rnatish va botni ishga tushirish

CMD da:
   cd C:\cs2bot
   pip install python-telegram-bot==20.7
   python cs2_bot.py

✅ "Bot ishga tushdi!" ko'rsangiz — tayyor!

---

## 6-QADAM: Botni sinash

1. Telegram da botingizni toping (@username_bot)
2. /start bosing
3. Tugmalar chiqishi kerak:
   📦 Case ochish  →  bot ichida ishlaydi
   🎰 Ruletka      →  WebApp ochiladi (github.com saytingiz)

---

## GURUHGA QO'SHISH

1. Guruhingizni oching → Members → Add member
2. @sizning_botingiz ni qo'shing
3. Admin qiling (kerak emas, lekin /start ishlashi uchun)
4. Guruhda /start bosing — bot javob beradi

---

## BOT DOIM ISHLASHI UCHUN (ixtiyoriy)

Agar kompyuterni o'chirsangiz bot ham to'xtaydi.
Doim ishlashi uchun bepul hosting:

Option 1 — Railway.app:
   railway.app → New Project → Deploy from GitHub
   requirements.txt yarating:
      python-telegram-bot==20.7
   Procfile yarating:
      worker: python cs2_bot.py

Option 2 — Render.com:
   render.com → New → Background Worker → GitHub repo ulang

---

## BUYRUQLAR

   /start  — Bosh menyu
   /bonus  — Bepul coin olish

---

## MUAMMOLAR

❌ "ModuleNotFoundError" → pip install python-telegram-bot==20.7
❌ "Unauthorized"        → BOT_TOKEN noto'g'ri
❌ WebApp ochilmaydi    → WEBAPP_URL noto'g'ri yoki HTTP (HTTPS kerak)
❌ Guruhda ishlamaydi   → Group Privacy ni o'chiring (BotFather da)
