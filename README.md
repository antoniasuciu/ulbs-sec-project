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
```

---

## 4. Controale de Securitate și Guvernanță
1. **Container Hardening:** Rețea Docker izolată (`siem-net`), `cap_drop: [ALL]`, `no-new-privileges: true` și limite RAM.
2. **Zero-Trust Secret Management:** Chei API criptate cu **SOPS + `age`** în `infra/secrets.enc.env`.
3. **CI/CD Security Gates:** Pre-commit hooks (`no-commit-to-branch`, `gitleaks`) și GitHub Actions (SHA-pinned) cu **Gitleaks**, **Checkov** și **Sigma Validation**.
4. **Guvernanță AI & Arhitectură:** Guardrails în `GEMINI.md` și `.gemini/settings.json`, decizii în `memory/architecture-decisions.md` (`memory/MEMORY.md`), riscuri în `RISK_REGISTER.md` și runbook în `skills/verify-stack/SKILL.md`.

---

## 5. Ghid de Rulare și Validare (Runbook)

> **Notă pentru evaluator / profesor:** Pentru a rula local fără cheia privată `age` a autorului, creați temporar `infra/.env` cu propria cheie API Shodan (`echo "SHODAN_API_KEY=<CHEIA_TA>" > infra/.env`) în locul decriptării SOPS de la pasul 2.

```bash
# 1. Validează regulile de detecție Sigma (Detection-as-Code)
python3 detection/tests/test_detection.py

# 2. Decriptează secretele și pornește stack-ul SIEM
SOPS_AGE_KEY_FILE=~/.age-sec-project.key sops --decrypt infra/secrets.enc.env > infra/.env
docker compose --file infra/docker-compose.yml --env-file infra/.env up -d

# 3. Așteaptă 25s pentru inițializarea OpenSearch, apoi trimite un eveniment simulat
sleep 25
curl -X POST [http://127.0.0.1:8080](http://127.0.0.1:8080) -H "Content-Type: application/json" -d '{"source":{"ip":"10.0.1.15"},"destination":{"ip":"45.33.32.156","port":4444}}'

# 4. Verifică documentul îmbogățit cu date Shodan în OpenSearch
sleep 5 && curl -s "[http://127.0.0.1:9200/siem-events-*/_search?pretty](http://127.0.0.1:9200/siem-events-*/_search?pretty)"

# 5. Oprește containerele și șterge secretele temporare
docker compose -f infra/docker-compose.yml down && rm -f infra/.env
```

### Rezultat Așteptat (Exemplu Validare E2E)
La rularea pasului 4 (`_search`), OpenSearch returnează evenimentul îmbogățit automat cu datele Shodan (porturi, servicii CPE, CVE-uri și tag-uri de risc):

```json
{
  "_index": "siem-events-2026.11.22",
  "_source": {
    "source": { "ip": "10.0.1.15" },
    "destination": { "ip": "45.33.32.156", "port": 4444 },
    "tags": ["shodan_vuln_detected", "misp_shodan_enriched"],
    "threat": {
      "enrich": {
        "shodan": {
          "ip": "45.33.32.156",
          "hostnames": ["scanme.nmap.org"],
          "ports": [22, 80, 123, 9929],
          "cpes": ["cpe:/a:openbsd:openssh:6.6.1p1", "cpe:/a:apache:http_server:2.4.7"],
          "vulns": ["CVE-2023-25690", "CVE-2024-38476", "..."]
        }
      }
    }
  }
}
```
