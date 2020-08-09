#Chad version
import requests

chat_id = 0
token = None

def send_message(text):
    requests.get(f'https://api.telegram.org/bot{token}/sendMessage', data={'chat_id': chat_id, 'text': text})