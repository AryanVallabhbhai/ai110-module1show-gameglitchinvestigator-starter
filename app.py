import random
import streamlit as st

from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
)

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

# FIXME: Logic breaks here - secret should be re-generated when difficulty changes, but isn't
#FIX: added logic that checks if the difficulty has changed and resets the game state accordingly
if "active_difficulty" not in st.session_state:
    st.session_state.active_difficulty = difficulty

if st.session_state.active_difficulty != difficulty:
    st.session_state.active_difficulty = difficulty
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 1
    st.session_state.history = []
    st.session_state.score = 0
    st.session_state.status = "playing"

if "attempts" not in st.session_state:
    st.session_state.attempts = 1

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("Make a guess")

#FIX: made sure the banner will update the range of the game when the difficulty changes    
st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)
#FIX: added logic to reset the game state when the "New Game" button is pressed
if new_game:
    st.session_state.attempts = 0
    st.session_state.history = []
    st.session_state.score = 0
    # FIX: reset status too, else a won/lost game stays stopped and the
    # submit block below is never reached after starting a new game.
    st.session_state.status = "playing"
    low, high = get_range_for_difficulty(difficulty)
    st.session_state.secret = random.randint(low, high)
    # FIX: stash so the message survives st.rerun() (inline st.success is wiped).
    st.session_state.flash = [("success", "New game started.")]
    st.session_state.balloons = False
    st.rerun()

# FIX: render feedback stashed from the previous submit (survives st.rerun()).
# Must run before the status-stop below so win/lose messages still show.
for kind, text in st.session_state.get("flash", []):
    getattr(st, kind)(text)
st.session_state.flash = []
if st.session_state.get("balloons"):
    st.balloons()
    st.session_state.balloons = False

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    # FIX: stash transient feedback in session_state so it survives the
    # st.rerun() below and gets rendered at the top of the next run.
    st.session_state.flash = []
    st.session_state.balloons = False

    if not ok:
        st.session_state.history.append(raw_guess)
        st.session_state.flash.append(("error", err))
    else:
        #FIX: fixed the casting of the guess to an int and added it to the history
        st.session_state.history.append(guess_int)

        secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)

        if show_hint:
            st.session_state.flash.append(("warning", message))

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.session_state.balloons = True
            st.session_state.status = "won"
            st.session_state.flash.append((
                "success",
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}",
            ))
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.session_state.flash.append((
                    "error",
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}",
                ))

    # FIX: rerun after mutating history/score so the debug panel and banner
    # reflect this guess immediately instead of lagging one submit behind.
    st.rerun()

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
