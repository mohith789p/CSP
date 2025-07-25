import streamlit as st
from config import APP_CONFIG, TEXT_CONSTANTS

def display_header(language):
    """Display the main header with title and subtitle"""
    if language == 'Telugu':
        st.markdown(f"""
        <div class="main-header">
            <h1>⚖️ {APP_CONFIG['TITLE_TELUGU']}</h1>
            <p>{APP_CONFIG['SUBTITLE_TELUGU']}</p>
            <small>{APP_CONFIG['POWERED_BY']}</small>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.subheader(TEXT_CONSTANTS['TELUGU']['LEGAL_CATEGORIES'])
        st.markdown("మీ ప్రశ్నకు సంబంధించిన విభాగాన్ని ఎంచుకుని, సహాయం పొందండి")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="main-header">
            <h1>⚖️ {APP_CONFIG['TITLE_ENGLISH']}</h1>
            <p>{APP_CONFIG['SUBTITLE_ENGLISH']}</p>
            <small>{APP_CONFIG['POWERED_BY']}</small>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.subheader(TEXT_CONSTANTS['ENGLISH']['LEGAL_CATEGORIES'])
        st.markdown("Select the relevant legal category and get assistance with your queries")
        st.markdown('</div>', unsafe_allow_html=True)

def select_category_and_question(language, legal_categories):
    """Display category and question selection interface"""
    
    if language == 'Telugu':
        st.markdown("##### వర్గాన్ని ఎంచుకోండి:")
        selected_category = st.selectbox(
            "",  # Empty label since we're using markdown above
            list(legal_categories.keys()),
            help="మీ ప్రశ్న సంబంధిత విభాగాన్ని ఎంచుకోండి",
            key="category_select"
        )
        
        st.markdown("<div style='height: 1.5rem'></div>", unsafe_allow_html=True)  # Add space
        
        questions = legal_categories.get(selected_category, [])
        st.markdown("##### ప్రశ్నను ఎంచుకోండి:")
        selected_question = st.selectbox(
            "",  # Empty label since we're using markdown above
            [TEXT_CONSTANTS['TELUGU']['CUSTOM_QUESTION']] + questions,
            help="ముందుగా తయారు చేసిన ప్రశ్న ఎంచుకోండి లేదా మీ స్వంత ప్రశ్న రాయండి",
            key="question_select"
        )
    else:
        # Similar updates for English version
        st.markdown("##### Select Category:")
        selected_category = st.selectbox(
            "",
            list(legal_categories.keys()),
            help="Choose the legal category related to your question",
            key="category_select"
        )
        
        st.markdown("<div style='height: 1.5rem'></div>", unsafe_allow_html=True)  # Add space
        
        questions = legal_categories.get(selected_category, [])
        st.markdown("##### Select Question:")
        selected_question = st.selectbox(
            "",
            [TEXT_CONSTANTS['ENGLISH']['CUSTOM_QUESTION']] + questions,
            help="Choose a preset question or write your own custom question",
            key="question_select"
        )
    
    return selected_category, selected_question

def display_recent_chat(language):
    """Display recent chat history in an expandable section"""
    if st.session_state.chat_history:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        
        if language == 'Telugu':
            expander_title = f"{TEXT_CONSTANTS['TELUGU']['RECENT_CONVERSATIONS']} ({len(st.session_state.chat_history)} మొత్తం)"
            with st.expander(expander_title, expanded=False):
                for i, chat in enumerate(reversed(st.session_state.chat_history[-5:])):
                    display_chat_item(chat, len(st.session_state.chat_history) - i, language)
        else:
            expander_title = f"{TEXT_CONSTANTS['ENGLISH']['RECENT_CONVERSATIONS']} ({len(st.session_state.chat_history)} total)"
            with st.expander(expander_title, expanded=False):
                for i, chat in enumerate(reversed(st.session_state.chat_history[-5:])):
                    display_chat_item(chat, len(st.session_state.chat_history) - i, language)
        
        st.markdown('</div>', unsafe_allow_html=True)

def display_chat_item(chat, chat_number, language):
    """Display individual chat item with proper formatting"""
    if language == 'Telugu':
        question_label = "ప్రశ్న:"
        answer_label = "సమాధానం:"
        unknown_time = "తెలియని సమయం"
        unknown_category = "తెలియని వర్గం"
        unknown_question = "తెలియని ప్రశ్న"
        unknown_response = "తెలియని సమాధానం"
    else:
        question_label = "Q:"
        answer_label = "A:"
        unknown_time = "Unknown time"
        unknown_category = "Unknown category"
        unknown_question = "Unknown question"
        unknown_response = "Unknown response"
    
    st.markdown(f"""
    <div class="chat-message">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem;">
            <strong style="color: #2a5298;">#{chat_number}</strong>
            <small style="color: #666;">{chat.get('timestamp', unknown_time)} | {chat.get('category', unknown_category)}</small>
        </div>
        <div style="margin-bottom: 0.5rem;">
            <strong style="color: #1976d2;">{question_label}</strong> 
            <span style="margin-left: 0.5rem;">{chat.get('question', unknown_question)[:100]}{'...' if len(chat.get('question', '')) > 100 else ''}</span>
        </div>
        <div>
            <strong style="color: #9c27b0;">{answer_label}</strong> 
            <span style="margin-left: 0.5rem;">{chat.get('response', unknown_response)[:150]}{'...' if len(chat.get('response', '')) > 150 else ''}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def input_area(language, selected_question):
    """Display the input area for questions"""
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    
    if language == 'Telugu':
        custom_question_option = TEXT_CONSTANTS['TELUGU']['CUSTOM_QUESTION']
        if selected_question == custom_question_option:
            st.markdown(f"### {TEXT_CONSTANTS['TELUGU']['TYPE_QUESTION']}")
            user_query = st.text_area(
                "",
                height=120,
                placeholder="ఉదాహరణ: నాకు ఒక ఇంట్లో వివాదం ఉంది, నేను ఏం చేయాలి? లేదా నా ఉద్యోగంలో సమస్యలు ఉన్నాయి...",
                help="మీ న్యాయ ప్రశ్నను తెలుగులో స్పష్టంగా వ్రాయండి",
                key="custom_question"
            )
        else:
            st.markdown(f"### {TEXT_CONSTANTS['TELUGU']['SELECTED_QUESTION']}")
            user_query = selected_question
            st.text_area("", value=selected_question, height=100, disabled=True, key="selected_question")
    else:
        custom_question_option = TEXT_CONSTANTS['ENGLISH']['CUSTOM_QUESTION']
        if selected_question == custom_question_option:
            st.markdown(f"### {TEXT_CONSTANTS['ENGLISH']['TYPE_QUESTION']}")
            user_query = st.text_area(
                "",
                height=120,
                placeholder="Example: I have a property dispute, what should I do? Or I'm facing issues at my workplace...",
                help="Please write your legal question clearly in English",
                key="custom_question"
            )
        else:
            st.markdown(f"### {TEXT_CONSTANTS['ENGLISH']['SELECTED_QUESTION']}")
            user_query = selected_question
            st.text_area("", value=selected_question, height=100, disabled=True, key="selected_question")
    
    st.markdown('</div>', unsafe_allow_html=True)
    return user_query

def display_legal_disclaimer(language):
    """Display comprehensive legal disclaimer and information"""
    st.markdown("---")
    
    if language == 'English':
        st.markdown(f"### {TEXT_CONSTANTS['ENGLISH']['LEGAL_DISCLAIMER']}")
    else:
        st.markdown(f"### {TEXT_CONSTANTS['TELUGU']['LEGAL_DISCLAIMER']}")

    col1, col2 = st.columns(2)

    with col1:
        display_limitations_card()
        display_emergency_contacts_card()

    with col2:
        display_consultation_advice_card()
        display_app_statistics_card()

def display_limitations_card():
    """Display important limitations information"""
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("#### 🔴 Important Limitations")
    st.info("""
    • **General Information Only**: This AI provides general legal information, not personalized legal advice

    • **Not a Lawyer**: This system cannot replace consultation with qualified legal professionals

    • **Accuracy**: While we strive for accuracy, legal information may change or vary by jurisdiction

    • **No Attorney-Client Relationship**: Using this service does not create any legal relationship
    """)
    st.markdown('</div>', unsafe_allow_html=True)

def display_emergency_contacts_card():
    """Display emergency contact information"""
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("#### 📞 Emergency Legal Help")
    st.warning(f"""
    • **National Legal Services Authority**: {APP_CONFIG['EMERGENCY_CONTACTS']['NLSA']} (Toll-free)

    • **Women Helpline**: {APP_CONFIG['EMERGENCY_CONTACTS']['WOMEN_HELPLINE']}

    • **Child Helpline**: {APP_CONFIG['EMERGENCY_CONTACTS']['CHILD_HELPLINE']}

    • **Cyber Crime**: {APP_CONFIG['EMERGENCY_CONTACTS']['CYBER_CRIME']}

    • **Police**: {APP_CONFIG['EMERGENCY_CONTACTS']['POLICE']}
    """)
    st.markdown('</div>', unsafe_allow_html=True)

def display_consultation_advice_card():
    """Display when to consult a lawyer advice"""
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("#### ✅ When to Consult a Lawyer")
    st.success("""
    • **Before filing any legal case** or application

    • **When drafting important legal documents**

    • **If you're involved in any legal dispute**

    • **For interpretation of specific laws** to your situation

    • **Before making important legal decisions**
    """)
    st.markdown('</div>', unsafe_allow_html=True)

def display_app_statistics_card():
    """Display application statistics"""
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("#### 📊 Application Statistics")
    st.info("""
    • **Total Categories**: 6 Legal Areas

    • **Preset Questions**: 32+ Sample Questions

    • **AI Models**: 3 Advanced Models

    • **Languages**: Telugu & English Support
    """)
    st.markdown('</div>', unsafe_allow_html=True)

def display_footer(language):
    """Display application footer with version information"""
    if language == 'Telugu':
        st.markdown(f"""
        <div class="footer-container">
            <h4 style="color: #2a5298; margin-bottom: 1rem;">{TEXT_CONSTANTS['TELUGU']['THANK_YOU']}</h4>
            <p style="color: #1976d2; margin: 0;">
                {TEXT_CONSTANTS['TELUGU']['DEVELOPED_WITH_LOVE']}
            </p>
            <small style="color: #666; margin-top: 0.5rem; display: block;">
                వెర్షన్ {APP_CONFIG['VERSION']} మెరుగుపరచబడింది | ద్విభాష ఎడిషన్ | AI-Powered Legal Assistant
            </small>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="footer-container">
            <h4 style="color: #2a5298; margin-bottom: 1rem;">{TEXT_CONSTANTS['ENGLISH']['THANK_YOU']}</h4>
            <p style="color: #1976d2; margin: 0;">
                {TEXT_CONSTANTS['ENGLISH']['DEVELOPED_WITH_LOVE']}
            </p>
            <small style="color: #666; margin-top: 0.5rem; display: block;">
                Version {APP_CONFIG['VERSION']} Enhanced | Bilingual Edition | AI-Powered Legal Assistant
            </small>
        </div>
        """, unsafe_allow_html=True)

def display_loading_animation():
    """Display loading animation"""
    st.markdown("""
    <div class="loading" style="text-align: center; padding: 2rem;">
        <div style="display: inline-block; width: 40px; height: 40px; border: 3px solid #f3f3f3; border-top: 3px solid #2a5298; border-radius: 50%; animation: spin 1s linear infinite;"></div>
        <p style="margin-top: 1rem; color: #2a5298;">Processing your query...</p>
    </div>
    <style>
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
    """, unsafe_allow_html=True)

def display_success_message(message, language="English"):
    """Display success message with proper styling"""
    if language == 'Telugu':
        success_icon = "✅ విజయవంతం"
    else:
        success_icon = "✅ Success"
    
    st.markdown(f"""
    <div class="feature-card" style="border-left: 4px solid #4caf50;">
        <div style="color: #4caf50; font-weight: 600; margin-bottom: 0.5rem;">
            {success_icon}
        </div>
        <div style="color: #333;">
            {message}
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_error_message(message, language="English"):
    """Display error message with proper styling"""
    if language == 'Telugu':
        error_icon = "❌ లోపం"
    else:
        error_icon = "❌ Error"
    
    st.markdown(f"""
    <div class="feature-card" style="border-left: 4px solid #f44336;">
        <div style="color: #f44336; font-weight: 600; margin-bottom: 0.5rem;">
            {error_icon}
        </div>
        <div style="color: #333;">
            {message}
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_info_message(message, language="English"):
    """Display info message with proper styling"""
    if language == 'Telugu':
        info_icon = "ℹ️ సమాచారం"
    else:
        info_icon = "ℹ️ Information"
    
    st.markdown(f"""
    <div class="feature-card" style="border-left: 4px solid #2196f3;">
        <div style="color: #2196f3; font-weight: 600; margin-bottom: 0.5rem;">
            {info_icon}
        </div>
        <div style="color: #333;">
            {message}
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_warning_message(message, language="English"):
    """Display warning message with proper styling"""
    if language == 'Telugu':
        warning_icon = "⚠️ హెచ్చరిక"
    else:
        warning_icon = "⚠️ Warning"
    
    st.markdown(f"""
    <div class="feature-card" style="border-left: 4px solid #ff9800;">
        <div style="color: #ff9800; font-weight: 600; margin-bottom: 0.5rem;">
            {warning_icon}
        </div>
        <div style="color: #333;">
            {message}
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_action_button(label, key, help_text=None, disabled=False):
    """Create a styled action button"""
    return st.button(
        label,
        key=key,
        help=help_text,
        disabled=disabled,
        use_container_width=True
    )

def display_language_selector():
    """Display language selection interface"""
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("#### 🌐 Language Selection / భాష ఎంపిక")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🇮🇳 తెలుగు (Telugu)", key="telugu_btn", use_container_width=True):
            st.session_state.language = 'Telugu'
            st.rerun()
    
    with col2:
        if st.button("🇬🇧 English", key="english_btn", use_container_width=True):
            st.session_state.language = 'English'
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_chat_response(response, language):
    """Display AI response with proper formatting"""
    st.markdown('<div class="feature-card assistant-message" style="opacity: 1;">', unsafe_allow_html=True)
    
    if language == 'Telugu':
        st.markdown("### 🤖 సమాధానం:")
    else:
        st.markdown("### 🤖 AI Response:")
    
    st.markdown(f"""
    <div style="background: rgba(255, 255, 255, 0.95); padding: 1.2rem; border-radius: 12px; margin-top: 0.5rem;">
        {response}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_user_query(query, language):
    """Display user query with proper formatting"""
    st.markdown('<div class="feature-card user-message" style="opacity: 1;">', unsafe_allow_html=True)
    
    if language == 'Telugu':
        st.markdown("### 👤 మీ ప్రశ్న:")
    else:
        st.markdown("### 👤 Your Question:")
    
    st.markdown(f"""
    <div style="background: rgba(255, 255, 255, 0.95); padding: 1.2rem; border-radius: 12px; margin-top: 0.5rem;">
        {query}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_sidebar_info(language):
    """Display sidebar information and controls"""
    if language == 'Telugu':
        st.sidebar.markdown("### 📚 అదనపు సమాచారం")
        st.sidebar.info("""
        **ఈ అప్లికేషన్ గురించి:**
        
        • AI ఆధారిత న్యాయ సహాయం
        • 6 ప్రధాన న్యాయ విభాగాలు
        • 32+ ముందుగా తయారు చేసిన ప్రశ్నలు
        • తెలుగు మరియు ఇంగ్లీష్ మద్దతు
        """)
        
        st.sidebar.warning("""
        **గుర్తుంచుకోండి:**
        
        • ఇది సాధారణ సమాచారం మాత్రమే
        • న్యాయవాది సలహా తీసుకోండి
        • ముఖ్యమైన విషయాలకు నిపుణుల సహాయం అవసరం
        """)
    else:
        st.sidebar.markdown("### 📚 Additional Information")
        st.sidebar.info("""
        **About This Application:**
        
        • AI-powered legal assistance
        • 6 major legal categories
        • 32+ preset questions
        • Telugu and English support
        """)
        
        st.sidebar.warning("""
        **Remember:**
        
        • This provides general information only
        • Consult a qualified lawyer
        • Seek professional help for important matters
        """)

def clear_chat_history(language):
    """Clear chat history with confirmation"""
    if language == 'Telugu':
        if st.button("🗑️ చాట్ చరిత్రను క్లియర్ చేయండి", key="clear_history"):
            st.session_state.chat_history = []
            display_success_message("చాట్ చరిత్రను విజయవంతంగా క్లియర్ చేసారు!", language)
    else:
        if st.button("🗑️ Clear Chat History", key="clear_history"):
            st.session_state.chat_history = []
            display_success_message("Chat history cleared successfully!", language)