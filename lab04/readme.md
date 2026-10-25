# IW04: Configurarea Jenkins pentru automatizarea sarcinilor DevOps

## Scopul lucrării

Învățarea configurării Jenkins pentru automatizarea sarcinilor DevOps, inclusiv crearea și gestionarea pipeline-urilor CI/CD.

## Descrierea proiectului

În această lucrare am ridicat, cu ajutorul Docker Compose, o infrastructură Jenkins formată din două containere:

- **jenkins-controller** – serverul Jenkins (imaginea `jenkins/jenkins:lts`), care oferă interfața web, stochează configurația și planifică job-urile;
- **ssh-agent** – un agent Jenkins construit din imaginea `jenkins/ssh-agent`, în care am instalat PHP CLI și Composer. Controllerul se conectează la el prin SSH și îi trimite job-urile spre execuție.

Pentru testarea pipeline-ului am folosit un proiect PHP mic (folderul `php-app/`) cu două clase (`Calculator` și `StringHelper`) și teste unitare scrise cu PHPUnit. Pipeline-ul descris în `Jenkinsfile` instalează dependențele cu Composer și rulează testele pe agentul cu eticheta `php-agent`.

### Structura folderului

```
lab04/
├── docker-compose.yml     # serviciile jenkins-controller și ssh-agent
├── Dockerfile             # imaginea agentului SSH (PHP CLI + Composer)
├── Jenkinsfile            # pipeline-ul CI
├── .env.example           # model pentru fișierul .env
├── .gitignore             # exclude secrets/, .env, vendor/
├── .dockerignore
├── php-app/               # proiectul PHP testat
│   ├── composer.json
│   ├── phpunit.xml
│   ├── src/
│   │   ├── Calculator.php
│   │   └── StringHelper.php
│   └── tests/
│       ├── CalculatorTest.php
│       └── StringHelperTest.php
└── readme.md
```

> Folderul `secrets/` și fișierul `.env` nu sunt încărcate în repository (sunt în `.gitignore`), deoarece conțin cheia privată SSH.

---

## 1. Configurarea Jenkins Controller

1. Am creat fișierul `docker-compose.yml` cu serviciul `jenkins-controller`:

   ```yaml
   services:
     jenkins-controller:
       image: jenkins/jenkins:lts
       container_name: jenkins-controller
       ports:
         - "8080:8080"
         - "50000:50000"
       volumes:
         - jenkins_home:/var/jenkins_home
       networks:
         - jenkins-network

   volumes:
     jenkins_home:
     jenkins_agent_volume:

   networks:
     jenkins-network:
       driver: bridge
   ```

   - portul `8080` – interfața web Jenkins;
   - portul `50000` – folosit de agenții inbound (JNLP);
   - volumul `jenkins_home` păstrează configurația, plugin-urile și job-urile între reporniri.

2. Am pornit containerul:

   ```bash
   docker compose up -d jenkins-controller
   ```

3. Am obținut parola inițială de administrator:

   ```bash
   docker exec jenkins-controller cat /var/jenkins_home/secrets/initialAdminPassword
   ```

4. Am deschis `http://localhost:8080`, am introdus parola, am ales **Install suggested plugins**, am creat contul de administrator și am păstrat URL-ul implicit `http://localhost:8080/`.

<!-- ![Jenkins unlock](images/jenkins-unlock.png) -->

---

## 2. Configurarea agentului SSH

1. Am generat perechea de chei SSH în folderul `secrets`:

   ```bash
   mkdir secrets
   cd secrets
   ssh-keygen -f jenkins_agent_ssh_key
   cd ..
   ```

   Rezultat: `secrets/jenkins_agent_ssh_key` (cheia privată) și `secrets/jenkins_agent_ssh_key.pub` (cheia publică).

2. Am creat `Dockerfile` pentru agent. Pe lângă `php-cli` cerut în sarcină, am adăugat extensiile necesare PHPUnit (`php-xml`, `php-mbstring`), utilitarele `unzip`/`git` și Composer:

   ```dockerfile
   FROM jenkins/ssh-agent

   # install PHP-CLI + extensiile cerute de PHPUnit + Composer
   RUN apt-get update && apt-get install -y --no-install-recommends \
           php-cli php-xml php-mbstring php-curl \
           unzip git curl ca-certificates \
       && rm -rf /var/lib/apt/lists/*

   RUN curl -sS https://getcomposer.org/installer \
       | php -- --install-dir=/usr/local/bin --filename=composer
   ```

3. Am adăugat serviciul `ssh-agent` în `docker-compose.yml`:

   ```yaml
     ssh-agent:
       build:
         context: .
         dockerfile: Dockerfile
       container_name: ssh-agent
       environment:
         - JENKINS_AGENT_SSH_PUBKEY=${JENKINS_AGENT_SSH_PUBKEY}
       volumes:
         - jenkins_agent_volume:/home/jenkins/agent
       depends_on:
         - jenkins-controller
       networks:
         - jenkins-network
   ```

