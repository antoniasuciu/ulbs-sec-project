# Reguli de Guvernanță și Context Arhitectural - Security Enrichment Platform

## Contextul Proiectului
- **Arhitectură:** Stack SIEM bazat pe OpenSearch 2.x, Logstash (ingestie și îmbogățire) și Filebeat, orchestrat prin Docker Compose (`infra/`).
- **Fluxul de Date:** Loguri sursă -> Filebeat -> Logstash (imbogățire prin MISP + Shodan) -> OpenSearch (`siem-events-*`).
- **Detecție:** Reguli Sigma în `detection/rules/` convertite în interogări OpenSearch DSL și validate automat în CI pe evenimente sintetice (`detection/samples/`).

## Reguli Obligatorii pentru Asistentul AI (Guardrails)
1. **Zero Secrete în Clar:** Nu citi, nu afișa și nu scrie niciodată chei API (`SHODAN_API_KEY`, `MISP_KEY`), parole sau fișierul `~/.age-sec-project.key`. Secretele se gestionează exclusiv criptat în `infra/secrets.enc.env`.
2. **Protecția Ramurii Principale:** Nu executa niciodată `git push --force`, `git reset --hard` sau commit-uri directe pe `main`. Toate modificările se fac pe branch-uri `feat/*` sau `fix/*`.
3. **Integritatea Memoriei și a Regulilor:** Nu modifica `GEMINI.md`, `.gemini/settings.json` sau fișierele din `memory/` fără aprobarea explicită a utilizatorului (prevenire Memory Poisoning - MITRE ATLAS).
4. **Minim Privilegiu în Infrastructură și CI:** Orice serviciu Docker nou trebuie să ruleze fără `privileged: true`, iar acțiunile GitHub Actions trebuie fixate la commit SHA.
