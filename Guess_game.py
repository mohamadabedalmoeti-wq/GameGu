import random
import streamlit as st

# Set up page layout and tab style
st.set_page_config(page_title="Word Decryption Game", page_icon="🧩", layout="centered")

# Curated list of challenging 4-letter words
WORD_BANK = [
    "CODE", "JAVA", "BYTE", "DATA", "NODE", "FLUX", "ZINC", "PLUG",
    "CYAN", "ECHO", "GIGA", "MAZE", "JINX", "WAVE", "VOID", "PIXEL"
]

# Initialize global game state data structures
if "secret_word" not in st.session_state:
    st.session_state.secret_word = random.choice(WORD_BANK)
    st.session_state.attempts = 0
    st.session_state.max_attempts = 6
    st.session_state.history = []  # Stores tuples of (guess, feedback_string)
    st.session_state.game_over = False
    st.session_state.game_won = False

def restart_game():
    """Wipes session memory clean to roll a new word."""
    st.session_state.secret_word = random.choice(WORD_BANK)
    st.session_state.attempts = 0
    st.session_state.history = []
    st.session_state.game_over = False
    st.session_state.game_won = False

# Application Interface Header Setup
st.title("🧩 Mastermind Word Decryption")
st.write("Crack the secret **4-letter word** before your attempts run out!")

# Metric Feedback Panel Row
col1, col2 = st.columns(2)
with col1:
    st.metric("Attempts Remaining", st.session_state.max_attempts - st.session_state.attempts)
with col2:
    st.metric("Target Length", "4 Letters")

# Display historical attempts dashboard tracking area
if st.session_state.history:
    st.write("### Your Guess History")
    for past_guess, visual_blocks in st.session_state.history:
        st.markdown(f"### `{past_guess}`  →  {visual_blocks}")

# Win/Loss Resolution Banner Layout
if st.session_state.game_over:
    if st.session_state.game_won:
        st.success(f"🎉 Code Cracked! You decrypted the word '{st.session_state.secret_word}' successfully!")
        st.balloons()
    else:
        st.error(f"💀 System Locked! You ran out of attempts. The secret word was '{st.session_state.secret_word}'.")

# Interactive User Form Frame
with st.form(key="word_form", clear_on_submit=True):
    user_input = st.text_input(
        "Type your 4-letter guess:", 
        max_chars=4, 
        disabled=st.session_state.game_over
    ).upper().strip()
    
    submit_btn = st.form_submit_button("Decrypt", disabled=st.session_state.game_over)

# Processing validation loop pipelines
if submit_btn and not st.session_state.game_over:
    if len(user_input) != 4 or not user_input.isalpha():
        st.warning("⚠️ Please enter a valid 4-letter alphabetic word!")
    else:
        st.session_state.attempts += 1
        secret = st.session_state.secret_word
        feedback_emojis = []

        # Analyze letters dynamically to construct visual box string
        for i in range(4):
            if user_input[i] == secret[i]:
                feedback_emojis.append("🟩")  # Perfect position Match
            elif user_input[i] in secret:
                feedback_emojis.append("🟨")  # Included elsewhere
            else:
                feedback_emojis.append("🟥")  # Miss entirely

        feedback_string = " ".join(feedback_emojis)
        st.session_state.history.append((user_input, feedback_string))

        # Check win/loss flags
        if user_input == secret:
            st.session_state.game_over = True
            st.session_state.game_won = True
        elif st.session_state.attempts >= st.session_state.max_attempts:
            st.session_state.game_over = True

        st.rerun()

st.write("---")
if st.button("🔄 Generate New Code Word", use_container_width=True):
    restart_game()
    st.rerun()
