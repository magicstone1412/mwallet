# mwallet

## Docker
### Clone
```
git clone https://github.com/magicstone1412/mwallet.git
cd mwallet
```
### Build
```
docker build -t skywirex/mwallet .
```
### Run
```
docker run -d --name mwallet \
  -e "TELEGRAM_BOT_TOKEN=1058413446:AAEj0N0AuvXbu-Kd0egdRS_MC33xxxxxxxx" \
  -e "TELEGRAM_CHAT_ID=-1000000000000" \
  -e "ETHERSCAN_API_KEY=XXXXXJDGFDTCVBY1B4YX4Z8GN45CJXXXXX" \
  -e "BSCSCAN_API_KEY=XXXXXX8QDPZA6BEJU596P6XD5G26TXXXXX" \
  --restart=unless-stopped \
 skywirex/mwallet
```

## Reference

Group chat ID: https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id


## Structure

/crypto_bot
│── bot.py
│── config.py
│── main.py
│── utils.py
│── wallet_monitor.py
│── requirements.txt
│── Dockerfile
│── .env

## Disclaimer

This bot is provided for educational purposes only and should not be used as financial advice. The bot does not have access to your wallet.