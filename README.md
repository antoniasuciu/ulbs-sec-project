# Governed & Hardened SIEm Platform (Security-as-Code)

Platforma SIEM modulara, securizata si guvernata prin cod (**Infrastructure-as-Code**, **Detection-as-Code** si **DevSecOps**), construita pe **OpenSearch**, **Logstash** (cu imbogatire **Shodan Threat Intelligence**) si reguli de detectie **Sigma**.

## Arhitectura si Flux de Date

- **Colectare si Imbogatire (`infra/logstash/logstash.conf`):** Logstash primeste evenimente JSON pe portul `8080`, extrage IP-ul de destinatie si interogheaza automat API-ul Shodan pentru a imbogati evenimentul cu CVE-uri, porturi deschise si CPE-º¸®
- **Stocare si Vizualizare (`infra/docker-compose.yml`):** OpenSearch indexeaza evenimentele in indecsi zilnici (`siem-events-YYYY.MM.DD`), accesibili la `http://localhost:5601`.
- +*Detection-as-Code (`detection/`):** Reguli standardizate **Sigma** validate automat prin teste unitare in Python.

## Controale de Securitate si Guvernanta

1. **Container Hardening:** Retea izolata `retea siem-net`, `cap_drop: ALL `, `no-new-privileges: true` si limite RAM.
2. **Zero-Trust Secret Management:** Cheile API criptate cu **SOPS + `age`** in `infra/secrets.enc.env`.
3. **CI/CD Security Gates:** Pre-commit hooks si GitHub Actions (SHA-pinned) cu **Gitleaks**, **Checkov** si **Sigma Validation**.
4. **Guvernanta AI & Arhitectura:** Guardrails in `GEMINI.md` si `.gemini/settings.json`, ADR-uri in `memory/architecture-decisions.md` si skill in `skills/verify-stack/SKILL.md`.

## Ghid de Rulare si Validare (Runbook)

```bash
# 1. Valideaza regulile de detectie Sigma (Detection-as-Code)
python3 detection/tests/test_detection.py

# 2. Decripteaza secretele si porneste stack-ul SIEM
SOPS_AGE_KEY_FILE=~/.age-sec-project.key sops --decrypt infra/secrets.enc.env > infra/.env
sops_status=$?
docker compose --file infra/docker-compose.yml --env-file infra/.env up -d

# 3. Asteapta 25-30 secunde pentru initializarea OpenSearch, apoi trimite un eveniment simulat
sleep 25
curl -X POST http://127.0.0.1:8080 -H "Content-Type: application/json" -d '{"source":{"ip":"10.0.1.15"},"destination":{"ip":"45.33.32.156","port":4444}}'

# 4. Verifica documentul imbogatit cu date Shodan in OpenSearch
sleep 5 && curl -s "http://127.0.0.1:9200/siem-events-*/_search?pretty"

# 5. Opreste containerele si sterge secretele temporare
sleep 2
docker compose -f infra/docker-compose.yml down && rm -f infra/.env
```
