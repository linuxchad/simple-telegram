import telegram
import time
import os

def message_test(message):
    if 'from' in message:
        print(f'Message from {message["from"]["first_name"]}(ChatID: {message["chat"]["id"]}): {message["text"]}')
    else:
        print(f'Message from {message["chat"]["title"]}: {message["text"]}')

def command_test(args, message):
    print(f'Command from {message["from"]["first_name"]}(ChatID: {message["chat"]["id"]}): {args}')

bot = telegram.Bot(os.environ['TOKEN'])
bot.message_hook(message_test)
bot.command_hook(command_test, 'start')
bot.start_polling(wait=1)
time.sleep(10)
bot.stop_polling()