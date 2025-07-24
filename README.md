# Telugu Legal Assistant - Enhanced Version 2.0 🏛️⚖️

An AI-powered legal guidance chatbot specifically designed for Telugu-speaking users, providing comprehensive legal information across various domains of Indian law.

## 🌟 New Features in Version 2.0

### 🎨 Enhanced User Interface
- **Modern Design**: Gradient backgrounds, improved card layouts, and better visual hierarchy
- **Responsive Layout**: Optimized for desktop and mobile devices  
- **Dark/Light Theme**: Better contrast and readability
- **Interactive Elements**: Hover effects and smooth transitions

### 🧠 Improved AI Capabilities
- **Multiple Model Support**: DialoGPT-Large, FLAN-T5-Base, and fallback options
- **Enhanced Prompts**: More detailed legal context and better response quality
- **Better Error Handling**: Graceful fallbacks and retry mechanisms
- **Memory Optimization**: Efficient model loading for 8GB RAM systems

### 💬 Advanced Chat Features
- **Chat History**: Persistent conversation storage and management
- **Export Functionality**: Download chat history as JSON
- **Language Options**: Telugu only, English only, or bilingual responses
- **Quick Actions**: Copy, rate, and follow-up on responses

### ⚙️ Smart Configuration
- **Model Selection**: Choose AI model based on system capabilities
- **Progress Tracking**: Real-time loading and processing indicators
- **Session Management**: Maintain state across interactions
- **Performance Metrics**: System status and usage statistics

## 📚 Supported Legal Areas

### 1. 🚨 క్రిమినల్ లా (Criminal Law)
- FIR filing procedures
- Arrest rights and bail applications
- Police custody rights
- Cyber crime reporting
- Dowry harassment cases

### 2. ⚖️ సివిల్ లా (Civil Law)
- Property disputes
- Contract breach cases
- Injunction procedures
- Damage claims
- Rental disputes

### 3. 👨‍👩‍👧‍👦 కుటుంబ న్యాయం (Family Law)
- Divorce procedures
- Child custody laws
- Marriage annulment
- Domestic violence protection
- Maintenance claims

### 4. 🏠 ఆస్తి చట్టం (Property Law)
- Will writing
- Property registration
- Inheritance rights
- Land disputes
- Survey settlements

### 5. 🛒 వినియోగదారు చట్టం (Consumer Law)
- Consumer complaints
- Online fraud reporting
- Product return rights
- Service charge disputes
- Banking issues

### 6. 💼 కార్మిక చట్టం (Labor Law)
- Job termination procedures
- Salary disputes
- Labor court complaints
- EPF and gratuity claims
- Workplace rights

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- 8GB RAM (minimum 4GB)
- Internet connection for translation services
- Modern web browser

### Installation

1. **Clone or Download** the project files
2. **Open Terminal/PowerShell** in the project directory
3. **Run the setup script**:
   ```bash
   python run_app.py
   ```

### Manual Installation

If the automatic setup doesn't work:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

## 🎯 How to Use

### Basic Usage
1. **Select Category**: Choose your legal issue type from the dropdown
2. **Pick Question**: Select a preset question or write your own custom query
3. **Configure Settings**: Use the sidebar to adjust model and language preferences
4. **Get Answer**: Click the "Get Answer" button to receive AI-generated guidance
5. **Review Response**: Read the detailed legal guidance provided
6. **Take Action**: Follow the suggested steps and consult a lawyer for specific cases

### Advanced Features
- **Chat History**: View and manage previous conversations
- **Export Data**: Download your chat history for record-keeping
- **Model Selection**: Choose between different AI models based on your system
- **Language Control**: Select your preferred response language
- **Quick Actions**: Copy responses, rate answers, and ask follow-ups

## 🔧 Technical Specifications

### AI Models
- **Primary**: Microsoft DialoGPT-Large (advanced conversational AI)
- **Secondary**: Google FLAN-T5-Base (text-to-text generation)
- **Fallback**: FLAN-T5-Small (lightweight option)

### Translation
- **Service**: Google Translate API
- **Languages**: Telugu ↔ English
- **Fallback**: Original text if translation fails

### Performance
- **Memory Usage**: Optimized for 8GB RAM
- **Response Time**: 10-30 seconds depending on model and query
- **Accuracy**: Based on training data up to model cutoff dates

## 📱 System Requirements

### Minimum
- **OS**: Windows 10, macOS 10.14, Ubuntu 18.04
- **RAM**: 4GB (8GB recommended)
- **Storage**: 2GB free space
- **Network**: Stable internet connection

### Recommended
- **RAM**: 8GB or higher
- **GPU**: NVIDIA GPU with CUDA support (optional)
- **Network**: High-speed internet for faster translations

## ⚠️ Important Legal Disclaimer

### 🔴 Critical Limitations
- **General Information Only**: This AI provides general legal information, not personalized advice
- **Not Legal Representation**: Cannot replace qualified legal professionals
- **No Attorney-Client Privilege**: Using this service creates no legal relationship
- **Accuracy Disclaimer**: Legal information may change or vary by jurisdiction

### ✅ When to Consult a Lawyer
- Before filing any legal case or application
- When drafting important legal documents
- If involved in any legal dispute
- For interpretation of specific laws to your situation
- Before making important legal decisions

### 📞 Emergency Legal Contacts
- **National Legal Services Authority**: 15100 (Toll-free)
- **Women Helpline**: 181
- **Child Helpline**: 1098
- **Cyber Crime**: 1930
- **Police**: 100

## 🔧 Troubleshooting

### Common Issues

#### Model Loading Fails
- **Solution**: Check internet connection and try fallback model
- **Alternative**: Restart application and select smaller model

#### Translation Errors
- **Solution**: Verify internet connection
- **Alternative**: Use English-only mode

#### Performance Issues
- **Solution**: Close other applications to free RAM
- **Alternative**: Select FLAN-T5-Small model

#### Application Won't Start
- **Solution**: Ensure Python and dependencies are installed
- **Command**: `pip install -r requirements.txt`

## 📈 Performance Optimization

### For Better Speed
1. Use **English-only** responses
2. Select **FLAN-T5-Base** model for faster loading
3. Close unnecessary applications
4. Use **wired internet** connection

### For Better Accuracy
1. Use **DialoGPT-Large** model
2. Enable **bilingual** responses
3. Provide **detailed questions**
4. Select appropriate **legal category**

## 🤝 Contributing

### Feedback
- Use the sidebar feedback section in the app
- Report issues through the application interface
- Suggest improvements for legal categories

### Development
- Legal experts can contribute to prompt engineering
- Developers can enhance UI/UX features
- Translators can improve Telugu language support

## 📊 Version History

### v2.0.0 (Current) - Enhanced Release
- ✅ Complete UI/UX overhaul
- ✅ Advanced chat management
- ✅ Multiple AI model support
- ✅ Enhanced error handling
- ✅ Performance optimizations
- ✅ Better mobile responsiveness

### v1.0.0 - Initial Release
- ✅ Basic Telugu legal assistance
- ✅ Simple Q&A interface
- ✅ Single model support
- ✅ Basic translation

## 📝 License

This project is developed for educational and informational purposes. Not for commercial legal practice.

## 🔗 Support

For technical support or legal guidance:
- Use the in-app feedback system
- Consult qualified legal professionals for specific cases
- Refer to official legal resources and authorities

---

**Developed with ❤️ for the Telugu-speaking legal community**

*Remember: "Justice delayed is justice denied" - Seek timely legal help when needed!* ⚖️
