import random
import streamlit as st
import streamlit.components.v1 as components

# Setup fluid responsive layout framework
st.set_page_config(page_title="Reflex Catching Arena", page_icon="🎮", layout="centered")

# --- INJECT MODERN 3D SKEUOMORPHIC UI CSS ---
st.markdown("""
    <style>
        /* Modern bright background with soft gradient */
        .stApp {
            background: linear-gradient(135deg, #eef2f7 0%, #d9e2ec 100%) !important;
            color: #334e68 !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        }
        
        /* Clean matrix display card container with soft 3D shadow */
        code {
            color: #102a43 !important;
            background-color: #f0f4f8 !important;
            border: 1px solid #bcccdc !important;
            border-radius: 16px !important;
            font-size: 1.5rem !important;
            line-height: 1.4 !important;
            letter-spacing: 2px;
            display: block;
            padding: 20px !important;
            box-shadow: inset 3px 3px 6px #d9e2ec, inset -3px -3px 6px #ffffff,
                        4px 4px 12px rgba(0, 0, 0, 0.05);
            text-align: center;
        }
        
        /* 3D Skeuomorphic Button Styling */
        div.stButton > button {
            background: linear-gradient(180deg, #ffffff 0%, #f0f4f8 100%) !important;
            color: #243b53 !important;
            border: 1px solid #bcccdc !important;
            border-radius: 12px !important;
            padding: 12px 24px !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
            box-shadow: 0 5px 0 #9fb3c8, 0 8px 12px rgba(0, 0, 0, 0.15) !important;
            transition: all 0.1s ease !important;
        }
        
        /* Interactive button click compression animation */
        div.stButton > button:active {
            box-shadow: 0 1px 0 #9fb3c8, 0 2px 4px rgba(0, 0, 0, 0.1) !important;
            transform: translateY(4px) !important;
        }
        
        /* Specific accent coloring for the Primary Start button */
        div.stButton > button[data-testid="baseButton-primary"] {
            background: linear-gradient(180deg, #4776e6 0%, #8e54e9 100%) !important;
            color: #ffffff !important;
            border: none !important;
            box-shadow: 0 5px 0 #3a60b9, 0 8px 12px rgba(71, 118, 230, 0.3) !important;
        }
        div.stButton > button[data-testid="baseButton-primary"]:active {
            box-shadow: 0 1px 0 #3a60b9, 0 2px 4px rgba(71, 118, 230, 0.2) !important;
            transform: translateY(4px) !important;
        }

        /* Title styling adjustment */
        h1 {
            color: #102a43 !important;
            font-weight: 800 !important;
            text-align: center;
            letter-spacing: -1px;
        }
    </style>
""", unsafe_allow_html=True)

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
    st.session_state.game_state = "LOBBY"
if "loop_delay" not in st.session_state:
    st.session_state.loop_delay = 0.30

# Layout Header Block
st.title("🎮 Reflex Catching Arena")
st.write("<div style='text-align: center; color: #486581; font-weight: 500;'>Press your keyboard <b>⬅️ Left Arrow</b> and <b>➡️ Right Arrow</b> keys to play!</div>", unsafe_allow_html=True)
st.write("---")

# Dashboard speed slider configuration
st.session_state.loop_delay = st.slider(
    "⚙️ Adjust Game Loop Speed (Refresh Interval):",
    min_value=0.05, max_value=1.00, value=st.session_state.loop_delay, step=0.05,
    disabled=(st.session_state.game_state == "RUNNING") # Speed can only be changed before starting or while paused
)

# Score Monitors Dashboard Panel
m1, m2 = st.columns(2)
with m1:
    st.metric("Live Score", st.session_state.score)
with m2:
    st.metric("High Score", st.session_state.high_score)

st.write("---")

# Invisible interface controls mapped to JavaScript hook indicators
col_b1, col_b2 = st.columns(2)
with col_b1:
    move_left = st.button("⬅️ Left", use_container_width=True, disabled=(st.session_state.game_state != "RUNNING"), key="hidden_l")
with col_b2:
    move_right = st.button("Right ➡️", use_container_width=True, disabled=(st.session_state.game_state != "RUNNING"), key="hidden_r")

# Adjust coordinates dynamically based on inputs
if move_left and st.session_state.shield_x > 1:
    st.session_state.shield_x -= 1
if move_right and st.session_state.shield_x < 10:
    st.session_state.shield_x += 1

# --- JAVASCRIPT KEYBOARD LISTENER ---
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

# --- ISOLATED CORE ENGINE CONTAINER ---
# FIX: Wrapping everything inside the same refresh fragment stops button lag
@st.fragment(run_every=st.session_state.loop_delay)
def run_game_engine():
    # --- MASTER CONTROL HUB (3D Console Buttons inside fragment) ---
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.session_state.game_state in ["LOBBY", "PAUSED"]:
            if st.button("▶️ Start Game", type="primary", use_container_width=True, key="frag_start"):
                st.session_state.game_state = "RUNNING"
                st.rerun()
        else:
            if st.button("⏸️ Pause", use_container_width=True, key="frag_pause"):
                st.session_state.game_state = "PAUSED"
                st.rerun()
    with c2:
        if st.button("⏹️ Stop", use_container_width=True, key="frag_stop", disabled=(st.session_state.game_state in ["LOBBY", "GAME_OVER"])):
            st.session_state.game_state = "GAME_OVER"
            st.rerun()
    with c3:
        if st.button("🔄 Reset", use_container_width=True, key="frag_reset"):
            if st.session_state.score > st.session_state.high_score:
                st.session_state.high_score = st.session_state.score
            st.session_state.score = 0
            st.session_state.obj_y = 0
            st.session_state.obj_x = random.randint(1, 10)
            st.session_state.shield_x = 5
            st.session_state.game_state = "LOBBY"
            st.rerun()

    st.write("")

    # --- STATE RENDERING LOGIC ---
    if st.session_state.game_state == "LOBBY":
        st.info("💡 Ready to play? Press the shiny blue '▶️ Start Game' button above to drop the threat matrix!")
        return
    elif st.session_state.game_state == "PAUSED":
        st.warning("⏸️ Game engine frozen. Click '▶️ Start Game' to unpause and resume your session.")
        return
    elif st.session_state.game_state == "GAME_OVER":
        st.error(f"💀 Game Over! The glitch breached your security layer. Final Score: {st.session_state.score}")
        return

    # --- RUNNING GAME ITERATION ---
    st.session_state.obj_y += 1
    current_shield = st.session_state.shield_x
    
    # Construct the screen grid map 
    matrix_output = ""
    for row in range(10):
        row_str = ""
        for col in range(1, 11):
            if row == st.session_state.obj_y and col == st.session_state.obj_x:
                row_str += "👾 "  
            elif row == 9 and col == current_shield:
                row_str += "🛡️ "  
            elif row == 9:
                row_str += "═ "   
            else:
                row_str += "⚪ "  
        matrix_output += row_str + "\n"

    st.code(matrix_output, language="text")

    # Target collision check paths at bottom floor level
    if st.session_state.obj_y >= 9:
        if st.session_state.obj_x == current_shield:
            st.session_state.score += 1
            st.session_state.obj_y = 0
            st.session_state.obj_x = random.randint(1, 10)
            st.toast("🎯 Intercept Clean!", icon="⚡")
            st.rerun()
        else:
            if st.session_state.score > st.session_state.high_score:
                st.session_state.high_score = st.session_state.score
            st.session_state.game_state = "GAME_OVER"
            st.toast("💥 Perimeter Breached!", icon="❌")
            st.rerun()

# Run continuous rendering thread loop dynamically
run_game_engine()
