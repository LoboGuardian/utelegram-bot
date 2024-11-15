# modules/logging.py

"""
This module provides centralized logging functionality to track updates, 
errors, and interactions with the Telegram bot. It also configures the 
logging system and provides helper functions for error handling.
"""

import logging
from telegram import Update
from telegram.ext import CallbackContext
from config.auth import ADMIN_ID

def configure_logging(log_filename="app.log", level=logging.WARNING, debug=False):
    """Configures logging for the Telegram bot."""
    # Get the root logger
    logger = logging.getLogger()

    # Prevent adding multiple handlers
    # if logger.hasHandlers():
        # return  # Avoid duplicate handlers

    # Set the logging level
    logger.setLevel(logging.DEBUG if debug else level)

    # Create file and console handlers
    file_handler = logging.FileHandler(log_filename)
    console_handler = logging.StreamHandler()

    # Define the format for log messages
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Apply the formatter to both handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logging.info("Logging is configured.")

    # Configure logging for specific libraries
    logging.getLogger('httpx').setLevel(logging.DEBUG if debug else logging.WARNING)

    # Uncomment as needed
    # logging.getLogger('apscheduler').setLevel(logging.WARNING)

    # Optional: Handle warnings (uncomment if needed)
    # import warnings
    # from telegram.warnings import PTBDeprecationWarning
    # warnings.filterwarnings("error", category=PTBDeprecationWarning)


# Logging utility functions

def handle_update(update: Update, context: CallbackContext) -> None:
    """Logs all incoming updates for monitoring and debugging."""
    if update.message:
        log_message = (
            f"Update Type: {type(update).__name__} | "
            f"Chat ID: {update.effective_chat.id if update.effective_chat else 'N/A'} | "
            f"User ID: {update.effective_user.id if update.effective_user else 'N/A'} | "
            f"Text: {getattr(update.message, 'text', 'N/A')}"
        )
        logging.info(log_message)
    elif update.callback_query:
        logging.info(f"Callback Query: {update.callback_query.data}")

def log_command_usage(command: str, user_id: int, chat_id: int) -> None:
    """Logs command usage by users."""
    logging.info(f"Command: {command} | User ID: {user_id} | Chat ID: {chat_id}")

async def log_error(update: object, context: CallbackContext) -> None:
    """Logs detailed information about errors."""
    error_msg = f"Update: {update} caused error: {context.error}"
    logging.error(error_msg)

    if isinstance(update, Update) and update.effective_chat:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Oops! Something went wrong. Please try again later."
        )

# Error handling commands

async def unknown_handle_command(update: Update, context: CallbackContext) -> None:
    """Handles unknown commands."""
    await update.message.reply_text(
        "¡Uy, no entendimos ese comando! \n૮₍ㅇㅅㅇ₎ა\n\n"
        "Recuerda que siempre puedes usar el comando /help para ver todas las cosas que puedo hacer por ti! ٩(๑❛ᴗ❛๑)۶."
    )
    logging.info(f"Unknown command: {update.message.text}")

async def error_handler_command(update: Update, context: CallbackContext):
    """Handles errors gracefully and logs them."""
    logging.error(f"Error in update: {update} - {context.error}")
    await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=(
            "¡Uy, ha ocurrido un error!  \n"
            "૮₍ ಥ ㅅ ಥ ₎ა\n\n"
            "Estamos trabajando en eso, ¡no te preocupes!\n\n"
            "Recuerda que siempre puedes usar el comando /help para ver todas las cosas que puedo hacer por ti! ٩(๑❛ᴗ❛๑)۶."
        )
    )

# Configure logging at the entry point
configure_logging(level=logging.INFO, debug=False)