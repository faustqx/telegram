const { TelegramClient } = require("telegram");
const { StringSession } = require("telegram/sessions");
const input = require('input'); // Kullanıcıdan veri almak için

const apiId = '21871272'; // Telegram API ID'nizi buraya yazın
const apiHash = '57efa4949cd41dccd628c04b8507ff2b'; // Telegram API Hash'inizi buraya yazın
const stringSession = new StringSession(''); // Dize oturumu

const welcomeMessage = 'Merhaba! Botumuza hoş geldiniz. Size nasıl yardımcı olabilirim?';

// Gönderilen mesajları takip etmek için bir Set kullanıyoruz
const sentMessages = new Set();

(async () => {
    console.log("Loading interactive example...");
    const client = new TelegramClient(stringSession, apiId, apiHash, { connectionRetries: 5 });
    await client.start({
        phoneNumber: async () => await input.text("Lütfen telefon numaranızı girin: "),
        password: async () => await input.text("Lütfen iki faktörlü kimlik doğrulama şifrenizi girin: "),
        phoneCode: async () => await input.text("Lütfen Telegram'dan gelen kodu girin: "),
        onError: (err) => console.log(err),
    });
    console.log("Kişisel hesaba giriş yapıldı.");
    console.log(client.session.save()); // Oturum dizesini saklayın

    client.addEventHandler(async (event) => {
        const message = event.message;
        const sender = await message.getSender();
        
        if (sender && !sentMessages.has(sender.id)) {
            await client.sendMessage(sender, { message: welcomeMessage });
            sentMessages.add(sender.id);
        }
    }, { event: 'message' });

    console.log("Bot çalışıyor...");
})();
