# krab55/plantuml Tomcat Docker Image

**Docker Hub URL**: [krab55/plantuml:latest](https://hub.docker.com/r/krab55/plantuml)

## Overview
This Docker image provides a ready-to-run [PlantUML Server](https://github.com/plantuml/plantuml-server) on Apache Tomcat 10, using OpenJDK 21 and Ubuntu 24.04.  
It is optimized for Kubernetes deployments with a built-in Tomcat health check endpoint.

---

## Features

- **Kubernetes-Ready**:  
  Exposes a `/health` endpoint via Tomcat's HealthCheckValve for robust liveness/readiness probes.
- **Secure**:  
  Runs as a non-root `tomcat` user with strict permissions.
- **Modern Stack**:  
  Ubuntu 24.04, Tomcat 10.0.20, OpenJDK 21, PlantUML Server v1.2025.0.
- **Resource Limits**:  
  Default JVM options: `-Xms512m -Xmx1024m -XX:MaxMetaspaceSize=256m`.

---

## Usage

```docker pull krab55/plantuml:latest
docker run -p 8080:8080 krab55/plantuml:latest
```

PlantUML will be available at [http://localhost:8080/](http://localhost:8080/).

---

## Kubernetes Deployment Example

```apiVersion: apps/v1
kind: Deployment
metadata:
  name: plantuml
spec:
  replicas: 2
  selector:
    matchLabels:
      app: plantuml
  template:
    metadata:
      labels:
        app: plantuml
    spec:
      containers:
        - name: plantuml
          image: krab55/plantuml:latest
          ports:
            - containerPort: 8080
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 40
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 20
            periodSeconds: 5
          resources:
            limits:
              memory: "1.5Gi"
              cpu: "1"```
```
---

## Configuration

```| Environment Variable | Default Value                                | Description             |
|----------------------|----------------------------------------------|-------------------------|
| `JAVA_OPTS`          | `-Xms512m -Xmx1024m -XX:MaxMetaspaceSize=256m` | JVM memory settings     |
| `TOMCAT_VERSION`     | `10.0.20`                                    | Apache Tomcat version   |
```
---

## Building from Source

```
docker build -t krab55/plantuml:latest .
```

---

## Notes

- The image automatically deploys PlantUML Server WAR as the Tomcat ROOT application.
- Health check endpoint `/health` is enabled for container monitoring, ideal for Kubernetes liveness/readiness probes.
- For more details, see the [PlantUML Server project](https://github.com/plantuml/plantuml-server).

---
