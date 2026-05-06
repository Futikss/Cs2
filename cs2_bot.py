"""
CS2 Case Opening Bot — To'liq versiya
======================================
pip install python-telegram-bot==20.7
"""

import random, json, os
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN  = "YOUR_BOT_TOKEN_HERE"   # <-- o'zgartiring
WEBAPP_URL = "YOUR_WEBAPP_URL_HERE"  # <-- o'zgartiring (GitHub Pages / Vercel)

DB_FILE = "users.json"

# ── DB ────────────────────────────────────────────────────────────────────────
def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE) as f: return json.load(f)
    return {}

def save_db(db):
    with open(DB_FILE, "w") as f: json.dump(db, f, ensure_ascii=False, indent=2)

def get_user(db, uid):
    k = str(uid)
    if k not in db:
        db[k] = {"balance": 2000, "inventory": [], "opened": 0, "name": ""}
    return db[k]

# ── CASES ─────────────────────────────────────────────────────────────────────
CASES = {
    "🔵 Prisma Case": {
        "price": 200, "emoji": "🔵",
        "skins": [
            {"name":"Glock-18 | Off World",           "rarity":"Consumer",   "emoji":"⚪","price":50},
            {"name":"MP9 | Hot Rod",                  "rarity":"Consumer",   "emoji":"⚪","price":60},
            {"name":"Five-SeveN | Kami",              "rarity":"Consumer",   "emoji":"⚪","price":55},
            {"name":"AK-47 | Uncharted",              "rarity":"Industrial", "emoji":"🔵","price":150},
            {"name":"M4A1-S | Nightmare",             "rarity":"Industrial", "emoji":"🔵","price":160},
            {"name":"AWP | Atheris",                  "rarity":"Mil-Spec",   "emoji":"🟣","price":400},
            {"name":"Desert Eagle | Trigger Disc.",   "rarity":"Mil-Spec",   "emoji":"🟣","price":380},
            {"name":"AK-47 | Asiimov",                "rarity":"Restricted", "emoji":"🟠","price":1200},
            {"name":"M4A4 | Buzz Kill",               "rarity":"Restricted", "emoji":"🟠","price":1100},
            {"name":"AWP | Hyper Beast",              "rarity":"Classified", "emoji":"🔴","price":4000},
            {"name":"AK-47 | Neon Rider",             "rarity":"Covert",     "emoji":"🟡","price":12000},
            {"name":"★ Karambit | Doppler",           "rarity":"Knife",      "emoji":"✨","price":55000},
        ]
    },
    "🟠 Fracture Case": {
        "price": 250, "emoji": "🟠",
        "skins": [
            {"name":"USP-S | Cortex",                 "rarity":"Consumer",   "emoji":"⚪","price":70},
            {"name":"MP5-SD | Phosphor",              "rarity":"Consumer",   "emoji":"⚪","price":65},
            {"name":"Tec-9 | Snek-9",                 "rarity":"Industrial", "emoji":"🔵","price":180},
            {"name":"Five-SeveN | Angry Mob",         "rarity":"Industrial", "emoji":"🔵","price":170},
            {"name":"AK-47 | Legion of Anubis",       "rarity":"Mil-Spec",   "emoji":"🟣","price":450},
            {"name":"M4A1-S | Mainframe 001",         "rarity":"Mil-Spec",   "emoji":"🟣","price":420},
            {"name":"Desert Eagle | Printstream",     "rarity":"Restricted", "emoji":"🟠","price":2000},
            {"name":"AWP | Exoskeleton",              "rarity":"Restricted", "emoji":"🟠","price":1800},
            {"name":"AK-47 | Ice Coaled",             "rarity":"Classified", "emoji":"🔴","price":6000},
            {"name":"M4A4 | Cyber Security",          "rarity":"Covert",     "emoji":"🟡","price":15000},
            {"name":"★ Butterfly | Tiger Tooth",      "rarity":"Knife",      "emoji":"✨","price":65000},
        ]
    },
    "🟡 Revolution Case": {
        "price": 300, "emoji": "🟡",
        "skins": [
            {"name":"MAC-10 | Monkeyflage",           "rarity":"Consumer",   "emoji":"⚪","price":80},
            {"name":"Nova | Sobaka",                  "rarity":"Consumer",   "emoji":"⚪","price":75},
            {"name":"UMP-45 | Wild Child",            "rarity":"Industrial", "emoji":"🔵","price":200},
            {"name":"Glock-18 | Umbral Rabbit",       "rarity":"Mil-Spec",   "emoji":"🟣","price":500},
            {"name":"M4A1-S | Emphorosaur-S",         "rarity":"Restricted", "emoji":"🟠","price":2500},
            {"name":"AK-47 | Head Shot",              "rarity":"Classified", "emoji":"🔴","price":8000},
            {"name":"AWP | Duality",                  "rarity":"Covert",     "emoji":"🟡","price":20000},
            {"name":"★ M9 Bayonet | Fade",            "rarity":"Knife",      "emoji":"✨","price":80000},
        ]
    },
    "🔪 Knife Case": {
        "price": 500, "emoji": "🔪",
        "skins": [
            {"name":"P250 | Valence",                 "rarity":"Consumer",   "emoji":"⚪","price":90},
            {"name":"MP7 | Whiteout",                 "rarity":"Industrial", "emoji":"🔵","price":220},
            {"name":"AK-47 | Safari Mesh",            "rarity":"Mil-Spec",   "emoji":"🟣","price":600},
            {"name":"AWP | Safari Mesh",              "rarity":"Restricted", "emoji":"🟠","price":2200},
            {"name":"M4A4 | Desert Storm",            "rarity":"Classified", "emoji":"🔴","price":7000},
            {"name":"★ Karambit | Fade",              "rarity":"Knife",      "emoji":"✨","price":90000},
            {"name":"★ M9 Bayonet | Doppler",         "rarity":"Knife",      "emoji":"✨","price":75000},
            {"name":"★ Butterfly | Doppler",          "rarity":"Knife",      "emoji":"✨","price":85000},
            {"name":"★ Talon | Crimson Web",          "rarity":"Knife",      "emoji":"✨","price":60000},
            {"name":"★ Stiletto | Tiger Tooth",       "rarity":"Knife",      "emoji":"✨","price":50000},
        ]
    },
    "🧤 Gloves Case": {
        "price": 400, "emoji": "🧤",
        "skins": [
            {"name":"Glock-18 | Groundwater",         "rarity":"Consumer",   "emoji":"⚪","price":60},
            {"name":"MP9 | Bulldozer",                "rarity":"Industrial", "emoji":"🔵","price":190},
            {"name":"Five-SeveN | Hot Shot",          "rarity":"Mil-Spec",   "emoji":"🟣","price":480},
            {"name":"USP-S | Stainless",              "rarity":"Restricted", "emoji":"🟠","price":1900},
            {"name":"AK-47 | Jaguar",                 "rarity":"Classified", "emoji":"🔴","price":7500},
            {"name":"AWP | Graphite",                 "rarity":"Covert",     "emoji":"🟡","price":18000},
            {"name":"★ Sport Gloves | Pandora's Box", "rarity":"Gloves",     "emoji":"🧤","price":95000},
            {"name":"★ Specialist Gloves | Crimson W","rarity":"Gloves",     "emoji":"🧤","price":80000},
            {"name":"★ Moto Gloves | Eclipse",        "rarity":"Gloves",     "emoji":"🧤","price":70000},
            {"name":"★ Bloodhound Gloves | Charred",  "rarity":"Gloves",     "emoji":"🧤","price":65000},
        ]
    },
}

