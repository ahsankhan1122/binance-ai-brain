import time
import pandas as pd
from binance.client import Client
from binance.enums import *
from telegram import Bot
from config import *
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Initialize Binance and Telegram
client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)
telegram_bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("google_credentials.json", scope)
gs_client = gspread.authorize(creds)
sheet = gs_client.open_by_key(GOOGLE_SHEET_ID).sheet1

def get_top_gainers():
    tickers = client.get_ticker()
    df = pd.DataFrame(tickers)
    df['priceChangePercent'] = pd.to_numeric(df['priceChangePercent'])
    top_gainers = df.sort_values(by='priceChangePercent', ascending=False).head(5)
    return top_gainers['symbol'].tolist()

def generate_signal(symbol):
    klines = client.get_klines(symbol=symbol, interval=TIMEFRAME, limit=50)
    df = pd.DataFrame(klines, columns=['time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 
                                       'quote_asset_volume', 'trades', 'taker_base', 'taker_quote', 'ignore'])
    df['close'] = pd.to_numeric(df['close'])
    
    df['ema_fast'] = df['close'].ewm(span=9).mean()
    df['ema_slow'] = df['close'].ewm(span=21).mean()
    
    if df['ema_fast'].iloc[-1] > df['ema_slow'].iloc[-1]:
        return "BUY"
    elif df['ema_fast'].iloc[-1] < df['ema_slow'].iloc[-1]:
        return "SELL"
    return "HOLD"

def send_telegram_message(message):
    telegram_bot.send_message(chat_id="@YourChannelOrChatID", text=message)

def log_to_google_sheets(data):
    sheet.append_row(data)

def main():
    while True:
        try:
            gainers = get_top_gainers()
            for coin in gainers:
                signal = generate_signal(coin)
                message = f"Signal for {coin}: {signal}"
                print(message)
                send_telegram_message(message)
                log_to_google_sheets([coin, signal, time.strftime("%Y-%m-%d %H:%M:%S")])
            time.sleep(SCAN_INTERVAL)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
