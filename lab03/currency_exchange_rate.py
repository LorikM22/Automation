import sys
import os
import json
import logging
from pathlib import Path
from datetime import datetime

import requests
from dotenv import load_dotenv

# Rădăcina proiectului = folderul părinte al lui lab03 (Automation/ local, /app în container)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
ERROR_LOG = PROJECT_ROOT / "error.log"

# Local cheia vine din lab02prep/.env; în container vine din env_file (docker-compose)
load_dotenv(PROJECT_ROOT / "lab02prep" / ".env")
API_KEY = os.getenv("API_KEY")

# În container API-ul NU este pe localhost, de aceea adresa se poate schimba din variabila API_URL
API_URL = os.getenv("API_URL", "http://localhost:8080/")


logging.basicConfig(
    filename=ERROR_LOG,
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def log_error(message):
    """Afișează eroarea și o salvează în error.log."""
    print(f"Eroare: {message}")
    logging.error(message)


def get_exchange_rate(from_currency, to_currency, date):
    """Trimite cererea către API și returnează rezultatul (sau None la eroare)."""

    try:
        response = requests.post(
            API_URL,
            params={
                "from": from_currency,
                "to": to_currency,
                "date": date
            },
            data={
                "key": API_KEY
            },
            timeout=10
        )

        # Citim mai întâi JSON-ul, ca să afișăm mesajul de eroare al API-ului
        # chiar dacă acesta răspunde cu un cod HTTP de eroare (ex. 400)
        try:
            result = response.json()
        except ValueError:
            response.raise_for_status()
            log_error("API-ul a returnat un răspuns care nu este JSON valid.")
            return None

        if result.get("error"):
            log_error(result["error"])
            return None

        response.raise_for_status()
        return result

    except requests.exceptions.RequestException as error:
        log_error(f"Nu s-a putut conecta la API ({API_URL}): {error}")
        return None


def save_data(result, from_currency, to_currency, date):
    """Salvează rezultatul în data/<FROM>_<TO>_<DATE>.json."""

    try:
        DATA_DIR.mkdir(exist_ok=True)

        filename = f"{from_currency}_{to_currency}_{date}.json"
        filepath = DATA_DIR / filename

        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)

        print(f"Datele au fost salvate în: {filepath}")
        return True

    except OSError as error:
        log_error(f"Nu s-a putut salva fișierul: {error}")
        return False


def validate_date(date):
    """Verifică formatul și perioada permisă."""

    try:
        date_object = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        log_error(
            f"Data '{date}' nu este validă. "
            f"Folosește formatul YYYY-MM-DD."
        )
        return False

    min_date = datetime.strptime("2025-01-01", "%Y-%m-%d").date()
    max_date = datetime.strptime("2025-09-15", "%Y-%m-%d").date()

    if date_object < min_date or date_object > max_date:
        log_error(
            f"Data {date} nu este în perioada disponibilă "
            f"(2025-01-01 – 2025-09-15)."
        )
        return False

    return True


def main():
    # Ora rulării apare în /var/log/cron.log, util pentru a verifica cron-ul
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Pornire: {' '.join(sys.argv[1:])}")

    if len(sys.argv) != 4:
        log_error(
            "Număr invalid de parametri. "
            "Utilizare: python currency_exchange_rate.py <FROM> <TO> <DATE>"
        )
        sys.exit(1)

    from_currency = sys.argv[1].upper()
    to_currency = sys.argv[2].upper()
    date = sys.argv[3]

    if not validate_date(date):
        sys.exit(1)

    result = get_exchange_rate(from_currency, to_currency, date)

    if result is None or not save_data(result, from_currency, to_currency, date):
        sys.exit(1)


if __name__ == "__main__":
    main()
