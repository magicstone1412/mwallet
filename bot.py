import re
import os
from telegram.ext import Updater, CommandHandler
from config import TELEGRAM_BOT_TOKEN, WALLETS_FILE
from wallet_monitor import monitor_wallets


def start(update, context):
    message = "Welcome! Use /add <blockchain> <wallet> or /remove <blockchain> <wallet>."
    context.bot.send_message(chat_id=update.message.chat_id, text=message)


def get_all_wallets():
    """Read the list of all tracked wallets from file."""
    if not os.path.exists(WALLETS_FILE):
        return []

    with open(WALLETS_FILE, "r") as f:
        return [line.strip() for line in f.readlines()]


def add_wallet(wallet_address, blockchain):
    """Add a wallet to the tracking list if it doesn't already exist."""
    wallets = get_all_wallets()

    # Normalize data: lowercase blockchain, trim wallet address
    blockchain = blockchain.lower().strip()
    wallet_address = wallet_address.strip()

    wallet_entry = f"{blockchain}:{wallet_address}"

    if wallet_entry in wallets:
        return False, wallets  # Wallet already exists, do not add

    with open(WALLETS_FILE, "a") as f:
        f.write(wallet_entry + "\n")

    return True, wallets + [wallet_entry]  # Add wallet and return updated list


def add(update, context):
    if len(context.args) < 2:
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Please provide a blockchain and a wallet address to add.")
        return

    # Trim whitespace from input data
    blockchain = context.args[0].strip().lower()
    wallet_address = context.args[1].strip()

    # Validate blockchain
    if blockchain not in ["eth", "bnb"]:
        context.bot.send_message(chat_id=update.message.chat_id, text=f"Invalid blockchain: {blockchain}")
        return

    # Validate wallet address format
    if not re.match(r"^0x[a-fA-F0-9]{40}$", wallet_address):
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=f"{wallet_address} is not a valid wallet address.")
        return

    added, wallets = add_wallet(wallet_address, blockchain)

    if added:
        message = f"✅ {wallet_address} has been added to the tracking list."
    else:
        message = f"⚠ Wallet {wallet_address} is already in the list."

    # Send the updated list of tracked wallets
    message += "\n\n📋 *All tracked wallets:*\n" + "\n".join(wallets)
    context.bot.send_message(chat_id=update.message.chat_id, text=message, parse_mode="Markdown")


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
