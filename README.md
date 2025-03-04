# Production-Ready Flask Couchbase Microservice

This repository contains a production-ready Flask microservice that connects to a Couchbase database. It is designed to demonstrate how to set up a web server with health check endpoints, graceful shutdown capabilities, and logging using Loguru. The application also integrates with Prometheus for monitoring and Grafana for visualization.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Monitoring with Prometheus](#monitoring-with-prometheus)
- [Logging](#logging)
- [Contributing](#contributing)
- [License](#license)

## Features

- Connects to a Couchbase database.
- Provides health check and shutdown endpoints.
- Implements request logging and error handling.
- Supports graceful shutdown of the server.
- Exports metrics for Prometheus monitoring.
- Integrates with Grafana for real-time monitoring and visualization.

## Requirements

- Python 3.7 or higher
- Couchbase Server
- Flask
- Loguru
- Prometheus Flask Exporter
- Grafana

You can install the required packages using the following command:

```bash
pip install -r requirements.txt
```

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Couchbase server and create a bucket. Update the configuration in the `.env` file or set environment variables as described in the Configuration section.

## Configuration

The application configuration is managed through environment variables. You can set the following variables:

- `FLASK_HOST`: The host for the Flask application (default: `0.0.0.0`).
- `FLASK_PORT`: The port for the Flask application (default: `8080`).
- `FLASK_DEBUG`: Enable or disable debug mode (default: `False`).
- `REQUEST_TIMEOUT`: Timeout for requests in seconds (default: `30`).
- `KEEP_ALIVE_TIMEOUT`: Keep-alive timeout in seconds (default: `5`).
- `GRACEFUL_SHUTDOWN_TIMEOUT`: Timeout for graceful shutdown in seconds (default: `5`).
- `FLASK_SECRET_KEY`: Secret key for session management (default: `your-secret-key-here`).
- `COUCHBASE_HOST`: Couchbase server host (default: `couchbase://localhost`).
- `COUCHBASE_USER`: Couchbase username (default: `Administrator`).
- `COUCHBASE_PASSWORD`: Couchbase password (default: `password`).
- `COUCHBASE_BUCKET`: Couchbase bucket name (default: `travel-sample`).

## Usage

To run the application, execute the following command:

```bash
python main.py
```

The application will start and listen for incoming requests on the specified host and port.

## Endpoints

- `GET /`: Returns a simple greeting message.
- `GET /health-check`: Returns a health check status.
- `POST /shutdown`: Initiates a graceful shutdown of the server.

## Monitoring with Prometheus

The application exports metrics that can be scraped by Prometheus. To set up Prometheus:

1. Configure your `prometheus.yml` to scrape metrics from the Flask application:

   ```yaml
   global:
     scrape_interval: 10s
   scrape_configs:
     - job_name: flask-app
       static_configs:
         - targets:
             - localhost:8080
       metrics_path: /metrics
   ```

2. Start Prometheus and point it to your configuration file.

3. Use Grafana to visualize the metrics collected by Prometheus. You can create dashboards to monitor the health and performance of your microservice.

## Logging

The application uses Loguru for logging. Logs are output to the console and also saved to a file (`logs/app.log`). The log level can be configured through the `LOG_LEVEL` environment variable.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
