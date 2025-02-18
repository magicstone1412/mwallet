import requests
import json
import time
from config import ETHERSCAN_API_KEY, BSCSCAN_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def fetch_transactions(wallet_address, blockchain):
    api_url = {
        'eth': f'https://api.etherscan.io/api?module=account&action=txlist&address={wallet_address}&sort=desc&apikey={ETHERSCAN_API_KEY}',
        'bnb': f'https://api.bscscan.com/api?module=account&action=txlist&address={wallet_address}&sort=desc&apikey={BSCSCAN_API_KEY}'
    }.get(blockchain, None)

    if not api_url:
        raise ValueError("Invalid blockchain specified")

    response = requests.get(api_url)
    data = response.json()

    return data.get('result', []) if isinstance(data.get('result', []), list) else []

def fetch_crypto_prices():
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=ethereum%2Cbinancecoin&vs_currencies=usd'
    response = requests.get(url).json()
    return {
        'eth': response['ethereum']['usd'],
        'bnb': response['binancecoin']['usd']
    }

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': message, 'parse_mode': 'HTML'}
    requests.post(url, data=payload)
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Sent: {message}")
