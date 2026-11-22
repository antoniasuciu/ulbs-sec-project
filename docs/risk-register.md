# Registru de Riscuri - Security Enrichment Platform

| ID | Categorie | Activ (Asset) | Amenințare / Tehnică | Probabilitate / Impact | Control Implementat |
|---|---|---|---|---|---|
| R-01 | Risc Operațional (AI) | Cod sursă & Credențiale | Gemini CLI introduce chei API în clar sau execută `git push --force` | Medie / Critic | Hook `pre-commit` cu Gitleaks + restricții în `.gemini/settings.json` |
| R-02 | Risc Operațional (AI) | `GEMINI.md` & `memory/` | Memory Poisoning (MITRE ATLAS) via PR extern sau fișier alterat | Scăzută / Ridicat | `CODEOWNERS` pe directoarele AI + revizuire obligatorie prin PR |
| R-03 | Risc Intern (Infra/CI) | Secrete & Pipeline | Scurgere parole OpenSearch în Git; compromitere GitHub Actions via tag-uri mobile | Medie / Critic | Criptare SOPS + `age`; fixare acțiuni CI la commit SHA + privilegiu minim |
| R-04 | Risc Extern (Threat) | Rețea / Host-uri | Comunicații C2 nedetectate către IP-uri malițioase cunoscute | Ridicată / Ridicat | Reguli Sigma testate în CI + îmbogățire Logstash cu MISP și Shodan |
