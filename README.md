# AI Hand-Tracking System (Distributed Microservices)

A high-performance, decoupled system using computer vision to control a GUI. This project demonstrates real-time communication between independent services using **gRPC** and **Redis Pub/Sub**.

## System Architecture
The project is split into three distinct services to ensure scalability and separation of concerns:

1.  **Detection Service (Edge/Producer):** Uses **MediaPipe** to detect hand landmarks. It acts as a gRPC client, streaming coordinates to the backend.
2.  **Tracking Service (Backbone/Broker):** A **gRPC Server** running inside **Docker**. It processes coordinate deltas to determine movement (UP/DOWN/LEFT/RIGHT) and publishes events to Redis.
3.  **GUI Service (Consumer):** A **Pygame** application that subscribes to Redis, manages the game state, and handles score logging.

## Technical Stack
*   **Protocol Buffers (gRPC):** Low-latency, strongly typed service-to-service communication.
*   **Redis Pub/Sub:** Event-driven message brokering for decoupling the UI from the logic.
*   **MediaPipe & OpenCV:** State-of-the-art hand tracking.
*   **Docker:** Containerized backend infrastructure.
*   **Logging:** Time-stamped persistence of game actions in `game_logs.log`.

---

## How to Run from Scratch

### 1. Prerequisites
*   Python 3.11+
*   Docker
*   A working Webcam

### 2. Setup Environment
Clone the repository and install dependencies:
```bash
python3 -m venv venv311
source venv311/bin/activate
pip install -r requirements.txt

Prepare your environment variables:
Bash

cp sample_env.env .env

3. Start the Backend (Docker)

We run the infrastructure and the tracking logic inside Docker to ensure a consistent environment.
Bash

docker run -d --name hand-redis -p 6379:6379 redis:latest

docker build -t tracking-image .
docker run -d --name hand-tracking-svc -p 50051:50051 tracking-image

4. Start the Application

Open two separate terminals:

Terminal A: The Game
Bash

python gui_service.py

Terminal B: Hand Detection
Bash

python detection_service.py

Features & Controls

    Right Hand Tracking: Move your hand to control the blue "+" sign.

    Score Logging: Every point earned is logged with a high-precision timestamp in game_logs.log.

    Dynamic Configuration: Adjust the player speed in real-time without restarting the services by using the Redis CLI:
    Bash

    docker exec -it hand-redis redis-cli set player_speed 40

File Structure

    detection_service.py: Webcam capture and MediaPipe processing.

    tracking_service.py: gRPC server and direction calculation.

    gui_service.py: Game UI and Redis subscriber.

    hand_pos.proto: gRPC service definitions.

    Dockerfile: Build instructions for the tracking backbone.

    game_logs.log: Automatically generated action logs.
