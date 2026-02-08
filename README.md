# 🤖 Streamlit + PydanticAI: Weather Agent Example

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
[![PydanticAI](https://img.shields.io/badge/PydanticAI-Agent-blue)](https://ai.pydantic.dev/)

A minimalist, high-performance example of a **Web UI** built with **Streamlit** powered by a **PydanticAI** agent. This project serves as a boilerplate for building streaming AI agents with robust tool-calling capabilities.

## 🌟 Why this example?

Integrating LLM agents into web interfaces often involves handling complex state, streaming responses, and tool outputs. This repository demonstrates a clean, production-ready pattern for:

- **Asynchronous Tool Calling**: The agent fetches real-time coordinates and weather data asynchronously using `httpx`.
- **Native Streaming**: Leveraging `pydantic-ai`'s `run_stream` to pipe tokens directly into Streamlit's chat UI for a snappy UX.
- **Robust State Management**: Using Streamlit's `session_state` to maintain a message history compatible with PydanticAI's internal message types.
- **Clean Architecture**: Decoupled API logic from agent tools, enabling better testability and maintenance.

## 🚀 Key Features

- **Agentic Logic**: Uses `pydantic-ai` for structured, type-safe tool execution.
- **Dynamic UI**: Responsive chat interface with built-in suggestion buttons.
- **Real-time Weather**: Integrated with Open-Meteo APIs (No API key required for weather data!).
- **Fast Development**: Managed with `uv` for instant environment reproducibility and high performance.

## 🛠️ Tech Stack

- **Framework**: [PydanticAI](https://ai.pydantic.dev/)
- **Frontend**: [Streamlit](https://streamlit.io/)
- **Runtime**: [Python 3.14+](https://www.python.org/)
- **Package Manager**: [uv](https://astral.sh/uv)
- **APIs**: [Open-Meteo](https://open-meteo.com/) (Geocoding & Forecast)

## 🏁 Quick Start

### 1. Install `uv`
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Setup and Install
```bash
git clone <repository-url>
cd streamlit-pydanticai-example
uv sync
```

### 3. Configure
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your-api-key
LLM_MODEL=gpt-4o-mini
```

### 4. Run the App
```bash
uv run streamlit run main.py
```

The application will be available at `http://localhost:8501`.

## 📂 Project Structure

- `main.py`: The heart of the application, containing the `weather_agent` and the Streamlit UI loop.
- `PLAN.md`: Documentation of the architectural improvements and refactoring steps.
- `pyproject.toml`: Modern dependency management and project configuration.
