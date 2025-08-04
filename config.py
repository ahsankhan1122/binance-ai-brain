import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Correctly fetch environment variables
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
TIMEFRAME = os.getenv("TIMEFRAME", "15m")
SCAN_INTERVAL = int(os.getenv("SCAN_INTERVAL", 60))
