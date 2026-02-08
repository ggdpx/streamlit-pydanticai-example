# 🤖 Streamlit + PydanticAI: Weather Agent Example

[![PydanticAI](https://img.shields.io/badge/PydanticAI-Agent-blue)](https://ai.pydantic.dev/)

A minimalist example of a **Web UI** built with **Streamlit** powered by a **PydanticAI** agent. This project serves as a boilerplate for building streaming AI agents with robust tool-calling capabilities.

## 🌟 Why this example?

This repository demonstrates a clean, production-ready pattern for:

- **Asynchronous Tool Calling**: The agent fetches real-time coordinates and weather data asynchronously using `httpx`.
- **Native Streaming**: Leveraging `pydantic-ai`'s `run_stream` to pipe tokens directly into Streamlit's chat UI for a snappy UX.
- **State Management**: Using Streamlit's `session_state` to maintain a message history compatible with PydanticAI's internal message types.
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

```sh
cd streamlit-pydanticai-example
uv sync
```

Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your-api-key
```

### 4. Run the App
```bash
uv run streamlit run main.py
```

The application will be available at `http://localhost:8501`.

## 📂 Project Structure

- `main.py`: The heart of the application, containing the `weather_agent` and the Streamlit UI loop.
- `pyproject.toml`: Modern dependency management and project configuration.
