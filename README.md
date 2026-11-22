# Governed & Hardened SIEM Platform (Security-as-Code)

Platforma SIEM modulara, securizata si guvernata prin cod (**Infrastructure-as-Code**, **Detection-as-Code** si **DevSecOps**), construita pe **OpenSearch**, **Logstash** (cu imbogatire automata **Shodan Threat Intelligence**) si reguli de detectie **Sigma**.

## 1. Ce am realizat in acest proiect
- **Pipeline Threat Intelligence (`infra/logstash/logstash.conf`):** Logstash primeste evenimente JSON pe portul `8080`, interogheaza live API-ul **Shodan** pentru IP-ul destinatie si adauga porturi deschise, servicii (`CPE`) si vulnerabilitati (`CVE`), etichetand alertele (`shodan_vuln_detected`, `misp_shodan_enriched`).
- **Infrastructura Hardened (`infra/docker-compose.yml`):** Stack OpenSearch + Logstash + Dashboards in retea izolata (`siem-net`), cu `cap_drop: [ALL]`, `no-new-privileges: true` si limite RAM.
- **Secrete Zero-Trust (`infra/secrets.enc.env`):** Cheile API sunt criptate cu **SOPS** si **age** (fara secrete in clar in repository).
- **Detection-as-Code (`detection/`):** Regula **Sigma** validata automat prin teste unitare in Python (`detection/tests/test_detection.py`).
- **DevSecOps & Guvernanta AI (`.github/workflows/`, `GEMINI.md`, `memory/`):** Pre-commit hooks si GitHub Actions (SHA-pinned) cu **Gitleaks**, **Checkov** si **Sigma Validation**, plus ADR-uri si guardrails AI.
