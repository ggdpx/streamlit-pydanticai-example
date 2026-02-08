# Weather Agent Documentation

This document describes the configuration and tools for the Weather Agent.

## Agent Overview
The Weather Agent is a minimalist chatbot built using **Pydantic AI** and **Streamlit**. It provides real-time weather information using the Open-Meteo API.

## Core Components

### 1. Model Configuration
- **Provider:** OpenAI (via `OpenAIModel`)
- **Default Model:** `gpt-4o-mini` (configurable via `LLM_MODEL` environment variable)

### 2. Tools
The agent has access to the following tools:

#### `get_location_coordinates`
- **Description:** Finds the latitude and longitude for a given location name.
- **Parameters:**
  - `location` (str): The name of the city/country.
- **Returns:** A dictionary containing `latitude`, `longitude`, and `city_name`.

#### `get_weather_by_coords`
- **Description:** Fetches current weather for specific coordinates.
- **Parameters:**
  - `latitude` (float): Latitude.
  - `longitude` (float): Longitude.
- **Returns:** A formatted string with temperature and windspeed.

## Operational Instructions
- To provide weather info, the agent MUST first call `get_location_coordinates` followed by `get_weather_by_coords`.
- This demonstrates the agent's ability to chain multiple tool calls to resolve a user request.
- Temperatures are returned in Celsius (°C) and windspeeds in km/h.

---

# Web Search Agent Documentation

This document describes the configuration for the Web Search Agent.

## Agent Overview
The Web Search Agent is a research assistant that uses PydanticAI's built-in `WebSearchTool` to find real-time information.

## Core Components

### 1. Model Configuration
- **Provider:** OpenAI (via `OpenAIModel`)
- **Default Model:** `gpt-4o` (configurable via `LLM_MODEL` environment variable)

### 2. Built-in Tools
#### `WebSearchTool`
- **Description:** Enables the model to perform web searches directly through the provider's infrastructure.
- **Capabilities:** Can perform multiple searches per turn to gather comprehensive information.

## Operational Instructions
- The agent uses the `WebSearchTool` whenever it needs up-to-date information not present in its training data.
- It is configured to handle complex research queries by breaking them down into multiple searches.

## How to Extend
To add more capabilities:
1. Define a new `@search_agent.tool` in `search.py`.
2. Update the system prompt to guide the agent on integrating search results with new specialized tools.
