import streamlit as st
from constants import SNAKES, LADDERS, PLAYER_COLORS, DICE_FACES


def apply_styles():
    """Injects all custom CSS into the Streamlit app."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif;
    }

    h1, h2, h3 {
        font-family: 'Fredoka One', cursive;
    }

    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        min-height: 100vh;
    }

    .game-title {
        font-family: 'Fredoka One', cursive;
        font-size: 3rem;
        text-align: center;
        background: linear-gradient(90deg, #f72585, #7209b7, #4cc9f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }

    .game-subtitle {
        text-align: center;
        color: #adb5bd;
        font-size: 1rem;
        margin-top: 0;
        margin-bottom: 2rem;
    }

    .info-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 1rem 1.5rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
    }

    .board-cell {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 52px;
        height: 52px;
        border-radius: 10px;
        font-family: 'Fredoka One', cursive;
        font-size: 0.85rem;
        margin: 2px;
        position: relative;
    }

    .board-wrapper {
        background: rgba(255,255,255,0.04);
        border-radius: 20px;
        padding: 1rem;
        border: 1px solid rgba(255,255,255,0.08);
        display: inline-block;
    }

    .dice-display {
        font-size: 5rem;
        text-align: center;
        animation: bounce 0.4s ease;
    }

    @keyframes bounce {
        0%   { transform: scale(0.5) rotate(-10deg); opacity: 0; }
        60%  { transform: scale(1.2) rotate(5deg); }
        100% { transform: scale(1) rotate(0deg); opacity: 1; }
    }

    .win-banner {
        font-family: 'Fredoka One', cursive;
        font-size: 2rem;
        text-align: center;
        background: linear-gradient(90deg, #f72585, #ffd60a);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 1rem;
        animation: bounce 0.6s ease;
    }

    .log-entry {
        font-size: 0.85rem;
        color: #ced4da;
        padding: 4px 0;
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }

    .stButton > button {
        font-family: 'Fredoka One', cursive;
        font-size: 1.1rem;
        border-radius: 12px;
        padding: 0.5rem 2rem;
        border: none;
        transition: all 0.2s;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(247, 37, 133, 0.4);
    }

    .stRadio > label { color: white !important; }
    </style>
    """, unsafe_allow_html=True)


def render_title():
    """Renders the game title and subtitle."""
    st.markdown('<p class="game-title">🐍 Snake & Ladder 🪜</p>', unsafe_allow_html=True)
    st.markdown('<p class="game-subtitle">50-square edition · Roll to glory!</p>', unsafe_allow_html=True)


def render_start_screen():
    """
    Renders the mode selection screen.
    Returns the selected mode string ('ai' or 'pvp'), or None if not started yet.
    """
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### Choose Game Mode")
        mode = st.radio(
            "",
            ["🤖  Player vs AI", "👥  Player vs Player"],
            label_visibility="collapsed"
        )
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🎲  Start Game!", use_container_width=True):
            return "ai" if "AI" in mode else "pvp"

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("**🗺️ Board Legend**")
    st.markdown("🐍 **Red squares** = Snakes — slide down! &nbsp;&nbsp; 🪜 **Blue squares** = Ladders — climb up!")
    st.markdown("🔴 Player 1 &nbsp;&nbsp; 🔵 Player 2 / AI")
    st.markdown("**Rules:** Land exactly on 50 to win. Overshoot = bounce back. Roll a 6 = extra turn!")
    st.markdown('</div>', unsafe_allow_html=True)

    return None


def render_player_stats(positions, stats, mode):
    """Renders the two player stat cards side by side."""
    p2_label = "AI 🤖" if mode == "ai" else "Player 2"

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f'<div class="info-card" style="border-color:#f72585;">'
            f'<span style="color:#f72585;font-family:Fredoka One,cursive;font-size:1.1rem;">🔴 Player 1</span><br>'
            f'<span style="font-size:1.8rem;font-weight:bold;color:white;">Square {positions["player_1"]}</span><br>'
            f'<span style="color:#adb5bd;font-size:0.8rem;">'
            f'Turns: {len(stats["player_1"]["rolls"])} &nbsp;|&nbsp; '
            f'🐍 {stats["player_1"]["snakes_hit"]} &nbsp;|&nbsp; '
            f'🪜 {stats["player_1"]["ladders_climbed"]}</span>'
            f'</div>',
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f'<div class="info-card" style="border-color:#4cc9f0;">'
            f'<span style="color:#4cc9f0;font-family:Fredoka One,cursive;font-size:1.1rem;">🔵 {p2_label}</span><br>'
            f'<span style="font-size:1.8rem;font-weight:bold;color:white;">Square {positions["player_2"]}</span><br>'
            f'<span style="color:#adb5bd;font-size:0.8rem;">'
            f'Turns: {len(stats["player_2"]["rolls"])} &nbsp;|&nbsp; '
            f'🐍 {stats["player_2"]["snakes_hit"]} &nbsp;|&nbsp; '
            f'🪜 {stats["player_2"]["ladders_climbed"]}</span>'
            f'</div>',
            unsafe_allow_html=True
        )


