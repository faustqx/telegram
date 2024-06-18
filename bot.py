from telethon import TelegramClient, events
import asyncio

# API kimlik bilgilerinizi buraya yazın
api_id = '21871272'
api_hash = '57efa4949cd41dccd628c04b8507ff2b'
phone_number = '+12563655354'

# Kullanıcının mesajlarına verilecek yanıtlar
response_map = {
    0: 'Merhaba! Nasıl yardımcı olabilirim?',
    1: 'Fiyat listesi: Example 2500₺, 5000₺'
}

# Kullanıcıların yanıt sırasını takip etmek için bir sözlük kullanıyoruz
user_messages_count = {}

async def main():
    # TelegramClient'i başlatma
    client = TelegramClient('session_name', api_id, api_hash)

    # Giriş yapma
    await client.start(phone_number)

    @client.on(events.NewMessage)
    async def handler(event):
        sender = await event.get_sender()
        sender_id = sender.id
        message_text = event.raw_text.lower()

        # Kullanıcının mesaj sayısını al veya sıfırla
        if sender_id not in user_messages_count:
            user_messages_count[sender_id] = 0
        else:
            user_messages_count[sender_id] += 1

        # Yanıt verilecek mesajı bul ve gönder
        response_index = user_messages_count[sender_id]
        if response_index in response_map:
            response = response_map[response_index]
            await event.reply(response)

    print("Bot çalışıyor...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
