import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------
# The token is read from an environment variable for security.
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# -------------------------------------------------------------------
# Text Content (Khmer)
# -------------------------------------------------------------------
# Main menu text
WELCOME_TEXT = (
    "🐔 សូមស្វាគមន៍មកកាន់ Chicken Care\n\n"
    "Learn practical information about chicken care, feeding, housing, hygiene and general poultry health.\n\n"
    "សូមជ្រើសរើសផ្នែកដែលអ្នកចង់ដឹង:"
)

# Content for each section
CARE_TEXT = (
    "🐔 **ការថែទាំមាន់**\n\n"
    "ការថែទាំមាន់ប្រចាំថ្ងៃគឺសំខាន់ណាស់សម្រាប់សុខភាព និងផលិតភាពរបស់ពួកវា។ ខាងក្រោមនេះជាការណែនាំមូលដ្ឋាន៖\n\n"
    "• **ផ្តល់ទឹកស្អាត**: ត្រូវប្រាកដថាមានទឹកស្អាតគ្រប់គ្រាន់ 24 ម៉ោង។\n"
    "• **សម្អាតទីជម្រក**: កំចាត់រាល់កាកសំណល់ និងបន្ទះក្តារចាស់ៗជាប្រចាំ។\n"
    "• **សង្កេតមើលឥរិយាបថ**: កត់សម្គាល់ប្រសិនបើមាន់ហាក់ដូចជាឈឺ ឬញ៉ាំអាហារតិច។\n"
    "• **រក្សាកំដៅ**: នៅពេលព្រឹក ឬពេលយប់ ត្រូវរក្សាកំដៅឱ្យបានត្រឹមត្រូវ។\n"
    "• **ផ្តល់ចំណីទៀងទាត់**: ផ្តល់ចំណីនៅពេលវេលាជាក់លាក់ជារៀងរាល់ថ្ងៃ។"
)

FEED_TEXT = (
    "🌾 **អាហារ និងចំណី**\n\n"
    "ចំណីគឺជាកត្តាសំខាន់ក្នុងការលូតលាស់ និងផលិតពងរបស់មាន់។ ខាងក្រោមនេះជាគោលការណ៍គ្រឹះ៖\n\n"
    "• **ចំណីមានតុល្យភាព**: ត្រូវមានជាតិប្រូតេអ៊ីន កាបូអ៊ីដ្រាត វីតាមីន និងជាតិរ៉ែគ្រប់គ្រាន់។\n"
    "• **ទឹកស្អាត**: ត្រូវផ្តល់ទឹកស្អាតដែលមិនមានក្លិន ឬសារធាតុគីមី។\n"
    "• **ការផ្តល់ចំណី**: ផ្តល់ចំណីតាមអាយុ និងប្រភេទមាន់ (មាន់ពង មាន់សាច់)។\n"
    "• **ជៀសវាងចំណីផ្អែម**: កុំផ្តល់ចំណីដែលមានជាតិស្ករខ្ពស់ ព្រោះអាចប៉ះពាល់ដល់សុខភាព។"
)

HOUSING_TEXT = (
    "🏠 **កន្លែងចិញ្ចឹម**\n\n"
    "ទីជម្រកដ៏ល្អគឺចាំបាច់ដើម្បីការពារមាន់ពីជំងឺ និងសត្វចម្លែក។ ខាងក្រោមនេះជាលក្ខណៈសំខាន់ៗ៖\n\n"
    "• **អនាម័យ**: ត្រូវសម្អាតជាប្រចាំ ដើម្បីការពារបាក់តេរី និងមេរោគ។\n"
    "• **ខ្យល់ចេញចូល**: ត្រូវមានខ្យល់ចេញចូលល្អ ប៉ុន្តែកុំឱ្យមានខ្យល់ខ្លាំងពេក។\n"
    "• **ជាន់ជម្រក**: ជាន់ត្រូវស្ងួត និងគ្មានទឹកជក់ ដើម្បីការពារជំងឺផ្លូវដង្ហើម។\n"
    "• **ទំហំគ្រប់គ្រាន់**: មាន់ត្រូវការទំហំគ្រប់គ្រាន់ដើម្បីធ្វើចលនា និងសម្រាក។\n"
    "• **ការពារអាកាសធាតុ**: ត្រូវមានដំបូលការពារភ្លៀង និងជញ្ជាំងការពារខ្យល់ត្រជាក់។"
)

