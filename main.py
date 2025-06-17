import asyncio
import time
import os
from datetime import datetime
import requests

from aiogram import Bot

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# إعداد البوت
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# العملات المطلوبة
symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]

def get_crypto_price(symbol):
  """جلب سعر العملة من Binance API"""
  try:
      url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
      response = requests.get(url)
      data = response.json()
      return float(data['price'])
  except Exception as e:
      print(f"❌ خطأ في جلب سعر {symbol}: {e}")
      return None

async def send_crypto_report():
  """إرسال تقرير أسعار العملات"""
  print("🚀 بدء تشغيل بوت العملات...")
  
  report = "📊 **تقرير العملات الشهري - Renko Monthly**\n\n"
  
  for symbol in symbols:
      price = get_crypto_price(symbol)
      if price:
          # تنسيق السعر حسب العملة
          if symbol == "BTCUSDT":
              formatted_price = f"${price:,.2f}"
          elif symbol == "ETHUSDT":
              formatted_price = f"${price:,.2f}"
          else:
              formatted_price = f"${price:.4f}"
          
          report += f"🔸 **{symbol.replace('USDT', '')}**: {formatted_price}\n"
      else:
          report += f"❌ **{symbol.replace('USDT', '')}**: غير متاح\n"
      
      time.sleep(0.5)  # تجنب الإفراط في الطلبات
  
  report += f"\n⏰ **وقت التحديث**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
  
  try:
      await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=report, parse_mode='Markdown')
      print("✅ تم إرسال التقرير بنجاح")
  except Exception as e:
      print(f"❌ خطأ في إرسال التقرير: {e}")

async def main():
  """الوظيفة الرئيسية"""
  try:
      await send_crypto_report()
  finally:
      await bot.session.close()
      
  print("✅ تم الانتهاء من التقرير")

if __name__ == "__main__":
  asyncio.run(main())
