# Weather Agent Documentation

This document describes the configuration and tools for the Weather Agent.

## Agent Overview
The Weather Agent is a minimalist chatbot built using **Pydantic AI** and **Streamlit**. It provides real-time weather information using the Open-Meteo API.

## Core Components

### 1. Model Configuration
- **Provider:** OpenAI (via `OpenAIModel`)
- **Default Model:** `gpt-4o-mini` (configurable via `LLM_MODEL` environment variable)

### 2. Tools
The agent has access to the following tool:

#### `get_weather`
- **Description:** Fetches current weather for a specific location.
- **Implementation Details:**
  - Uses `httpx` for asynchronous HTTP requests.
  - First calls the **Open-Meteo Geocoding API** to convert a location name (e.g., "London") into latitude and longitude.
  - Then calls the **Open-Meteo Forecast API** to get current weather data.
- **Parameters:**
  - `location` (str): The name of the city/country.

## Operational Instructions
- The agent should always use the `get_weather` tool when asked about the weather.
- If a location is ambiguous or not found, the agent should ask for clarification.
- Temperatures are returned in Celsius (°C) and windspeeds in km/h.

## Environment Variables
Ensure the following are set in your `.env` file:
- `OPENAI_API_KEY`: Required for the LLM.
- `LLM_MODEL`: (Optional) Defaults to `gpt-4o-mini`.

## How to Extend
To add more capabilities:
1. Define a new `@weather_agent.tool` in `main.py`.
2. Update the system prompt if necessary to guide the agent on when to use the new tool.
