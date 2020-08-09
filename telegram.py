import threading
import requests
import json
import time

class Bot():

    def __init__(self, token):
        self.token = token
        self.message_hooks = list()
        self.command_hooks = dict()
        self.offset = 0
        self.stop = True

    def send_message(self, chat_id, text):
        requests.get(f'https://api.telegram.org/bot{self.token}/sendMessage', data={'chat_id': chat_id, 'text': text})

    def process_updates(self, update_offset=True):
        updates = json.loads(requests.get(f'https://api.telegram.org/bot{self.token}/getUpdates', data={'offset': self.offset}).text)
        if updates['ok']:
            for u in updates['result']:
                if update_offset:
                    self.offset = u['update_id'] + 1
                if 'message' in u:
                    message = u['message']
                    if 'entities' in message:
                        if message['entities'][0]['type'] == 'bot_command':
                            args = message['text'][1:].split()
                            if args[0] in self.command_hooks:
                                self.command_hooks[args[0]](args, message)
                            break
                    for hook in self.message_hooks:
                        hook(message)
                elif 'channel_post' in u:
                    for hook in self.message_hooks:
                        hook(u['channel_post'])
        return updates

    # Helpers, not really needed
    
    def message_hook(self, hook):
        self.message_hooks.append(hook)

    def command_hook(self, hook, command):
        self.command_hooks[command] = hook

    def _poll(self, wait):
        while not self.stop:
            self.process_updates()
            time.sleep(wait)

    def start_polling(self, wait=10):
        if not self.stop:
            raise Exception('Stop wtf')
        self.stop = False
        self._thread = threading.Thread(target=self._poll, args=[wait], daemon=True)
        self._thread.start()

    def stop_polling(self):  # Not immediate, but shouldn't matter
        self.stop = True
        