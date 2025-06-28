import logging
import yfinance as yf
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "7429182869:AAFJUL3St8dSevmInoqz4PFO5RNKUISU9QM"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot aktif! Kirim /analisa_xau atau /analisa_btc")

async def analisa_xau(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = yf.download("XAUUSD=X", period="1d", interval="30m")
    candle = data.iloc[-1]
    open_ = candle["Open"]
    close = candle["Close"]
    trend = "naik 🚀" if close > open_ else "turun 📉"
    pesan = f"XAUUSD 30M: {close:.2f} ({trend})"
    await update.message.reply_text(pesan)

async def analisa_btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = yf.download("BTC-USD", period="1d", interval="30m")
    candle = data.iloc[-1]
    open_ = candle["Open"]
    close = candle["Close"]
    trend = "naik 🚀" if close > open_ else "turun 📉"
    pesan = f"BTCUSD 30M: {close:.2f} ({trend})"
    await update.message.reply_text(pesan)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("analisa_xau", analisa_xau))
app.add_handler(CommandHandler("analisa_btc", analisa_btc))

print("Bot sedang berjalan... 🚀")
app.run_polling()
