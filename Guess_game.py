import time
import random
import streamlit as st

# Setup dynamic responsive layout framework
st.set_page_config(page_title="Reflex Reaction Game", page_icon="⚡", layout="centered")

# Initialize real-time state engine parameters
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.high_score = 0
    st.session_state.speed = 1.0  # Falling velocity step multiplier
    st.session_state.obj_y = 0     # Falling item vertical position track
    st.session_state.obj_x = random.randint(1, 10) # Horizontal lane position
    st.session_state.game_over = False

def restart_arena():
    """Resets core tracking coordinates to spin a fresh game iteration."""
    if st.session_state.score > st.session_state.high_score:
        st.session_state.high_score = st.session_state.score
    st.session_state.score = 0
    st.session_state.speed = 1.0
    st.session_state.obj_y = 0
    st.session_state.obj_x = random.randint(1, 10)
    st.session_state.game_over = False

# Screen Graphic Header Layout
st.title("⚡ Reflex Catching Arena")
st.write("Slide your shield left and right to intercept the falling glitch object!")

# Live Dashboard Monitors
m1, m2, m3 = st.columns(3)
with m1:
    st.metric("Live Score", st.session_state.score)
with m2:
    st.metric("Top High Score", st.session_state.high_score)
with m3:
    st.metric("Velocity Multiplier", f"{st.session_state.speed:.1f}x")

st.write("---")

# Render The Visual Matrix grid viewport
grid_placeholder = st.empty()

# Interactive Mouse Interface Slider Control
player_x = st.slider(
    "🛡️ Move Your Shield Position:", 
    min_value=1, 
    max_value=10, 
    value=5, 
    step=1,
    disabled=st.session_state.game_over
)

# Active Falling Motion Loop Mechanics
if not st.session_state.game_over:
    # Increment downward movement
    st.session_state.obj_y += 1
    
    # Render the text matrix map frame inside placeholder channel
    matrix_output = ""
    for row in range(8):
        row_str = ""
        for col in range(1, 11):
            if row == st.session_state.obj_y and col == st.session_state.obj_x:
                row_str += "👾 "  # Falling Danger Item
            elif row == 7 and col == player_x:
                row_str += "🛡️ "  # Interactive Player Shield
            elif row == 7:
                row_str += "═ "   # Surface baseline limit indicator
            else:
                row_str += "░ "   # Deep Space Void tiles
        matrix_output += row_str + "\n"
        
    grid_placeholder.code(matrix_output, language="text")

    # Evaluation conditions at Ground Level (Row 7)
    if st.session_state.obj_y == 7:
        if st.session_state.obj_x == player_x:
            # Catch event resolution pathway
            st.session_state.score += 1
            st.session_state.speed += 0.3  # Escalate falling velocity difficulty
            st.session_state.obj_y = 0     # Spawn new object back at top
            st.session_state.obj_x = random.randint(1, 10)
            st.toast("⚡ Clean Intercept!", icon="🎯")
        else:
            # Miss event resolution pathway
            st.session_state.game_over = True
            st.toast("💥 Perimeter Breached!", icon="❌")
        st.rerun()
    else:
        # Pause execution to simulate visual game loop frames dynamically
        sleep_duration = max(0.05, 0.4 / st.session_state.speed)
        time.sleep(sleep_duration)
        st.rerun()

else:
    # Resolution Overlay Screen Display UI Block
    st.error(f"💀 System Compromised! The glitch slipped through. Final Score: {st.session_state.score}")
    if st.button("🔄 Initialize Counter-Measures (Restart)", use_container_width=True):
        restart_arena()
        st.rerun()