WEIGHTS = {
    "Consumer":40,"Industrial":30,"Mil-Spec":15,
    "Restricted":9,"Classified":4,"Covert":1.5,
    "Knife":0.4,"Gloves":0.1
}

RARITY_BAR = {
    "Consumer":"▓░░░░░░","Industrial":"▓▓░░░░░","Mil-Spec":"▓▓▓░░░░",
    "Restricted":"▓▓▓▓░░░","Classified":"▓▓▓▓▓░░","Covert":"▓▓▓▓▓▓░",
    "Knife":"▓▓▓▓▓▓▓","Gloves":"▓▓▓▓▓▓▓"
}

def spin_case(case_name):
    skins = CASES[case_name]["skins"]
    w = [WEIGHTS[s["rarity"]] for s in skins]
    return random.choices(skins, weights=w, k=1)[0]

# ── HANDLERS ──────────────────────────────────────────────────────────────────
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    db = load_db()
    user = get_user(db, update.effective_user.id)
    user["name"] = update.effective_user.first_name or "O'yinchi"
    save_db(db)
    kb = [
        [InlineKeyboardButton("📦 Case ochish", callback_data="menu_cases")],
        [InlineKeyboardButton("🎰 Ruletka", web_app=WebAppInfo(url=WEBAPP_URL))],
        [InlineKeyboardButton("🎒 Inventar", callback_data="inventory"),
         InlineKeyboardButton("💰 Balans",   callback_data="balance")],
        [InlineKeyboardButton("🏆 Top",      callback_data="top"),
         InlineKeyboardButton("🎁 Bonus",    callback_data="get_bonus")],
    ]
    await update.message.reply_text(
        f"🎮 *CS2 Case Simulator*\n\n"
        f"Salom, *{user['name']}*! 👋\n"
        f"💰 Balans: *{user['balance']:,} coin*\n"
        f"📦 Ochilgan: *{user['opened']} ta*\n\n"
        f"📦 Case — bot ichida oching\n"
        f"🎰 Ruletka — WebApp da o'ynang",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(kb)
    )

