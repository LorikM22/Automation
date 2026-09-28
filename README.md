# Automation

Acest repository conține scripturi Shell realizate pentru automatizarea unor sarcini în sistemul Linux.

## Laboratoare
---------------------------------------------------------

### Lab 01 — Cleanup Script

Scriptul `cleanup.sh` este folosit pentru curățarea unui director prin ștergerea fișierelor cu anumite extensii.

În mod implicit, scriptul șterge fișierele cu extensia `.tmp`.

Pentru mai multe informații despre utilizarea scriptului și exemple de comenzi, consultați README-ul din folderul `lab1`.

## Structura proiectului

```text
automation/
├── README.md
└── lab1/
    ├── README.md
    └── cleanup.sh
```

---------------------------------------------------------------
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