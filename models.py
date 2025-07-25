import streamlit as st
from googletrans import Translator
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

@st.cache_resource
def load_translator():
    """Load Google Translator with error handling"""
    try:
        translator = Translator()
        # Test translation to ensure it works
        test_translation = translator.translate("test", src='en', dest='te')
        if test_translation and test_translation.text:
            return translator
        else:
            raise Exception("Translation test failed")
    except Exception:
        st.error("Translation service error. Please check your internet connection and try again.")
        return None


@st.cache_resource
def load_optimized_model(model_choice="Auto"):
    """Load the best model optimized for 8GB RAM with progress tracking"""
    import time
    import streamlit as st

    progress_bar = st.progress(0)
    status_text = st.empty()

    try:
        if model_choice == "Auto" or model_choice == "DialoGPT-Large":
            model_name = "microsoft/DialoGPT-large"
        elif model_choice == "FLAN-T5-Base":
            model_name = "google/flan-t5-base"
        else:
            model_name = "microsoft/DialoGPT-large"

        status_text.text(f"🔄 Loading {model_name}...")
        progress_bar.progress(20)

        device = "cuda" if torch.cuda.is_available() else "cpu"
        status_text.text(f"🔄 Detected device: {device}")
        progress_bar.progress(40)

        # Load tokenizer
        status_text.text("🔄 Loading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        progress_bar.progress(60)

        # Load model
        status_text.text("🔄 Loading model...")
        if "flan-t5" in model_name.lower():
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float32,
                low_cpu_mem_usage=True
            )
            task = "text2text-generation"
        else:
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16 if device == "cuda" else torch.float32,
                low_cpu_mem_usage=True,
                device_map="auto" if device == "cuda" else None
            )
            task = "text-generation"

        progress_bar.progress(80)
        status_text.text("🔄 Creating pipeline...")

        pipe = pipeline(
            task,
            model=model,
            tokenizer=tokenizer,
            device=0 if device == "cuda" else -1,
            batch_size=1,
            max_length=512 if "flan-t5" in model_name.lower() else None,
            max_new_tokens=None if "flan-t5" in model_name.lower() else 512
        )

        progress_bar.progress(100)
        status_text.text("✅ Model loaded successfully!")

        progress_bar.empty()
        status_text.empty()

        model_type = "FLAN-T5-Base" if "flan-t5" in model_name.lower() else "DialoGPT-Large"
        return pipe, model_type

    except Exception:
        progress_bar.progress(100)
        status_text.text("❌ Loading failed, trying fallback...")

        # Fallback to smaller model if large model fails
        try:
            st.warning("⚠️ Primary model failed. Loading backup model...")
            fallback_model = "google/flan-t5-small"

            tokenizer = AutoTokenizer.from_pretrained(fallback_model)
            model = AutoModelForCausalLM.from_pretrained(
                fallback_model,
                torch_dtype=torch.float32,
                low_cpu_mem_usage=True
            )

            pipe = pipeline(
                "text2text-generation",
                model=model,
                tokenizer=tokenizer,
                device=-1,
                max_length=512
            )

            progress_bar.empty()
            status_text.empty()
            st.success("✅ Fallback model loaded successfully!")

            return pipe, "FLAN-T5-Small (Fallback)"

        except Exception:
            progress_bar.empty()
            status_text.empty()
            st.error("❌ All models failed to load. Please try refreshing the page or check your internet connection.")
            return None, None
