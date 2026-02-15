# Bolt-v0 AI System

A high-performance, FastAPI-based AI orchestration system that intelligently routes user queries between specialized agents (`Bolt` and `v0`) based on prompt complexity and context.

## 🚀 Features

-   **Dual Agent Architecture**:
    -   **Bolt Agent**: Optimized for technical, performance, and algorithmic queries.
    -   **v0 Agent**: Specialized for creative and design-oriented tasks.
-   **Smart Orchestration**:
    -   Dynamic token allocation based on prompt complexity.
    -   Intelligent routing using Zero-Shot Classification.
-   **Performance Optimization**:
    -   In-memory response caching.
    -   Rate limiting to prevent abuse.
    -   Model preloading for reduced latency.
-   **Web Interface**:
    -   Clean, responsive chat interface served via FastAPI and Jinja2 templates.

## 🛠️ Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd Toltira-main
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## 🏃‍♂️ Usage

1.  **Start the Server**:
    Run the application using the provided entry point.
    ```bash
    python main.py
    ```
    *By default, the server runs on port 8001.*

2.  **Access the Interface**:
    Open your browser and navigate to:
    `http://localhost:8001`

3.  **Interact with the AI**:
    Enter your prompt in the input field. The system will automatically route your request to the most suitable agent.

## 📂 Project Structure

-   `main.py`: Application entry point and FastAPI configuration.
-   `agents/`: Contains the logic for `bolt_agent` and `v0_agent`, along with the `orchestrator`.
-   `utils/`: Utility modules for performance tracking and token supervision.
-   `templates/`: HTML templates for the web interface.
-   `static/`: Static assets (CSS, JS).
-   `preload_models.py`: Script to initialize and warmup AI models.

## 🔧 Utilities

-   **Preload Models**: You can explicitly warm up the models by running:
    ```bash
    python preload_models.py
    ```

## 📝 License

[License Information Here]
