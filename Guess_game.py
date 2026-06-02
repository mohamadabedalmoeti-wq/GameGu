import time
import random
import streamlit as st

# Setup page style framework
st.set_page_config(page_title="Reflex Catching Arena", page_icon="⚡", layout="centered")

# Initialize persistent tracking variables safely
if "score" not in st.session_state:
    st.session_state.score = 0
if "high_score" not in st.session_state:
    st.session_state.high_score = 0
if "obj_y" not in st.session_state:
    st.session_state.obj_y = 0
if "obj_x" not in st.session_state:
    st.session_state.obj_x = random.randint(1, 10)
if "game_over" not in st.session_state:
    st.session_state.game_over = False

def restart_arena():
    """Wipes coordinate tracking to spin a fresh game iteration."""
    if st.session_state.score > st.session_state.high_score:
        st.session_state.high_score = st.session_state.score
    st.session_state.score = 0
    st.session_state.obj_y = 0
    st.session_state.obj_x = random.randint(1, 10)
    st.session_state.game_over = False

# Layout Header
st.title("⚡ Reflex Catching Arena")
st.write("Slide your shield left and right to intercept the falling glitch object!")

# Engine Speed Selector - Choose your starting pace
speed_choice = st.radio(
    "⚙️ Select Game Speed Pace:",
    options=["🐢 Slow", "🎮 Normal", "🔥 Fast"],
    index=1,
    horizontal=True,
    disabled=st.session_state.game_over
)

# Convert selector text to actual delay seconds
if "Slow" in speed_choice:
    loop_delay = 0.5   # 2 frames per second
elif "Normal" in speed_choice:
    loop_delay = 0.3 # 3.3 frames per second
else:
    loop_delay = 0.1   # 10 frames per second (Original hyper speed)

# Live Score Dashboard Layout Monitors
m1, m2 = st.columns(2)
with m1:
    st.metric("Live Score", st.session_state.score)
with m2:
    st.metric("Top High Score", st.session_state.high_score)

st.write("---")

# Interactive Mouse Interface Slider Control
player_x = st.slider(
    "🛡️ Move Your Shield Position:", 
    min_value=1, 
    max_value=10, 
    value=5, 
    step=1,
    disabled=st.session_state.game_over
)

# Isolate the visualization inside a self-contained automatic fragment engine loop
@st.fragment(run_every=loop_delay)
def run_game_engine(shield_pos):
    """Executes background layout processing without getting frozen by slider changes."""
    if st.session_state.game_over:
        return

    # Advance falling motion downwards
    st.session_state.obj_y += 1
    
    # Construct the graphic text frame layout view matrix (Increased row count to 10 for more reaction time)
    matrix_output = ""
    for row in range(10):
        row_str = ""
        for col in range(1, 11):
            if row == st.session_state.obj_y and col == st.session_state.obj_x:
                row_str += "👾 "  # Falling Glitch Target
            elif row == 9 and col == shield_pos:
                row_str += "🛡️ "  # Live User Shield Position
            elif row == 9:
                row_str += "═ "   # Surface platform bound line
            else:
                row_str += "░ "   # Void empty screen panels
        matrix_output += row_str + "\n"

    # Print the calculated matrix directly on screen inside a clean code box container
    st.code(matrix_output, language="text")

    # Game logic validation checks at the bottom drop point (Row 9)
    if st.session_state.obj_y >= 9:
        if st.session_state.obj_x == shield_pos:
            # Catch Success Route
            st.session_state.score += 1
            st.session_state.obj_y = 0
            st.session_state.obj_x = random.randint(1, 10)
            st.toast("🎯 Intercept Clean!", icon="⚡")
            st.rerun()
        else:
            # Failure Collision Route
            st.session_state.game_over = True
            st.toast("💥 Perimeter Breached!", icon="❌")
            st.rerun()

# Run our active graphics container framework instantly
if not st.session_state.game_over:
    run_game_engine(player_x)
else:
    # Game Over Layout Overlay Banner Block
    st.error(f"💀 System Compromised! The glitch slipped through. Final Score: {st.session_state.score}")
    if st.button("🔄 Initialize Counter-Measures (Restart)", use_container_width=True):
        restart_arena()
        st.rerun()
