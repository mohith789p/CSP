import streamlit as st
from datetime import datetime
import time
from utils import translate_with_fallback
from prompts import generate_legal_response
from models import load_translator, load_optimized_model

def process_query_telugu(user_query, selected_category, model_choice):
    status_container = st.container()
    result_container = st.container()

    with status_container:
        progress_col1, progress_col2 = st.columns([3,1])
        with progress_col1:
            overall_progress = st.progress(0)
            status_text = st.empty()
        with progress_col2:
            step_counter = st.empty()

        # Step 1: Load translator
        step_counter.text("దశ 1/4")
        status_text.text("🔄 అనువాద సేవను లోడ్ చేస్తున్నాం...")
        overall_progress.progress(10)

        if not st.session_state.translator:
            st.session_state.translator = load_translator()

        if not st.session_state.translator:
            st.error("❌ అనువాద సేవ అందుబాటులో లేదు. దయచేసి మీ ఇంటర్నెట్ కనెక్షన్ తనిఖీ చేయండి.")
            st.stop()

        overall_progress.progress(25)
        status_text.text("✅ అనువాద సేవ సిద్ధం")

        # Step 2: Load AI model
        step_counter.text("దశ 2/4")
        status_text.text("🔄 AI మోడల్ లోడ్ చేస్తున్నాం...")
        overall_progress.progress(30)

        if not st.session_state.model_loaded or st.session_state.current_model is None:
            model_pipeline, model_type = load_optimized_model(model_choice)
            if model_pipeline:
                st.session_state.current_model = (model_pipeline, model_type)
                st.session_state.model_loaded = True
            else:
                st.error("❌ AI మోడల్ లోడింగ్ విఫలమైంది. దయచేసి పేజీని రిఫ్రెష్ చేసి మళ్లీ ప్రయత్నించండి.")
                st.stop()
        else:
            model_pipeline, model_type = st.session_state.current_model

        overall_progress.progress(50)
        status_text.text(f"✅ AI మోడల్ సిద్ధం: {model_type}")

        # Step 3: Process query
        step_counter.text("దశ 3/4")
        status_text.text("🔄 మీ ప్రశ్నను ప్రాసెస్ చేస్తున్నాం...")
        overall_progress.progress(60)

        try:
            # Translate Telugu to English if needed
            if user_query != "" and any(char in user_query for char in 'అఆఇఈఉఊఋఌఎఏఐఒఓఔకఖగఘ'):
                status_text.text("🔄 తెలుగు → ఇంగ్లీష్ అనువదిస్తున్నాం...")
                translated_query = translate_with_fallback(
                    st.session_state.translator, user_query, 'te', 'en'
                )
            else:
                translated_query = user_query

            overall_progress.progress(70)

            # Generate AI response
            status_text.text("🤖 AI న్యాయ మార్గదర్శకత్వం రూపొందిస్తున్నది...")
            english_response = generate_legal_response(
                model_pipeline, translated_query, model_type, selected_category
            )

            overall_progress.progress(85)

            # Translate response to Telugu
            status_text.text("🔄 ఇంగ్లీష్ → తెలుగు అనువదిస్తున్నాం...")
            telugu_response = translate_with_fallback(
                st.session_state.translator, english_response, 'en', 'te'
            )

            overall_progress.progress(95)

            # Save to chat history
            chat_entry = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "category": selected_category,
                "question": user_query,
                "translated_question": translated_query,
                "response": telugu_response,
                "english_response": english_response,
                "model_used": model_type,
                "response_language": "Telugu"
            }
            st.session_state.chat_history.append(chat_entry)

            overall_progress.progress(100)
            status_text.text("✅ సమాధానం విజయవంతంగా రూపొందించబడింది!")

            time.sleep(1)
            status_container.empty()

        except Exception as e:
            overall_progress.progress(100)
            status_text.text("❌ ప్రాసెసింగ్ విఫలమైంది")
            st.error(f"ప్రాసెసింగ్ లోపం: {str(e)}")
            st.info("దయచేసి మళ్లీ ప్రయత్నించండి లేదా అనువాద సేవలకు మీ ఇంటర్నెట్ కనెక్షన్ తనిఖీ చేయండి.")
            st.stop()

    with result_container:
        st.markdown("### 📘 సమాధానం:")
        if telugu_response:
            st.markdown(f"""
            <div class="assistant-message">
                <strong>ప్రశ్న:</strong> {user_query}<br><br>
                <strong>సమాధానం:</strong> {telugu_response}<br><br>
                <small><em>AI మోడల్: {model_type} | వర్గం: {selected_category} | సమయం: {datetime.now().strftime("%H:%M:%S")}</em></small>
            </div>
            """, unsafe_allow_html=True)

        # (Action buttons left as is in main or UI modules)


def process_query_english(user_query, selected_category, model_choice):
    status_container = st.container()
    result_container = st.container()

    with status_container:
        progress_col1, progress_col2 = st.columns([3,1])
        with progress_col1:
            overall_progress = st.progress(0)
            status_text = st.empty()
        with progress_col2:
            step_counter = st.empty()

        step_counter.text("Step 1/4")
        status_text.text("🔄 Loading translation service...")
        overall_progress.progress(10)

        if not st.session_state.translator:
            st.session_state.translator = load_translator()

        overall_progress.progress(25)
        status_text.text("✅ Translation service ready")

        step_counter.text("Step 2/4")
        status_text.text("🔄 Loading AI model...")
        overall_progress.progress(30)

        if not st.session_state.model_loaded or st.session_state.current_model is None:
            model_pipeline, model_type = load_optimized_model(model_choice)
            if model_pipeline:
                st.session_state.current_model = (model_pipeline, model_type)
                st.session_state.model_loaded = True
            else:
                st.error("❌ AI model loading failed. Please refresh the page and try again.")
                st.stop()
        else:
            model_pipeline, model_type = st.session_state.current_model

        overall_progress.progress(50)
        status_text.text(f"✅ AI model ready: {model_type}")

        step_counter.text("Step 3/4")
        status_text.text("🔄 Processing your question...")
        overall_progress.progress(60)

        try:
            overall_progress.progress(70)
            status_text.text("🤖 AI generating legal guidance...")
            english_response = generate_legal_response(
                model_pipeline, user_query, model_type, selected_category
            )

            overall_progress.progress(95)

            chat_entry = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "category": selected_category,
                "question": user_query,
                "translated_question": user_query,
                "response": english_response,
                "english_response": english_response,
                "model_used": model_type,
                "response_language": "English"
            }
            st.session_state.chat_history.append(chat_entry)

            overall_progress.progress(100)
            status_text.text("✅ Response generated successfully!")

            time.sleep(1)
            status_container.empty()

        except Exception as e:
            overall_progress.progress(100)
            status_text.text("❌ Processing failed")
            st.error(f"Processing error: {str(e)}")
            st.info("Please try again or check your internet connection.")
            st.stop()

    with result_container:
        st.markdown("### 📘 Legal Response:")
        if english_response:
            st.markdown(f"""
            <div class="user-message">
                <strong>Question:</strong> {user_query}<br><br>
                <strong>Answer:</strong> {english_response}<br><br>
                <small><em>AI Model: {model_type} | Category: {selected_category} | Time: {datetime.now().strftime("%H:%M:%S")}</em></small>
            </div>
            """, unsafe_allow_html=True)

        # (Action buttons left as is in main or UI modules)
