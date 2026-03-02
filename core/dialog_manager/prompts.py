from __future__ import annotations


class Copy:
    """
    Uzbek receptionist-style copy for Safra.
    Short, clear, friendly.
    """

    GREETING = "Assalomu alaykum! Safra stomatologiya klinikasiga xush kelibsiz. Qanday yordam bera olaman?"
    ASK_SERVICE = "Qaysi xizmat kerak: konsultatsiya, tish davolash yoki tish tozalash?"
    ASK_DATE = "Qaysi kunga yozay: bugunmi yoki ertagami? (yoki sana: YYYY-MM-DD)"
    ASK_TIME = "Qaysi vaqt qulay? Masalan: 10:00 yoki 15:00."
    ASK_NAME = "Ismingizni ayting, iltimos."
    CONFIRM_BOOKING = "Tasdiqlaysizmi: {date} kuni soat {time}, xizmat: {service}, doktor: {doctor}?"
    BOOKED = "Ajoyib! Bron qilindi: {date} soat {time}. Kelganingizda registratsiya qilamiz."
    SLOT_ALT = "Bu vaqt band. Sizga mana bu variantlar mos keladimi: {slots}?"
    LOCATION = "Manzil: {address}. Mo‘ljal: {landmark}."
    PREP = "Tayyorgarlik: {instructions}"
    PRICE_POLICY = "Narx ko‘rikdan keyin aniq bo‘ladi. Xohlasangiz, ko‘rik uchun vaqt bron qilib beraman."
    HANDOFF = "Tushunarli. Hozir operatorga ulayman. Iltimos, kuting."
    RECOVERY = "Kechirasiz, to‘liq tushunmadim. Qaytadan ayta olasizmi?"