async def button(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    d = q.data
    db = load_db()
    user = get_user(db, q.from_user.id)

    # ── Case menyusi
    if d == "menu_cases":
        kb = []
        for cname, cd in CASES.items():
            kb.append([InlineKeyboardButton(f"{cname} — {cd['price']} coin", callback_data=f"open_{cname}")])
        kb.append([InlineKeyboardButton("🔙 Orqaga", callback_data="back")])
        await q.edit_message_text("📦 *Case tanlang:*", parse_mode="Markdown",
                                  reply_markup=InlineKeyboardMarkup(kb))

    # ── Case ochish
    elif d.startswith("open_"):
        cname = d[5:]
        if cname not in CASES: return
        price = CASES[cname]["price"]
        if user["balance"] < price:
            await q.edit_message_text(
                f"❌ *Balans yetarli emas!*\n\n💰 Sizda: {user['balance']:,}\n📦 Narx: {price:,}",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🎁 Bonus ol", callback_data="get_bonus"),
                    InlineKeyboardButton("🔙 Orqaga",   callback_data="menu_cases")
                ]])
            ); return
        user["balance"] -= price
        user["opened"]  += 1
        skin = spin_case(cname)
        user["inventory"].append(skin)
        save_db(db)

        kb = [
            [InlineKeyboardButton(f"🔄 Yana ({price} coin)", callback_data=f"open_{cname}")],
            [InlineKeyboardButton("💰 Sot",        callback_data="sell_last"),
             InlineKeyboardButton("📦 Boshqa case",callback_data="menu_cases")],
            [InlineKeyboardButton("🏠 Bosh menyu", callback_data="back")],
        ]
        await q.edit_message_text(
            f"📦 *{cname}* ochildi!\n"
            f"━━━━━━━━━━━━━━━━\n"
            f"{skin['emoji']} *{skin['name']}*\n"
            f"🎖 {skin['rarity']} {RARITY_BAR.get(skin['rarity'],'')}\n"
            f"💵 Qiymati: *{skin['price']:,} coin*\n"
            f"━━━━━━━━━━━━━━━━\n"
            f"💰 Qolgan: *{user['balance']:,} coin*",
            parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb)
        )

    # ── Sotish
    elif d == "sell_last":
        if user["inventory"]:
            s = user["inventory"].pop()
            user["balance"] += s["price"]
            save_db(db)
            await q.answer(f"✅ {s['name']} — {s['price']:,} coin ga sotildi!", show_alert=True)
        else:
            await q.answer("Inventar bo'sh!", show_alert=True)

    # ── Inventar
    elif d == "inventory":
        inv = user["inventory"]
        if not inv:
            txt = "🎒 *Inventar bo'sh!*"
        else:
            total = sum(s["price"] for s in inv)
            items = "\n".join(f"{s['emoji']} {s['name']} — {s['price']:,}" for s in inv[-10:])
            txt = f"🎒 *Inventar* (oxirgi 10)\n\n{items}\n\n💰 Jami: *{total:,} coin*"
        await q.edit_message_text(txt, parse_mode="Markdown",
                                  reply_markup=InlineKeyboardMarkup([[
                                      InlineKeyboardButton("🔙 Orqaga", callback_data="back")
                                  ]]))

    # ── Balans
    elif d == "balance":
        iv = sum(s["price"] for s in user["inventory"])
        await q.edit_message_text(
            f"💰 *Moliyaviy holat*\n\n"
            f"🪙 Balans: *{user['balance']:,}*\n"
            f"🎒 Inventar: *{iv:,}*\n"
            f"💎 Jami: *{user['balance']+iv:,}*\n"
            f"📦 Ochilgan: *{user['opened']} ta*",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🎁 Bonus", callback_data="get_bonus"),
                InlineKeyboardButton("🔙 Orqaga",callback_data="back")
            ]])
        )

    # ── Bonus
    elif d == "get_bonus":
        bonus = random.randint(400, 1000)
        user["balance"] += bonus
        save_db(db)
        await q.answer(f"🎁 +{bonus} coin!", show_alert=True)

    # ── Top
    elif d == "top":
        db2 = load_db()
        ranked = sorted(db2.items(),
            key=lambda x: x[1].get("balance",0)+sum(s["price"] for s in x[1].get("inventory",[])),
            reverse=True)[:10]
        medals = ["🥇","🥈","🥉"]+["🏅"]*7
        lines = [f"{medals[i]} {v.get('name','O\'yinchi')} — {v.get('balance',0)+sum(s['price'] for s in v.get('inventory',[])):,}"
                 for i,(k,v) in enumerate(ranked)]
        await q.edit_message_text(
            "🏆 *Top 10*\n\n" + "\n".join(lines),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Orqaga",callback_data="back")]])
        )

    # ── Bosh menyu
    elif d == "back":
        kb = [
            [InlineKeyboardButton("📦 Case ochish", callback_data="menu_cases")],
            [InlineKeyboardButton("🎰 Ruletka", web_app=WebAppInfo(url=WEBAPP_URL))],
            [InlineKeyboardButton("🎒 Inventar", callback_data="inventory"),
             InlineKeyboardButton("💰 Balans",   callback_data="balance")],
            [InlineKeyboardButton("🏆 Top",      callback_data="top"),
             InlineKeyboardButton("🎁 Bonus",    callback_data="get_bonus")],
        ]
        await q.edit_message_text(
            f"🎮 *CS2 Case Simulator*\n\n💰 Balans: *{user['balance']:,}*\n📦 Ochilgan: *{user['opened']}*",
            parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb)
        )
    save_db(db)

async def bonus_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    db = load_db(); user = get_user(db, update.effective_user.id)
    b = random.randint(400, 1000); user["balance"] += b; save_db(db)
    await update.message.reply_text(f"🎁 +{b} coin! Balans: *{user['balance']:,}*", parse_mode="Markdown")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("bonus", bonus_cmd))
    app.add_handler(CallbackQueryHandler(button))
    print("✅ Bot ishga tushdi!")
    app.run_polling()

if __name__ == "__main__":
    main()
