FROM python:3.12-slim

# Fusul orar al Moldovei, ca 06:00 și 17:00 să fie ora locală, nu UTC
ENV TZ=Europe/Chisinau \
    PYTHONUNBUFFERED=1 \
    LANG=C.UTF-8

# 1. Dependențe de sistem: cron și datele despre fusuri orare
RUN apt-get update \
    && apt-get install -y --no-install-recommends cron tzdata \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 1. Bibliotecile Python necesare scriptului
COPY requirements.txt /app/lab03/requirements.txt
RUN pip install --no-cache-dir -r /app/lab03/requirements.txt

# 2. Copiem scriptul, fișierul cronjob și entrypoint-ul
COPY currency_exchange_rate.py /app/lab03/currency_exchange_rate.py
COPY cronjob /app/lab03/cronjob
COPY entrypoint.sh /entrypoint.sh

# 3. Configurăm cron: eliminăm terminațiile Windows (CRLF) și instalăm crontab-ul
RUN sed -i 's/\r$//' /app/lab03/cronjob /entrypoint.sh \
    && chmod 0644 /app/lab03/cronjob \
    && crontab /app/lab03/cronjob \
    && chmod +x /entrypoint.sh

# 4–5. La pornire: se creează /var/log/cron.log și se lansează cron
ENTRYPOINT ["/entrypoint.sh"]