4. Am creat fișierul `.env` cu cheia publică:

   ```bash
   echo "JENKINS_AGENT_SSH_PUBKEY=$(cat secrets/jenkins_agent_ssh_key.pub)" > .env
   ```

   Docker Compose citește automat `.env` și înlocuiește `${JENKINS_AGENT_SSH_PUBKEY}`. La pornire, imaginea `jenkins/ssh-agent` scrie această cheie în `~/.ssh/authorized_keys` al utilizatorului `jenkins`.

5. Am repornit proiectul pentru a aplica modificările:

   ```bash
   docker compose down
   docker compose up -d --build
   docker compose ps
   ```

6. Am verificat că PHP și Composer sunt disponibile în agent:

   ```bash
   docker exec ssh-agent php -v
   docker exec ssh-agent composer --version
   ```

### Conectarea agentului SSH la Jenkins

1. **Plugin.** În *Manage Jenkins → Plugins → Installed plugins* am verificat că **SSH Build Agents** (SSH Agents Plugin) este instalat (dacă nu – se instalează din *Available plugins*).

2. **Credențiale.** *Manage Jenkins → Credentials → System → Global credentials → Add Credentials*:
   - Kind: **SSH Username with private key**
   - ID: `jenkins-agent-ssh-key`
   - Username: `jenkins`
   - Private Key: *Enter directly* – am lipit conținutul fișierului `secrets/jenkins_agent_ssh_key`.

3. **Nod nou.** *Manage Jenkins → Nodes → New Node*:
   - Node name: `ssh-agent1`, tip **Permanent Agent**
   - Remote root directory: `/home/jenkins/agent`
   - Labels: `php-agent`
   - Usage: *Only build jobs with label expressions matching this node*
   - Launch method: **Launch agents via SSH**
     - Host: `ssh-agent` (numele serviciului din rețeaua `jenkins-network`)
     - Credentials: `jenkins (jenkins-agent-ssh-key)`
     - Host Key Verification Strategy: **Non verifying Verification Strategy** (în mediul local de laborator)
     - Advanced → JavaPath: `/opt/java/openjdk/bin/java`

4. După salvare, în jurnalul nodului (*Log*) a apărut mesajul `Agent successfully connected and online`, iar nodul `ssh-agent1` a apărut ca online.

<!-- ![Nod ssh-agent1 online](images/node-online.png) -->

---

## 3. Crearea și configurarea pipeline-ului Jenkins

1. Am adăugat proiectul PHP în `lab04/php-app` și `Jenkinsfile` în `lab04/`, apoi le-am încărcat în GitHub.

2. Conținutul `Jenkinsfile`:

   ```groovy
   pipeline {
       agent {
           label 'php-agent'
       }

       stages {
           stage('Install Dependencies') {
               steps {
                   echo 'Preparing project...'
                   dir('lab04/php-app') {
                       sh 'php -v'
                       sh 'composer --version'
                       sh 'composer install --no-interaction --prefer-dist'
                   }
               }
           }

           stage('Test') {
               steps {
                   echo 'Running tests...'
                   dir('lab04/php-app') {
                       sh 'mkdir -p build'
                       sh 'vendor/bin/phpunit --log-junit build/junit.xml'
                   }
               }
           }
       }

       post {
           always {
               junit allowEmptyResults: true, testResults: 'lab04/php-app/build/junit.xml'
               echo 'Pipeline completed.'
           }
           success {
               echo 'All stages completed successfully!'
           }
           failure {
               echo 'Errors detected in the pipeline.'
           }
       }
   }
   ```

   - `agent { label 'php-agent' }` – pipeline-ul rulează doar pe nodul cu eticheta `php-agent`, adică pe containerul `ssh-agent`;
   - **Install Dependencies** – instalează PHPUnit și generează autoloader-ul prin Composer;
   - **Test** – rulează testele și salvează rezultatul în format JUnit;
   - `post { always { junit ... } }` – publică rezultatele testelor în Jenkins (graficul și lista testelor apar pe pagina build-ului).

3. În Jenkins: *New Item* → nume `lab04-php-pipeline` → tip **Pipeline** → OK.

4. În secțiunea *Pipeline*:
   - Definition: **Pipeline script from SCM**
   - SCM: **Git**
   - Repository URL: `https://github.com/<username>/automation.git`
   - Branch Specifier: `*/lab04` (sau ramura în care se află lucrarea)
   - Script Path: `lab04/Jenkinsfile`

5. Am apăsat **Build Now**. În *Console Output* se vede că job-ul rulează pe `ssh-agent1`, Composer instalează dependențele, iar PHPUnit execută testele:

   ```
   Running on ssh-agent1 in /home/jenkins/agent/workspace/lab04-php-pipeline
   ...
   OK (10 tests, 13 assertions)
   ...
   Pipeline completed.
   All stages completed successfully!
   Finished: SUCCESS
   ```

<!-- ![Pipeline reușit](images/pipeline-success.png) -->

