# Build stage
FROM python:3.10-alpine AS builder

WORKDIR /app

RUN python -m venv /app/venv

# Enable venv
ENV PATH="/app/venv/bin:$PATH"

COPY requirements.txt .

RUN pip install -r requirements.txt

# Final stage
FROM python:3.10-alpine

WORKDIR /app

COPY --from=builder /app/venv /app/venv

COPY . .

ARG TELEGRAM_BOT_TOKEN

ARG TELEGRAM_CHAT_ID

ARG ETHERSCAN_API_KEY

ARG BSCSCAN_API_KEY

ENV PATH="/app/venv/bin:$PATH"

CMD  ["python", "./main.py"]