# 🐍 Snake & Ladder Streamlit App

A simple, interactive Snake & Ladder game built with Python and [Streamlit](https://streamlit.io/). This project demonstrates how to manage game state, handle logic, and create a custom UI in a Streamlit application.

## 🚀 How to Run

1.  **Install dependencies**:
    ```bash
    pip install streamlit
    ```
2.  **Run the app**:
    ```bash
    streamlit run app.py
    ```

## 📂 Project Structure

-   `app.py`: The main entry point. It handles the game loop, session state, and coordinates updates between logic and UI.
-   `game_logic.py`: Contains the core rules of the game (movement, collisions, win conditions).
-   `ui.py`: Manages the visual presentation, including custom CSS styling and board rendering.
-   `constants.py`: Stores static data like board configuration (Snake/Ladder positions) and colors.

## 🧠 Key Logic & Functions

### 1. Game State Management (`app.py`)
Streamlit reruns the script on every interaction. We use `st.session_state` to persist data across reruns.
-   `init_state()`: Initializes variables like player positions, current turn, and game mode (PvP or AI).
-   `handle_turn(player)`: Orchestrates a single turn—rolling dice, moving the player, updating stats, and checking for a win.

### 2. Core Rules (`game_logic.py`)
This file is pure Python logic, independent of the UI.
-   `roll_dice()`: Returns a random integer between 1 and 6.
-   `move_player(position, roll)`: Calculates the new position.
    -   **Overshoot Rule**: If a player rolls higher than needed to reach 50, they bounce back.
    -   **Snakes & Ladders**: Checks if the new position is in the `SNAKES` or `LADDERS` dictionary and adjusts the position accordingly.
-   `check_extra_turn(roll)`: Grants an extra turn if the player rolls a 6.

### 3. User Interface (`ui.py`)
We use HTML/CSS injection to create a custom look that goes beyond standard Streamlit widgets.
-   `render_board(positions)`: Dynamically generates an HTML grid representing the board, placing player tokens (`🔴`, `🔵`) on their respective squares.
-   `render_game_dashboard(...)`: Layouts the board and controls side-by-side using `st.columns`.

## 🎮 Game Rules
-   **Objective**: Be the first to reach square **50**.
-   **Movement**: Roll the dice to move forward.
-   **Snakes (🐍)**: If you land on a snake's head, you slide down to its tail.
-   **Ladders (🪜)**: If you land on a ladder's base, you climb up to the top.
-   **Extra Turn**: Rolling a **6** gives you another turn immediately.
