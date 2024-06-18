from telethon import TelegramClient, events
import asyncio

# API kimlik bilgilerinizi buraya yazın
api_id = '21871272'
api_hash = '57efa4949cd41dccd628c04b8507ff2b'
phone_number = '+12563655354'

welcome_message = 'Merhaba! Botumuza hoş geldiniz. Size nasıl yardımcı olabilirim?'
sent_messages = set()  # Gönderilen mesajları takip etmek için bir set kullanıyoruz

async def main():
    # TelegramClient'i başlatma
    client = TelegramClient('session_name', api_id, api_hash)

    # Giriş yapma
    await client.start(phone_number)

    @client.on(events.NewMessage)
    async def handler(event):
        sender = await event.get_sender()
        if sender.id not in sent_messages:
            await event.reply(welcome_message)
            sent_messages.add(sender.id)

    print("Bot çalışıyor...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
