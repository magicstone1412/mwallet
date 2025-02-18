import os
from dotenv import load_dotenv

load_dotenv()

ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')
BSCSCAN_API_KEY = os.getenv('BSCSCAN_API_KEY')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
WALLETS_FILE = "watched_wallets.txt"
LATEST_TX_FILE = "latest_tx_hashes.json"
LAST_RUN_FILE = "last_run_time.txt"
