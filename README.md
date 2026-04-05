# Advanced Monitoring Stack with Prometheus, Grafana, Loki, Alertmanager, Blackbox Exporter, Node Exporter, and cAdvisor

This repository now ships a more production-style observability stack for Docker workloads. It still simulates 10 Linux hosts with Node Exporter, but it also adds alerting, synthetic monitoring, log aggregation, and Grafana auto-provisioning so the stack is useful beyond basic metric collection.

## What's Included

- `10` Linux containers exporting host metrics through Node Exporter
- `Prometheus` for metric collection, alert rule evaluation, and target health
- `Alertmanager` for routing and grouping alerts
- `Grafana` with pre-provisioned data sources and dashboards
- `cAdvisor` for Docker and container runtime metrics
- `Blackbox Exporter` for HTTP health checks against internal services
- `Loki + Promtail` for centralized logs from the Docker host and containers
- Persistent volumes for Prometheus, Grafana, and Loki

## Architecture

```text
Node Exporters (10 hosts) ----\
                               \
cAdvisor -----------------------> Prometheus ----> Alertmanager
                                /        \
Blackbox Exporter probes ------/          \----> Grafana

Docker/container logs ----> Promtail ----> Loki ----> Grafana
```

## Services

| Service           | URL                                                        | Notes                  |
| ----------------- | ---------------------------------------------------------- | ---------------------- |
| Grafana           | [http://localhost:3000](http://localhost:3000)             | `admin / admin`        |
| Prometheus        | [http://localhost:9090](http://localhost:9090)             | Targets, rules, alerts |
| Alertmanager      | [http://localhost:9093](http://localhost:9093)             | Alert routing UI       |
| cAdvisor          | [http://localhost:8080](http://localhost:8080)             | Container metrics      |
| Blackbox Exporter | [http://localhost:9115](http://localhost:9115)             | Probe metrics          |
| Loki              | [http://localhost:3100/ready](http://localhost:3100/ready) | Log backend readiness  |

## Quick Start

```bash
docker compose up -d --build
```

Grafana is pre-provisioned with:

- a `Prometheus` data source
- a `Loki` data source
- the `Advanced Monitoring Stack` dashboard

## What Changed from the Basic Stack

- Added Prometheus alert rules in [`/Users/sameeralam/Documents/GitHub/Monitoring/prometheus/rules/alerts.yml`](/Users/sameeralam/Documents/GitHub/Monitoring/prometheus/rules/alerts.yml)
- Added Alertmanager config in [`/Users/sameeralam/Documents/GitHub/Monitoring/alertmanager/alertmanager.yml`](/Users/sameeralam/Documents/GitHub/Monitoring/alertmanager/alertmanager.yml)
- Added Blackbox Exporter config in [`/Users/sameeralam/Documents/GitHub/Monitoring/blackbox/blackbox.yml`](/Users/sameeralam/Documents/GitHub/Monitoring/blackbox/blackbox.yml)
- Added Loki and Promtail configs in [`/Users/sameeralam/Documents/GitHub/Monitoring/loki/loki-config.yml`](/Users/sameeralam/Documents/GitHub/Monitoring/loki/loki-config.yml) and [`/Users/sameeralam/Documents/GitHub/Monitoring/promtail/promtail-config.yml`](/Users/sameeralam/Documents/GitHub/Monitoring/promtail/promtail-config.yml)
- Added Grafana provisioning in [`/Users/sameeralam/Documents/GitHub/Monitoring/grafana/provisioning/datasources/datasources.yml`](/Users/sameeralam/Documents/GitHub/Monitoring/grafana/provisioning/datasources/datasources.yml) and [`/Users/sameeralam/Documents/GitHub/Monitoring/grafana/provisioning/dashboards/dashboards.yml`](/Users/sameeralam/Documents/GitHub/Monitoring/grafana/provisioning/dashboards/dashboards.yml)

## Prometheus Jobs

- `prometheus`
- `alertmanager`
- `node_exporter`
- `cadvisor`
- `blackbox-exporter`
- `blackbox-http`

## Included Alerts

- `TargetDown`
- `HostHighCPU`
- `HostHighMemory`
- `ContainerHighCPU`
- `ContainerHighMemory`
- `SyntheticProbeFailed`

## Grafana Dashboard

The provisioned dashboard includes:

- fleet-wide CPU and memory overview
- per-node CPU and memory trends
- container CPU and memory charts
- synthetic probe success and latency
- firing alerts table
- live logs from Loki

![alt text](<Screenshot 2026-04-05 at 11.57.50 PM.png>)

## Suggested Next Additions

If you want to make this stack even more advanced, these are the highest-value next steps:

1. Connect Alertmanager to Slack, Microsoft Teams, Discord, email, or PagerDuty so alerts leave the lab and reach people.
2. Add recording rules for SLO-style metrics such as request availability, error budgets, and per-service latency percentiles.
3. Instrument an application with OpenTelemetry and send traces to Tempo so Grafana can correlate metrics, logs, and traces.
4. Add exporters for your real infrastructure, such as `postgres_exporter`, `redis_exporter`, `nginx-prometheus-exporter`, `mysqld_exporter`, and cloud provider exporters.
5. Add service discovery for Kubernetes, Docker Swarm, EC2, or Consul instead of static target lists.
6. Add Grafana alerting and on-call dashboards for business KPIs, deployment markers, and release health.
7. Add long-term metric storage with Thanos, Mimir, or VictoriaMetrics if retention and multi-node scale matter.
8. Add log parsing pipelines in Promtail for JSON logs, nginx access logs, and application severity labels.
9. Add SSL/TLS, secrets management, and non-default credentials before using the stack outside local development.
10. Add exporters for uptime of external APIs, DNS, ICMP, and TCP checks through more Blackbox modules.

## Operational Notes

- Prometheus evaluates rules every `15s`
- Blackbox Exporter probes Grafana, Prometheus, cAdvisor, Alertmanager, and Loki
- Grafana auto-loads the dashboard at startup
- Promtail tails host logs and Docker container JSON logs

## Troubleshooting

- If Grafana starts without the dashboard, check Grafana logs and verify the mounted provisioning paths.
- If Promtail cannot read Docker logs on your platform, confirm Docker exposes container logs under `/var/lib/docker/containers`.
- If alerts appear in Prometheus but not in notifications, add a real receiver integration to Alertmanager.
- If Node Exporter containers fail to build, the Dockerfile may need internet access during image build to download the exporter binary.

## License

MIT License
