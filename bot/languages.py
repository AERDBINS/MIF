texts = {
    "common": {
        "back_button": "↩️ Ortga",
        "contact_admin": "📞 Admin bilan aloqa"
    },
    "about_center_info": {
        "uz": "... O‘zbekcha matn ...",
        "ru": "... Русский текст ...",
        "en": "... English text ..."
    },
    "telegram": {
        "uz": "📢 Telegram",
        "ru": "📢 Телеграм",
        "en": "📢 Telegram"
    },
    "instagram": {
        "uz": "📸 Instagram",
        "ru": "📸 Инстаграм",
        "en": "📸 Instagram"
    },
    "youtube": {
        "uz": "▶️ YouTube",
        "ru": "▶️ YouTube",
        "en": "▶️ YouTube"
    },
    "about_teachers": {
        "uz": "👨‍🏫 O‘qituvchilar haqida",
        "ru": "👨‍🏫 О преподавателях",
        "en": "👨‍🏫 About Teachers"
    },
    "choose_teacher": {
        "uz": "Quyidagi ustozlardan birini tanlang:",
        "ru": "Выберите преподавателя ниже:",
        "en": "Choose a teacher below:"
    },
    "photo_not_found": {
        "uz": "❌ Rasm topilmadi.",
        "ru": "❌ Фото не найдено.",
        "en": "❌ Photo not found."
    },
    "uz": {
        "start_text": "Assalomu alaykum! Botimizga xush kelibsiz. Davom etish uchun tilni tanlang:",
        "language_chosen": "Til muvaffaqiyatli o‘zgartirildi!",
        "subscribe_text": "📢 Iltimos, kanalga obuna bo‘ling:",
        "check_sub": "✅ Obunani tekshirish",
        "go_to_channel": "📢 Kanalga o‘tish",
        "Kursni_tanlang": "📚 Fanlardan birini tanlang:",
        "main_menu": "🏠 Asosiy menyu",
        "menu_buttons": [
            "🎓 O‘quv markazi haqida",
            "📚 Kurslar",
            "📝 Ro‘yxatdan o‘tish",
            "🧪 Test",
            "📞 Admin bilan aloqa",
            "⚙️ Sozlamalar"
        ]
    },

    "ru": {
        "start_text": "Здравствуйте! Добро пожаловать в наш бот. Пожалуйста, выберите язык:",
        "language_chosen": "Язык успешно изменён!",
        "subscribe_text": "📢 Пожалуйста, подпишитесь на канал:",
        "check_sub": "✅ Проверить подписку",
        "go_to_channel": "📢 Перейти в канал",
        "Kursni_tanlang": "📚 Выберите курс:",
        "main_menu": "🏠 Главное меню",
        "menu_buttons": [
            "🎓 О учебном центре",
            "📚 Курсы",
            "📝 Регистрация",
            "🧪 Тест",
            "📞 Связаться с админом",
            "⚙️ Настройки"
        ]
    },

    "en": {
        "start_text": "Hello! Welcome to our bot. Please choose your language:",
        "language_chosen": "Language successfully changed!",
        "subscribe_text": "📢 Please subscribe to the channel:",
        "check_sub": "✅ Check subscription",
        "go_to_channel": "📢 Go to Channel",
        "Kursni_tanlang": "📚 Choose a course:",
        "main_menu": "🏠 Main Menu",
        "menu_buttons": [
            "🎓 About the Center",
            "📚 Courses",
            "📝 Register",
            "🧪 Test",
            "📞 Contact Admin",
            "⚙️ Settings"
        ]
    }
}


def get_text(key: str, lang: str = "uz") -> str | list:
    """
    Berilgan kalit va til bo‘yicha matnni qaytaradi.
    """
    # Til bo‘yicha tekshir
    lang_texts = texts.get(lang, texts["uz"])

    # Avval til ichida izla
    if key in lang_texts:
        return lang_texts[key]

    # Umumiy bo‘limdan izla
    if key in texts["common"]:
        return texts["common"][key]

    # Topilmasa
    return f"[{key}]"