### Testele unitare

| Clasa | Ce se testează |
|---|---|
| `CalculatorTest` | adunare, scădere, înmulțire, împărțire, excepție la împărțirea la zero, media aritmetică, excepție pentru listă goală |
| `StringHelperTest` | generarea unui slug, verificarea palindromului, numărarea cuvintelor |

Testele pot fi rulate și local:

```bash
cd php-app
composer install
vendor/bin/phpunit
```

---

## 4. Răspunsuri la întrebări

### Care sunt avantajele utilizării Jenkins pentru automatizarea sarcinilor DevOps?

- **Open-source și gratuit**, cu o comunitate mare și documentație bogată.
- **Ecosistem de peste 1800 de plugin-uri** – integrare cu Git/GitHub, Docker, Kubernetes, Slack, SonarQube, servicii cloud etc.
- **Pipeline as Code** – pipeline-ul este descris în `Jenkinsfile`, versionat împreună cu codul, poate fi revizuit și reprodus.
- **Arhitectură distribuită controller/agent** – build-urile rulează pe agenți separați, cu medii diferite (PHP, Java, Node.js), în paralel, fără a încărca serverul principal.
- **Declanșare automată** – la fiecare push (webhook), după program (cron) sau după alte job-uri.
- **Raportare** – istoricul build-urilor, rezultatele testelor (JUnit), artefacte, notificări în caz de eșec.
- **Independent de platformă** – rulează pe Linux, Windows, macOS, în Docker sau Kubernetes; poate fi găzduit local (self-hosted), deci datele rămân în infrastructura proprie.

### Ce alte tipuri de agenți Jenkins există?

- **Agenți SSH** – controllerul se conectează la agent prin SSH (cel folosit în această lucrare).
- **Agenți inbound (JNLP / WebSocket)** – agentul inițiază conexiunea către controller (portul 50000); util când agentul se află în spatele unui NAT/firewall. Imaginea oficială: `jenkins/inbound-agent`.
- **Agenți Docker** – pentru fiecare build se pornește un container temporar (plugin-ul Docker / `agent { docker { image 'php:8.3-cli' } }`), care este șters după execuție.
- **Agenți Kubernetes** – plugin-ul Kubernetes creează pod-uri ca agenți la cerere și îi șterge după build.
- **Agenți cloud** – mașini virtuale create dinamic în AWS EC2, Azure VM, Google Compute Engine prin plugin-urile corespunzătoare.
- **Agenți Windows** – lansați ca serviciu Windows sau prin SSH/inbound pentru build-uri .NET etc.
- **Nodul built-in (controller)** – execuția direct pe controller; nerecomandat în producție din motive de securitate și performanță.

După modul de existență, agenții pot fi **permanenți** (Permanent Agent, ca `ssh-agent1`) sau **efemeri/dinamici** (cloud, Docker, Kubernetes).

### Ce probleme au apărut la configurarea Jenkins și cum au fost rezolvate?

1. **Agentul nu pornea din cauza variabilei `JENKINS_AGENT_SSH_PUBKEY` goale.**
   Fișierul `.env` lipsea / era în alt folder decât `docker-compose.yml`. Am creat `.env` în același folder, cu comanda `echo "JENKINS_AGENT_SSH_PUBKEY=$(cat secrets/jenkins_agent_ssh_key.pub)" > .env`, și am verificat cu `docker compose config` că valoarea este preluată.

2. **Eroare de verificare a cheii host-ului** (`No Known Hosts file was found` / `Host key verification failed`).
   Am setat *Host Key Verification Strategy* la *Non verifying Verification Strategy* (acceptabil pentru un mediu local de laborator). O variantă mai sigură este *Manually trusted key*.

3. **`java: command not found` la lansarea agentului.**
   La conexiunea SSH non-interactivă `PATH` nu conține Java. Am indicat în setările avansate ale nodului *JavaPath* = `/opt/java/openjdk/bin/java`.

4. **`composer: not found` și erori de extensii lipsă la rularea PHPUnit** (`ext-dom`, `ext-mbstring`).
   Dockerfile-ul din sarcină instala doar `php-cli`. Am adăugat `php-xml`, `php-mbstring`, `unzip`, `git` și Composer, apoi am reconstruit imaginea cu `docker compose up -d --build`.

5. **Riscul de a publica cheia privată în GitHub.**
   Am adăugat `secrets/` și `.env` în `.gitignore` (și în `.dockerignore`), iar în repository am lăsat doar `.env.example` ca model.

---

## Concluzii

Am configurat Jenkins Controller și un agent SSH în containere Docker, conectate printr-o rețea comună. Agentul cu eticheta `php-agent` are mediul PHP necesar, iar pipeline-ul definit în `Jenkinsfile` preia codul din GitHub, instalează dependențele și rulează testele unitare automat, publicând rezultatele în Jenkins. Astfel, fiecare modificare a codului poate fi verificată automat, fără intervenție manuală.
