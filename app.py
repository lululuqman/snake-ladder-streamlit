import streamlit as st

# MUST BE FIRST COMMAND
st.set_page_config(page_title="Snake & Ladder", page_icon="🎲", layout="wide", initial_sidebar_state="expanded")

from constants import PLAYER_COLORS, DICE_FACES
from game_logic import roll_dice, move_player, check_extra_turn, get_initial_stats, update_stats, get_other_player
from ui import apply_styles, render_title, render_start_screen, render_game_dashboard

apply_styles()
render_title()

def init_state():
    defaults = {
        "game_started": False, "mode": None,
        "positions": {"player_1": 0, "player_2": 0},
        "current_player": "player_1", "game_over": False,
        "winner": None, "last_roll": None, "log": [],
        "stats": {"player_1": get_initial_stats(), "player_2": get_initial_stats()},
        "extra_turn": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_state()

def reset_game():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

def handle_turn(player):
    roll = roll_dice()
    st.session_state.last_roll = roll

    new_position, message, event = move_player(st.session_state.positions[player], roll)
    
    # Fun visual feedback for snakes and ladders
    if event == "snake":
        st.toast("Oh no! Bitten by a snake! 🐍")
    elif event == "ladder":
        st.toast("Climbing up! 🪜")

    st.session_state.positions[player] = new_position
    st.session_state.stats[player] = update_stats(st.session_state.stats[player], roll, event)

    # Sidebar log entry formatting
    emoji = PLAYER_COLORS[player]["emoji"]
    label = "AI" if st.session_state.mode == "ai" and player == "player_2" else PLAYER_COLORS[player]["label"]
    
    log_entry = f"{emoji} <b>{label}</b> rolled {DICE_FACES[roll]}<br><span style='font-size:0.75rem; color:#adb5bd;'>{message}</span>"
    st.session_state.log.insert(0, log_entry)

    if event == "win":
        st.session_state.game_over = True
        st.session_state.winner = player
        st.session_state.extra_turn = False
        st.balloons() # Celebrate!
        return

    if check_extra_turn(roll):
        st.session_state.extra_turn = True
        st.session_state.log.insert(0, f"✨ {emoji} <b>{label}</b> rolled a 6! Extra turn!")
    else:
        st.session_state.extra_turn = False
        st.session_state.current_player = get_other_player(player)

# ── Routing ──────────────────────────────────────────────────────────────
if not st.session_state.game_started:
    selected_mode = render_start_screen()
    if selected_mode:
        st.session_state.mode = selected_mode
        st.session_state.game_started = True
        st.rerun()
else:
    current = st.session_state.current_player
    
    roll_clicked, back_clicked = render_game_dashboard(
        positions=st.session_state.positions,
        stats=st.session_state.stats,
        mode=st.session_state.mode,
        current_player=current,
        extra_turn=st.session_state.extra_turn,
        last_roll=st.session_state.last_roll,
        log=st.session_state.log,
        game_over=st.session_state.game_over,
        winner=st.session_state.winner
    )
    
    # Actions
    if back_clicked:
        reset_game()
    elif roll_clicked:
        if st.session_state.game_over:
            reset_game() # Play again uses the same button
        else:
            handle_turn(current)
            st.rerun()