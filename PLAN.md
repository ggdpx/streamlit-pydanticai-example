# Code Improvement Plan

This document outlines the planned refactoring and organizational improvements for the Streamlit Pydantic AI Weather Chatbot, ranked from least to most impactful.

## 1. Initialize Session State
*   **Action:** Move `st.session_state` initialization into a dedicated `init_session_state()` function.
*   **Impact:** Reduces boilerplate in the `main()` function and centralizes state management.

## 2. Extract Suggestion Rendering
*   **Action:** Create a `render_suggestions(suggestions)` function to handle the column and button logic.
*   **Impact:** Cleans up the main UI flow and makes the suggestion logic reusable or easier to modify.

## 3. Encapsulate Chat History Display
*   **Action:** Create a `display_chat_messages(messages)` function to handle the iteration and type-checking of Pydantic AI messages.
*   **Impact:** Significantly improves readability of the `main()` loop by hiding the complexity of message part parsing.

## 4. Refactor Stream Processing vs. UI Updates (COMPLETED)
*   **Action:** Split `run_agent_with_streaming` into logic for managing the agent stream and logic for updating the Streamlit UI.
*   **Impact:** Separates concerns between state management and UI rendering, making the streaming logic easier to debug and maintain.

## 5. Decouple API Logic from Agent Tools (COMPLETED)
*   **Action:** Move `httpx` API calls into standalone async functions (e.g., `fetch_weather_data`) that tools call.
*   **Impact:** (Highest) Enables independent testing of API logic, removes `RunContext` dependency for core functionality, and improves code reuse and error handling.
