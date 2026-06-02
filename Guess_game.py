import random
import streamlit as st
import streamlit.components.v1 as components

# Setup page layout configuration
st.set_page_config(page_title="Cyber Catching Arena", page_icon="⚡", layout="centered")

# --- INJECT CYBERPUNK ARCADE SKIN THEME CSS ---
st.markdown("""
    <style>
        /* General Canvas Layout styling */
        .stApp {
            background-color: #0d0f1d !important;
            color: #00ffcc !important;
            font-family: 'Courier New', Courier, monospace !important;
        }
        /* Style the matrix display box frame container */
        code {
            color: #ff007f !important;
            background-color: #05060b !important;
            border: 2px solid #00ffcc !important;
            border-radius: 8px !important;
            font-size: 1.4rem !important;
            line-height: 1.3 !important;
            text-shadow: 0 0 8px #ff007f, 0 0 2px #00ffcc;
            display: block;
            padding: 15px !important;
        }
        /* Custom Metric Dashboard layout wrappers styling */
        [data-testid="stMetricValue"] {
            color: #00ffcc !important;
            font-size: 2.2rem !important;
            text-shadow: 0 0 10px #00ffcc;
        }
        [data-testid="stMetricLabel"] {
            color: #8b9bb4 !important;
        }
        /* Main Headings */
        h1, h3 {
            color: #ff007f !important;
            text-shadow: 0 0 15px #ff007f, 0 0 2px #ffffff;
            text-align: center;
        }
    </style>
""", unsafe_with_html_context=True)

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
    st.session_state.shield_x = 5  
if "game_state" not in st.session_state:
    st.session_state.game_state = "LOBBY"  # Valid states: LOBBY, RUNNING, PAUSED, GAME_OVER

# State Machine Control Handlers
def trigger_start():
    st.session_state.game_state = "RUNNING"

def trigger_pause():
    st.session_state.game_state = "PAUSED"

def trigger_stop():
    st.session_state.game_state = "GAME_OVER"

def trigger_restart():
    if st.session_state.score > st.session_state.high_score:
        st.session_state.high_score = st.session_state.score
    st.session_state.score = 0
    st.session_state.obj_y = 0
    st.session_state.obj_x = random.randint(1, 10)
    st.session_state.shield_x = 5
    st.session_state.game_state = "RUNNING"

# Layout Header Graphic Block
st.title("⚡ CYBER CATCHING ARENA")
st.write("<div style='text-align: center; color: #8b9bb4;'>Control with your <b>⬅️ Left Arrow</b> and <b>➡️ Right Arrow</b> keyboard keys!</div>", unsafe_with_html_context=True)
st.write("---")

# --- MASTER CONTROL HUB (Top Navigation Console) ---
c1, c2, c3 = st.columns(3)
with c1:
    if st.session_state.game_state in ["LOBBY", "PAUSED"]:
        st.button("▶️ Start / Resume", type="primary", use_container_width=True, on_click=trigger_start)
    else:
        st.button("⏸️ Pause Engine", use_container_width=True, on_click=trigger_pause, disabled=(st.session_state.game_state == "GAME_OVER"))
with c2:
    st.button("⏹️ Emergency Stop", type="secondary", use_container_width=True, on_click=trigger_stop, disabled=(st.session_state.game_state in ["LOBBY", "GAME_OVER"]))
with c3:
    st.button("🔄 Full Reset", use_container_width=True, on_click=trigger_restart)

# Interactive Velocity Modifier
loop_delay = st.slider(
    "⚙️ Adjust Hardware Refresh Interval (Seconds per step):",
    min_value=0.05, max_value=1.00, value=0.30, step=0.05,
    disabled=(st.session_state.game_state != "RUNNING")
)

# Score Monitors Dashboard
m1, m2 = st.columns(2)
with m1:
    st.metric("Live Collected Score", st.session_state.score)
with m2:
    st.metric("All-Time System High Score", st.session_state.high_score)

st.write("---")

# Invisible system interface controls mapped to JavaScript framework hooks
col_b1, col_b2 = st.columns(2)
with col_b1:
    move_left = st.button("⬅️ Left", use_container_width=True, disabled=(st.session_state.game_state != "RUNNING"), key="hidden_l")
with col_b2:
    move_right = st.button("Right ➡️", use_container_width=True, disabled=(st.session_state.game_state != "RUNNING"), key="hidden_r")

# Adjust coordinates dynamically 
if move_left and st.session_state.shield_x > 1:
    st.session_state.shield_x -= 1
if move_right and st.session_state.shield_x < 10:
    st.session_state.shield_x += 1

# --- JAVASCRIPT KEYBOARD EVENT HANDLERS ---
js_keyboard_listener = """
<script>
    const doc = window.parent.document;
    doc.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowLeft') {
            const btnLeft = Array.from(doc.querySelectorAll('button')).find(el => el.textContent.includes('⬅️ Left'));
            if (btnLeft && !btnLeft.disabled) btnLeft.click();
        } else if (e.key === 'ArrowRight') {
            const btnRight = Array.from(doc.querySelectorAll('button')).find(el => el.textContent.includes('Right ➡️'));
            if (btnRight && !btnRight.disabled) btnRight.click();
        }
    });
</script>
"""
components.html(js_keyboard_listener, height=0, width=0)

# --- ISOLATED GRAPHICS VISUALIZATION LAYER ---
@st.fragment(run_every=loop_delay)
def run_game_engine():
    """Renders visual layout maps dynamically without locking browser input interfaces."""
    # Handle frozen screens during Pause or Stop modes
    if st.session_state.game_state != "RUNNING":
        return

    # Increment object falling velocity coordinates
    st.session_state.obj_y += 1
    current_shield = st.session_state.shield_x
    
    # Construct the screen grid map 
    matrix_output = ""
    for row in range(10):
        row_str = ""
        for col in range(1, 11):
            if row == st.session_state.obj_y and col == st.session_state.obj_x:
                row_str += "👾 "  # Falling Target
            elif row == 9 and col == current_shield:
                row_str += "🛡️ "  # User Shield
            elif row == 9:
                row_str += "═ "   # Surface baseline limit
            else:
                row_str += "░ "   # Grid cell blocks
        matrix_output += row_str + "\n"

    st.code(matrix_output, language="text")

    # Target collision check paths at Row 9
    if st.session_state.obj_y >= 9:
        if st.session_state.obj_x == current_shield:
            st.session_state.score += 1
            st.session_state.obj_y = 0
            st.session_state.obj_x = random.randint(1, 10)
            st.toast("🎯 Intercept Clean!", icon="⚡")
            st.rerun()
        else:
            st.session_state.game_state = "GAME_OVER"
            st.toast("💥 System Compromised!", icon="❌")
            st.rerun()

# --- CONSOLE CONDITION VIEW PORTS ---
if st.session_state.game_state == "LOBBY":
    st.info("🎮 MAIN SYSTEM ONLINE: Click the 'Start / Resume' button above to initialize the falling threat matrix!")
elif st.session_state.game_state == "PAUSED":
    st.warning("⏸️ GAME ENGINE PAUSED: The grid state is frozen. Tap 'Start / Resume' to continue tracking.")
elif st.session_state.game_state == "GAME_OVER":
    st.error(f"💀 GAME OVER: Perimeter breached! Final Score reached: {st.session_state.score}")
    if st.button("🚀 Re-Initialize Core Systems (Play Again)", use_container_width=True):
        trigger_restart()
        st.rerun()
else:
    # Run the continuous looping engine layout when explicitly marked RUNNING
    run_game_engine()
