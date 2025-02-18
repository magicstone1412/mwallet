import re
from telegram.ext import Updater, CommandHandler
from config import TELEGRAM_BOT_TOKEN, WALLETS_FILE
from wallet_monitor import monitor_wallets

def start(update, context):
    message = "Welcome! Use /add <blockchain> <wallet> or /remove <blockchain> <wallet>."
    context.bot.send_message(chat_id=update.message.chat_id, text=message)

def add(update, context):
    if len(context.args) < 2:
        update.message.reply_text("Usage: /add <blockchain> <wallet_address>")
        return

    blockchain, wallet_address = context.args[0].lower(), context.args[1]

    if not re.match(r'^0x[a-fA-F0-9]{40}$', wallet_address):
        update.message.reply_text("Invalid wallet address.")
        return

    with open(WALLETS_FILE, 'a') as f:
        f.write(f"{blockchain}:{wallet_address}\n")

    update.message.reply_text(f"Added {wallet_address} to {blockchain.upper()} monitoring.")

def remove(update, context):
    if len(context.args) < 2:
        update.message.reply_text("Usage: /remove <blockchain> <wallet_address>")
        return

    blockchain, wallet_address = context.args[0].lower(), context.args[1]

    with open(WALLETS_FILE, 'r') as f:
        lines = f.readlines()
    with open(WALLETS_FILE, 'w') as f:
        for line in lines:
            if line.strip() != f"{blockchain}:{wallet_address}":
                f.write(line)

    update.message.reply_text(f"Removed {wallet_address} from {blockchain.upper()} monitoring.")

def setup_bot():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('add', add))
    dispatcher.add_handler(CommandHandler('remove', remove))
    updater.start_polling()
