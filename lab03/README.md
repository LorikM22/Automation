# Laboratorul 3 – Automatizarea scriptului cu cron

## Scopul laboratorului

Scopul laboratorului este configurarea planificatorului de sarcini **cron** pentru rularea automată a scriptului `currency_exchange_rate.py` din laboratorul 2. Cron rulează într-un container Docker, iar rezultatul fiecărei sarcini este scris în `/var/log/cron.log`.

---

## Structura proiectului

```text
Automation/
├── lab02/                         # laboratorul 2 (scriptul original)
├── lab02prep/                     # serviciul API + .env (în .gitignore)
├── lab03/
│   ├── currency_exchange_rate.py  # scriptul din lab02, adaptat pentru container
│   ├── requirements.txt           # bibliotecile Python (requests, python-dotenv)
│   ├── cronjob                    # sarcinile cron
│   ├── entrypoint.sh              # configurează și pornește cron în container
│   ├── Dockerfile                 # construiește imaginea cu Python + cron
│   ├── docker-compose.yml         # construiește imaginea și pornește containerul
│   └── readme.md                  # acest fișier
└── data/                          # fișierele JSON (comun cu lab02)
```

### Rolul fiecărui fișier

| Fișier | Rol |
|---|---|
| `currency_exchange_rate.py` | Cere cursul valutar de la API și îl salvează în `data/<FROM>_<TO>_<DATE>.json`. Erorile sunt scrise în `error.log`. |
| `requirements.txt` | Lista bibliotecilor Python instalate în imagine. |
| `cronjob` | Conține cele două sarcini cron (zilnică și săptămânală). |
| `entrypoint.sh` | Salvează variabilele de mediu în `/etc/environment`, creează `/var/log/cron.log`, afișează log-ul și pornește `cron -f`. |
| `Dockerfile` | Pornește de la imaginea oficială `python:3.12-slim`, instalează `cron`, `tzdata` și bibliotecile, copiază fișierele și instalează crontab-ul. |
| `docker-compose.yml` | Construiește imaginea, transmite cheia API și adresa API-ului, montează folderul `data`. |

---

## Sarcinile cron

```text
0 6 * * *   ... MDL EUR $(date -d "yesterday" +%Y-%m-%d)
0 17 * * 5  ... MDL USD $(date -d "7 days ago" +%Y-%m-%d)
```

Formatul unei linii cron: `minut oră zi_lună lună zi_săptămână comandă`.

1. `0 6 * * *` – în fiecare zi la 06:00; data este **ziua precedentă**.
2. `0 17 * * 5` – vinerea (5) la 17:00; data este **cu o săptămână în urmă** (vinerea precedentă).

Observații:

* În fișierul cron caracterul `%` are sens special, de aceea este scris `\%`.
* Cron are un `PATH` minim, așa că Python este apelat cu calea completă `/usr/local/bin/python`.
* `>> /var/log/cron.log 2>&1` adaugă în log atât mesajele normale, cât și erorile.
* Containerul folosește fusul orar `Europe/Chisinau`, deci orele sunt cele locale.

---

## Modificări față de laboratorul 2

* Adresa API-ului se citește din variabila `API_URL` (implicit `http://localhost:8080/`). În container `localhost` este chiar containerul, iar API-ul rulează pe calculatorul gazdă, deci se folosește `http://host.docker.internal:8080/`.
* Cheia `API_KEY` vine din `lab02prep/.env` prin `env_file` în `docker-compose.yml`.
* Scriptul afișează ora fiecărei rulări, ca să se vadă în `cron.log` când a lucrat cron.
* La eroare scriptul se termină cu codul `1`.
* Mesajul de eroare al API-ului este afișat chiar dacă API-ul răspunde cu un cod HTTP de eroare.

---

## Pregătirea ramurii

```bash
git checkout -b lab03
mkdir lab03
cp lab02/currency_exchange_rate.py lab03/
```

---

## Construirea și pornirea containerului

1. Se pornește serviciul API (într-un terminal separat, lăsat deschis):

```bash
cd lab02prep
docker compose up
```

2. Se construiește și se pornește containerul cu cron:

```bash
cd lab03
docker compose up --build -d
```

3. Oprirea containerului:

```bash
docker compose down
```

---

## Verificarea funcționării cron

**Log-ul containerului** (entrypoint-ul afișează conținutul `/var/log/cron.log` cu `tail -f`):

```bash
docker compose logs -f
```

**Sarcinile instalate:**

```bash
docker compose exec currency-cron crontab -l
```

**Conținutul fișierului de log:**

```bash
docker compose exec currency-cron cat /var/log/cron.log
```

**Verificarea că cron rulează și ora din container:**

```bash
docker compose exec currency-cron sh -c "pgrep cron && date"
```

**Test manual al scriptului din container** (verifică legătura cu API-ul):

```bash
docker compose exec currency-cron /usr/local/bin/python /app/lab03/currency_exchange_rate.py MDL EUR 2025-05-01
```

Fișierul `MDL_EUR_2025-05-01.json` trebuie să apară în `Automation/data/`.

**Test rapid al cron-ului:** în `cronjob` se decomentează linia `* * * * *` (rulează în fiecare minut), apoi:

```bash
docker compose up --build -d
docker compose logs -f
```

După un minut în log apar mesajele scriptului. După test linia se comentează la loc.

**Erorile scriptului** sunt scrise și în `error.log` din container:

```bash
docker compose exec currency-cron cat /app/error.log
```

---

## Notă despre perioada datelor

API-ul are date doar pentru perioada **2025-01-01 – 2025-09-15**. Sarcinile cron calculează data față de ziua curentă (2026), deci scriptul va scrie în `cron.log` mesajul că data nu este în perioada disponibilă. Acest mesaj arată că sarcina a fost pornită de cron la ora corectă. Pentru a obține un fișier JSON se folosește testul manual sau linia de test cu o dată fixă.

---

## Concluzie

În cadrul laboratorului a fost configurat un container Docker care:

* conține Python, bibliotecile necesare și cron;
* rulează zilnic la 06:00 cererea MDL → EUR pentru ziua precedentă;
* rulează vinerea la 17:00 cererea MDL → USD pentru săptămâna precedentă;
* scrie rezultatul sarcinilor în `/var/log/cron.log`;
* salvează fișierele JSON în folderul `data` al proiectului.
