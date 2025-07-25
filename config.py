import streamlit as st

# Application configuration
APP_CONFIG = {
    "page": {
        "title": "తెలుగు న్యాయ సహాయకుడు",
        "icon": "⚖️",
        "layout": "wide",
        "sidebar_state": "collapsed"
    },
    "model": {
        "default": "Auto (Recommended)",
        "temperature": 0.7,
        "max_length": 512,
        "min_length": 100
    },
    "ui": {
        "chat_history_limit": 5,
        "input_height": 120,
        "response_height": 300
    },
    # Add these new configuration keys
    "TITLE_TELUGU": "తెలుగు న్యాయ సహాయక చాట్‌బాట్",
    "SUBTITLE_TELUGU": "కృత్రిమ మేధస్సు ఆధారిత న్యాయ మార్గదర్శకత్వం",
    "TITLE_ENGLISH": "Legal Assistant AI Chatbot",
    "SUBTITLE_ENGLISH": "AI-Powered Legal Guidance & Information System",
    "POWERED_BY": "Microsoft DialoGPT-Large + Google FLAN-T5 | Optimized for 8GB RAM",
    "VERSION": "2.1",
    "EMERGENCY_CONTACTS": {
        "NLSA": "15100",
        "WOMEN_HELPLINE": "181",
        "CHILD_HELPLINE": "1098",
        "CYBER_CRIME": "1930",
        "POLICE": "100"
    }
}

TEXT_CONSTANTS = {
    "TELUGU": {  # Changed from "Telugu" to "TELUGU"
        "LEGAL_CATEGORIES": "📋 న్యాయ విభాగాలు",
        "LEGAL_DISCLAIMER": "⚠️ ముఖ్యమైన న్యాయ నిరాకరణ",
        "THANK_YOU": "ధన్యవాదాలు",
        "DEVELOPED_WITH_LOVE": "అందుబాటులో ఉన్న న్యాయ మార్గదర్శకత్వం అందించడం కోసం ❤️తో అభివృద్ధి చేయబడింది",
        "SELECT_CATEGORY": "వర్గాన్ని ఎంచుకోండి:",
        "SELECT_QUESTION": "ప్రశ్నను ఎంచుకోండి:",
        "CUSTOM_QUESTION": "💬 కస్టమ్ ప్రశ్న రాయండి...",
        "TYPE_QUESTION": "✍️ మీ న్యాయ ప్రశ్నను ఇక్కడ టైప్ చేయండి:",
        "SELECTED_QUESTION": "ఎంచుకున్న ప్రశ్న:",
        "RECENT_CONVERSATIONS": "📜 ఇటీవలి సంభాషణలు"
    },
    "ENGLISH": {  # Changed from "English" to "ENGLISH"
        "LEGAL_CATEGORIES": "📋 Legal Categories",
        "LEGAL_DISCLAIMER": "⚠️ Important Legal Disclaimer",
        "THANK_YOU": "Thank You",
        "DEVELOPED_WITH_LOVE": "Developed with ❤️ to provide accessible legal guidance",
        "SELECT_CATEGORY": "Select Category:",
        "SELECT_QUESTION": "Select Question:",
        "CUSTOM_QUESTION": "💬 Write custom question...",
        "TYPE_QUESTION": "✍️ Type your legal question here:",
        "SELECTED_QUESTION": "Selected Question:",
        "RECENT_CONVERSATIONS": "📜 Recent Conversations"
    }
}

def set_page_config():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title=APP_CONFIG["page"]["title"],
        page_icon=APP_CONFIG["page"]["icon"],
        layout=APP_CONFIG["page"]["layout"],
        initial_sidebar_state=APP_CONFIG["page"]["sidebar_state"]
    )