def render_board(positions):
    """Renders the 5x10 game board with player tokens."""
    p1_pos = positions["player_1"]
    p2_pos = positions["player_2"]

    rows = []
    for row in range(4, -1, -1):
        cells = []
        for col in range(10):
            # Alternate row direction (snaking pattern)
            square = row * 10 + col + 1 if row % 2 == 0 else row * 10 + (9 - col) + 1

            # Cell color based on content
            if square in SNAKES:
                bg = "rgba(247,37,133,0.25)"
                border = "1px solid #f72585"
            elif square in LADDERS:
                bg = "rgba(76,201,240,0.25)"
                border = "1px solid #4cc9f0"
            else:
                bg = "rgba(255,255,255,0.06)"
                border = "1px solid rgba(255,255,255,0.1)"

            # Player tokens
            tokens = ""
            if p1_pos == square:
                tokens += "🔴"
            if p2_pos == square:
                tokens += "🔵"

            # Snake/ladder icon (only shown when no player is on it)
            icon = ""
            if not tokens:
                if square in SNAKES:
                    icon = "🐍"
                elif square in LADDERS:
                    icon = "🪜"

            cell_html = (
                f'<div class="board-cell" style="background:{bg};border:{border};">'
                f'<div style="font-size:0.65rem;color:#adb5bd;position:absolute;top:3px;left:5px;">{square}</div>'
                f'<div style="font-size:1rem;margin-top:8px;">{tokens if tokens else icon}</div>'
                f'</div>'
            )
            cells.append(cell_html)
        rows.append("".join(cells))

    board_html = (
        '<div class="board-wrapper">'
        + "".join(f'<div style="display:flex;justify-content:center;">{r}</div>' for r in rows)
        + "</div>"
    )
    st.markdown(board_html, unsafe_allow_html=True)


def render_dice(last_roll):
    """Renders the last dice roll as a unicode dice face."""
    if last_roll:
        st.markdown(
            f'<div class="dice-display">{DICE_FACES[last_roll]}</div>',
            unsafe_allow_html=True
        )


def render_turn_indicator(current_player, extra_turn, mode):
    """Shows whose turn it is and if they get an extra turn."""
    label = PLAYER_COLORS[current_player]["label"]
    color = PLAYER_COLORS[current_player]["bg"]

    if mode == "ai" and current_player == "player_2":
        label = "AI 🤖"

    if extra_turn:
        msg = f"✨ {label} gets an extra turn!"
    else:
        msg = f"⏳ {label}'s Turn"

    st.markdown(
        f'<div style="text-align:center;color:{color};font-family:Fredoka One,cursive;font-size:1.2rem;">{msg}</div>',
        unsafe_allow_html=True
    )


def render_roll_button(current_player, mode):
    """
    Renders the correct roll button based on mode and current player.
    Returns True if the button was clicked, False otherwise.
    """
    if mode == "ai" and current_player == "player_2":
        return st.button("👀  Watch AI Roll", use_container_width=True)
    else:
        label = PLAYER_COLORS[current_player]["label"]
        return st.button(f"🎲  Roll Dice — {label}", use_container_width=True)


def render_win_banner(winner, mode):
    """Renders the win message and play again button."""
    label = PLAYER_COLORS[winner]["label"]
    if mode == "ai" and winner == "player_2":
        label = "AI 🤖"

    st.markdown(f'<div class="win-banner">🏆 {label} Wins! 🏆</div>', unsafe_allow_html=True)
    return st.button("🔄  Play Again", use_container_width=True)


def render_log(log):
    """Renders the last 10 roll history entries."""
    if log:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**📜 Roll History**")
        for entry in log[:10]:
            st.markdown(f'<div class="log-entry">{entry}</div>', unsafe_allow_html=True)


def render_back_button():
    """Renders the back to menu button. Returns True if clicked."""
    st.markdown("<br>", unsafe_allow_html=True)
    return st.button("🏠  Back to Menu")