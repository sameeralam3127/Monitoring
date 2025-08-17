FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

# Install monitoring tools + Node Exporter
RUN apt-get update && \
    apt-get install -y curl vim htop procps net-tools wget && \
    wget https://github.com/prometheus/node_exporter/releases/download/v1.6.1/node_exporter-1.6.1.linux-amd64.tar.gz && \
    tar xvf node_exporter-1.6.1.linux-amd64.tar.gz && \
    mv node_exporter-1.6.1.linux-amd64/node_exporter /usr/local/bin/ && \
    rm -rf node_exporter-1.6.1.linux-amd64*

# Expose Node Exporter port
EXPOSE 9100

# Start Node Exporter automatically
CMD ["/usr/local/bin/node_exporter"]
