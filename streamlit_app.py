import streamlit as st
import google.generativeai as genai

# 1. Professional Page Config
st.set_page_config(page_title="Burmese AI Pro", page_icon="🇲🇲", layout="centered")

# 2. Beautiful Custom CSS
st.markdown("""
    <style>
    /* Main Background */
    .stApp { background-color: #0E1117; color: white; }
    
    /* Center the Title */
    .main-title { text-align: center; color: #FF4B4B; font-size: 40px; font-weight: bold; margin-bottom: 20px; }
    
    /* Style Buttons */
    div.stButton > button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        border-radius: 10px;
        height: 50px;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    div.stButton > button:hover { background-color: #FF2B2B; transform: scale(1.02); }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] { background-color: #1A1C24; border-right: 1px solid #3d445a; }
    
    /* Hide Streamlit Branding */
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">🇲🇲 Burmese AI Pro</div>', unsafe_allow_html=True)

# 3. Sidebar Setup
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Gemini API Key", type="password", placeholder="Paste your key here...")
    st.divider()
    st.info("Ensure your VPN is OFF for the best speed in Thailand.")

if api_key:
    genai.configure(api_key=api_key)
    
    # 4. Clean Layout using Columns
    col1, col2 = st.columns(2)
    with col1:
        tone = st.selectbox("🎭 Select Tone", ["Comedy 😊", "Horror 💀", "Drama 🤍", "Action ⚡"])
    with col2:
        model_choice = st.selectbox("🤖 AI Model", ["gemini-1.5-pro (Better)", "gemini-1.5-flash (Faster)"])

    st.markdown("---")
    
    # 5. File Uploader
    uploaded_file = st.file_uploader("📂 Upload English SRT File", type=['srt'])
    
    if uploaded_file:
        content = uploaded_file.getvalue().decode("utf-8")
        with st.expander("👁️ Preview Original Script"):
            st.text(content[:1000])

        if st.button("🚀 Start Translation"):
            # Model Selection
            model_name = 'gemini-1.5-pro' if "pro" in model_choice else 'gemini-1.5-flash'
            model = genai.GenerativeModel(model_name)
            
            prompt = f"Translate this movie script/SRT to natural Burmese with a {tone} style. Output ONLY the SRT content. Keep all timestamps identical. Content: \n\n{content}"
            
            with st.spinner("Translating... Please stay on this page."):
                try:
                    response = model.generate_content(prompt)
                    clean_srt = response.text.strip().replace("```srt", "").replace("```", "").strip()
                    
                    st.success("✅ Movie-Ready Translation Complete!")
                    st.text_area("Result Preview", clean_srt[:1000], height=250)
                    
                    st.download_button(
                        label="📥 Download Burmese SRT",
                        data=clean_srt,
                        file_name="movie_burmese.srt",
                        mime="text/plain"
                    )
                except Exception as e:
                    st.error(f"Error: {e}")
else:
    st.warning("👈 Please enter your API key in the sidebar to begin.")
  
