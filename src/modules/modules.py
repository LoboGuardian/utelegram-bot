# modules/modules.py

"""
This module aggregates all commands for centralized access.
"""
from modules.system_command import (
    admin_command, my_id, uptime_command
    )

# Define your greeting message once for consistency
GREETING_MESSAGE = "Konichiwa"

async def start_command(update, context) -> None:
    """
    Greets the user in a friendly manner.

    Args:
        update (telegram.Update): Incoming update containing message information.
        context (telegram.ext.CallbackContext): Context containing information about the current state.
    """
    user_name = update.effective_user.full_name
    greeting = f"{GREETING_MESSAGE}, un gusto saludarte {user_name}!"
    await update.message.reply_text(greeting)

async def help_command(update, context):
    """Provides a list of commands and their descriptions."""
    commands_info = [
        # ("/start", "Inicia la interacción con el bot."),
        # ("/help", "Muestra esta ayuda."),
        # Add more commands as needed
    ]

    # Dynamically add other commands from the COMMANDS dictionary
    commands_info.extend((f"/{cmd}", command.__doc__ or "Sin descripción.") for cmd, command in COMMANDS.items() if cmd not in {'help', 'start'})

    commands_list = "\n".join([f"{command}: {description}" for command, description in commands_info])

    help_message = (
        f"{GREETING_MESSAGE}, aquí tienes una lista de comandos:\n\n"
        f"{commands_list}\n\n"
        "Recuerda que siempre puedes usar el comando /help para ver esta lista nuevamente."
    )
    await update.message.reply_text(help_message)

# Centralized list of all commands for dynamic registration
# 
# Sort and order the COMMANDS dictionary by module import
COMMANDS = {
    "start": start_command,
    "help": help_command,
    # System commands
    "uptime": uptime_command,
    "admin_cmd": admin_command,
    "my_id": my_id,
}
