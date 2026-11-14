"""Day 1 tests: the monitoring stack config is valid and wired up —
Compose services, Prometheus scrape jobs, Grafana provisioning and the
dashboard JSON. No Docker needed in CI; these are config checks only.
"""

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MON = ROOT / "monitoring"


def _load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def test_compose_has_prometheus_and_grafana():
    compose = _load_yaml(MON / "docker-compose.yml")
    services = compose["services"]
    assert "prometheus" in services
    assert "grafana" in services
    assert "9090:9090" in services["prometheus"]["ports"]
    assert "3000:3000" in services["grafana"]["ports"]
    assert services["grafana"]["depends_on"] == ["prometheus"]


def test_prometheus_scrapes_flask_app():
    config = _load_yaml(MON / "prometheus.yml")
    jobs = {job["job_name"]: job for job in config["scrape_configs"]}
    assert "prometheus" in jobs
    flask = jobs["flask-app"]
    assert flask["metrics_path"] == "/metrics"
    targets = flask["static_configs"][0]["targets"]
    assert "host.docker.internal:5000" in targets


def test_grafana_datasource_points_at_prometheus():
    ds = _load_yaml(MON / "grafana" / "provisioning" / "datasources" / "datasource.yml")
    source = ds["datasources"][0]
    assert source["type"] == "prometheus"
    assert source["url"] == "http://prometheus:9090"
    assert source["isDefault"] is True


def test_dashboard_json_valid_and_has_anomaly_panel():
    with open(MON / "grafana" / "dashboards" / "app-health.json") as f:
        dashboard = json.load(f)
    assert dashboard["title"] == "App Health"
    titles = [p["title"] for p in dashboard["panels"]]
    assert "App up" in titles
    assert "Anomaly score" in titles
