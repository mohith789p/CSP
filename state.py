import streamlit as st

def initialize_session_state():
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'model_loaded' not in st.session_state:
        st.session_state.model_loaded = False
    if 'current_model' not in st.session_state:
        st.session_state.current_model = None
    if 'translator' not in st.session_state:
        st.session_state.translator = None
    if 'language' not in st.session_state:
        st.session_state.language = 'Telugu'  # Default language
