---
name: verify-stack
description: Verifică starea containerelor SIEM, sănătatea clusterului OpenSearch și prezența secretelor criptate fără a expune chei în clar.
---
# Procedură de Verificare Stack SIEM
1. Verifică existența `infra/secrets.enc.env` și asigură-te că nu există niciun fișier `.env` necriptat în `infra/`.
2. Rulează `docker compose -f infra/docker-compose.yml ps` pentru a confirma că toate serviciile sunt `Up` / `healthy`.
3. Interoghează endpoint-ul OpenSearch (`/_cluster/health`) fără a afișa credențialele în loguri.
