FROM python:3.13-alpine

RUN pip install --upgrade pip

LABEL Maintainer="skywirex.com"

WORKDIR /app

COPY . .

## set blank ENV
ARG TELEGRAM_BOT_TOKEN
ARG TELEGRAM_CHAT_ID
ARG ETHERSCAN_API_KEY
ARG BSCSCAN_API_KEY

## set blank ENV
ENV TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN

ENV TELEGRAM_CHAT_ID=$TELEGRAM_CHAT_ID

ENV ETHERSCAN_API_KEY=$ETHERSCAN_API_KEY

ENV BSCSCAN_API_KEY=$BSCSCAN_API_KEY
## end set blank ENV

RUN apk --no-cache add ca-certificates #Avoid an error occurred: HTTPSConnectionPool

RUN pip install --no-cache-dir -r requirements.txt

## CMD [ "python", "./main.py"]