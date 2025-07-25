import streamlit as st

def translate_with_fallback(translator, text, src_lang, dest_lang, max_retries=3):
    for attempt in range(max_retries):
        try:
            if translator:
                result = translator.translate(text, src=src_lang, dest=dest_lang)
                if result and result.text:
                    return result.text
            raise Exception("Translation failed")
        except Exception:
            if attempt < max_retries - 1:
                st.warning(f"Translation attempt {attempt + 1} failed, retrying...")
                continue
            else:
                st.error(f"Translation failed after {max_retries} attempts.")
                return text  # Return original text if translation fails