def inject_custom_css():
    """Inject custom CSS for modern UI styling"""
    st.markdown("""
    <style>
        /* Main container styling */
        .main .block-container {
            padding-top: 1rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }
        
        /* Header styling with glassmorphism effect */
        .main-header {
            background: linear-gradient(135deg, rgba(30, 60, 114, 0.9) 0%, rgba(42, 82, 152, 0.9) 50%, rgba(46, 125, 50, 0.8) 100%);
            backdrop-filter: blur(10px);
            padding: 2rem;
            border-radius: 20px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.1);
            position: relative;
            overflow: hidden;
        }
        
        .main-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="20" cy="20" r="2" fill="rgba(255,255,255,0.1)"/><circle cx="80" cy="80" r="2" fill="rgba(255,255,255,0.1)"/><circle cx="40" cy="60" r="1" fill="rgba(255,255,255,0.1)"/></svg>');
            pointer-events: none;
        }
        
        .main-header h1 {
            font-size: 2.5rem;
            margin: 0 0 0.5rem 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            background: linear-gradient(45deg, #ffffff, #e3f2fd);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .main-header p {
            font-size: 1.2rem;
            margin: 0.5rem 0;
            opacity: 0.9;
        }
        
        .main-header small {
            opacity: 0.8;
            font-size: 0.9rem;
        }

        

        /* Enhanced form controls */
        .stSelectbox > div > div {
            background: #ffffff !important;
            border: 2px solid rgba(42, 82, 152, 0.2) !important;
            border-radius: 12px !important;
            transition: all 0.3s ease !important;
            margin-bottom: 1.5rem !important;  /* Add spacing between selectboxes */
        }
        
        .stSelectbox > div > div > div {
            color: #333333 !important;
            font-weight: 500 !important;
            font-size: 1rem !important;
        }

        /* Enhanced textarea styling */
        .stTextArea > div > div > textarea {
            background: #ffffff !important;
            border: 2px solid rgba(42, 82, 152, 0.2) !important;
            border-radius: 12px !important;
            font-size: 16px !important;
            color: #000000 !important;
            padding: 1rem !important;
            margin-top: 0.5rem !important;
        }
        
        .stTextArea > div > div > textarea::placeholder {
            color: #666666 !important;
            opacity: 1 !important;
        }

        /* Style for labels and text */
        .stSelectbox label, .stTextArea label {
            color: #333333 !important;
            font-weight: 600 !important;
            font-size: 1.1rem !important;
            margin-bottom: 0.5rem !important;
        }

        /* Enhanced button styling */
        .stButton > button {
            background: linear-gradient(135deg, #2a5298 0%, #1e3c72 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.75rem 2rem !important;
            font-weight: 600 !important;
            font-size: 1.1rem !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 4px 12px rgba(42, 82, 152, 0.3) !important;
            position: relative !important;
            overflow: hidden !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 20px rgba(42, 82, 152, 0.4) !important;
        }
        
        .stButton > button:active {
            transform: translateY(0) !important;
        }

        /* Chat message styling */
        .chat-message {
            padding: 1.5rem;
            border-radius: 16px;
            margin: 1rem 0;
            border: 1px solid rgba(42, 82, 152, 0.1);
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
            transition: all 0.3s ease;
        }
        
        .chat-message:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
        }
        
        .user-message {
            background: #3497f7;
            color: #ffffff;
        }
        
        .assistant-message {
            background: #3497f7;
            color: #ffffff;
            padding: 1.5rem;
            border-radius: 16px;
        }

        /* Enhanced subheader styling */
        .stMarkdown h3 {
            color: #2a5298;
            font-weight: 600;
            margin: 1.5rem 0 1rem 0;
            font-size: 1.4rem;
        }

        /* Improved info boxes */
        .stInfo > div {
            background: linear-gradient(135deg, rgba(227, 242, 253, 0.9) 0%, rgba(187, 222, 251, 0.9) 100%) !important;
            border: 1px solid rgba(33, 150, 243, 0.2) !important;
            border-radius: 12px !important;
            backdrop-filter: blur(5px) !important;
        }
        
        .stSuccess > div {
            background: linear-gradient(135deg, rgba(232, 245, 233, 0.9) 0%, rgba(200, 230, 201, 0.9) 100%) !important;
            border: 1px solid rgba(76, 175, 80, 0.2) !important;
            border-radius: 12px !important;
            backdrop-filter: blur(5px) !important;
        }
        
        .stWarning > div {
            background: linear-gradient(135deg, rgba(255, 243, 224, 0.9) 0%, rgba(255, 224, 178, 0.9) 100%) !important;
            border: 1px solid rgba(255, 152, 0, 0.2) !important;
            border-radius: 12px !important;
            backdrop-filter: blur(5px) !important;
        }

        /* Enhanced expander styling */
        .streamlit-expanderHeader {
            background: linear-gradient(135deg, rgba(248, 249, 250, 0.9) 0%, rgba(233, 236, 239, 0.9) 100%) !important;
            border-radius: 12px !important;
            border: 1px solid rgba(42, 82, 152, 0.1) !important;
        }

        /* Footer styling */
        .footer-container {
            margin-top: 3rem;
            padding: 2rem;
            background: linear-gradient(135deg, rgba(227, 242, 253, 0.9) 0%, rgba(187, 222, 251, 0.9) 100%);
            border-radius: 16px;
            border: 1px solid rgba(33, 150, 243, 0.2);
            text-align: center;
            backdrop-filter: blur(10px);
        }

        /* Responsive design */
        @media (max-width: 768px) {
            .main-header h1 {
                font-size: 2rem;
            }
            
            .feature-card {
                padding: 1rem;
            }
            
            .stButton > button {
                width: 100%;
                margin: 0.5rem 0;
            }
        }

        /* Loading animation */
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        .loading {
            animation: pulse 1.5s ease-in-out infinite;
        }

        /* Smooth scrolling */
        html {
            scroll-behavior: smooth;
        }

        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #2a5298 0%, #1e3c72 100%);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        }
    </style>
    """, unsafe_allow_html=True)