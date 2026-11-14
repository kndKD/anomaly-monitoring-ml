# ML Anomaly Detection Monitoring

**Innovation: ML Anomaly Detection**

Replace static thresholds ("CPU > 80%") with learned baselines: an
Isolation Forest model per metric, an Anomaly Score panel in Grafana,
and alerts only when values deviate from learned normal.

## Purpose

Static thresholds cry wolf. This project learns what "normal" looks
like for the Project 1 app, then alerts only on real deviation.

## Architecture

See [docs/architecture.md](docs/architecture.md) — Prometheus scrapes
the app → history → Isolation Forest training → daily inference →
anomaly score via Pushgateway → Grafana panel + adaptive alerts.
Static thresholds stay as a fallback, clearly labelled.

## Tools used

Python 3.12, Prometheus, Grafana, scikit-learn (Isolation Forest),
k6 (load tests), pytest, ruff, GitHub Actions. Self-hosted stack or
Grafana Cloud free tier — no paid monitoring.

## Run locally

```bash
docker compose -f monitoring/docker-compose.yml up -d
# Prometheus on :9090, Grafana on :3000 (admin/admin — LOCAL DEV ONLY)
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python -m pytest -q
```

## Status (Day 1)

Monitoring stack only: Compose (Prometheus + Grafana), scrape config,
datasource + dashboard provisioning, and an App Health dashboard with
an Anomaly Score panel. The app `/metrics` endpoint lands Day 2 (the
flask-app target shows down until then); the anomaly model trains Day 5
on load-test history.

## Measurable impact

- False-positive alert count: static thresholds vs adaptive, measured
  over the same load-test scenarios. The "40–60% reduction" target is
  a target to test, not a result to claim in advance.
- Silent failures detected that thresholds missed (listed with evidence).

## What I learned

- _To be filled in as the project runs._

## Challenges

- _To be filled in as the project runs._
