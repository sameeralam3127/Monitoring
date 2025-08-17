# Monitoring Stack with Linux Containers, Prometheus, Grafana, Node Exporter, and cAdvisor

This repository provides a full Docker-based monitoring stack to manage 10 Linux containers and monitor their system resources using Prometheus, Grafana, Node Exporter, and cAdvisor.

---

## Repository: [https://github.com/sameeralam3127/monitoring](https://github.com/sameeralam3127/monitoring)

---

## Features

- 10 Ubuntu Linux containers representing hosts.
- Node Exporter installed on each container to expose system metrics.
- cAdvisor to monitor container metrics.
- Prometheus to collect metrics from Node Exporters and cAdvisor.
- Grafana for visualization of metrics.
- Docker Compose for easy deployment.

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/sameeralam3127/monitoring.git
cd monitoring
```

### 2. Docker Setup

Make sure Docker and Docker Compose are installed.

```bash
docker --version
docker-compose --version
```

### 3. Build and Start the Containers

```bash
docker-compose up -d --build
```

This will:

- Build the Linux host image with Node Exporter.
- Start 10 Linux containers.
- Start Prometheus, Grafana, and cAdvisor.

### 4. Accessing Services on Browser

| Service    | URL                                            | Default Login |
| ---------- | ---------------------------------------------- | ------------- |
| Grafana    | [http://localhost:3000](http://localhost:3000) | admin / admin |
| Prometheus | [http://localhost:9090](http://localhost:9090) | N/A           |
| cAdvisor   | [http://localhost:8080](http://localhost:8080) | N/A           |

### 5. Configure Grafana

1. Log in to Grafana at `http://localhost:3000`.
2. Add Prometheus as a data source:

   - URL: `http://prometheus:9090`

3. Import dashboards for Node Exporter and cAdvisor metrics.

### 6. Verify Node Exporter Metrics

Prometheus should show all Node Exporter targets as **UP**:

- Go to Prometheus UI: `http://localhost:9090/targets`
- Check that `node_exporter` targets are reachable.

### 7. Monitor Resource Usage

- cAdvisor UI shows container CPU, memory, and network usage.
- Grafana dashboards visualize metrics over time.

---

## Docker Compose Services

- `linux_system_1` to `linux_system_10`: Ubuntu containers with Node Exporter.
- `cadvisor`: Monitors all running containers.
- `prometheus`: Collects metrics from Node Exporter and cAdvisor.
- `grafana`: Dashboard and visualization.

---

## Notes

- Node Exporter port mapping is incremental: `9101` for `linux_system_1`, `9102` for `linux_system_2`, etc.
- Prometheus configuration in `prometheus/prometheus.yml` lists all Node Exporter targets and cAdvisor.
- All containers run in detached mode (`-d`) for continuous monitoring.

---

## License

MIT License
