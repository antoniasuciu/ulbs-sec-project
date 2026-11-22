# Decizii Arhitecturale (ADR)
- **ADR-001 (Secret Management):** SOPS + `age` ales pentru criptarea `infra/secrets.enc.env` direct în Git, evitând dependența de un Vault extern la nivel de laborator.
- **ADR-002 (SIEM Engine):** OpenSearch 2.x + Logstash ales pentru compatibilitate nativă cu regulile Sigma convertite în OpenSearch DSL.
- **ADR-003 (AI Governance):** Izolarea contextului în `GEMINI.md` și blocarea comenzilor distructive în `.gemini/settings.json`, protejate prin `CODEOWNERS`.
