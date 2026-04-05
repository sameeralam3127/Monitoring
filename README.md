# Advanced Monitoring Stack

This repository contains a Docker-based monitoring and observability stack for Linux containers. It includes host metrics, container metrics, alerting, synthetic health checks, centralized logging, and a pre-provisioned Grafana dashboard.

## Stack Components

- `Prometheus` for scraping metrics and evaluating alert rules
- `Grafana` for dashboards and visualization
- `Alertmanager` for alert routing
- `Node Exporter` running in 10 Linux containers for host-level metrics
- `cAdvisor` for container-level metrics
- `Blackbox Exporter` for HTTP health checks
- `Loki` for log storage
- `Promtail` for collecting logs and sending them to Loki

## Services and Ports

| Service             | Port   | URL                                                        |
| ------------------- | ------ | ---------------------------------------------------------- |
| Grafana             | `3000` | [http://localhost:3000](http://localhost:3000)             |
| Prometheus          | `9090` | [http://localhost:9090](http://localhost:9090)             |
| Alertmanager        | `9093` | [http://localhost:9093](http://localhost:9093)             |
| cAdvisor            | `8080` | [http://localhost:8080](http://localhost:8080)             |
| Blackbox Exporter   | `9115` | [http://localhost:9115](http://localhost:9115)             |
| Loki Ready Endpoint | `3100` | [http://localhost:3100/ready](http://localhost:3100/ready) |

Node Exporter containers are exposed on ports `9101` to `9110`.

## Setup Prerequisites

Before starting, make sure you have:

- Docker installed
- Docker Compose available through `docker compose`
- Internet access during the first build because the Docker image downloads Node Exporter

Check versions:

```bash
docker --version
docker compose version
```

## Setup Steps

### 1. Clone the repository

```bash
git clone https://github.com/sameeralam3127/monitoring.git
cd monitoring
```

### 2. Start the full stack

```bash
docker compose up -d --build
```

This command will:

- build the Linux container image from `Dockerfile`
- start `10` Linux containers with Node Exporter
- start Prometheus, Grafana, Alertmanager, cAdvisor, Blackbox Exporter, Loki, and Promtail
- create persistent Docker volumes for Grafana, Prometheus, and Loki

### 3. Verify the containers are running

```bash
docker compose ps
```

### 4. Open the services

- Grafana: [http://localhost:3000](http://localhost:3000)
- Prometheus: [http://localhost:9090](http://localhost:9090)
- Alertmanager: [http://localhost:9093](http://localhost:9093)
- cAdvisor: [http://localhost:8080](http://localhost:8080)

Grafana default login:

- Username: `admin`
- Password: `admin`

## Grafana Setup

Grafana is already provisioned automatically using:

- `grafana/provisioning/datasources/datasources.yml`
- `grafana/provisioning/dashboards/dashboards.yml`
- `grafana/dashboards/advanced-monitoring-dashboard.json`

After login, you should already see:

- `Prometheus` as the default data source
- `Loki` as the log data source
- `Advanced Monitoring Stack` dashboard

## Prometheus Configuration

Prometheus configuration lives in:

- `prometheus/prometheus.yml`
- `prometheus/rules/alerts.yml`

Configured scrape jobs:

- `prometheus`
- `alertmanager`
- `node_exporter`
- `cadvisor`
- `blackbox-exporter`
- `blackbox-http`

Included alerts:

- `TargetDown`
- `HostHighCPU`
- `HostHighMemory`
- `ContainerHighCPU`
- `ContainerHighMemory`
- `SyntheticProbeFailed`

## Logging Setup

Logging is configured with:

- `loki/loki-config.yml`
- `promtail/promtail-config.yml`

Promtail collects:

- host log files from `/var/log`
- Docker container logs from `/var/lib/docker/containers`

## Blackbox Monitoring

Blackbox Exporter configuration is stored in:

- `blackbox/blackbox.yml`

It probes internal HTTP endpoints for:

- Grafana
- Prometheus
- cAdvisor
- Alertmanager
- Loki

## Useful Commands

Start stack:

```bash
docker compose up -d --build
```

Stop stack:

```bash
docker compose down
```

Stop stack and remove volumes:

```bash
docker compose down -v
```

View container status:

```bash
docker compose ps
```

View logs for a service:

```bash
docker compose logs -f prometheus
docker compose logs -f grafana
docker compose logs -f promtail
```

Restart a service:

```bash
docker compose restart grafana
```

## Dashboard Preview

The repository also includes:

- `grafana-dashboard.json` as a standalone dashboard export
- `Screenshot 2026-04-05 at 11.57.50 PM.png` as a dashboard preview image

![Dashboard Preview](./Screenshot%202026-04-05%20at%2011.57.50%E2%80%AFPM.png)

## Troubleshooting

- If Prometheus targets show as down, open [http://localhost:9090/targets](http://localhost:9090/targets).
- If Grafana loads without dashboards, check the mounted provisioning files under `grafana/provisioning/`.
- If Promtail cannot read Docker logs, verify that Docker stores container logs under `/var/lib/docker/containers`.
- If the Node Exporter image build fails, retry with working internet access because the Dockerfile downloads the exporter binary during build.
- If alerts do not notify anywhere, add a real receiver configuration in `alertmanager/alertmanager.yml`.

## Suggested Next Improvements

- Add Slack, email, or PagerDuty integrations to Alertmanager
- Add OpenTelemetry and Tempo for traces
- Add exporters for Postgres, Redis, Nginx, MySQL, and application services
- Add TLS, secrets, and stronger credentials for non-local use
- Add long-term metric storage with Thanos, Mimir, or VictoriaMetrics

## License

MIT License
