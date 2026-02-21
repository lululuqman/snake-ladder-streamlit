import streamlit as st

from constants import PLAYER_COLORS, DICE_FACES
from game_logic import (
    roll_dice,
    move_player,
    check_extra_turn,
    get_initial_stats,
    update_stats,
    get_other_player,
)
from ui import (
    apply_styles,
    render_title,
    render_start_screen,
    render_player_stats,
    render_board,
    render_dice,
    render_turn_indicator,
    render_roll_button,
    render_win_banner,
    render_log,
    render_back_button,
)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Snake & Ladder", page_icon="🎲", layout="centered")

apply_styles()
render_title()


# ── Session state init ────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "game_started": False,
        "mode": None,
        "positions": {"player_1": 0, "player_2": 0},
        "current_player": "player_1",
        "game_over": False,
        "winner": None,
        "last_roll": None,
        "log": [],
        "stats": {
            "player_1": get_initial_stats(),
            "player_2": get_initial_stats(),
        },
        "extra_turn": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_state()


# ── Reset helper ──────────────────────────────────────────────────────────────
def reset_game():
    """Clears all session state to return to a fresh start."""
    keys = [
        "game_started", "mode", "positions", "current_player",
        "game_over", "winner", "last_roll", "log", "stats", "extra_turn"
    ]
    for key in keys:
        del st.session_state[key]
    st.rerun()


# ── Core turn handler ─────────────────────────────────────────────────────────
def handle_turn(player):
    """
    Runs a full turn for the given player:
    1. Rolls dice
    2. Moves player
    3. Updates stats
    4. Logs the event
    5. Checks for extra turn or switches player
    """
    roll = roll_dice()
    st.session_state.last_roll = roll

    new_position, message, event = move_player(
        st.session_state.positions[player], roll
    )

    st.session_state.positions[player] = new_position
    st.session_state.stats[player] = update_stats(
        st.session_state.stats[player], roll, event
    )

    # Build log entry
    emoji = PLAYER_COLORS[player]["emoji"]
    label = PLAYER_COLORS[player]["label"]
    if st.session_state.mode == "ai" and player == "player_2":
        label = "AI 🤖"

    log_entry = f"{emoji} **{label}** rolled {DICE_FACES[roll]} ({roll}) — {message}"
    st.session_state.log.insert(0, log_entry)

    # Check win
    if event == "win":
        st.session_state.game_over = True
        st.session_state.winner = player
        st.session_state.extra_turn = False
        return

    # Check extra turn
    if check_extra_turn(roll):
        st.session_state.extra_turn = True
        st.session_state.log.insert(0, f"{emoji} **{label}** rolled 6 — Extra turn!")
    else:
        st.session_state.extra_turn = False
        st.session_state.current_player = get_other_player(player)


# ── Start screen ──────────────────────────────────────────────────────────────
if not st.session_state.game_started:
    selected_mode = render_start_screen()
    if selected_mode:
        st.session_state.mode = selected_mode
        st.session_state.game_started = True
        st.rerun()


# ── Game screen ───────────────────────────────────────────────────────────────
else:
    current = st.session_state.current_player

    render_player_stats(
        st.session_state.positions,
        st.session_state.stats,
        st.session_state.mode
    )

    render_board(st.session_state.positions)
    st.markdown("<br>", unsafe_allow_html=True)

    # Win state
    if st.session_state.game_over:
        play_again = render_win_banner(st.session_state.winner, st.session_state.mode)
        if play_again:
            reset_game()

    # Active game
    else:
        render_turn_indicator(current, st.session_state.extra_turn, st.session_state.mode)
        render_dice(st.session_state.last_roll)

        if render_roll_button(current, st.session_state.mode):
            handle_turn(current)
            st.rerun()

    render_log(st.session_state.log)

    if render_back_button():
        reset_game()