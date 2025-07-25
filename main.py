import streamlit as st
import warnings
import time

from config import set_page_config, inject_custom_css
from state import initialize_session_state
from data import legal_categories_telugu, legal_categories_english
from ui_components import (
    display_header,
    select_category_and_question,
    display_recent_chat,
    input_area,
    display_legal_disclaimer,
    display_footer
)
from query import process_query_telugu, process_query_english

warnings.filterwarnings("ignore")

# Page setup and style
set_page_config()
inject_custom_css()

# Initialize session state
initialize_session_state()

# Set model_choice and response_language based on language
model_choice = "Auto (Recommended)"  # you can modify as necessary
response_language = "Telugu & English" if st.session_state.language == 'English' else "Telugu Only"

# Language toggle button at top right
col_left, col_right = st.columns([7,1])
with col_right:
    if st.button(f"🌐 {st.session_state.language}", help="Click to switch language"):
        st.session_state.language = 'English' if st.session_state.language == 'Telugu' else 'Telugu'
        st.rerun()  # replaced deprecated st.rerun

# Display header
display_header(st.session_state.language)

# Select legal categories data
legal_categories = legal_categories_telugu if st.session_state.language == 'Telugu' else legal_categories_english

# Create layout for selection
col1, col2 = st.columns([3,1])
with col1:
    selected_category, selected_question = select_category_and_question(st.session_state.language, legal_categories)

with col2:
    st.write("")  # spacer

# Display recent chat history
display_recent_chat(st.session_state.language)

# Input area for question
user_query = input_area(st.session_state.language, selected_question)

# Main action button in center column
col1, col2, col3 = st.columns([1,2,1])
with col2:
    if st.session_state.language == 'Telugu':
        if st.button("💬 సమాధానం పొందండి", type="primary", use_container_width=True):
            if not user_query.strip():
                st.warning("⚠️ దయచేసి ప్రశ్నను నమోదు చేయండి")
            else:
                process_query_telugu(user_query, selected_category, model_choice)
    else:
        if st.button("💬 Get Answer", type="primary", use_container_width=True):
            if not user_query.strip():
                st.warning("⚠️ Please enter a question")
            else:
                process_query_english(user_query, selected_category, model_choice)

# Legal disclaimer
display_legal_disclaimer(st.session_state.language)

# Final reminder and footer
st.error("🏛️ **Remember**: 'Justice delayed is justice denied' - Seek timely legal help when needed!")
display_footer(st.session_state.language)