HEALTH_TEXT = (
    "❤️ **សុខភាពមាន់**\n\n"
    "ការត្រួតពិនិត្យសុខភាពមាន់ជាប្រចាំគឺជាការងារសំខាន់។ ខាងក្រោមនេះជាចំណុចដែលត្រូវយកចិត្តទុកដាក់៖\n\n"
    "• **សង្កេតឥរិយាបថ**: មើលថាតើមាន់មានសកម្មភាពធម្មតា ឬញ៉ាំអាហារធម្មតាឬអត់។\n"
    "• **ការផ្លាស់ប្តូរចំណី**: ប្រសិនបើមាន់ញ៉ាំចំណីតិច ឬឈប់ញ៉ាំ នោះអាចជាសញ្ញានៃជំងឺ។\n"
    "• **អនាម័យ**: ត្រូវរក្សាអនាម័យក្នុងទីជម្រក និងឧបករណ៍ផ្តល់ចំណី។\n"
    "• **ការពិគ្រោះជាមួយពេទ្យសត្វ**: ប្រសិនបើមានបញ្ហាសុខភាពធ្ងន់ធ្ងរ គួរពិគ្រោះជាមួយពេទ្យសត្វជំនាញ។"
)

FACTS_TEXT = (
    "📚 **ចំណេះដឹង**\n\n"
    "ខាងក្រោមនេះជាការពិតគួរឱ្យចាប់អារម្មណ៍អំពីមាន់ និងសត្វស្លាប៖\n\n"
    "• មាន់អាចចងចាំមុខមនុស្សបានរាប់សិបនាក់។\n"
    "• មាន់មានចក្ខុវិស័យពណ៌ និងអាចមើលឃើញពណ៌ក្នុងវិសាលគមធំជាងមនុស្ស។\n"
    "• មាន់ញីអាចញាស់ពងដោយមិនចាំបាច់មានមាន់ឈ្មោល។\n"
    "• មាន់មានទម្ងន់ខុសៗគ្នាទៅតាមពូជ និងអាយុ។"
)

ABOUT_TEXT = (
    "ℹ️ **អំពីបូត**\n\n"
    "Chicken Care Khmer គឺជាបូតអប់រំដែលផ្តល់ព័ត៌មានអំពីការថែទាំមាន់ និងចំណេះដឹងទូទៅអំពីសត្វស្លាប។\n\n"
    "គោលបំណងរបស់បូតគឺដើម្បីជួយអ្នកចិញ្ចឹមមាន់ឱ្យមានចំណេះដឹងគ្រឹះអំពីការថែទាំ អាហារ ទីជម្រក និងសុខភាពមាន់។\n\n"
    "បូតនេះមិនផ្តល់ព័ត៌មានអំពីការភ្នាល់ ឬល្បែងស៊ីសងណាមួយឡើយ។"
)

