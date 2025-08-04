import streamlit as st
import requests
import time


# --- Page Configuration ---
st.set_page_config(
    page_title="Smart Document Scanner",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- App State for Dark Mode ---
if 'darkmode' not in st.session_state:
    st.session_state.darkmode = True  # Default to dark mode

# --- Dark/Light Mode Toggle ---
def switch_mode():
    st.session_state.darkmode = not st.session_state.darkmode
    st.rerun()

# --- Theme Colors ---
if st.session_state.darkmode:
    bg_color = "#1a1a1a"
    card_bg = "#2d2d2d"
    text_color = "#ffffff"
    accent_color = "#00d4aa"
    secondary_color = "#0099cc"
    border_color = "#404040"
    success_color = "#00cc88"
    error_color = "#ff6b6b"
else:
    bg_color = "#ffffff"
    card_bg = "#f8f9fa"
    text_color = "#2c3e50"
    accent_color = "#007acc"
    secondary_color = "#0056b3"
    border_color = "#dee2e6"
    success_color = "#28a745"
    error_color = "#dc3545"

# --- Working CSS for Streamlit ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main app styling */
    .stApp {{
        background-color: {bg_color} !important;
        font-family: 'Inter', sans-serif !important;
    }}
    
    /* Main container */
    .main .block-container {{
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        max-width: 1000px !important;
    }}
    
    /* Fix all text colors */
    .stApp, .stApp p, .stApp span, .stApp div, .stApp h1, .stApp h2, .stApp h3, 
    .stApp h4, .stApp h5, .stApp h6, .stApp label, .stMarkdown, .stMarkdown p,
    .stMarkdown div, .stMarkdown span, .stText {{
        color: {text_color} !important;
        font-family: 'Inter', sans-serif !important;
    }}
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {{
        color: {text_color} !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
    }}
    
    /* Physics Light Bulb Toggle */
    .bulb-toggle {{
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        cursor: pointer;
        display: flex;
        flex-direction: column;
        align-items: center;
        background: transparent;
    }}
    
    .bulb-string {{
        width: 3px;
        height: 50px;
        background: #8b7355;
        border-radius: 2px;
        margin-bottom: 3px;
        transform-origin: top center;
        transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    }}
    
    .bulb-light {{
        width: 40px;
        height: 55px;
        background: {'#ffd700' if st.session_state.darkmode else '#fff5b7'};
        border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
        position: relative;
        box-shadow: 0 0 20px {'rgba(255, 215, 0, 0.8)' if st.session_state.darkmode else 'rgba(255, 245, 183, 0.6)'};
        border: 2px solid {border_color};
        transition: all 0.3s ease;
        transform-origin: top center;
    }}
    
    .bulb-light:hover {{
        transform: scale(1.1) rotate(8deg);
        box-shadow: 0 0 30px {'rgba(255, 215, 0, 1)' if st.session_state.darkmode else 'rgba(255, 245, 183, 0.8)'};
    }}
    
    .bulb-light::after {{
        content: '';
        position: absolute;
        bottom: -6px;
        left: 50%;
        transform: translateX(-50%);
        width: 22px;
        height: 10px;
        background: {border_color};
        border-radius: 0 0 3px 3px;
    }}
    
    .bulb-swing {{
        animation: bulbSwing 1s ease-in-out;
    }}
    
    @keyframes bulbSwing {{
        0%, 100% {{ transform: rotate(0deg); }}
        25% {{ transform: rotate(15deg); }}
        75% {{ transform: rotate(-15deg); }}
    }}
    
    /* Custom styled containers using HTML */
    .custom-container {{
        background: {card_bg} !important;
        border: 1px solid {border_color} !important;
        border-radius: 20px !important;
        padding: 2rem !important;
        margin: 1.5rem 0 !important;
        box-shadow: 0 8px 32px rgba(0,0,0,{'0.3' if st.session_state.darkmode else '0.1'}) !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px) !important;
    }}
    
    .custom-container:hover {{
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 40px rgba(0,0,0,{'0.4' if st.session_state.darkmode else '0.15'}) !important;
    }}
    
    /* File uploader styling */
    [data-testid="stFileUploader"] {{
        background: {card_bg} !important;
        border: 2px dashed {accent_color} !important;
        border-radius: 20px !important;
        padding: 2rem !important;
    }}
    
    [data-testid="stFileUploader"]:hover {{
        border-color: {secondary_color} !important;
        background: {card_bg} !important;
        transform: scale(1.01) !important;
    }}
    
    [data-testid="stFileUploader"] label {{
        color: {text_color} !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }}
    
    [data-testid="stFileUploader"] > div > div > div {{
        text-align: center !important;
    }}
    
    /* Button styling */
    .stButton > button {{
        background: linear-gradient(135deg, {secondary_color}, {accent_color}) !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 0.8rem 2rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.2) !important;
        min-height: 50px !important;
        width: 100% !important;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3) !important;
        filter: brightness(1.1) !important;
    }}
    
    /* Success and error messages */
    .stSuccess > div {{
        background: {success_color} !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 1rem 1.5rem !important;
        font-weight: 500 !important;
        border: none !important;
        font-size: 1rem !important;
    }}
    
    .stError > div {{
        background: {error_color} !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 1rem 1.5rem !important;
        font-weight: 500 !important;
        border: none !important;
        font-size: 1rem !important;
    }}
    
    /* Metrics styling */
    [data-testid="metric-container"] {{
        background: {card_bg} !important;
        border: 1px solid {border_color} !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        text-align: center !important;
        box-shadow: 0 4px 15px rgba(0,0,0,{'0.2' if st.session_state.darkmode else '0.1'}) !important;
    }}
    
    [data-testid="metric-container"] [data-testid="metric-container"] > div:first-child {{
        color: {text_color} !important;
        opacity: 0.7 !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
    }}
    
    [data-testid="metric-container"] [data-testid="metric-container"] > div:last-child {{
        color: {accent_color} !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
    }}
    
    /* Image styling */
    [data-testid="stImage"] img {{
        border-radius: 15px !important;
        box-shadow: 0 8px 25px rgba(0,0,0,{'0.3' if st.session_state.darkmode else '0.15'}) !important;
        transition: all 0.3s ease !important;
    }}
    
    [data-testid="stImage"]:hover img {{
        transform: scale(1.02) !important;
        box-shadow: 0 12px 35px rgba(0,0,0,{'0.4' if st.session_state.darkmode else '0.2'}) !important;
    }}
    
    /* Expander styling */
    [data-testid="stExpander"] {{
        background: {card_bg} !important;
        border: 1px solid {border_color} !important;
        border-radius: 12px !important;
        margin: 1rem 0 !important;
    }}
    
    [data-testid="stExpander"] > div:first-child {{
        background: {card_bg} !important;
        color: {text_color} !important;
        font-weight: 600 !important;
        border-radius: 12px 12px 0 0 !important;
    }}
    
    [data-testid="stExpander"] [data-testid="stExpanderToggleIcon"] {{
        color: {text_color} !important;
    }}
    
    /* JSON display */
    .stJson {{
        background: rgba(0,0,0,0.1) !important;
        border-radius: 8px !important;
        border: 1px solid {border_color} !important;
        color: {text_color} !important;
    }}
    
    /* Spinner */
    .stSpinner > div {{
        border-top-color: {accent_color} !important;
    }}
    
    /* Hide default elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    .stDeployButton {{display: none;}}
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {{
        .bulb-toggle {{
            top: 15px;
            right: 15px;
            transform: scale(0.8);
        }}
        
        .custom-container {{
            padding: 1.5rem !important;
            margin: 1rem 0 !important;
        }}
        
        [data-testid="stFileUploader"] {{
            padding: 1.5rem !important;
        }}
    }}
</style>
""", unsafe_allow_html=True)


# --- Light Bulb Toggle with Click Handler ---
bulb_animation = "bulb-swing" if st.session_state.get('just_toggled') else ""

st.markdown(f"""
<div class="bulb-toggle" onclick="toggleTheme()" title="Click to switch theme">
    <div class="bulb-string"></div>
    <div class="bulb-light {bulb_animation}"></div>
</div>

<script>
function toggleTheme() {{
    // Find and click the hidden toggle button
    const buttons = window.parent.document.querySelectorAll('button');
    for (let btn of buttons) {{
        if (btn.textContent.includes('Toggle Theme')) {{
            btn.click();
            break;
        }}
    }}
}}
</script>
""", unsafe_allow_html=True)

# --- Hidden Toggle Button ---
if st.button("Toggle Theme", key="hidden_toggle", help="Switch between light and dark mode"):
    st.session_state.just_toggled = True
    switch_mode()

if st.session_state.get('just_toggled'):
    st.session_state.just_toggled = False

# --- Header ---
st.markdown(f"""
<div style="text-align: center; padding: 2rem 0; margin-bottom: 1rem;">
    <h1 style="font-size: 3rem; font-weight: 700; color: {text_color}; margin-bottom: 1rem; line-height: 1.2;">
        📸 Smart Document Scanner
    </h1>
    <p style="font-size: 1.2rem; color: {text_color}; opacity: 0.8; max-width: 700px; margin: 0 auto; line-height: 1.6;">
        Upload a photo of your document and our AI will automatically extract key information 
        like ED Number, Date, and recipient details, then send everything to your Google Sheet.
    </p>
</div>
""", unsafe_allow_html=True)

# --- File Upload Section ---
st.markdown(f'<div class="custom-container">', unsafe_allow_html=True)
st.markdown(f"<h3 style='color: {text_color}; margin-bottom: 1rem;'>📁 Upload Document</h3>", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Choose your document image (JPG, PNG, JPEG)",
    type=["jpg", "jpeg", "png"],
    help="For best results, ensure good lighting and clear text visibility"
)
st.markdown('</div>', unsafe_allow_html=True)

# --- Process Upload ---
if uploaded_file:
    # Image Preview
    st.markdown(f'<div class="custom-container">', unsafe_allow_html=True)
    st.markdown(f"<h3 style='color: {text_color}; margin-bottom: 1rem;'>🖼️ Document Preview</h3>", unsafe_allow_html=True)
    st.image(uploaded_file, use_container_width=True, caption="Your uploaded document")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Processing Section
    st.markdown(f'<div class="custom-container">', unsafe_allow_html=True)
    st.markdown(f"<h3 style='color: {text_color}; margin-bottom: 1rem;'>🚀 Process Document</h3>", unsafe_allow_html=True)
    
    if st.button("Extract Information & Send to Google Sheet", key="process_btn"):
        with st.spinner("📊 Analyzing document and extracting information..."):
            try:
                # TODO: Replace with your actual webhook URL
                n8n_url = "https://n8n-railway-production-9cf8.up.railway.app/webhook/e8fada1c-1a55-4bd1-af8f-b97c848cc477"
                
                files = {"image": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                response = requests.post(n8n_url, files=files)

                if response.status_code == 200:
                    st.success("✅ Document processed successfully! Your Google Sheet has been updated.")
                    
                    # Display extracted data
                    try:
                        if response.headers.get("Content-Type", "").startswith("application/json"):
                            resp_json = response.json()
                            if isinstance(resp_json, dict) and resp_json:
                                st.markdown(f"<h4 style='color: {text_color}; margin: 1.5rem 0 1rem 0;'>📋 Extracted Information</h4>", unsafe_allow_html=True)
                                
                                # Create metrics display
                                col1, col2, col3 = st.columns(3)
                                
                                with col1:
                                    if 'ed_number' in resp_json:
                                        st.metric("📄 ED Number", resp_json['ed_number'])
                                
                                with col2:
                                    if 'date' in resp_json:
                                        st.metric("📅 Date", resp_json['date'])
                                
                                with col3:
                                    if 'to_name' in resp_json:
                                        st.metric("👤 To Name", resp_json['to_name'])
                                
                                # Expandable JSON view
                                with st.expander("📄 View Complete Data"):
                                    st.json(resp_json)
                    except Exception:
                        st.info("✅ Document processed successfully!")
                
                else:
                    st.error(f"❌ Processing failed with status: {response.status_code}")
                    if response.text:
                        st.error(f"Error details: {response.text}")
                    
            except requests.exceptions.Timeout:
                st.error("⏱️ Request timed out. Please try again.")
            except requests.exceptions.ConnectionError:
                st.error("🔌 Cannot connect to processing server. Please check if the service is running.")
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- Tips Section ---
st.markdown(f'<div class="custom-container">', unsafe_allow_html=True)
st.markdown(f"<h3 style='color: {text_color}; margin-bottom: 1.5rem;'>💡 Tips for Best Results</h3>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div style='color: {text_color};'>
        <h4 style='color: {accent_color}; margin-bottom: 1rem;'>📷 Photo Quality</h4>
        <ul style='line-height: 1.8;'>
            <li>✅ Ensure good lighting</li>
            <li>✅ Keep document flat and straight</li>
            <li>✅ Avoid shadows and glare</li>
            <li>✅ Use high resolution when possible</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style='color: {text_color};'>
        <h4 style='color: {accent_color}; margin-bottom: 1rem;'>📋 Document Requirements</h4>
        <ul style='line-height: 1.8;'>
            <li>✅ ED Number should be clearly visible</li>
            <li>✅ Date field must be legible</li>
            <li>✅ 'To Name' field should be complete</li>
            <li>✅ Avoid blurry or distorted images</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- Footer ---
st.markdown(f"""
<div style="text-align: center; padding: 2rem; color: {text_color}; opacity: 0.7; margin-top: 2rem; border-top: 1px solid {border_color};">
    <strong style='font-size: 1.1rem;'>💡 Click the light bulb in the top-right corner to toggle between light and dark themes!</strong><br><br>
    <div style='margin-top: 1rem;'>
        🔒 Your documents are processed securely and not stored on our servers<br>
        Built with ❤️ by Shaurya 
    </div>
</div>
""", unsafe_allow_html=True)
