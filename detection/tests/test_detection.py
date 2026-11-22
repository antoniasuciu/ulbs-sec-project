import json
import yaml
from pathlib import Path

def test_sigma_rule_and_samples():
    rule_path = Path("detection/rules/c2_shodan_suspicious_outbound.yml")
    samples_path = Path("detection/samples/events.json")

    rule = yaml.safe_load(rule_path.read_text(encoding="utf-8"))
    assert "detection" in rule, "Regula Sigma nu contine sectiunea detection"
    suspicious_ports = set(rule["detection"]["selection_ports"]["destination.port"])

    events = json.loads(samples_path.read_text(encoding="utf-8"))
    alerts = []
    for ev in events:
        port_match = ev.get("destination", {}).get("port") in suspicious_ports
        tag_match = "shodan_vuln_detected" in ev.get("tags", [])
        if port_match or tag_match:
            alerts.append(ev["event_id"])

    assert alerts == ["evt-001-malicious"], f"Rezultat neasteptat la detectie: {alerts}"
    print("OK: Regula Sigma a detectat corect evenimentul malitios si a ignorat traficul benign.")

if __name__ == "__main__":
    test_sigma_rule_and_samples()
