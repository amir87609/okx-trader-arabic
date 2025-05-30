from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import config
from users import get_okx_account, set_okx_account, activate_subscription, is_active

# كل القوائم الرئيسية
MAIN_MENU = [
    ["تداول العملات", "تحليل السوق والعملات"],
    ["ادارة المال والمخاطر", "تثبيت على عملة معينة"],
    ["الرصيد والمتابعة", "المساعدة"],
    ["التنبيهات الذكية", "أوامر متقدمة"],
    ["التقارير", "نسخ التداول"],
    ["تعلم التداول", "إعدادات الحساب"]
]

# قوائم فرعية لكل خانة
TRADING_MENU = [
    ["شراء عملة", "بيع عملة"],
    ["شراء بوقت محدد", "توزيع رأس المال"],
    ["رجوع ← القائمة الرئيسية"]
]
ANALYSIS_MENU = [
    ["تحليل عملة", "توقع حركة السوق"],
    ["مقارنة عملتين", "تنبيهات التحليل"],
    ["رجوع ← القائمة الرئيسية"]
]
RISK_MENU = [
    ["تفعيل وقف الخسارة", "تفعيل جني الأرباح"],
    ["إدارة رأس المال", "إحصائيات الأداء"],
    ["رجوع ← القائمة الرئيسية"]
]
LOCK_MENU = [
    ["تثبيت على عملة", "إلغاء التثبيت"],
    ["رجوع ← القائمة الرئيسية"]
]
BALANCE_MENU = [
    ["عرض الرصيد", "سحب الأرباح"],
    ["تحويل العملات", "محفظة تجريبية"],
    ["رجوع ← القائمة الرئيسية"]
]
ALERTS_MENU = [
    ["تنبيه تغير السعر", "تنبيه الحيتان"],
    ["تنبيه الأخبار", "تخصيص التنبيهات"],
    ["رجوع ← القائمة الرئيسية"]
]
ADVANCED_MENU = [
    ["أمر OCO", "شراء DCA"],
    ["جدولة طلبات", "أوامر صوتية"],
    ["رجوع ← القائمة الرئيسية"]
]
REPORTS_MENU = [
    ["تقرير أسبوعي", "تقرير شهري"],
    ["جدول العمليات", "ملخص الأرباح"],
    ["رجوع ← القائمة الرئيسية"]
]
COPYTRADING_MENU = [
    ["نسخ متداول محترف", "عرض قائمة المتداولين"],
    ["مسابقة التداول", "جدول الترتيب"],
    ["رجوع ← القائمة الرئيسية"]
]
EDUCATION_MENU = [
    ["نصيحة اليوم", "دروس تعليمية"],
    ["أسئلة وأجوبة", "سياسة الزكاة"],
    ["رجوع ← القائمة الرئيسية"]
]
SETTINGS_MENU = [
    ["إضافة حساب OKX", "إدارة المحافظ"],
    ["تغيير اللغة", "إعدادات الصوت"],
    ["سحب الأرباح", "تنبيهات الاشتراك"],
    ["رجوع ← القائمة الرئيسية"]
]

# دالة عرض أي قائمة
async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, menu):
    reply_markup = ReplyKeyboardMarkup(menu, resize_keyboard=True)
    await update.message.reply_text("يرجى اختيار أحد الخيارات:", reply_markup=reply_markup)

# دالة التحكم في جميع القوائم
async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "تداول العملات":
        await show_menu(update, context, TRADING_MENU)
    elif text == "تحليل السوق والعملات":
        await show_menu(update, context, ANALYSIS_MENU)
    elif text == "ادارة المال والمخاطر":
        await show_menu(update, context, RISK_MENU)
    elif text == "تثبيت على عملة معينة":
        await show_menu(update, context, LOCK_MENU)
    elif text == "الرصيد والمتابعة":
        await show_menu(update, context, BALANCE_MENU)
    elif text == "التنبيهات الذكية":
        await show_menu(update, context, ALERTS_MENU)
    elif text == "أوامر متقدمة":
        await show_menu(update, context, ADVANCED_MENU)
    elif text == "التقارير":
        await show_menu(update, context, REPORTS_MENU)
    elif text == "نسخ التداول":
        await show_menu(update, context, COPYTRADING_MENU)
    elif text == "تعلم التداول":
        await show_menu(update, context, EDUCATION_MENU)
    elif text == "إعدادات الحساب":
        await show_menu(update, context, SETTINGS_MENU)
    elif text == "المساعدة":
        await update.message.reply_text(f"للمساعدة راسل المطور: @{config.ADMIN_USERNAME}")
    elif "رجوع ← القائمة الرئيسية" in text:
        await show_menu(update, context, MAIN_MENU)
    else:
        await update.message.reply_text(f"تم اختيار: {text}\nسيتم تنفيذ الأمر قريبًا أو اختر من القائمة.")

# دالة بدء البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if not is_active(user_id):
        await update.message.reply_text("يجب تفعيل الاشتراك الشهري. أرسل رمز التفعيل:")
        return
    await show_menu(update, context, MAIN_MENU)

# دالة تفعيل الاشتراك
async def subscription_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    code = update.message.text.strip()
    if activate_subscription(user_id, code):
        await update.message.reply_text("تم تفعيل الاشتراك الشهري بنجاح! أرسل /start للبدء.")
    else:
        await update.message.reply_text("رمز الاشتراك غير صحيح. حاول مرة أخرى.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, subscription_handler))  # كود الاشتراك
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))          # القوائم والتداول
    app.run_polling()
