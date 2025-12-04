import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

# --- Configuration ---
# NOTE: The BOT_TOKEN is read from the environment variable set in Koyeb.
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
QRCRAFTER_WEB_APP_URL = "https://qrcrafter.vercel.app"
APP_STORE_LINK = "https://play.google.com/store/apps/details?id=com.appkadag.qrcrafter" 

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Keyboard Definitions ---

def get_main_inline_keyboard():
    """Returns the inline keyboard for the main menu, primarily featuring the Web App launch button."""
    keyboard = [
        [InlineKeyboardButton("🚀 Launch QRCrafter Mini App", web_app=WebAppInfo(url=QRCRAFTER_WEB_APP_URL))],
        [InlineKeyboardButton("❓ Features", callback_data='cmd_features'),
         InlineKeyboardButton("💡 How to Use", callback_data='cmd_how_to_use')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_reply_keyboard():
    """Returns a persistent Reply Keyboard for quick command and Q&A access."""
    keyboard = [
        [KeyboardButton("/start"), KeyboardButton("/help"), KeyboardButton("/features")],
        [KeyboardButton("/how_to_use"), KeyboardButton("/rate"), KeyboardButton("/web_app")],
        [KeyboardButton("What can you generate?")]
    ]
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)

# --- Handlers ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /start command with a personalized greeting and user details."""
    user = update.effective_user
    
    # Personalized Greeting with username and ID
    greeting_text = (
        f"👋 Hello, **{user.first_name}**! Welcome to **QRCrafter Bot**.\n\n"
        f"Your Telegram ID is: `{user.id}`\n\n"
        "I'm here to help you create beautiful and functional QR codes using our full-featured Mini App. "
        "It runs perfectly right inside Telegram!"
    )
    
    await update.message.reply_text(
        greeting_text,
        reply_markup=get_reply_keyboard(),
        parse_mode="Markdown"
    )
    
    await update.message.reply_text(
        "**Choose your next action:**\n"
        "1. **Launch the Mini App** to start crafting your QR code now.\n"
        "2. **Use the commands** on the keyboard below for more information.",
        reply_markup=get_main_inline_keyboard(),
        parse_mode="Markdown"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /help command, providing a comprehensive list of all bot commands."""
    help_text = (
        "**📚 QRCrafter Bot Help & Commands**\n\n"
        "**Main Commands:**\n"
        "• `/start` - Get the welcome message and personalized greeting.\n"
        "• `/help` - Show this comprehensive list of commands.\n"
        "• `/rate` - Share your feedback and rate the bot/app.\n\n"
        "**Information & Utility:**\n"
        "• `/features` - See the full list of QR code types we can generate.\n"
        "• `/how_to_use` - Step-by-step instructions for using the Mini App.\n"
        "• `/web_app` - Get the direct link and quick details about the Mini App.\n\n"
        "**Q&A:**\n"
        "• You can also ask questions like 'What can you generate?' or 'How do I make a Wi-Fi QR code?'"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def features_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /features command and details the Web App's capabilities."""
    features_text = (
        "✨ **QRCrafter Full Features List** ✨\n\n"
        "The QRCrafter Mini App is an advanced QR code generator supporting a wide range of data types:\n"
        "• **Connectivity:** Wi-Fi access (SSID, password, encryption type).\n"
        "• **Contact:** V-Card (virtual business cards for easy contact sharing).\n"
        "• **Web:** URLs, Website Links, and Social Media profiles.\n"
        "• **Communication:** Phone Numbers, SMS, and Email messages.\n"
        "• **General:** Plain Text (for notes, keys, or short messages).\n"
        "• **Customization:** Full control over colors, background, and dark mode for a personalized look."
    )
    await update.message.reply_text(features_text, parse_mode="Markdown")

async def how_to_use_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /how_to_use command with instructions."""
    how_to_use_text = (
        "📖 **How to Use QRCrafter Mini App**\n\n"
        "The easiest way is to use the Mini App inside Telegram:\n\n"
        "1. **Launch the App:** Click the **'🚀 Launch QRCrafter Mini App'** button from the main menu (or use `/web_app`).\n"
        "2. **Select Type:** Choose the data type you need (e.g., *URL*, *V-Card*, or *Wi-Fi*).\n"
        "3. **Input Details:** Fill in the required fields (like the URL, or contact details).\n"
        "4. **Customize:** Adjust colors or background using the in-app tools.\n"
        "5. **Generate & Share:** Your QR code appears instantly! Download it or share the image directly."
    )
    await update.message.reply_text(how_to_use_text, parse_mode="Markdown")

async def rate_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /rate command with a button linking to the review page."""
    keyboard = [
        [InlineKeyboardButton("⭐ Rate QRCrafter Now!", url=APP_STORE_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "We're thrilled you love QRCrafter! Your feedback helps us improve.\n\n"
        "Please tap the button below to leave a quick rating and review:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def web_app_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /web_app command, providing a quick link to the Mini App."""
    keyboard = [
        [InlineKeyboardButton("Open QRCrafter Mini App", web_app=WebAppInfo(url=QRCRAFTER_WEB_APP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"Here is the direct launch button for the QRCrafter Mini App:\n"
        f"Link: `{QRCRAFTER_WEB_APP_URL}`",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles inline button presses that correspond to commands."""
    query = update.callback_query
    await query.answer() 
    
    if query.data == 'cmd_features':
        await features_command(query, context)
    elif query.data == 'cmd_how_to_use':
        await how_to_use_command(query, context)
    else:
        # Re-send the main menu for unknown actions
        await query.edit_message_text(
            text="Unknown action. Please use one of the commands on the reply keyboard or the main app button.",
            reply_markup=get_main_inline_keyboard()
        )

async def generic_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles incoming text messages (Q&A) and guides the user."""
    user_input = update.message.text.lower()
    
    if any(keyword in user_input for keyword in ["what can you generate", "what can you do", "types of qr codes"]):
        response = (
            "I can help you generate QR codes for almost anything! This includes **Wi-Fi credentials**, "
            "**contact V-Cards**, **URLs**, **plain text**, and more.\n"
            "For the full details, tap `/features` or '🚀 Launch Mini App'!"
        )
    elif any(keyword in user_input for keyword in ["wi-fi", "wifi", "connect"]):
        response = (
            "Yes! QRCrafter can generate QR codes that let users connect to a Wi-Fi network instantly. "
            "Just launch the Mini App, select 'Wi-Fi' as the data type, and enter your network details."
        )
    elif any(keyword in user_input for keyword in ["vcard", "contact", "business card"]):
        response = (
            "Absolutely! QRCrafter handles V-Cards. You can encode all your contact information "
            "into a single QR code. Scanning it automatically saves your details."
        )
    elif any(keyword in user_input for keyword in ["hello", "hi", "hey", "greet"]):
        response = (
            f"Hello, {update.effective_user.first_name}! Ready to craft a QR code? "
            f"Tap the '🚀 Launch QRCrafter Mini App' button to get started immediately, or type `/help` for commands."
        )
    else:
        response = (
            "I'm primarily focused on helping you launch the QRCrafter Mini App and providing information about its features.\n\n"
            "To start generating QR codes, please click the **'🚀 Launch QRCrafter Mini App'** button or use the `/help` command."
        )

    await update.message.reply_text(response, parse_mode="Markdown")

# --- Main Bot Execution ---

def main() -> None:
    """Start the bot and register all handlers."""
    if not BOT_TOKEN:
        logger.error("FATAL ERROR: The TELEGRAM_BOT_TOKEN environment variable is not set. Cannot start bot.")
        return

    # Create the Application and pass your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()

    # Register handlers
    application.add_handlers([
        CommandHandler("start", start_command),
        CommandHandler("help", help_command),
        CommandHandler("features", features_command),
        CommandHandler("how_to_use", how_to_use_command),
        CommandHandler("rate", rate_command),
        CommandHandler("web_app", web_app_command),
        CallbackQueryHandler(button_handler),
        MessageHandler(filters.TEXT & ~filters.COMMAND, generic_message_handler)
    ])

    # Start the Bot in polling mode (suitable for simple deployments like Koyeb)
    logger.info("QRCrafter Bot is starting polling...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
