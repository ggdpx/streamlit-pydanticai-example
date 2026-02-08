import asyncio
import os

import streamlit as st
import httpx
from pydantic_ai import Agent, RunContext
from pydantic_ai.messages import (
    ModelRequest,
    ModelResponse,
    UserPromptPart,
    TextPart,
)
from pydantic_ai.models.openai import OpenAIChatModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the model
llm = os.getenv("LLM_MODEL", "gpt-4o-mini")
model = OpenAIChatModel(llm)

# Define the Agent
weather_agent = Agent(
    model,
    system_prompt=(
        "You are a helpful weather assistant. "
        "To provide weather information, you must first find the coordinates of the location using `get_location_coordinates`, "
        "then use those coordinates to get the weather with `get_weather_by_coords`."
    ),
)


async def fetch_location_coordinates(location: str) -> dict[str, float | str]:
    """Fetch latitude and longitude for a given location using the Open-Meteo Geocoding API."""
    async with httpx.AsyncClient(timeout=60) as client:
        geo_resp = await client.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": location, "count": 1, "language": "en", "format": "json"},
        )
        geo_data = geo_resp.json()

        if not geo_data.get("results"):
            return {"error": f"Could not find coordinates for {location}."}

        result = geo_data["results"][0]
        return {
            "latitude": result["latitude"],
            "longitude": result["longitude"],
            "city_name": result["name"]
        }


async def fetch_weather_by_coords(latitude: float, longitude: float) -> str:
    """Fetch current weather for specific coordinates using the Open-Meteo Forecast API."""
    async with httpx.AsyncClient(timeout=60) as client:
        weather_resp = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={"latitude": latitude, "longitude": longitude, "current_weather": True},
        )
        weather_data = weather_resp.json()
        current = weather_data.get("current_weather")

        if not current:
            return "Could not retrieve weather for these coordinates."

        return (
            f"The current weather is {current['temperature']}°C "
            f"with a windspeed of {current['windspeed']} km/h."
        )


@weather_agent.tool
async def get_location_coordinates(ctx: RunContext[None], location: str) -> dict[str, float | str]:
    """
    Find the latitude and longitude for a given location name.

    Args:
        location: The city and country, e.g., "Paris, France"
    """
    print(f"Getting coordinates of {location}")
    return await fetch_location_coordinates(location)


@weather_agent.tool
async def get_weather_by_coords(ctx: RunContext[None], latitude: float, longitude: float) -> str:
    """
    Get the current weather for specific coordinates.

    Args:
        latitude: The latitude coordinate.
        longitude: The longitude coordinate.
    """
    print(f"Getting weather of {latitude}, {longitude}")
    return await fetch_weather_by_coords(latitude, longitude)


# Streamlit UI
async def run_agent_with_streaming(user_input: str):
    """Run the agent and stream the response to the UI."""
    message_placeholder = st.empty()

    # Use a manual context manager to have better control over the spinner
    run_stream_cm = weather_agent.run_stream(
        user_input,
        message_history=st.session_state.messages[:-1],
    )

    with st.spinner("Thinking..."):
        result = await run_stream_cm.__aenter__()
        try:
            partial_text = ""
            stream = result.stream_text(delta=True)

            # Wait for the first chunk to arrive
            try:
                first_chunk = await anext(stream)
                partial_text += first_chunk
                message_placeholder.markdown(partial_text)
            except StopAsyncIteration:
                pass
        except Exception as e:
            await run_stream_cm.__aexit__(type(e), e, e.__traceback__)
            raise

    # The spinner disappears here. Now we continue streaming the rest of the response.
    try:
        async for chunk in stream:
            partial_text += chunk
            message_placeholder.markdown(partial_text)

        # Update session state with new messages
        filtered_messages = [
            msg
            for msg in result.new_messages()
            if not (
                isinstance(msg, ModelRequest)
                and any(isinstance(p, UserPromptPart) for p in msg.parts)
            )
        ]
        st.session_state.messages.extend(filtered_messages)
    finally:
        await run_stream_cm.__aexit__(None, None, None)


async def main():
    st.title("Minimalist Weather Chatbot")
    st.write("Ask me about the weather anywhere in the world!")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for msg in st.session_state.messages:
        if isinstance(msg, ModelRequest):
            for part in msg.parts:
                if isinstance(part, UserPromptPart):
                    with st.chat_message("user"):
                        st.markdown(part.content)
        elif isinstance(msg, ModelResponse):
            for part in msg.parts:
                if isinstance(part, TextPart):
                    with st.chat_message("assistant"):
                        st.markdown(part.content)

    # Suggestions
    suggestions = [
        "What is the weather in Paris, France",
        "What is the weather in 3 biggest cities of UK",
    ]

    # Handle chat input and suggestions
    user_input = st.chat_input("What's the weather like in...")

    # Display suggestions as buttons
    cols = st.columns(len(suggestions))
    for i, suggestion in enumerate(suggestions):
        if cols[i].button(suggestion, use_container_width=True):
            user_input = suggestion

    if user_input:
        st.session_state.messages.append(
            ModelRequest(parts=[UserPromptPart(content=user_input)])
        )

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            await run_agent_with_streaming(user_input)


if __name__ == "__main__":
    asyncio.run(main())
