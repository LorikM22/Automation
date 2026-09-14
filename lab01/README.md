# Cleanup Script

## Descriere

`cleanup.sh` este un script Shell care ajută la curățarea unui director prin ștergerea fișierelor cu anumite extensii.

În mod implicit, scriptul șterge fișierele cu extensia `.tmp`.

Scriptul permite și specificarea mai multor extensii care trebuie șterse.

La final, scriptul afișează numărul total de fișiere șterse.

## Cum se utilizează

Scriptul trebuie executat cu cel puțin un argument: calea către directorul care trebuie curățat.

### Ștergerea fișierelor `.tmp`

Dacă nu este specificată nicio extensie, scriptul șterge automat fișierele `.tmp`.

```bash
./cleanup.sh /home/user/automation/lab1
```

### Ștergerea mai multor tipuri de fișiere

Pot fi specificate una sau mai multe extensii:

```bash
./cleanup.sh /home/user/automation/lab1 .tmp .log
```

În acest caz, vor fi șterse fișierele cu extensiile `.tmp` și `.log`.

Un alt exemplu:

```bash
./cleanup.sh /home/user/automation/lab1 .tmp .log .bak
```

## Argumente

| Argument        | Descriere                                                    |
| --------------- | ------------------------------------------------------------ |
| `$1`            | Calea către directorul care trebuie curățat                  |
| `$2`, `$3`, ... | Extensiile fișierelor care trebuie șterse                    |
| implicit        | Dacă nu este specificată nicio extensie, se folosește `.tmp` |

## Verificări și erori

Scriptul verifică:

* dacă a fost specificat directorul;
* dacă directorul există;
* ce extensii trebuie șterse.

Dacă directorul nu există sau nu a fost specificat, scriptul afișează un mesaj de eroare și se oprește.

## Rezultat

La finalul execuției este afișat numărul de fișiere șterse.

Exemplu:
Au fost șterse 3 fișiere.
Au fost șterse 3 fișiere.
```
