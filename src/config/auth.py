#!/bin/env python
# -*- coding: UTF-8 -*-

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

TOKEN = os.getenv("TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

# Validate essential environment variables
if not TOKEN:
    raise ValueError("The Telegram bot TOKEN is missing from the environment variables.")

if not ADMIN_ID:
    raise ValueError("The ADMIN_ID is missing from the environment variables.")


