# Telegram-бот для отметки на мероприятие

Бот позволяет:
- отметить, что пользователь придет
- выбрать стандартное время прихода
- ввести свое время вручную
- отметить, что не придет
- посмотреть свой текущий статус
- администратору посмотреть список `/list`
- администратору посмотреть статистику `/stats`

## Структура

```text
.
├── bot.py
├── requirements.txt
├── .env.example
└── app
    ├── config.py
    ├── database.py
    ├── keyboards.py
    ├── texts.py
    ├── utils.py
    └── handlers
        ├── admin.py
        ├── common.py
        └── registration.py
```

## Запуск

### 1. Установить зависимости

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
```

Для Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Настроить окружение

Скопируй `.env.example` в `.env`:

```bash
cp .env.example .env
```

Заполни:
- `BOT_TOKEN` — токен от BotFather
- `ADMIN_IDS` — твой Telegram user id, можно несколько через запятую

### 3. Запустить

```bash
python bot.py
```

## Команды

Для всех:
- `/start`
- `/menu`

Для админа:
- `/list`
- `/stats`

## Как это работает

Бот сохраняет данные в SQLite (`bot.db`).
Для каждого пользователя на текущую дату хранится одна запись:
- статус `coming` или `not_coming`
- время прихода

Если пользователь отмечается повторно, запись обновляется.
