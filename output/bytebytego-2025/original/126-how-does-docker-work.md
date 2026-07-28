# 126 - How does Docker Work?

- Source: ByteByteGo Big Archive System Design 2025
- PDF pages: 265-265
- Figures: 1

## Figures

![How does Docker Work? - figure 1](../assets/126/figure-01.png)

## Original Extracted Text

Docker's architecture comprises three main components:

   ● Docker Client
      This is the interface through which users interact. It communicates with the Docker daemon.

   ● Docker Host
      Here, the Docker daemon listens for Docker API requests and manages various Docker
      objects, including images, containers, networks, and volumes.

   ● Docker Registry
      This is where Docker images are stored. Docker Hub, for instance, is a widely-used public
      registry.
