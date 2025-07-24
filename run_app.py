#!/usr/bin/env python3
"""
Telugu Legal Assistant - Application Runner
Enhanced version with improved features and better user experience
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def run_streamlit_app():
    """Run the Streamlit application"""
    print("🚀 Starting Telugu Legal Assistant...")
    print("📱 The application will open in your default web browser")
    print("🔗 If it doesn't open automatically, go to: http://localhost:8501")
    print("\n" + "="*60)
    print("TELUGU LEGAL ASSISTANT v2.0 - ENHANCED")
    print("⚖️ AI-Powered Legal Guidance for Telugu Speakers")
    print("="*60 + "\n")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.address", "localhost",
            "--server.port", "8501",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Application stopped. Thank you for using Telugu Legal Assistant!")
    except Exception as e:
        print(f"❌ Error running application: {e}")

def main():
    """Main function"""
    print("🔧 Telugu Legal Assistant Setup")
    print("-" * 40)
    
    # Check if we're in the correct directory
    if not os.path.exists("app.py"):
        print("❌ app.py not found. Please run this script from the project directory.")
        return
    
    # Check if requirements.txt exists
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found. Please ensure all files are present.")
        return
    
    # Install requirements
    if install_requirements():
        print("\n🎯 Setup complete! Starting application...")
        run_streamlit_app()
    else:
        print("❌ Setup failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
