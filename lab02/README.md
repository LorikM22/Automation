# Laboratorul 2 – Currency Exchange Rate API

## Scopul laboratorului

Scopul acestui laborator este realizarea unui script Python care interacționează cu un serviciu API pentru obținerea cursului valutar dintre două monede la o anumită dată.

Scriptul primește monedele și data prin linia de comandă, face o solicitare către API și salvează rezultatul într-un fișier JSON.

De asemenea, sunt tratate erorile API și ale parametrilor introduși de utilizator.

---

## Structura laboratorului

```text
lab02/
│
├── currency_exchange_rate.py
└── README.md

În rădăcina proiectului sunt create automat:

Automation/
│
├── data/
│   ├── USD_EUR_2025-01-01.json
│   ├── USD_EUR_2025-03-01.json
│   └── ...
│
└── error.log

Folderul data este creat automat de program dacă nu există.

Fișierul error.log este creat atunci când apare o eroare.

Cerințe

Pentru rularea laboratorului sunt necesare:

Python 3
biblioteca requests
Docker Desktop
serviciul API pornit local pe portul 8080

Instalarea bibliotecii requests:

pip install requests
Pornirea serviciului API

Serviciul API se află în folderul lab02prep.

Din acest folder se rulează:

docker compose up

API-ul va fi disponibil la:

http://localhost:8080/

Terminalul în care rulează Docker trebuie lăsat deschis.

Rularea programului

Din rădăcina proiectului Automation se execută:

python lab02/currency_exchange_rate.py <FROM> <TO> <DATE>

Exemplu:

python lab02/currency_exchange_rate.py USD EUR 2025-01-01

Unde:

USD – moneda din care se face conversia;
EUR – moneda în care se face conversia;
2025-01-01 – data pentru care se solicită cursul valutar.
Monede disponibile

API-ul permite utilizarea următoarelor monede:

MDL
USD
EUR
RON
RUS
UAH

Exemplu:

python lab02/currency_exchange_rate.py EUR MDL 2025-05-01
Perioada disponibilă

Datele disponibile pentru cursurile valutare sunt cuprinse între:

2025-01-01

și

2025-09-15
Salvarea datelor

După executarea cu succes a programului, rezultatul este salvat în folderul:

data/

Numele fișierului conține monedele și data solicitării.

Exemplu:

USD_EUR_2025-01-01.json

Conținutul fișierului are forma:

{
    "error": "",
    "data": {
        "from": "USD",
        "to": "EUR",
        "rate": 0.92,
        "date": "2025-01-01"
    }
}

Valoarea exactă a cursului este furnizată de API.

Tratarea erorilor

Programul verifică mai multe tipuri de erori:

număr incorect de parametri;
format invalid al datei;
dată în afara perioadei disponibile;
monedă necunoscută;
eroare de conectare la API;
răspuns invalid de la API;
eroare la salvarea fișierului.

Erorile sunt afișate în consolă și sunt salvate în:

error.log

Exemplu de comandă cu o monedă invalidă:

python lab02/currency_exchange_rate.py ABC EUR 2025-05-01

În consolă va apărea un mesaj de eroare, iar acesta va fi înregistrat și în error.log.

Exemplu:

2026-09-28 13:45:32 - ERROR - The currency ABC is unknown
Testarea programului

Conform cerinței, programul trebuie testat pentru cel puțin 5 date din perioada disponibilă.

Exemple de teste:

python lab02/currency_exchange_rate.py USD EUR 2025-01-01
python lab02/currency_exchange_rate.py USD EUR 2025-03-01
python lab02/currency_exchange_rate.py USD EUR 2025-05-01
python lab02/currency_exchange_rate.py USD EUR 2025-07-01
python lab02/currency_exchange_rate.py USD EUR 2025-09-01

Pentru fiecare solicitare reușită se creează un fișier JSON separat în folderul data.

Exemplu de rezultat

După executarea comenzilor, folderul data poate conține:

data/
├── USD_EUR_2025-01-01.json
├── USD_EUR_2025-03-01.json
├── USD_EUR_2025-05-01.json
├── USD_EUR_2025-07-01.json
└── USD_EUR_2025-09-01.json
Concluzie

În cadrul laboratorului a fost realizat un script Python care:

primește două monede și o dată prin linia de comandă;
trimite o solicitare către API;
primește cursul valutar;
salvează rezultatul în format JSON;
creează automat folderul data;
tratează erorile și le salvează în error.log;
este testat pentru mai multe date din perioada disponibilă.