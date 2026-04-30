# AI Hand-Tracking System (Distributed Microservices)

A high-performance, decoupled system using computer vision to control a GUI. This project demonstrates real-time communication between independent services using **gRPC** and **Redis Pub/Sub**.

---

## 🏗 System Architecture
The project is split into three distinct services to ensure scalability and separation of concerns:

1.  **Detection Service (Edge/Producer):** Uses MediaPipe to detect hand landmarks. It acts as a gRPC client, streaming normalized coordinates to the backend.
2.  **Tracking Service (Backbone/Broker):** A gRPC Server running inside Docker. It processes coordinate deltas to determine movement (UP/DOWN/LEFT/RIGHT) and publishes events to Redis.
3.  **GUI Service (Consumer):** A Pygame application that subscribes to Redis, manages the game state, and handles score logging. It dynamically fetches player configuration (speed) from Redis in real-time.

---

## 🚀 Technical Stack
*   **Protocol Buffers (gRPC):** Low-latency, strongly typed service-to-service communication.
*   **Redis Pub/Sub:** Event-driven message brokering for decoupling the UI from the logic.
*   **MediaPipe & OpenCV:** State-of-the-art hand tracking and computer vision.
*   **Docker & Docker Compose:** Containerized backend infrastructure for consistent deployment.
*   **Logging:** Time-stamped persistence of game actions in `game_logs.log`.

---

## 🛠 How to Run from Scratch

### 1. Prerequisites
*   Python 3.11+
*   Docker (with Compose V2 support)
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

We use Docker Compose to orchestrate the Redis database and the Tracking gRPC service.
Bash

docker compose up --build -d

    Note: Use docker compose (with a space) to ensure V2 compatibility.

4. Start the Application

Open two separate terminals and ensure your virtual environment is active in both.

Terminal A: The Game
Bash

python gui_service.py

Terminal B: Hand Detection
Bash

python detection_service.py

🎮 Features & Controls

    Right Hand Tracking: Move your hand in front of the webcam to control the blue "+" sign.

    Score Logging: Every point earned is logged with a high-precision timestamp in game_logs.log.

    Dynamic Configuration: This project uses Redis as a centralized state provider. Adjust player speed in real-time without restarting services:
    Bash

    docker exec -it hand-redis redis-cli set player_speed 40

📂 File Structure

    detection_service.py: Webcam capture and MediaPipe processing.

    tracking_service.py: gRPC server and direction calculation.

    gui_service.py: Game UI and Redis subscriber.

    hand_pos.proto: gRPC service definitions.

    docker-compose.yml: Orchestration for backend services.

    Dockerfile: Build instructions for the tracking backbone.

    game_logs.log: Automatically generated action logs.