import osimport certififrom pyrogram import Client, errorsimport telebotfrom telebot import typesimport threadingimport asynciofrom backend import appfrom db import databaseDB = database()App = app()os.environ['SSL_CERT_FILE'] = certifi.where()api_id = '20662205'api_hash = '8f1754a96f4db97c9db22dfc7b68b597'TELEGRAM_TOKEN = "7696711925:AAGNsGUEwGF3JXiza2Y_gIHTd_4zZc1wh6g"bot = telebot.TeleBot(TELEGRAM_TOKEN, threaded=False, num_threads=55, skip_pending=True)# قائمة المشرفينADMIN_IDS = [1621709020, 6374412293]  # استبدل بـ ID المشرفين# حالة البوت والتواصلbot_status = {"active": True}communication_status = {"active": False}@bot.message_handler(commands=['start'])def main_menu(message):    AddAccount = types.InlineKeyboardButton("اضافة حساب 🛎", callback_data="AddAccount")    Accounts = types.InlineKeyboardButton("اكواد حساباتك 🖲", callback_data="Accounts")    a1 = types.InlineKeyboardButton("نقل أعضاء 👤😇", callback_data="a1")    admin_panel = types.InlineKeyboardButton("لوحة الإدارة 🛠", callback_data="admin_panel")    inline = types.InlineKeyboardMarkup([[a1], [AddAccount], [Accounts], [admin_panel]])    bot.send_message(        message.chat.id,        """*مرحباً بك 👋اختر ما تريد من الأزرار أدناه 🔥يمكنك نقل الأعضاء لجروبك 🛎أو استخدام الميزات الأخرى المتاحة ☄Creator: @S3_9B*""",        reply_markup=inline,        parse_mode="markdown"    )@bot.callback_query_handler(lambda call: True)def handle_callbacks(call):    if call.data == "Accounts":        num = DB.accounts()        bot.edit_message_text(            chat_id=call.message.chat.id,            message_id=call.message.message_id,            text=f"حساباتك المسجلة بالكامل: {num}",            parse_mode="markdown"        )    elif call.data == "AddAccount":        msg = bot.edit_message_text(            chat_id=call.message.chat.id,            message_id=call.message.message_id,            text="*قم بإرسال الرقم الذي تريد تسجيله مع رمز الدولة الآن* 📞🎩",            parse_mode="markdown"        )        bot.register_next_step_handler(msg, add_account)    elif call.data == "a1":        msg = bot.edit_message_text(            chat_id=call.message.chat.id,            message_id=call.message.message_id,            text="*قم بإرسال رابط الجروب المراد النقل منه* 🖲",            parse_mode="markdown"        )        bot.register_next_step_handler(msg, statement)    elif call.data == "admin_panel":        admin_panel(call.message)def admin_panel(message):    if message.chat.id in ADMIN_IDS:        activate_bot = types.InlineKeyboardButton("تفعيل البوت ✅", callback_data="activate_bot")        deactivate_bot = types.InlineKeyboardButton("تعطيل البوت ❌", callback_data="deactivate_bot")        add_admin = types.InlineKeyboardButton("رفع مشرف 👤", callback_data="add_admin")        remove_admin = types.InlineKeyboardButton("تنزيل مشرف 🚫", callback_data="remove_admin")        enable_communication = types.InlineKeyboardButton("تفعيل التواصل 💬", callback_data="enable_communication")        disable_communication = types.InlineKeyboardButton("تعطيل التواصل 🛑", callback_data="disable_communication")        bot_members = types.InlineKeyboardButton("عدد أعضاء البوت 📊", callback_data="bot_members")        markup = types.InlineKeyboardMarkup(            [[activate_bot, deactivate_bot], [add_admin, remove_admin],             [enable_communication, disable_communication], [bot_members]]        )        bot.send_message(message.chat.id, "لوحة التحكم 🛠:", reply_markup=markup)    else:        bot.send_message(message.chat.id, "❌ ليس لديك الصلاحيات للوصول إلى لوحة الإدارة.")@bot.callback_query_handler(func=lambda call: True)def admin_commands(call):    if call.data == "activate_bot":        bot_status["active"] = True        bot.answer_callback_query(call.id, "✅ تم تفعيل البوت!")    elif call.data == "deactivate_bot":        bot_status["active"] = False        bot.answer_callback_query(call.id, "❌ تم تعطيل البوت!")    elif call.data == "add_admin":        msg = bot.send_message(call.message.chat.id, "👤 أرسل آيدي العضو لرفعه كمشرف:")        bot.register_next_step_handler(msg, add_admin_step)    elif call.data == "remove_admin":        msg = bot.send_message(call.message.chat.id, "🚫 أرسل آيدي المشرف لتنزيله:")        bot.register_next_step_handler(msg, remove_admin_step)    elif call.data == "enable_communication":        communication_status["active"] = True        bot.answer_callback_query(call.id, "✅ تم تفعيل التواصل!")    elif call.data == "disable_communication":        communication_status["active"] = False        bot.answer_callback_query(call.id, "❌ تم تعطيل التواصل!")    elif call.data == "bot_members":        num_members = DB.get_bot_members()  # افترض أن لديك وظيفة لحساب الأعضاء        bot.send_message(call.message.chat.id, f"📊 عدد أعضاء البوت: {num_members}")def add_account(message):    try:        if "+" in message.text:            bot.send_message(message.chat.id, "*انتظر جاري الفحص* ⏱", parse_mode="markdown")            _client = Client("::memory::", in_memory=True, api_id=api_id, api_hash=api_hash, lang_code="ar")            _client.connect()            SendCode = _client.send_code(message.text)            Mas = bot.send_message(message.chat.id, "*أدخل الرمز المرسل إليك 🔏*", parse_mode="markdown")            bot.register_next_step_handler(Mas, sign_up, _client, message.text, SendCode.phone_code_hash, message.text)        else:            bot.send_message(message.chat.id, "*يرجى إرسال رقم صحيح.*")    except Exception as e:        bot.send_message(message.chat.id, f"ERORR : {e}")def sign_up(message, _client, phone, hash, name):    try:        bot.send_message(message.chat.id, "*انتظر قليلاً ⏱*", parse_mode="markdown")        _client.sign_in(phone, hash, message.text)        bot.send_message(message.chat.id, "*تم تأكيد الحساب بنجاح ✅ *", parse_mode="markdown")        ses = _client.export_session_string()        DB.AddAcount(ses, name, message.chat.id)    except errors.SessionPasswordNeeded:        Mas = bot.send_message(message.chat.id, "*أدخل كلمة المرور الخاصة بحسابك 🔐*", parse_mode="markdown")        bot.register_next_step_handler(Mas, add_password, _client, name)def add_password(message, _client, name):    try:        _client.check_password(message.text)        ses = _client.export_session_string()        DB.AddAcount(ses, name, message.chat.id)        bot.send_message(message.chat.id, "*تم تأكيد الحساب بنجاح ✅*", parse_mode="markdown")        _client.stop()    except Exception as e:        bot.send_message(message.chat.id, f"ERORR : {e}")# التواصل مع المشرف@bot.message_handler(func=lambda message: communication_status["active"])def forward_to_admin(message):    for admin_id in ADMIN_IDS:        bot.forward_message(admin_id, message.chat.id, message.message_id)# التحقق من حالة البوت@bot.message_handler(func=lambda message: not bot_status["active"])def bot_disabled(message):    bot.send_message(message.chat.id, "❌ البوت معطل حالياً، يرجى المحاولة لاحقاً.")bot.infinity_polling(none_stop=True, timeout=15, long_polling_timeout=15)