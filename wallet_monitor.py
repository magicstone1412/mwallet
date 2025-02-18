import os
import json
import time
from config import WALLETS_FILE, LATEST_TX_FILE, LAST_RUN_FILE
from utils import fetch_transactions, fetch_crypto_prices, send_telegram_message

def load_json(file_path, default_value):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return default_value

def save_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f)

def load_last_run_time():
    if not os.path.exists(LAST_RUN_FILE):
        last_run_time = int(time.time()) # Get current time
        with open(LAST_RUN_FILE, "w") as f:
            f.write(str(last_run_time))
        return last_run_time  # Returns current time

    with open(LAST_RUN_FILE, "r") as f:
        return int(f.read())

def save_last_run_time():
    with open(LAST_RUN_FILE, "w") as f:
        f.write(str(int(time.time())))

def monitor_wallets():
    latest_tx_hashes = load_json(LATEST_TX_FILE, {})
    last_run_time = load_last_run_time()

    while True:
        try:
            crypto_prices = fetch_crypto_prices()

            with open(WALLETS_FILE, 'r') as f:
                wallets = [line.strip().split(':') for line in f.readlines()]

            for blockchain, wallet_address in wallets:
                transactions = fetch_transactions(wallet_address, blockchain)

                for tx in transactions:
                    tx_hash = tx['hash']
                    tx_time = int(tx['timeStamp'])

                    if tx_hash not in latest_tx_hashes and tx_time > last_run_time:
                        value = float(tx['value']) / 10**18
                        usd_value = value * crypto_prices[blockchain]
                        direction = "Incoming" if tx['to'].lower() == wallet_address.lower() else "Outgoing"
                        message = f"{direction} transaction on {wallet_address}\nValue: {value:.6f} {blockchain.upper()} (${usd_value:.2f})"
                        send_telegram_message(message)
                        latest_tx_hashes[tx_hash] = tx_time

            save_json(LATEST_TX_FILE, latest_tx_hashes)
            save_last_run_time()

            time.sleep(60)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)
