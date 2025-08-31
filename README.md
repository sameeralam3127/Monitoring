# Monitoring Stack with Linux Containers, Prometheus, Grafana, Node Exporter, and cAdvisor

This repository provides a full Docker-based monitoring stack to manage 10 Linux containers and monitor their system resources using Prometheus, Grafana, Node Exporter, and cAdvisor.

---

## Features

- **10 Linux containers** running Node Exporter to simulate monitored hosts
- **cAdvisor** for Docker container metrics
- **Prometheus** for collecting metrics
- **Grafana** for visualization
- **Persistent storage** for Prometheus and Grafana
- **Pre-built Grafana dashboards** (JSON file included)

---

##  Tech Stack

- **Docker & Docker Compose** — container orchestration
- **Prometheus** — metrics collection and alerting
- **Grafana** — visualization and dashboards
- **Node Exporter** — system-level metrics (CPU, RAM, disk, services, users)
- **cAdvisor** — container resource metrics

---

##  Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/sameeralam3127/monitoring.git
cd monitoring
```

### 2. Check Docker Installation

```bash
docker --version
docker-compose --version
```

### 3. Build and Start the Stack

```bash
docker-compose up -d --build
```

This will:

- Build `linux_system` images with Node Exporter
- Start **10 Linux containers**
- Start **Prometheus, Grafana, and cAdvisor**

---

## Accessing Services

| Service    | URL                                            | Login           |
| ---------- | ---------------------------------------------- | --------------- |
| Grafana    | [http://localhost:3000](http://localhost:3000) | `admin / admin` |
| Prometheus | [http://localhost:9090](http://localhost:9090) | N/A             |
| cAdvisor   | [http://localhost:8080](http://localhost:8080) | N/A             |

---

##  Grafana Setup

1. Log in to Grafana at [http://localhost:3000](http://localhost:3000)
   Username: `admin`
   Password: `admin`

2. Add **Prometheus as a data source**:

   - URL: `http://prometheus:9090`

3. Import Dashboard:

   - Navigate to **Dashboards → Import**
   - Upload the provided JSON file in `grafana/dashboard.json`

---

##  Prometheus Example Queries

- **CPU Usage** (per container):

  ```promql
  rate(node_cpu_seconds_total{mode="user"}[5m])
  ```

- **Memory Usage**:

  ```promql
  node_memory_Active_bytes / node_memory_MemTotal_bytes * 100
  ```

- **Running Services (systemd)**:

  ```promql
  node_systemd_unit_state{state="active"}
  ```

- **Failed Services**:

  ```promql
  node_systemd_unit_state{state="failed"}
  ```

- **Logged-in Users**:

  ```promql
  node_users_logged_in
  ```

- **Docker Container CPU Usage (from cAdvisor)**:

  ```promql
  rate(container_cpu_usage_seconds_total{name=~".+"}[5m])
  ```

---

## Troubleshooting

- **Prometheus target down**

  - Check Prometheus targets at [http://localhost:9090/targets](http://localhost:9090/targets)
  - Verify container is running: `docker ps`
  - Restart service:

    ```bash
    docker-compose restart prometheus
    ```

- **Grafana not saving dashboards**

  - Ensure `grafana_data` volume is correctly mounted
  - Restart Grafana:

    ```bash
    docker-compose restart grafana
    ```

- **cAdvisor not accessible**

  - Check logs:

    ```bash
    docker logs cadvisor
    ```

---

## Notes

- Each Linux container exposes Node Exporter on a unique port (`9101` … `9110`)
- Prometheus config is in `prometheus/prometheus.yml`
- All services use **persistent volumes**

---

## License

MIT License
