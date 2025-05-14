import streamlit as st
import functions as func

@st.cache_data
def load_dictionary(file):
    return func.process_dict(file)

words_dict = load_dictionary('Svenska_ordbok.txt')

st.title("Swedish-English Dictionary Quiz")

# --- Session state initialization ---
if 'random_word' not in st.session_state:
    st.session_state['random_word'] = func.generate_swe_word(words_dict)
if 'translation_submitted' not in st.session_state:
    st.session_state['translation_submitted'] = False
if 'synonym_submitted' not in st.session_state:
    st.session_state['synonym_submitted'] = False
if 'show_answer' not in st.session_state:
    st.session_state['show_answer'] = False
if 'reset_needed' not in st.session_state:
    st.session_state['reset_needed'] = False
if 'eng_guess' not in st.session_state:
    st.session_state['eng_guess'] = ""
if 'syn_guess' not in st.session_state:
    st.session_state['syn_guess'] = ""

# --- Reset logic for Next Word ---
if st.session_state['reset_needed']:
    st.session_state['random_word'] = func.generate_swe_word(words_dict)
    st.session_state['translation_submitted'] = False
    st.session_state['synonym_submitted'] = False
    st.session_state['show_answer'] = False
    st.session_state['reset_needed'] = False
    st.session_state['eng_guess'] = ""
    st.session_state['syn_guess'] = ""

random_word = st.session_state['random_word']
st.write(f"**Swedish word:** {random_word.upper()}")

def display_answer(label, result):
    if 'full_answer' in result:
        st.write(label)
        # If only one answer but contains slashes, split and enumerate
        if len(result['full_answer']) == 1 and "/" in result['full_answer'][0]:
            meanings = [m.strip() for m in result['full_answer'][0].split('/')]
            for idx, ans in enumerate(meanings, 1):
                st.write(f"{idx}. {ans}")
        # If multiple answers, enumerate
        elif len(result['full_answer']) > 1:
            for idx, ans in enumerate(result['full_answer'], 1):
                st.write(f"{idx}. {ans}")
        # Single answer, just print
        else:
            st.write(result['full_answer'][0])

# --- Translation Phase ---
with st.form("translation_form"):
    eng_guess = st.text_input(
        "English translation:",
        key="eng_guess",
        disabled=st.session_state['translation_submitted'] or st.session_state['show_answer']
    )
    submitted_translation = st.form_submit_button(
        "Submit",
        disabled=st.session_state['translation_submitted'] or st.session_state['show_answer']
    )

# Show Answer button (only enabled if not already submitted or shown)
show_answer_btn = st.button(
    "Show Answer",
    disabled=st.session_state['translation_submitted'] or st.session_state['show_answer']
)

# --- Handle translation submission ---
if submitted_translation and not st.session_state['translation_submitted']:
    translation_result = func.check_guess(eng_guess, words_dict, random_word, syn=0)
    st.session_state['translation_submitted'] = True

    if translation_result['status'] == 'invalid':
        st.error("INCORRECT! No valid answer given.")
        display_answer("The correct answer is:", translation_result)
    elif translation_result['status'] == 'correct':
        st.success("CORRECT!")
        display_answer("The full answer is:", translation_result)
    elif translation_result['status'] == 'incorrect':
        st.error("INCORRECT!")
        display_answer("The correct answer is:", translation_result)

# --- Synonym Phase (if translation correct and synonyms exist) ---
show_synonym = (
    st.session_state['translation_submitted']
    and not st.session_state['synonym_submitted']
    and len(words_dict[random_word]) > 1
    and not st.session_state['show_answer']
)

if show_synonym:
    with st.form("synonym_form"):
        syn_guess = st.text_input(
            "Enter synonym:",
            key="syn_guess",
            disabled=st.session_state['synonym_submitted']
        )
        submitted_synonym = st.form_submit_button(
            "Submit Synonym",
            disabled=st.session_state['synonym_submitted']
        )

    if submitted_synonym and not st.session_state['synonym_submitted']:
        synonym_result = func.check_guess(syn_guess, words_dict, random_word, syn=1)
        st.session_state['synonym_submitted'] = True

        if synonym_result['status'] == 'invalid':
            st.error("INCORRECT! No valid answer given.")
            display_answer("The correct answer is:", synonym_result)
        elif synonym_result['status'] == 'correct':
            st.success("CORRECT!")
            display_answer("The full answer is:", synonym_result)
        elif synonym_result['status'] == 'incorrect':
            st.error("INCORRECT!")
            display_answer("The correct answer is:", synonym_result)

# --- Show Answer button logic (shows both translation and synonym) ---
if show_answer_btn and not st.session_state['show_answer']:
    st.session_state['show_answer'] = True
    # Show translation answer
    translation_result = func.check_guess("", words_dict, random_word, syn=0)
    display_answer("The correct translation is:", translation_result)
    # Show synonym answer if exists
    if len(words_dict[random_word]) > 1:
        synonym_result = func.check_guess("", words_dict, random_word, syn=1)
        display_answer("The correct synonym is:", synonym_result)

# --- Next Word button at the bottom ---
if st.button("Next Word"):
    st.session_state['reset_needed'] = True
    st.rerun()
