from threading import Thread
from bot import setup_bot
from wallet_monitor import monitor_wallets

if __name__ == "__main__":
    Thread(target=setup_bot).start()
    print("Telegram bot started.")
    monitor_wallets()
