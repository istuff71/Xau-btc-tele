import logging
import yfinance as yf
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "7429182869:AAFJUL3St8dSevmInoqz4PFO5RNKUISU9QM"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def get_trend(data):
    candle = data.iloc[-1]
    return "Bullish 🚀" if candle["Close"] > candle["Open"] else "Bearish 📉", candle["Close"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot aktif! Kirim /analisa_xau, /analisa_btc, atau /analisa_mtf_xau /analisa_mtf_btc")

async def analisa_xau(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = yf.download("XAUUSD=X", period="1d", interval="30m")
    trend, close = get_trend(data)
    pesan = f"XAUUSD 30M: {close:.2f} ({trend})"
    await update.message.reply_text(pesan)

async def analisa_btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = yf.download("BTC-USD", period="1d", interval="30m")
    trend, close = get_trend(data)
    pesan = f"BTCUSD 30M: {close:.2f} ({trend})"
    await update.message.reply_text(pesan)

async def analisa_mtf_xau(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data_h1 = yf.download("XAUUSD=X", period="1d", interval="60m")
    data_m30 = yf.download("XAUUSD=X", period="1d", interval="30m")
    trend_h1, price_h1 = get_trend(data_h1)
    trend_m30, price_m30 = get_trend(data_m30)
    sinyal = "BUY ✅" if "Bullish" in trend_h1 and "Bullish" in trend_m30 else              "SELL ⚠️" if "Bearish" in trend_h1 and "Bearish" in trend_m30 else              "Tunggu Konfirmasi ⏳"
    pesan = (
        f"📊 Multi-Timeframe XAUUSD
"
        f"H1: {trend_h1} ({price_h1:.2f})
"
        f"M30: {trend_m30} ({price_m30:.2f})

"
        f"Sinyal Gabungan: {sinyal}"
    )
    await update.message.reply_text(pesan)

async def analisa_mtf_btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data_h1 = yf.download("BTC-USD", period="1d", interval="60m")
    data_m30 = yf.download("BTC-USD", period="1d", interval="30m")
    trend_h1, price_h1 = get_trend(data_h1)
    trend_m30, price_m30 = get_trend(data_m30)
    sinyal = "BUY ✅" if "Bullish" in trend_h1 and "Bullish" in trend_m30 else              "SELL ⚠️" if "Bearish" in trend_h1 and "Bearish" in trend_m30 else              "Tunggu Konfirmasi ⏳"
    pesan = (
        f"📊 Multi-Timeframe BTCUSD
"
        f"H1: {trend_h1} ({price_h1:.2f})
"
        f"M30: {trend_m30} ({price_m30:.2f})

"
        f"Sinyal Gabungan: {sinyal}"
    )
    await update.message.reply_text(pesan)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("analisa_xau", analisa_xau))
app.add_handler(CommandHandler("analisa_btc", analisa_btc))
app.add_handler(CommandHandler("analisa_mtf_xau", analisa_mtf_xau))
app.add_handler(CommandHandler("analisa_mtf_btc", analisa_mtf_btc))

print("Bot sedang berjalan... 🚀")
app.run_polling()
