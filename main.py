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
    system_prompt="You are a helpful weather assistant. Use the get_weather tool to provide accurate information.",
)


@weather_agent.tool
async def get_weather(ctx: RunContext[None], location: str) -> str:
    """
    Get the current weather for a given location.

    Args:
        location: The city and country, e.g., "Paris, France"
    """
    print(f"Checking weather of {location}")
    # Use Open-Meteo geocoding to find coordinates
    async with httpx.AsyncClient(timeout=60) as client:
        geo_resp = await client.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": location, "count": 1, "language": "en", "format": "json"},
        )
        geo_data = geo_resp.json()

        if not geo_data.get("results"):
            print(f"Could not find coordinates for {location}.")
            return f"Could not find coordinates for {location}."

        result = geo_data["results"][0]
        lat, lon = result["latitude"], result["longitude"]
        city_name = result["name"]

        # Get current weather
        weather_resp = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={"latitude": lat, "longitude": lon, "current_weather": True},
        )
        weather_data = weather_resp.json()
        current = weather_data.get("current_weather")

        if not current:
            return f"Could not retrieve weather for {city_name}."

        return (
            f"The current weather in {city_name} is {current['temperature']}°C "
            f"with a windspeed of {current['windspeed']} km/h."
        )


# Streamlit UI
async def run_agent_with_streaming(user_input: str):
    """Run the agent and stream the response to the UI."""
    async with weather_agent.run_stream(
        user_input,
        message_history=st.session_state.messages[:-1],
    ) as result:
        partial_text = ""
        message_placeholder = st.empty()

        async for chunk in result.stream_text(delta=True):
            partial_text += chunk
            message_placeholder.markdown(partial_text)

        # Update session state with new messages
        # We exclude the user prompt from result.new_messages() as it's already added
        filtered_messages = [
            msg
            for msg in result.new_messages()
            if not (
                isinstance(msg, ModelRequest)
                and any(isinstance(p, UserPromptPart) for p in msg.parts)
            )
        ]
        st.session_state.messages.extend(filtered_messages)


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

    # Chat input
    if user_input := st.chat_input("What's the weather like in..."):
        st.session_state.messages.append(
            ModelRequest(parts=[UserPromptPart(content=user_input)])
        )

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            await run_agent_with_streaming(user_input)


if __name__ == "__main__":
    asyncio.run(main())
