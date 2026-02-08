import asyncio
import os

import streamlit as st
from pydantic_ai import Agent
from pydantic_ai import WebSearchTool
from pydantic_ai.messages import (
    ModelRequest,
    ModelResponse,
    UserPromptPart,
    TextPart,
)
from pydantic_ai.models.openai import OpenAIResponsesModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the model
# Note: WebSearchTool is a built-in tool executed by the model provider.
# It requires OpenAIResponsesModel for OpenAI models.
llm = os.getenv("LLM_MODEL", "gpt-4o")
model = OpenAIResponsesModel(llm)

# Define the Agent with the built-in WebSearchTool
search_agent = Agent(
    model,
    builtin_tools=[WebSearchTool()],
    system_prompt=(
        "You are a helpful research assistant. "
        "Use the web search tool to find accurate and up-to-date information. "
        "For complex questions, perform multiple searches to gather different perspectives or more details."
    ),
)


def filter_new_messages(new_messages):
    """Filter out user prompt parts from the new messages to avoid duplication in history."""
    return [
        msg
        for msg in new_messages
        if not (
            isinstance(msg, ModelRequest)
            and any(isinstance(p, UserPromptPart) for p in msg.parts)
        )
    ]


async def handle_agent_stream(user_input: str):
    """Handles the agent's stream, updating the UI and session state."""
    run_stream_cm = search_agent.run_stream(
        user_input,
        message_history=st.session_state.messages[:-1],
    )

    thoughts_placeholder = st.empty()

    with thoughts_placeholder.container():
        with st.spinner("Searching the web..."):
            result = await run_stream_cm.__aenter__()
            try:
                partial_text = ""
                stream = result.stream_text(delta=True)

                # Wait for the first chunk to arrive while showing the spinner
                try:
                    first_chunk = await anext(stream)
                    partial_text += first_chunk
                except StopAsyncIteration:
                    pass
            except Exception as e:
                await run_stream_cm.__aexit__(type(e), e, e.__traceback__)
                raise

    message_placeholder = st.empty()
    if partial_text:
        message_placeholder.markdown(partial_text)

    try:
        async for chunk in stream:
            partial_text += chunk
            message_placeholder.markdown(partial_text)

        st.session_state.messages.extend(filter_new_messages(result.new_messages()))
    finally:
        await run_stream_cm.__aexit__(None, None, None)


async def run_agent_with_streaming(user_input: str):
    """Run the agent and stream the response to the UI."""
    await handle_agent_stream(user_input)


def init_session_state():
    """Initialize the session state for the application."""
    if "messages" not in st.session_state:
        st.session_state.messages = []


def display_chat_messages(messages):
    """Iterate through and display the chat history."""
    for msg in messages:
        if isinstance(msg, ModelRequest):
            for part in msg.parts:
                if isinstance(part, UserPromptPart):
                    with st.chat_message("user"):
                        st.markdown(part.content)
        elif isinstance(msg, ModelResponse):
            if any(isinstance(p, TextPart) for p in msg.parts):
                with st.chat_message("assistant"):
                    for part in msg.parts:
                        if isinstance(part, TextPart):
                            st.markdown(part.content)


def render_suggestions(suggestions: list[str]) -> str | None:
    """Render suggestion buttons and return the clicked suggestion if any."""
    cols = st.columns(len(suggestions))
    clicked_suggestion = None
    for i, suggestion in enumerate(suggestions):
        if cols[i].button(suggestion, use_container_width=True):
            clicked_suggestion = suggestion
    return clicked_suggestion


async def main():
    st.title("Web Search Research Assistant")
    st.write(
        "I can search the web to answer your questions with the latest information."
    )

    init_session_state()

    suggestion = render_suggestions(
        [
            "What is the latest news about PydanticAI?",
            "Who won the last Super Bowl?",
        ]
    )

    # Display chat history
    display_chat_messages(st.session_state.messages)

    # Handle chat input and suggestions
    user_input = st.chat_input("Ask me anything...")

    if suggestion:
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
