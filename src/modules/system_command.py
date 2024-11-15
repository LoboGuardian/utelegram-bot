import logging
import os
import platform
import sys
import time
import asyncio
import glob
import importlib
import subprocess
from typing import Tuple, List
from datetime import datetime, timedelta
from functools import wraps
from config.auth import ADMIN_ID
from telegram import Update
from telegram.ext import CallbackContext

# Track the bot's start time for uptime calculations
start_time = time.time()


def admin_required(func):
    """Decorator to restrict command access to admin users only."""
    @wraps(func)
    async def wrapper(update: Update, context: CallbackContext) -> None:
        user_id = update.effective_user.id
        command = update.message.text

        logging.info(f"User ID: {user_id}, Admin ID: {ADMIN_ID}, Command: {command}")

        if str(user_id) != str(ADMIN_ID):
            await update.message.reply_text("You are not authorized to use this command.")
            logging.warning(f"Unauthorized access by User ID: {user_id} for command: {command}")
            return

        try:
            await func(update, context)
        except Exception as e:
            logging.error(f"Error while executing command: {e}")
            await update.message.reply_text("An error occurred while processing your request.")

    return wrapper

@admin_required
async def admin_command(update: Update, context: CallbackContext) -> None:
    """Access admin-only command."""
    await update.message.reply_text("You have admin access.")

@admin_required
async def uptime_command(update: Update, context: CallbackContext) -> None:
    """Send the system's uptime."""
    with open("/proc/uptime", "r") as f:
        uptime_seconds = float(f.readline().split()[0])
    await update.message.reply_text(f"System uptime: {format_duration(int(uptime_seconds))}")


def format_duration(seconds: int) -> str:
    """Format duration into a human-readable string."""
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    parts = [
        f"{days} day{'s' if days != 1 else ''}" if days else '',
        f"{hours} hour{'s' if hours != 1 else ''}" if hours else '',
        f"{minutes} minute{'s' if minutes != 1 else ''}" if minutes else '',
        f"{seconds} second{'s' if seconds != 1 else ''}" if seconds else '',
    ]
    return ', '.join(part for part in parts if part)


@admin_required
async def my_id(update: Update, context: CallbackContext) -> None:
    """Show the user's ID."""
    user_id = update.effective_user.id
    await update.message.reply_text(f"Your user ID is: {user_id}")
