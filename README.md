# 🧠 Бот для отслеживания мемкойнов — Solana и Ethereum

Этот бот автоматически отслеживает новые токены в Solana и Ethereum, фильтрует их по ключевым метрикам (контракты, ликвидность, холдеры, авторы) и отправляет уведомления в Telegram.

---

## 🚀 Возможности

- Получение данных с Solscan / Etherscan / Birdeye и др.
- Фильтрация по параметрам (LP, holders, deployer history)
- Сохранение постов в формате .txt для каждого аккаунта
- Многопоточная работа ботов с очередями
- Подключение через ZennoPoster / Flask / Telegram

---

## 📦 Установка

```bash
git clone https://github.com/IvanDeFi/memecoin-watcher-bot.git
cd memecoin-watcher-bot
pip install -r requirements.txt
```

---

## ⚙️ Настройка

Создайте `.env` файл, скопировав `.env.example`:

```bash
cp .env.example .env
```

Отредактируйте `.env`, добавив свои ключи:

```env
TELEGRAM_TOKEN=ваш_токен
TELEGRAM_CHAT_ID=ваш_chat_id
ETHERSCAN_API_KEY=ваш_ключ
SOLSCAN_API_KEY=ваш_ключ
...
```

---

## 🧪 Запуск

```bash
python main.py
```

---

## 📁 Структура проекта

```
memecoin-watcher-bot/
├── main.py
├── config.yaml
├── .env
├── accounts/
│   ├── account1.txt
│   ├── ...
├── logs/
├── utils/
│   ├── logger.py
│   └── ...
└── ...
```

---

## 💬 Дополнительно

Можно подключить:
- ZennoPoster (парсинг, запуск шаблонов, постинг)
- Telegram Bot (уведомления)
- Flask (админка/GUI по желанию)

---

## 🛡 Безопасность

Файл `.env` НЕ должен загружаться на GitHub. Добавлен в `.gitignore`.
