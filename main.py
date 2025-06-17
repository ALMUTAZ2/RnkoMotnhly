import asyncio
import time
import os
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By

from aiogram import Bot
from aiogram.types import FSInputFile

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# إعداد البوت (نفس الطريقة الأصلية)
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# العملات المطلوبة (نفس القائمة الأصلية)
symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]

def setup_driver():
    """إعداد المتصفح للعمل على السيرفر"""
    options = Options()
    options.add_argument("--headless")  # تشغيل بدون واجهة
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")  # نفس الحجم الأصلي
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins")
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")
    
    # إعداد تفضيلات مشابهة للكود الأصلي
    options.set_preference("layout.css.devPixelsPerPx", "1.0")
    
    service = Service()
    return webdriver.Firefox(service=service, options=options)

async def capture_and_send(symbol, driver):
    """نفس الوظيفة الأصلية مع تحسينات للسيرفر"""
    print(f"📈 تحميل الشارت: {symbol}")
    try:
        # نفس الرابط الأصلي
        driver.get(f"https://www.tradingview.com/chart/?symbol=BINANCE:{symbol}")
        time.sleep(8)  # انتظار أطول قليلاً للسيرفر
        
        # محاولة العثور على منطقة الشارت (نفس الطريقة الأصلية)
        try:
            chart = driver.find_element(By.CSS_SELECTOR, ".layout__area--center")
        except:
            # بديل في حالة عدم العثور على العنصر
            chart = driver.find_element(By.CSS_SELECTOR, ".chart-container")
        
        # حفظ الصورة في مجلد مؤقت
        file_name = f"/tmp/{symbol}.png"
        chart.screenshot(file_name)

        # إرسال الصورة (نفس الطريقة الأصلية)
        photo = FSInputFile(file_name)
        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID, 
            text=f"📊 شارت {symbol} - Renko Monthly"  # نفس النص الأصلي
        )
        await bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=photo)

        # حذف الملف (نفس الطريقة الأصلية)
        os.remove(file_name)
        print(f"✅ تم إرسال {symbol}")

    except Exception as e:
        print(f"❌ خطأ في {symbol}: {e}")

async def main():
    """نفس الوظيفة الرئيسية مع تعديلات السيرفر"""
    print("🚀 بدء تشغيل بوت الشارتات...")
    
    driver = setup_driver()
    
    try:
        # نفس الحلقة الأصلية
        for symbol in symbols:
            await capture_and_send(symbol, driver)
            time.sleep(2)  # انتظار بين الشارتات
            
    finally:
        driver.quit()  # نفس الطريقة الأصلية
        await bot.session.close()  # نفس الطريقة الأصلية
        
    print("✅ تم الانتهاء من جميع الشارتات")

if __name__ == "__main__":
    asyncio.run(main())  # نفس طريقة التشغيل الأصلية
