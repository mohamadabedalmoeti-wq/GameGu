import random
import streamlit as st

# Set up page styling and tab title
st.set_page_config(page_title="Number Guessing Game", page_icon="🎯", layout="centered")

# Initialize session state variables to store game data across browser refreshes
if "secret_number" not in st.session_state:
    st.session_state.secret_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.max_attempts = 10
    st.session_state.score = 100
    st.session_state.game_over = False
    st.session_state.feedback = "Enter a number below and click Guess!"
    st.session_state.feedback_type = "info" # info, success, warning, error

def reset_game():
    """Resets all backend variables for a brand new game round."""
    st.session_state.secret_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.score = 100
    st.session_state.game_over = False
    st.session_state.feedback = "Game restarted! Good luck!"
    st.session_state.feedback_type = "info"

# Application Visual Layout Header
st.title("🎯 Number Guessing Game")
st.write("I'm thinking of a number between 1 and 100. Can you guess it?")

# Live Stats Dashboard Panel
col1, col2 = st.columns(2)
with col1:
    attempts_left = st.session_state.max_attempts - st.session_state.attempts
    st.metric(label="Attempts Remaining", value=attempts_left)
with col2:
    st.metric(label="Current Score", value=st.session_state.score)

# Render Dynamic Alerts Framework
if st.session_state.feedback_type == "success":
    st.success(st.session_state.feedback)
elif st.session_state.feedback_type == "warning":
    st.warning(st.session_state.feedback)
elif st.session_state.feedback_type == "error":
    st.error(st.session_state.feedback)
else:
    st.info(st.session_state.feedback)

# User Interactive Form Frame
with st.form(key="guess_form", clear_on_submit=True):
    user_guess = st.number_input(
        "Enter your guess (1-100):", 
        min_value=1, 
        max_value=100, 
        step=1,
        disabled=st.session_state.game_over
    )
    submit_button = st.form_submit_button(label="Submit Guess", disabled=st.session_state.game_over)

# Processing Logic Loop upon submission execution
if submit_button and not st.session_state.game_over:
    st.session_state.attempts += 1
    
    if user_guess == st.session_state.secret_number:
        st.session_state.feedback = f"🎉 Correct! You won in {st.session_state.attempts} attempts! Final Score: {st.session_state.score}"
        st.session_state.feedback_type = "success"
        st.session_state.game_over = True
        st.balloons() # Triggers celebration animation graphics
    else:
        st.session_state.score -= 10
        if user_guess < st.session_state.secret_number:
            st.session_state.feedback = f"📈 {user_guess} is too low! Try a higher number."
            st.session_state.feedback_type = "warning"
        else:
            st.session_state.feedback = f"📉 {user_guess} is too high! Try a lower number."
            st.session_state.feedback_type = "warning"

        if st.session_state.attempts >= st.session_state.max_attempts:
            st.session_state.feedback = f"💀 Game Over! You ran out of attempts. The correct number was {st.session_state.secret_number}."
            st.session_state.feedback_type = "error"
            st.session_state.game_over = True
    
    # Refresh the UI page view to load calculations instantly
    st.rerun()

# Global Options Layout Block
st.write("---")
if st.button("🔄 Restart Game", use_container_width=True):
    reset_game()
    st.rerun()
