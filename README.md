# SensEI Telegram Bot

"SensEI" is a Telegram bot application built with Django and serves content using WSGI Gunicorn.

## Database

The application utilizes PostgreSQL as its primary database.

## Models

Here's a brief overview of the models being used:

### 1. Profile

- **external_id**: Represents the user's ID in the social network. Each ID is unique.
- **name**: Stores the name of the user.

Representation: `#{external_id} {name}`

### 2. Message

- **profile**: ForeignKey linking to the Profile model. Represents the user's profile.
- **user_text**: Text messages sent by the user.
- **bot_answer**: Responses sent by the bot to the user.
- **created_at**: Timestamp indicating when the message was received.

Representation: `Message {primary_key} {profile}`

### 3. UserPrompt

- **profile**: ForeignKey linking to the Profile model. Represents the user's profile.
- **prompt**: Text of the prompt.
- **created_at**: Timestamp indicating when the prompt was created.

Representation: `UserPrompt {primary_key} {profile}`

## How to Use

To get a prompt for a user, simply input the command `/start`.


### Установка вебхука для Telegram бота
Этот код позволяет установить вебхук для вашего Telegram бота. 
Вебхук позволяет Telegram отправлять входящие обновления (сообщения, события и т. д.) на указанный URL. 
Вы можете использовать этот механизм, чтобы интегрировать своего бота с вашим приложением или сервисом.
Чтобы настроить вебхук для вашего Telegram бота, выполните следующие шаги:

Откройте терминал или командную строку в каталоге вашего проекта.

#### Для Windows (PowerShell):

```
powershell
Invoke-WebRequest `
-Uri 'https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook' `
-Method Post `
-Body @{url='<YOUR_WEBHOOK_URL>'}
```

#### Для Linux и macOS (Bash):
```
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"url": "<YOUR_WEBHOOK_URL>"}' \
     "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook"
```

### Request
```
 Invoke-WebRequest `
 -Uri 'https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook' `
 -Method Post `
 -Body @{url='https://tgsensei.evolwe.ai/telegram_webhook/'}                                                          
```
### Response
```
StatusCode        : 200
StatusDescription : OK
Content           : {"ok":true,"result":true,"description":"Webhook was set"}
RawContent        : HTTP/1.1 200 OK
                    Connection: keep-alive
                    Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
                    Access-Control-Allow-Origin: *
                    Access-Control-Allow-Methods: GET, POST, OPTIONS
                    Acce...
Forms             : {}
Headers           : {[Connection, keep-alive], [Strict-Transport-Security, max-age=31536000; includeSubDomains; preload
                    ], [Access-Control-Allow-Origin, *], [Access-Control-Allow-Methods, GET, POST, OPTIONS]...}
Images            : {}
InputFields       : {}
Links             : {}
ParsedHtml        : mshtml.HTMLDocumentClass
RawContentLength  : 57
```

### Проверить установлен ли webhook

#### Windows:
```
Invoke-WebRequest -Uri "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo"
```

#### Для Linux и macOS (Bash):
```
curl https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo
```



## Additional Information
- **Setup Instructions**: How to get the bot running locally, necessary environment variables, etc.
- **API Endpoints (if any)**: Detailed documentation about the endpoints, how to call them, and what responses to expect.
- **Deployment**: Steps for deploying the bot to a live environment.
- **Contributing**: Guidelines for developers who want to contribute.
