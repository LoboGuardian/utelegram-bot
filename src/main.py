#!/bin/env python
# -*-coding:UTF-8-*-
# main.py

"""
Main entry point for the Telegram bot. It initializes the bot using the
Telegram API, sets up command handlers, and manages message handling.

"""

import logging
from config.auth import TOKEN, ADMIN_ID
from modules.text_command import button_callback
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackContext,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
from modules.logging import (
    unknown_handle_command,
    error_handler_command,
    handle_update
)
from modules.modules import COMMANDS  # Dynamically import commands

async def notify_admin(context: ContextTypes.DEFAULT_TYPE, message: str) -> None:
    """Send a message to the admin."""
    try:
        await context.bot.send_message(chat_id=int(ADMIN_ID), text=message)
        logging.info(f"Sent admin notification: {message}")
    except Exception as e:
        logging.error(f"Failed to send admin notification: {e}")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for the /start command."""
    await update.message.reply_text("Hello! The bot is running.")

async def on_startup(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a notification when the bot starts."""
    await notify_admin(context, "🚀 The bot has started successfully!")

async def on_update(update: Update, context: CallbackContext) -> None:
    """Handle every update and log it."""
    handle_update(update, context)

# Main function to start the bot
def main() -> None:
    application = ApplicationBuilder().token(TOKEN).post_init(on_startup).build()

    # Register command handlers dynamically
    for command, handler in COMMANDS.items():
        application.add_handler(CommandHandler(command, handler))

    
    # Callback query handler for button presses
    application.add_handler(CallbackQueryHandler(button_callback))

    # Message handlers``
    
#    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, COMMANDS["echo"]))

    application.add_handler(MessageHandler(filters.COMMAND, unknown_handle_command))

    # Register the error handler
    application.add_error_handler(error_handler_command)

    # Run the bot until manually stopped
    application.run_polling()

if __name__ == '__main__':
    main()