# -------------------------------------------------------------------
# Keyboard Layouts
# -------------------------------------------------------------------
def get_main_menu_keyboard():
    """Returns the main menu inline keyboard."""
    keyboard = [
        [InlineKeyboardButton("🐔 ការថែទាំមាន់", callback_data="menu_care")],
        [InlineKeyboardButton("🌾 អាហារ និងចំណី", callback_data="menu_feed")],
        [InlineKeyboardButton("🏠 កន្លែងចិញ្ចឹម", callback_data="menu_housing")],
        [InlineKeyboardButton("❤️ សុខភាពមាន់", callback_data="menu_health")],
        [InlineKeyboardButton("📚 ចំណេះដឹង", callback_data="menu_facts")],
        [InlineKeyboardButton("ℹ️ អំពីបូត", callback_data="menu_about")],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_keyboard():
    """Returns a keyboard with a single 'Back to Menu' button."""
    keyboard = [
        [InlineKeyboardButton("⬅️ ត្រឡប់ទៅម៉ឺនុយ", callback_data="back_to_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

# -------------------------------------------------------------------
# Command Handlers
# -------------------------------------------------------------------
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends the main menu when /start is issued."""
    await update.message.reply_text(
        WELCOME_TEXT,
        reply_markup=get_main_menu_keyboard(),
        parse_mode="Markdown",
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a help message when /help is issued."""
    help_text = (
        "📖 **របៀបប្រើប្រាស់បូត**\n\n"
        "បូតនេះផ្តល់ព័ត៌មានអប់រំអំពីការថែទាំមាន់។\n\n"
        "• ប្រើ `/start` ដើម្បីបើកម៉ឺនុយមេ។\n"
        "• ចុចលើប៊ូតុងណាមួយដើម្បីមើលព័ត៌មានលម្អិត។\n"
        "• ចុចប៊ូតុង **⬅️ ត្រឡប់ទៅម៉ឺនុយ** ដើម្បីត្រឡប់ទៅម៉ឺនុយមេវិញ។\n\n"
        "ប្រសិនបើអ្នកមានសំណួរ សូមប្រើប្រាស់ម៉ឺនុយដើម្បីស្វែងរកព័ត៌មានដែលអ្នកចង់ដឹង។"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends the about message when /about is issued."""
    await update.message.reply_text(ABOUT_TEXT, parse_mode="Markdown")

# -------------------------------------------------------------------
# Callback Query Handlers
# -------------------------------------------------------------------
async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles all inline button presses."""
    query = update.callback_query
    # Always answer the callback query to prevent the loading spinner.
    await query.answer()

    data = query.data

    if data == "back_to_menu":
        # Edit the message back to the main menu
        await query.edit_message_text(
            WELCOME_TEXT,
            reply_markup=get_main_menu_keyboard(),
            parse_mode="Markdown",
        )
    elif data == "menu_care":
        await query.edit_message_text(
            CARE_TEXT, reply_markup=get_back_keyboard(), parse_mode="Markdown"
        )
    elif data == "menu_feed":
        await query.edit_message_text(
            FEED_TEXT, reply_markup=get_back_keyboard(), parse_mode="Markdown"
        )
    elif data == "menu_housing":
        await query.edit_message_text(
            HOUSING_TEXT, reply_markup=get_back_keyboard(), parse_mode="Markdown"
        )
    elif data == "menu_health":
        await query.edit_message_text(
            HEALTH_TEXT, reply_markup=get_back_keyboard(), parse_mode="Markdown"
        )
    elif data == "menu_facts":
        await query.edit_message_text(
            FACTS_TEXT, reply_markup=get_back_keyboard(), parse_mode="Markdown"
        )
    elif data == "menu_about":
        await query.edit_message_text(
            ABOUT_TEXT, reply_markup=get_back_keyboard(), parse_mode="Markdown"
        )
    else:
        # Fallback for any unknown callback data
        await query.edit_message_text(
            "សូមអភ័យទោស សូមចុច /start ដើម្បីចាប់ផ្តើមឡើងវិញ。",
            reply_markup=get_back_keyboard(),
            parse_mode="Markdown",
        )

# -------------------------------------------------------------------
# Main Application
# -------------------------------------------------------------------
def main() -> None:
    """Starts the bot."""
    if not TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN environment variable not set!")
        return

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))

    # Register the callback query handler
    application.add_handler(CallbackQueryHandler(menu_callback))

    # Run the bot until the user presses Ctrl-C
    logger.info("Bot is starting...")
    application.run_polling()

if __name__ == "__main__":
    main()
