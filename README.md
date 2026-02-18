# 🎲 Django Board Games Platform

A real-time multiplayer board game platform built with **Django** and **Django Channels (WebSockets)**. Play classic games like **Tic-Tac-Toe** (and coming soon: Ludo) with friends instantly!

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Django](https://img.shields.io/badge/Django-4.2-green)
![Channels](https://img.shields.io/badge/WebSockets-Channels-orange)

## ✨ Features

-   **Real-Time Multiplayer**: Instant moves and updates using WebSockets.
-   **Lobby System**: Create a room, share the code, and play anywhere.
-   **Player Identity**: Enter your name and see who you are playing against.
-   **Responsive Design**: Premium dark-mode UI that works on desktop and mobile.
-   **Spectator Mode**: Watch games in progress if he room is full.

## 🚀 Getting Started

### Prerequisites

-   Python 3.8+ installed.

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/boardgames.git
    cd boardgames
    ```

2.  **Create a Virtual Environment**:
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run Migrations**:
    ```bash
    python manage.py migrate
    ```

5.  **Start the Server**:
    ```bash
    python manage.py runserver 0.0.0.0:8000
    ```

6.  **Play!**
    -   Open your browser at `http://localhost:8000`.
    -   Enter your name and create a room.
    -   Share the Room Code with a friend!

## ☁️ Deployment

This project is ready for deployment on platforms like [Render](https://render.com).

1.  **See [deployment.md](deployment.md)** for a full step-by-step guide.
2.  **Quick Start**:
    -   Push to GitHub.
    -   Create a new Web Service on Render.
    -   **Start Command**: `uvicorn boardgames.asgi:application --host 0.0.0.0 --port $PORT`

## 🛠️ Built With

-   **Django**: The web framework for perfectionists with deadlines.
-   **Django Channels**: Asynchronous support for Django (WebSockets).
-   **Daphne / Uvicorn**: ASGI servers for handling WebSocket connections.
-   **Vanilla JS**: Lightweight frontend logic.

## 🔜 Coming Soon

-   🔴 **Ludo**: Full 4-player Ludo game support.
-   🏆 **Leaderboard**: Track wins and losses.
