from telethon import TelegramClient, events, Button
import asyncio

# API kimlik bilgilerinizi buraya yazın
api_id = '27399795'
api_hash = 'c6d90d96b20a5f52c04f1e8cb3935c4a'
phone_number = '+905300842733'

# Her bir saatlik mesaj
hourly_message = (
    "💗 KENDİME AİT YERİM YOK 💗\n\n"
    "🔥SEVGİLİ TADINDA GÖRÜŞÜYORUM 🔥\n\n"
    "🏠 EVE. OTELE. APARTA REZiDANS. GELiYORUM\n\n"
    "💸 ÜCRET ELDEN\n\n"
    "❗️ÖNDEN ÖDEME YOK\n\n"
    "Sevgili Tadinda Guven Ve Kalite Ön Planda"
)

# Gönderilecek fotoğrafın yolu
photo_path = 'fotoğraf.jpg'

# Buton ile yönlendirilecek link
button_url = "https://wa.me/+905346254881"
button_text = "Detaylar için tıklayın"

# Grupların kullanıcı adlarını `gruplar.txt` dosyasından oku
with open('gruplar.txt', 'r') as file:
    group_usernames = [line.strip() for line in file.readlines()]

async def send_hourly_message(client):
    while True:
        print("Belirtilen gruplara mesaj gönderiliyor...")
        for group_username in group_usernames:
            try:
                entity = await client.get_entity(group_username)
                await client.send_message(entity, hourly_message, buttons=[Button.url(button_text, button_url)])
                await client.send_file(entity, photo_path, caption=hourly_message)
                print(f"{group_username} grubuna mesaj ve fotoğraf gönderildi.")
            except Exception as e:
                print(f"{group_username} grubuna mesaj ve fotoğraf gönderilemedi: {e}")
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
