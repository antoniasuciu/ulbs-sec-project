# Governed & Hardened SIEM Platform (Security-as-Code)

## 1. Descrierea Proiectului
Acest proiect reprezintă o platformă completă și automatizată de analiză, îmbogățire și detecție de securitate (**un mini-SIEM / XDR modular**), construită și administrată cu ajutorul unui agent AI (**Gemini CLI**), dar guvernată prin **reguli stricte de securitate (Security-as-Code)**.

Platforma demonstrează modul în care o echipă modernă de Security Engineering proiectează, operează și securizează un sistem de monitorizare: fiecare modificare trece printr-un repository guvernat și un pipeline **CI/CD** automatizat, secretele sunt protejate criptografic la nivel *Zero-Trust*, iar evenimentele brute sunt îmbogățite în timp real cu informații externe de **Threat Intelligence**.

---

## 2. Stadiul Implementării și Validarea Funcționalității
Toți pașii arhitecturali, operaționali și de securitate au fost implementați, testați și validați end-to-end, proiectul îndeplinind integral obiectivele stabilite:
- **Pipeline SIEM & Threat Intelligence funcțional:** Logstash ingerează evenimente JSON, interoghează live API-ul extern **Shodan**, atașează automat porturile deschise, serviciile identificate (`CPE`) și vulnerabilitățile cunoscute (`CVE`), și indexează alertările rezultate în **OpenSearch** pentru vizualizare în **Dashboards** (validat prin teste reale E2E).
- **Detection-as-Code validat automat:** Regulile standardizate **Sigma** sunt verificate printr-o suită de teste unitare în Python (`detection/tests/test_detection.py`), confirmând detectarea traficului malițios și ignorarea traficului legitim.
- **Securitate și Guvernanță verificată în CI/CD:** Toate controalele de securitate (scanare anti-secrete cu **Gitleaks**, audit de infrastructură cu **Checkov**, validare **Sigma** și acțiuni GitHub fixate prin commit **SHA**) sunt active și trec cu succes.
- **Guvernanță AI & Managementul Riscurilor documentate:** Riscurile operaționale AI, interne și externe sunt mapate în [`RISK_REGISTER.md`](RISK_REGISTER.md), iar politicile sunt impuse prin [`GEMINI.md`](GEMINI.md), `.gemini/settings.json`, [`memory/MEMORY.md`](memory/MEMORY.md) și [`skills/verify-stack/SKILL.md`](skills/verify-stack/SKILL.md).

---

## 3. Arhitectura și Fluxul de Date
- **Colectare și Îmbogățire (`infra/logstash/logstash.conf`):** Logstash primește evenimente JSON în format ECS pe portul `8080`, extrage IP-ul de destinație și interoghează automat API-ul **Shodan** pentru a îmbogăți evenimentul cu `CVE`-uri, porturi deschise și `CPE`-uri, etichetând alertările cu risc (`shodan_vuln_detected`, `misp_shodan_enriched`).
- **Stocare și Vizualizare (`infra/docker-compose.yml`):** OpenSearch indexează evenimentele îmbogățite în indecși zilnici (`siem-events-YYYY.MM.DD`), accesibili pentru analiză vizuală la `http://localhost:5601`.
- **Detection-as-Code (`detection/`):** Reguli standardizate **Sigma** pentru detectarea comunicațiilor suspecte (ex. C2), validate automat prin teste unitare în Python.
```
