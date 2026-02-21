import streamlit as st
from constants import SNAKES, LADDERS, PLAYER_COLORS, DICE_FACES

def apply_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@400;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }
    h1, h2, h3 { font-family: 'Fredoka One', cursive; }
    .stApp {
        background: linear-gradient(135deg, #FFD8DF 0%, #F0FFDF 50%, #A8DF8E 100%);
        min-height: 100vh;
    }

    /* Compact Typography */
    .game-title {
        font-family: 'Fredoka One', cursive;
        font-size: 2.2rem;
        text-align: center;
        background: linear-gradient(90deg, #f72585, #7209b7, #4cc9f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .game-subtitle {
        text-align: center; color: #adb5bd; font-size: 0.9rem;
        margin-top: 0; margin-bottom: 1rem;
    }

    /* Compact Cards & Board */
    .info-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px; padding: 0.5rem 1rem;
        margin-bottom: 0.5rem; backdrop-filter: blur(10px);
    }
    .board-cell {
        display: inline-flex; align-items: center; justify-content: center;
        width: 42px; height: 42px; border-radius: 8px;
        font-family: 'Fredoka One', cursive; font-size: 0.8rem;
        margin: 2px; position: relative;
    }
    .board-wrapper {
        background: rgba(255,255,255,0.04); border-radius: 16px;
        padding: 0.5rem; border: 1px solid rgba(255,255,255,0.08);
        display: inline-block; width: 100%; text-align: center;
    }
    
    /* Dice & Log */
    .dice-display {
        font-size: 4rem; text-align: center; animation: bounce 0.4s ease;
        line-height: 1; margin: 0;
    }
    @keyframes bounce {
        0%   { transform: scale(0.5) rotate(-10deg); opacity: 0; }
        60%  { transform: scale(1.2) rotate(5deg); }
        100% { transform: scale(1) rotate(0deg); opacity: 1; }
    }
    .win-banner {
        font-family: 'Fredoka One', cursive; font-size: 1.8rem;
        text-align: center; background: linear-gradient(90deg, #f72585, #ffd60a);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        padding: 0.5rem; animation: bounce 0.6s ease;
    }
    .log-entry {
        font-size: 0.8rem; color: #ced4da; padding: 4px 0;
        border-bottom: 1px solid rgba(255,255,255,0.05); line-height: 1.2;
    }

    /* Buttons */
    .stButton > button {
        font-family: 'Fredoka One', cursive; font-size: 1rem;
        border-radius: 10px; padding: 0.25rem 1rem;
        border: none; transition: all 0.2s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(247, 37, 133, 0.4);
    }
    .stRadio > label { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

def render_title():
    st.markdown('<p class="game-title">🐍 Snake & Ladder 🪜</p>', unsafe_allow_html=True)
    st.markdown('<p class="game-subtitle">50-square edition · No Scrolling Required!</p>', unsafe_allow_html=True)

def render_start_screen():
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### Choose Game Mode")
        mode = st.radio("", ["🤖  Player vs AI", "👥  Player vs Player"], label_visibility="collapsed")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🎲  Start Game!", use_container_width=True):
            return "ai" if "AI" in mode else "pvp"
    return None

def render_player_stats(positions, stats, mode):
    p2_label = "AI 🤖" if mode == "ai" else "Player 2"
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f'<div class="info-card" style="border-color:#f72585;">'
            f'<span style="color:#f72585;font-family:Fredoka One;font-size:1rem;">🔴 Player 1</span><br>'
            f'<span style="font-size:1.5rem;font-weight:bold;color:white;">Sq {positions["player_1"]}</span><br>'
            f'<span style="color:#adb5bd;font-size:0.75rem;">'
            f'Turns: {len(stats["player_1"]["rolls"])} | 🐍 {stats["player_1"]["snakes_hit"]} | 🪜 {stats["player_1"]["ladders_climbed"]}</span>'
            f'</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(
            f'<div class="info-card" style="border-color:#4cc9f0;">'
            f'<span style="color:#4cc9f0;font-family:Fredoka One;font-size:1rem;">🔵 {p2_label}</span><br>'
            f'<span style="font-size:1.5rem;font-weight:bold;color:white;">Sq {positions["player_2"]}</span><br>'
            f'<span style="color:#adb5bd;font-size:0.75rem;">'
            f'Turns: {len(stats["player_2"]["rolls"])} | 🐍 {stats["player_2"]["snakes_hit"]} | 🪜 {stats["player_2"]["ladders_climbed"]}</span>'
            f'</div>', unsafe_allow_html=True)

def render_board(positions):
    p1_pos = positions["player_1"]
    p2_pos = positions["player_2"]
    rows = []
    for row in range(4, -1, -1):
        cells = []
        for col in range(10):
            square = row * 10 + col + 1 if row % 2 == 0 else row * 10 + (9 - col) + 1
            bg = "rgba(247,37,133,0.25)" if square in SNAKES else "rgba(76,201,240,0.25)" if square in LADDERS else "rgba(255,255,255,0.06)"
            border = "1px solid #f72585" if square in SNAKES else "1px solid #4cc9f0" if square in LADDERS else "1px solid rgba(255,255,255,0.1)"
            
            tokens = ("🔴" if p1_pos == square else "") + ("🔵" if p2_pos == square else "")
            icon = "🐍" if not tokens and square in SNAKES else "🪜" if not tokens and square in LADDERS else ""
            
            cell_html = (
                f'<div class="board-cell" style="background:{bg};border:{border};">'
                f'<div style="font-size:0.55rem;color:#adb5bd;position:absolute;top:2px;left:4px;">{square}</div>'
                f'<div style="font-size:0.9rem;margin-top:6px;">{tokens if tokens else icon}</div>'
                f'</div>'
            )
            cells.append(cell_html)
        rows.append("".join(cells))

    board_html = '<div class="board-wrapper">' + "".join(f'<div style="display:flex;justify-content:center;">{r}</div>' for r in rows) + "</div>"
    st.markdown(board_html, unsafe_allow_html=True)

def render_sidebar_elements(log):
    st.sidebar.markdown("**🗺️ Board Legend**")
    st.sidebar.markdown("🐍 **Red** = Snakes &nbsp;|&nbsp; 🪜 **Blue** = Ladders<br>🔴 Player 1 &nbsp;|&nbsp; 🔵 P2/AI", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
    if log:
        st.sidebar.markdown("**📜 Roll History**")
        log_container = st.sidebar.container(height=300, border=False)
        for entry in log[:15]:
            log_container.markdown(f'<div class="log-entry">{entry}</div>', unsafe_allow_html=True)
            
    st.sidebar.markdown("---")
    return st.sidebar.button("🏠 Back to Menu", use_container_width=True)

def render_game_dashboard(positions, stats, mode, current_player, extra_turn, last_roll, log, game_over, winner):
    """The main 2-column orchestrator."""
    col_board, col_controls = st.columns([2, 1], gap="large")
    
    with col_board:
        render_player_stats(positions, stats, mode)
        render_board(positions)
        
    with col_controls:
        st.markdown("<br>", unsafe_allow_html=True) # Spacer
        
        # Turn indicator
        label = "AI 🤖" if mode == "ai" and current_player == "player_2" else PLAYER_COLORS[current_player]["label"]
        color = PLAYER_COLORS[current_player]["bg"]
        msg = f"✨ {label} gets an extra turn!" if extra_turn else f"⏳ {label}'s Turn"
        
        if not game_over:
            st.markdown(f'<div style="text-align:center;color:{color};font-family:Fredoka One;font-size:1.1rem;">{msg}</div>', unsafe_allow_html=True)
        
        # Dice container
        dice_container = st.container(height=120, border=False)
        with dice_container:
            if last_roll:
                st.markdown(f'<div class="dice-display">{DICE_FACES[last_roll]}</div>', unsafe_allow_html=True)
        
        # Actions
        roll_clicked = False
        if game_over:
            win_label = "AI 🤖" if mode == "ai" and winner == "player_2" else PLAYER_COLORS[winner]["label"]
            st.markdown(f'<div class="win-banner">🏆 {win_label} Wins!</div>', unsafe_allow_html=True)
            roll_clicked = st.button("🔄 Play Again", use_container_width=True)
        else:
            btn_label = "👀 Watch AI Roll" if mode == "ai" and current_player == "player_2" else f"🎲 Roll Dice — {label}"
            roll_clicked = st.button(btn_label, use_container_width=True)

    back_clicked = render_sidebar_elements(log)
    return roll_clicked, back_clicked