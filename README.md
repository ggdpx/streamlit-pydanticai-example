# 🤖 Streamlit + PydanticAI: Examples

[![PydanticAI](https://img.shields.io/badge/PydanticAI-Agent-blue)](https://ai.pydantic.dev/)

A collection of minimalist examples for **Web UIs** built with **Streamlit** and powered by **PydanticAI** agents. These examples serve as boilerplates for building streaming AI agents with robust tool-calling capabilities.

## 🚀 Examples

### 1. Weather Chatbot (`weather.py`)
A real-time weather assistant demonstrating:
- **Asynchronous Tool Calling**: Fetches coordinates and weather data using `httpx`.
- **Native Streaming**: Tokens piped directly into Streamlit's chat UI.

## 🏁 Quick Start

```sh
cd streamlit-pydanticai-example
uv sync
```

Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your-api-key
```

### 4. Run the Weather Example
```bash
uv run streamlit run weather.py
```

The application will be available at `http://localhost:8501`.

## 📂 Project Structure

- `weather.py`: The implementation of the `weather_agent` and the Streamlit UI loop.
- `pyproject.toml`: Modern dependency management and project configuration.
