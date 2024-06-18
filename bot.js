const MTProto = require('telegram-mtproto').MTProto;
const { Storage } = require('mtproto-storage-fs');
const input = require('input');
const path = require('path');

// Telegram API kimlik bilgileri
const api = {
  layer: 57,
  initConnection: 0x69796de9,
  api_id: '21871272', // Telegram API ID'nizi buraya yazın
  api_hash: '57efa4949cd41dccd628c04b8507ff2b' // Telegram API Hash'inizi buraya yazın
};

// Sunucu ayarları
const server = {
  dev: false // Geliştirici modda iseniz true yapın
};

const app = {
  storage: new Storage(path.resolve(__dirname, './storage.json'))
};

// MTProto istemcisini oluşturma
const client = MTProto({ server, api, app });

const phone = {
  num: '+12563655354', // Telefon numaranızı buraya yazın
};

const welcomeMessage = 'Merhaba! Botumuza hoş geldiniz. Size nasıl yardımcı olabilirim?';

// Gönderilen mesajları takip etmek için bir Set kullanıyoruz
const sentMessages = new Set();

async function getCode() {
  const { phone_code_hash } = await client('auth.sendCode', {
    phone_number: phone.num,
    current_number: false,
    api_id: api.api_id,
    api_hash: api.api_hash
  });
  return phone_code_hash;
}

async function signIn(codeHash, code) {
  const { user } = await client('auth.signIn', {
    phone_number: phone.num,
    phone_code_hash: codeHash,
    phone_code: code
  });
  return user;
}

async function handleMessage(update) {
  const messages = update.updates.filter(u => u._ === 'updateNewMessage');

  for (const message of messages) {
    const chatId = message.message.peer_id.user_id;

    // Daha önce bu kullanıcıya mesaj gönderilmediyse karşılama mesajı gönder
    if (!sentMessages.has(chatId)) {
      await client('messages.sendMessage', {
        peer: { _: 'inputPeerUser', user_id: chatId },
        message: welcomeMessage,
        random_id: Math.random() * 0xffffff | 0
      });

      // Kullanıcıyı gönderilen mesajlar setine ekle
      sentMessages.add(chatId);
    }
  }
}

async function main() {
  try {
    const codeHash = await getCode();
    console.log('Telegramdan aldığınız kodu girin:');
    const code = await input.text('Kod:');
    const user = await signIn(codeHash, code);
    console.log(`Giriş yaptınız: ${user.username}`);

    client.updates.on('updates', handleMessage);

  } catch (err) {
    console.error(err);
  }
}

main();
