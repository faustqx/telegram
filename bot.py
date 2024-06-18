from telethon import TelegramClient, events
import asyncio

# API kimlik bilgilerinizi buraya yazın
api_id = '27777717'
api_hash = '7591c98b80d35f58d380e68e526ac589'
phone_number = '+905318635833'

# Her bir saatlik mesaj
hourly_message = (
    "💗 KENDİME AİT YERİM YOK 💗\n\n"
    "🔥SEVGİLİ TADINDA GÖRÜŞÜYORUM 🔥\n\n"
    "🏠 EVE. OTELE. APARTA REZiDANS. GELiYORUM\n\n"
    "💸 ÜCRET ELDEN\n\n"
    "❗️ÖNDEN ÖDEME YOK\n\n"
    "Sevgili Tadinda Guven Ve Kalite Ön Planda"
)

async def send_hourly_message(client):
    while True:
        print("Tüm sohbetlere mesaj gönderiliyor...")
        async for dialog in client.iter_dialogs():
            if dialog.is_user and not dialog.entity.bot:  # Kullanıcılara mesaj gönder, botlara değil
                await client.send_message(dialog.id, hourly_message)
        print("Mesajlar gönderildi.")
        await asyncio.sleep(3600)  # 1 saat bekle

async def main():
    # TelegramClient'i başlatma
    client = TelegramClient('session_name', api_id, api_hash)

    # Giriş yapma
    await client.start(phone_number)

    # Saatlik mesajları göndermek için arka plan görevini başlatma
    asyncio.create_task(send_hourly_message(client))

    print("Bot çalışıyor...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
    
