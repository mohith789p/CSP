import streamlit as st
from datetime import datetime
from googletrans import Translator
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import warnings
import time
warnings.filterwarnings("ignore")

# Page configuration
st.set_page_config(
    page_title="తెలుగు న్యాయ సహాయకుడు", 
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
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

# Set default values for removed sidebar options
model_choice = "Auto (Recommended)"
response_language = "Telugu & English" if st.session_state.language == 'English' else "Telugu Only"

# Language toggle button at top right
col_left, col_right = st.columns([4, 1])
with col_right:
    if st.button(f"🌐 {st.session_state.language}", help="Click to switch language"):
        st.session_state.language = 'English' if st.session_state.language == 'Telugu' else 'Telugu'
        st.rerun()

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #2a5298;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .user-message {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
        border-left: 4px solid #9c27b0;
    }
    .stSelectbox > div > div {
        background-color: #ffffff !important;
        border: 2px solid #2a5298 !important;
        border-radius: 10px !important;
        color: #000000 !important;
    }
    .stSelectbox > div > div > div {
        color: #000000 !important;
        font-weight: 500 !important;
    }
    .stSelectbox label {
        color: #2a5298 !important;
        font-weight: bold !important;
        font-size: 16px !important;
    }
    .stTextArea > div > div > textarea {
        background-color: #f8f9fa;
        border-radius: 10px;
        border: 2px solid #e9ecef;
        font-size: 16px;
    }
    .legal-disclaimer {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #ff9800;
        margin-top: 2rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton > button {
        background: linear-gradient(90deg, #2a5298 0%, #1e3c72 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .feature-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #e9ecef;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# Title and header
if st.session_state.language == 'Telugu':
    st.markdown("""
    <div class="main-header">
        <h1>⚖️ తెలుగు న్యాయ సహాయక చాట్‌బాట్</h1>
        <p>కృత్రిమ మేధస్సు ఆధారిత న్యాయ మార్గదర్శకత్వం</p>
        <small>Microsoft DialoGPT-Large + Google FLAN-T5 ద్వారా శక్తివంతం | 8GB RAM కోసం అనుకూలీకృతం</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Legal question categories
    st.subheader("📋 న్యాయ విభాగాలు")
else:
    st.markdown("""
    <div class="main-header">
        <h1>⚖️ Legal Assistant AI Chatbot</h1>
        <p>AI-Powered Legal Guidance & Information System</p>
        <small>Powered by Microsoft DialoGPT-Large + Google FLAN-T5 | Optimized for 8GB RAM</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Legal question categories
    st.subheader("📋 Legal Categories")

legal_categories_telugu = {
    "క్రిమినల్ లా": [
        "FIR దాఖలు చేసే ప్రక్రియ ఏమిటి?",
        "అరెస్టు అయిన వ్యక్తి హక్కులు ఏమిటి?", 
        "బెయిల్ ఎలా అప్లై చేయాలి?",
        "అంతిసిపేటరీ బెయిల్ అంటే ఏమిటి?",
        "పోలీసు కస్టడీలో హక్కులు ఏమిటి?",
        "సైబర్ క్రైమ్ ఎలా నివేదించాలి?",
        "దహేజ్ వేధింపుల విષయంలో ఏం చేయాలి?"
    ],
    "సివిల్ లా": [
        "వస్తుల వివాదాలను ఎలా పరిష్కరించాలి?",
        "కాంట్రాక్ట్ ఉల్లంఘన కేసు ఎలా దాఖలు చేయాలి?",
        "ఇంజంక్షన్ ఎలా పొందాలి?",
        "నష్టపరిహారం ఎలా క్లెయిమ్ చేయాలి?",
        "అద్దె వివాదాలను ఎలా పరిష్కరించాలి?",
        "పొరుగువారితో వివాదాలు ఎలా పరిష్కరించాలి?"
    ],
    "కుటుంబ న్యాయం": [
        "విడాకుల ప్రక్రియ ఏమిటి?",
        "పిల్లల కస్టడీ చట్టాలు ఏమిటి?",
        "వివాహ రద్దు ఎలా చేయాలి?",
        "గృహ హింస నుండి రక్షణ ఎలా పొందాలి?",
        "భరణ భత్యం ఎలా క్లెయిమ్ చేయాలి?",
        "పెళ్లి రిజిస్ట్రేషన్ ఎలా చేయాలి?"
    ],
    "ఆస్తి చట్టం": [
        "ఇచ్ఛాపత్రాన్ని ఎలా వ్రాయాలి?",
        "ఆస్తి రిజిస్ట్రేషన్ ప్రక్రియ ఏమిటి?",
        "వారసత్వ హక్కులు ఏమిటి?",
        "భూమి వివాదాలను ఎలా పరిష్కరించాలి?",
        "సర్వే సెట్టిల్‌మెంట్ అంటే ఏమిటి?",
        "ఆస్తి మార్పిడి ప్రక్రియ ఏమిటి?"
    ],
    "వినియోగదారు చట్టం": [
        "వినియోగదారు ఫిర్యాదు ఎలా దాఖలు చేయాలి?",
        "ఆన్‌లైన్ మోసాలను ఎలా నివేదించాలి?",
        "వస్తువుల వాపసీ హక్కులు ఏమిటి?",
        "సర్వీస్ ఛార్జీలపై ఫిర్యాదు ఎలా చేయాలి?",
        "బ్యాంకు సమస్యలను ఎలా పరిష్కరించాలి?"
    ],
    "కార్మిక చట్టం": [
        "ఉద్యోగ విడిచిపెట్టే ప్రక్రియ ఏమిటి?",
        "అనుకోకుండా ఉద్యోగం కోల్పోయినప్పుడు ఏం చేయాలి?",
        "జీతం ఇవ్వకపోతే ఏం చేయాలి?",
        "కార్మిక న్యాయస్థానంలో ఫిర్యాదు ఎలా చేయాలి?",
        "EPF మరియు గ్రాట్యూటీ ఎలా క్లెయిమ్ చేయాలి?"
    ]
}

legal_categories_english = {
    "Criminal Law": [
        "What is the process for filing an FIR?",
        "What are the rights of an arrested person?", 
        "How to apply for bail?",
        "What is anticipatory bail?",
        "What are the rights in police custody?",
        "How to report cyber crime?",
        "What to do in case of dowry harassment?"
    ],
    "Civil Law": [
        "How to resolve property disputes?",
        "How to file a contract breach case?",
        "How to obtain an injunction?",
        "How to claim damages?",
        "How to resolve rental disputes?",
        "How to resolve disputes with neighbors?"
    ],
    "Family Law": [
        "What is the divorce process?",
        "What are child custody laws?",
        "How to annul a marriage?",
        "How to get protection from domestic violence?",
        "How to claim maintenance/alimony?",
        "How to register a marriage?"
    ],
    "Property Law": [
        "How to write a will?",
        "What is the property registration process?",
        "What are inheritance rights?",
        "How to resolve land disputes?",
        "What is survey settlement?",
        "What is the property transfer process?"
    ],
    "Consumer Law": [
        "How to file a consumer complaint?",
        "How to report online fraud?",
        "What are product return rights?",
        "How to complain about service charges?",
        "How to resolve banking issues?"
    ],
    "Labor Law": [
        "What is the job resignation process?",
        "What to do when unfairly terminated?",
        "What to do if salary is not paid?",
        "How to file a complaint in labor court?",
        "How to claim EPF and gratuity?"
    ]
}

# Select categories based on language
legal_categories = legal_categories_telugu if st.session_state.language == 'Telugu' else legal_categories_english

# Create layout for better organization
col1, col2 = st.columns([3, 1])

with col1:
    # Category selection
    if st.session_state.language == 'Telugu':
        selected_category = st.selectbox(
            "వర్గాన్ని ఎంచుకోండి:",
            list(legal_categories.keys()),
            help="మీ ప్రశ్న సంబంధిత విభాగాన్ని ఎంచుకోండి"
        )
        
        # Question selection
        if selected_category:
            questions = legal_categories[selected_category]
            selected_question = st.selectbox(
                "ప్రశ్నను ఎంచుకోండి:",
                ["💬 కస్టమ్ ప్రశ్న రాయండి..."] + questions,
                help="ముందుగా తయారు చేసిన ప్రశ్న ఎంచుకోండి లేదా మీ స్వంత ప్రశ్న రాయండి"
            )
    else:
        selected_category = st.selectbox(
            "Select Category:",
            list(legal_categories.keys()),
            help="Choose the legal category related to your question"
        )
        
        # Question selection
        if selected_category:
            questions = legal_categories[selected_category]
            selected_question = st.selectbox(
                "Select Question:",
                ["💬 Write custom question..."] + questions,
                help="Choose a preset question or write your own custom question"
            )

with col2:
    # Empty space for better layout balance
    st.write("")

# Display recent chat history
if st.session_state.chat_history:
    if st.session_state.language == 'Telugu':
        with st.expander(f"📜 ఇటీవలి సంభాషణలు ({len(st.session_state.chat_history)} మొత్తం)", expanded=False):
            for i, chat in enumerate(reversed(st.session_state.chat_history[-5:])):  # Show last 5
                st.markdown(f"""
                <div class="chat-message">
                    <small><strong>#{len(st.session_state.chat_history)-i}</strong> | {chat.get('timestamp', 'తెలియని సమయం')} | {chat.get('category', 'తెలియని వర్గం')}</small><br>
                    <strong>ప్రశ్న:</strong> {chat.get('question', 'తెలియని ప్రశ్న')[:100]}{'...' if len(chat.get('question', '')) > 100 else ''}<br>
                    <strong>సమాధానం:</strong> {chat.get('response', 'తెలియని సమాధానం')[:150]}{'...' if len(chat.get('response', '')) > 150 else ''}
                </div>
                """, unsafe_allow_html=True)
    else:
        with st.expander(f"📜 Recent Conversations ({len(st.session_state.chat_history)} total)", expanded=False):
            for i, chat in enumerate(reversed(st.session_state.chat_history[-5:])):  # Show last 5
                st.markdown(f"""
                <div class="chat-message">
                    <small><strong>#{len(st.session_state.chat_history)-i}</strong> | {chat.get('timestamp', 'Unknown time')} | {chat.get('category', 'Unknown category')}</small><br>
                    <strong>Q:</strong> {chat.get('question', 'Unknown question')[:100]}{'...' if len(chat.get('question', '')) > 100 else ''}<br>
                    <strong>A:</strong> {chat.get('response', 'Unknown response')[:150]}{'...' if len(chat.get('response', '')) > 150 else ''}
                </div>
                """, unsafe_allow_html=True)

# Input area
if st.session_state.language == 'Telugu':
    if selected_question == "💬 కస్టమ్ ప్రశ్న రాయండి...":
        user_query = st.text_area(
            "✍️ మీ న్యాయ ప్రశ్నను ఇక్కడ టైప్ చేయండి:",
            height=120,
            placeholder="ఉదాహరణ: నాకు ఒక ఇంట్లో వివాదం ఉంది, నేను ఏం చేయాలి? లేదా నా ఉద్యోగంలో సమస్యలు ఉన్నాయి...",
            help="మీ న్యాయ ప్రశ్నను తెలుగులో స్పష్టంగా వ్రాయండి"
        )
    else:
        user_query = selected_question
        st.text_area("ఎంచుకున్న ప్రశ్న:", value=selected_question, height=100, disabled=True)
else:
    if selected_question == "💬 Write custom question...":
        user_query = st.text_area(
            "✍️ Type your legal question here:",
            height=120,
            placeholder="Example: I have a property dispute, what should I do? Or I'm facing issues at my workplace...",
            help="Please write your legal question clearly in English"
        )
    else:
        user_query = selected_question
        st.text_area("Selected Question:", value=selected_question, height=100, disabled=True)

# Load models and translator with optimizations for 8GB RAM
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
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Model selection based on choice and available memory
        if model_choice == "Auto" or model_choice == "DialoGPT-Large":
            model_name = "microsoft/DialoGPT-large"
        elif model_choice == "FLAN-T5-Base":
            model_name = "google/flan-t5-base"
        else:
            model_name = "microsoft/DialoGPT-large"
        
        status_text.text(f"🔄 Loading {model_name}...")
        progress_bar.progress(20)
        
        # Check available memory and adjust accordingly
        device = "cuda" if torch.cuda.is_available() else "cpu"
        status_text.text(f"🔄 Detected device: {device}")
        progress_bar.progress(40)
        
        # Load tokenizer
        status_text.text("🔄 Loading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        progress_bar.progress(60)
        
        # Load model with memory optimization
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
        
        # Create pipeline with optimizations
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
        
        # Clean up progress indicators
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

def create_advanced_legal_prompt(query, category="General"):
    """Create a specialized prompt for legal queries with Indian context"""
    return f"""You are an expert Indian legal consultant specializing in {category} with comprehensive knowledge of:

LEGAL FRAMEWORK:
- Indian Constitution (Articles, Fundamental Rights & Duties)
- Indian Penal Code (IPC) & Bharatiya Nyaya Sanhita (BNS) 2023
- Criminal Procedure Code (CrPC) & Bharatiya Nagarik Suraksha Sanhita (BNSS) 2023
- Civil Procedure Code (CPC) & Evidence Act
- Family laws: Hindu Marriage Act, Special Marriage Act, Muslim Personal Law
- Property laws: Transfer of Property Act, Registration Act
- Consumer Protection Act 2019 & Labor Laws
- Recent Supreme Court & High Court judgments

RESPONSE REQUIREMENTS:
1. ✅ Provide accurate, practical legal guidance
2. 📋 Include relevant legal sections/acts when applicable
3. 🔄 Give step-by-step procedural guidance
4. ⏰ Mention approximate timelines and costs
5. 📄 List required documents and forms
6. ⚖️ Reference landmark judgments if relevant
7. 🏛️ Suggest appropriate courts/forums
8. ⚠️ Always recommend consulting qualified lawyers for specific cases

CATEGORY: {category}
QUERY: {query}

Provide comprehensive legal guidance in clear, professional English:"""

def generate_legal_response(model_pipeline, query, model_type, category="General"):
    """Generate response using the loaded model with enhanced parameters"""
    try:
        legal_prompt = create_advanced_legal_prompt(query, category)
        
        # Enhanced generation parameters
        generation_params = {
            "temperature": 0.7,
            "do_sample": True,
            "repetition_penalty": 1.2,
            "length_penalty": 1.0,
            "no_repeat_ngram_size": 3
        }
        
        if "flan-t5" in model_type.lower():
            # T5 model parameters
            response = model_pipeline(
                legal_prompt,
                max_length=600,
                min_length=100,
                **generation_params
            )
            generated_text = response[0]['generated_text']
        else:
            # GPT model parameters
            response = model_pipeline(
                legal_prompt,
                max_new_tokens=500,
                min_length=len(legal_prompt) + 50,
                pad_token_id=model_pipeline.tokenizer.eos_token_id,
                eos_token_id=model_pipeline.tokenizer.eos_token_id,
                return_full_text=False,
                **generation_params
            )
            generated_text = response[0]['generated_text']
        
        # Post-process the response
        generated_text = generated_text.strip()
        
        # Add standard legal disclaimer if not present
        if "consult" not in generated_text.lower() and "lawyer" not in generated_text.lower():
            generated_text += "\n\n⚠️ IMPORTANT: This is general information only. Please consult a qualified lawyer for advice specific to your situation."
        
        return generated_text
        
    except Exception as e:
        error_msg = f"Response generation error: {str(e)}. Please try again or rephrase your question."
        st.error(error_msg)
        return error_msg

def translate_with_fallback(translator, text, src_lang, dest_lang, max_retries=3):
    """Translate text with retry mechanism and fallback"""
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

def process_query_telugu():
    # Create containers for dynamic updates
    status_container = st.container()
    result_container = st.container()
    
    with status_container:
        # Initialize progress tracking
        progress_col1, progress_col2 = st.columns([3, 1])
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
            if user_query != selected_question or any(char in user_query for char in 'అఆఇఈఉఊఋఌఎఏఐఒఓఔకఖగఘ'):
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
            
            # Clear progress indicators after a short delay
            time.sleep(1)
            status_container.empty()
            
        except Exception as e:
            overall_progress.progress(100)
            status_text.text("❌ ప్రాసెసింగ్ విఫలమైంది")
            st.error(f"ప్రాసెసింగ్ లోపం: {str(e)}")
            st.info("దయచేసి మళ్లీ ప్రయత్నించండి లేదా అనువాద సేవలకు మీ ఇంటర్నెట్ కనెక్షన్ తనిఖీ చేయండి.")
            st.stop()
    
    # Display results in Telugu
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
        
        # Action buttons in Telugu
        st.markdown("### 🎯 త్వరిత చర్యలు")
        action_col1, action_col2, action_col3, action_col4 = st.columns(4)
        
        with action_col1:
            if st.button("📋 సమాధానం కాపీ చేయండి"):
                st.code(telugu_response, language="text")
                st.success("సమాధానం కాపీ చేయడానికి సిద్ధం!")
        
        with action_col2:
            if st.button("🔄 తదుపరి ప్రశ్న అడగండి"):
                st.info("పైన మీ తదుపరి ప్రశ్నను టైప్ చేసి మళ్లీ 'సమాధానం పొందండి' క్లిక్ చేయండి!")
        
        with action_col3:
            if st.button("⭐ సమాధానానికి రేటింగ్ ఇవ్వండి"):
                rating = st.select_slider("ఈ సమాధానానికి రేటింగ్ ఇవ్వండి:", options=[1, 2, 3, 4, 5], value=4)
                st.success(f"రేటింగ్ ఇచ్చినందుకు ధన్యవాదాలు: {rating}/5 నక్షత్రాలు!")
        
        with action_col4:
            if st.button("🚨 సమస్య నివేదించండి"):
                st.warning("నిర్దిష్ట న్యాయ సమస్యలకు దయచేసి అర్హత కలిగిన న్యాయవాదిని సంప్రదించండి.")


def process_query_english():
    # Create containers for dynamic updates
    status_container = st.container()
    result_container = st.container()
    
    with status_container:
        # Initialize progress tracking
        progress_col1, progress_col2 = st.columns([3, 1])
        with progress_col1:
            overall_progress = st.progress(0)
            status_text = st.empty()
        with progress_col2:
            step_counter = st.empty()
        
        # Step 1: Load translator (optional for English)
        step_counter.text("Step 1/4")
        status_text.text("🔄 Loading translation service...")
        overall_progress.progress(10)
        
        if not st.session_state.translator:
            st.session_state.translator = load_translator()
        
        overall_progress.progress(25)
        status_text.text("✅ Translation service ready")
        
        # Step 2: Load AI model
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
        
        # Step 3: Process query
        step_counter.text("Step 3/4")
        status_text.text("🔄 Processing your question...")
        overall_progress.progress(60)
        
        try:
            overall_progress.progress(70)
            
            # Generate AI response
            status_text.text("🤖 AI generating legal guidance...")
            english_response = generate_legal_response(
                model_pipeline, user_query, model_type, selected_category
            )
            
            overall_progress.progress(95)
            
            # Save to chat history
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
            
            # Clear progress indicators after a short delay
            time.sleep(1)
            status_container.empty()
            
        except Exception as e:
            overall_progress.progress(100)
            status_text.text("❌ Processing failed")
            st.error(f"Processing error: {str(e)}")
            st.info("Please try again or check your internet connection.")
            st.stop()
    
    # Display results in English
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
        
        # Action buttons in English
        st.markdown("### 🎯 Quick Actions")
        action_col1, action_col2, action_col3, action_col4 = st.columns(4)
        
        with action_col1:
            if st.button("📋 Copy Response"):
                st.code(english_response, language="text")
                st.success("Response ready to copy!")
        
        with action_col2:
            if st.button("🔄 Ask Follow-up"):
                st.info("Type your follow-up question above and click 'Get Answer' again!")
        
        with action_col3:
            if st.button("⭐ Rate Response"):
                rating = st.select_slider("Rate this response:", options=[1, 2, 3, 4, 5], value=4)
                st.success(f"Thank you for rating: {rating}/5 stars!")
        
        with action_col4:
            if st.button("🚨 Report Issue"):
                st.warning("Please ensure to consult a qualified lawyer for specific legal issues.")


# Main processing
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.session_state.language == 'Telugu':
        if st.button("💬 సమాధానం పొందండి", type="primary", use_container_width=True):
            if not user_query.strip():
                st.warning("⚠️ దయచేసి ప్రశ్నను నమోదు చేయండి")
            else:
                process_query_telugu()
    else:
        if st.button("💬 Get Answer", type="primary", use_container_width=True):
            if not user_query.strip():
                st.warning("⚠️ Please enter a question")
            else:
                process_query_english()



# Legal disclaimer section
st.markdown("---")
st.subheader("⚠️ Important Legal Disclaimer" if st.session_state.language == 'English' else "⚠️ ముఖ్యమైన న్యాయ నిరాకరణ")

# Use columns for better layout
disclaimer_col1, disclaimer_col2 = st.columns(2)

with disclaimer_col1:
    st.markdown("#### 🔴 Important Limitations")
    st.info("""
    • **General Information Only**: This AI provides general legal information, not personalized legal advice
    
    • **Not a Lawyer**: This system cannot replace consultation with qualified legal professionals
    
    • **Accuracy**: While we strive for accuracy, legal information may change or vary by jurisdiction
    
    • **No Attorney-Client Relationship**: Using this service does not create any legal relationship
    """)
    
    st.markdown("#### 📞 Emergency Legal Help")
    st.warning("""
    • **National Legal Services Authority**: 15100 (Toll-free)
    
    • **Women Helpline**: 181
    
    • **Child Helpline**: 1098
    
    • **Cyber Crime**: 1930
    
    • **Police**: 100
    """)

with disclaimer_col2:
    st.markdown("#### ✅ When to Consult a Lawyer")
    st.success("""
    • **Before filing any legal case** or application
    
    • **When drafting important legal documents**
    
    • **If you're involved in any legal dispute**
    
    • **For interpretation of specific laws** to your situation
    
    • **Before making important legal decisions**
    """)
    
    st.markdown("#### � Application Statistics")
    st.info("""
    • **Total Categories**: 6 Legal Areas
    
    • **Preset Questions**: 32+ Sample Questions
    
    • **AI Models**: 3 Advanced Models
    
    • **Languages**: English Support
    """)

# Final reminder
st.error("🏛️ **Remember**: 'Justice delayed is justice denied' - Seek timely legal help when needed!")

# Footer
if st.session_state.language == 'Telugu':
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0; padding: 1rem; background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); border-radius: 10px; border: 1px solid #2196f3;">
        <small style="color: #1976d2;">
            అందుబాటులో ఉన్న న్యాయ మార్గదర్శకత్వం అందించడం కోసం ❤️తో అభివృద్ధి చేయబడింది | వెర్షన్ 2.1 మెరుగుపరచబడింది | ద్విభాష ఎడిషన్
        </small>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0; padding: 1rem; background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); border-radius: 10px; border: 1px solid #2196f3;">
        <small style="color: #1976d2;">
            Developed with ❤️ to provide accessible legal guidance | Version 2.1 Enhanced | Bilingual Edition
        </small>
    </div>
    """, unsafe_allow_html=True)