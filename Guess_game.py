import random
import streamlit as st
import streamlit.components.v1 as components

# Setup page layout
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
if "shield_x" not in st.session_state:
    st.session_state.shield_x = 5  # Player start position
if "game_over" not in st.session_state:
    st.session_state.game_over = False

def restart_arena():
    """Wipes tracking positions to spin a fresh game round."""
    if st.session_state.score > st.session_state.high_score:
        st.session_state.high_score = st.session_state.score
    st.session_state.score = 0
    st.session_state.obj_y = 0
    st.session_state.obj_x = random.randint(1, 10)
    st.session_state.shield_x = 5
    st.session_state.game_over = False

# Layout Header Graphic Block
st.title("⚡ Reflex Catching Arena")
st.write("Use your **⬅️ Left Arrow** and **➡️ Right Arrow** keys on your keyboard to slide your shield!")

# Game Speed Selection Configuration Block
speed_choice = st.radio(
    "⚙️ Select Game Speed Pace:",
    options=["🐢 Slow", "🎮 Normal", "🔥 Fast"],
    index=1,
    horizontal=True,
    disabled=st.session_state.game_over
)

if "Slow" in speed_choice:
    loop_delay = 0.15
elif "Normal" in speed_choice:
    loop_delay = 0.13
else:
    loop_delay = 0.11

# Live Dashboard Layout Monitors
m1, m2 = st.columns(2)
with m1:
    st.metric("Live Score", st.session_state.score)
with m2:
    st.metric("Top High Score", st.session_state.high_score)

st.write("---")

# Invisible interface controls triggered directly by our JavaScript script
col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    move_left = st.button("⬅️ Left", use_container_width=True, disabled=st.session_state.game_over)
with col_btn2:
    move_right = st.button("Right ➡️", use_container_width=True, disabled=st.session_state.game_over)

# Adjust coordinates based on inputs
if move_left and st.session_state.shield_x > 1:
    st.session_state.shield_x -= 1
if move_right and st.session_state.shield_x < 10:
    st.session_state.shield_x += 1

# --- JAVASCRIPT KEYBOARD LISTENER CODES ---
# This snippet listens to window keyboard events and virtually clicks the buttons above
js_keyboard_listener = """
<script>
    const doc = window.parent.document;
    doc.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowLeft') {
            const btnLeft = Array.from(doc.querySelectorAll('button')).find(el => el.textContent.includes('⬅️ Left'));
            if (btnLeft) btnLeft.click();
        } else if (e.key === 'ArrowRight') {
            const btnRight = Array.from(doc.querySelectorAll('button')).find(el => el.textContent.includes('Right ➡️'));
            if (btnRight) btnRight.click();
        }
    });
</script>
"""
components.html(js_keyboard_listener, height=0, width=0)

# Isolate the visualization inside a self-contained automatic fragment engine loop
@st.fragment(run_every=loop_delay)
def run_game_engine():
    """Executes background layout processing without freezing during control inputs."""
    if st.session_state.game_over:
        return

    # Advance falling motion downwards
    st.session_state.obj_y += 1
    current_shield = st.session_state.shield_x
    
    # Construct the graphic text frame view matrix
    matrix_output = ""
    for row in range(10):
        row_str = ""
        for col in range(1, 11):
            if row == st.session_state.obj_y and col == st.session_state.obj_x:
                row_str += "👾 "  # Falling Target
            elif row == 9 and col == current_shield:
                row_str += "🛡️ "  # User Shield
            elif row == 9:
                row_str += "═ "   # Surface deck limit
            else:
                row_str += "░ "   # Grid cells
        matrix_output += row_str + "\n"

    st.code(matrix_output, language="text")

    # Target collision check resolutions at base level
    if st.session_state.obj_y >= 9:
        if st.session_state.obj_x == current_shield:
            st.session_state.score += 1
            st.session_state.obj_y = 0
            st.session_state.obj_x = random.randint(1, 10)
            st.toast("🎯 Intercept Clean!", icon="⚡")
            st.rerun()
        else:
            st.session_state.game_over = True
            st.toast("💥 Perimeter Breached!", icon="❌")
            st.rerun()

# Run game processing engine
if not st.session_state.game_over:
    run_game_engine()
else:
    st.error(f"💀 System Compromised! The glitch slipped through. Final Score: {st.session_state.score}")
    if st.button("🔄 Initialize Counter-Measures (Restart)", use_container_width=True):
        restart_arena()
        st.rerun()
