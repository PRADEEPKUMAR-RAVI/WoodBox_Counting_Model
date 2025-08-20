import streamlit as st
import requests
from PIL import Image
from io import BytesIO
from streamlit_lottie import st_lottie

API_PREDICT_URL = "http://127.0.0.1:8000/predict/"
API_HEALTH_URL = "http://127.0.0.1:8000/health/"
API_BASE = "http://127.0.0.1:8000" 

st.set_page_config(page_title="SS-Suite Counter", page_icon="🪵", layout="wide")

# ----------------- CUSTOM CSS -----------------
st.markdown("""
    <style>
        .title { text-align: center; font-size: 2.2em; font-weight: bold; color: #2E86C1; }
        .section-header { font-size: 1.3em; color: #1B4F72; margin-top: 1em; margin-bottom: 0.5em; }
        div.stButton > button {
            background: linear-gradient(90deg, #1ABC9C, #16A085);
            color: white; font-size: 16px; font-weight: bold;
            border-radius: 12px; padding: 0.5em 1em; transition: 0.3s;
        }
        div.stButton > button:hover {
            transform: scale(1.05);
            background: linear-gradient(90deg, #16A085, #149174);
        }
        /* Left column container styling */
        .left-box {
            background-color: #F4F6F7;
            padding: 20px;
            border-radius: 12px;
            min-height: 90vh;
        }
    </style>
""", unsafe_allow_html=True)


# ----------------- HEADER -----------------
st.markdown('<h2 class="title">🪵 SS - Suite Counting System</h2>', unsafe_allow_html=True)

# ----------------- MAIN LAYOUT -----------------
left_col, right_col = st.columns([1, 3], gap="large")


st.markdown("""
<style>
/* Style ONLY the left column's main container */
div[data-testid="stHorizontalBlock"] > div:first-child div[data-testid="stVerticalBlock"] {
    background: #F4F6F7;
    padding: 20px;
    min-height: 100vh;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

/* Optional: tighten spacing inside the left panel */
div[data-testid="stHorizontalBlock"] > div:first-child div[data-testid="stVerticalBlock"] .stMarkdown,
div[data-testid="stHorizontalBlock"] > div:first-child div[data-testid="stVerticalBlock"] .stAlert {
    margin-bottom: 0.75rem;
}
</style>
""", unsafe_allow_html=True)

# # ---- LEFT (HEALTH CHECK) ----
with left_col:
    st.markdown('<div class="left-panel">', unsafe_allow_html=True)

    st.markdown("### 📡 System Health")

    # health check
    ok = False
    try:
        resp = requests.get(API_HEALTH_URL, timeout=3)
        ok = resp.status_code == 200 and resp.json().get("health") == "ok"
    except Exception:
        ok = False

    if ok:
        st.success("🟢 Backend Running")
    else:
        st.error("🔴 Backend Down")

    # Lottie animation
    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    lottie_health = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_j1adxtyb.json")
    if lottie_health:
        st_lottie(lottie_health, height=150, key="health_anim")

    st.markdown('</div>', unsafe_allow_html=True)

# ---- RIGHT (UPLOAD + PREDICTION) ----
with right_col:
    st.markdown('<p class="section-header">📤 Upload Image</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        if st.button("🔍 Count"):
            with st.spinner("⏳ Model is analyzing... Please wait..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    response = requests.post(API_PREDICT_URL, files=files)

                    if response.status_code == 200:
                        result = response.json()

                        st.markdown(
                            f"""
                            <div style='
                                padding: 1em; 
                                background: #E8F8F5; 
                                border-radius: 12px; 
                                text-align: center; 
                                font-size: 20px; 
                                font-weight: bold; 
                                color: #117A65;'>
                                ✅ Detected <span style="color:#0E6655;">{result['stacked_wood_boxes']}</span> stacked wood boxes!
                            </div>
                            """, unsafe_allow_html=True
                        )

                        col1, col2 = st.columns(2)
                        with col1:
                            st.image(uploaded_file, caption="📷 Uploaded Image (Before)", use_container_width=True)
                        with col2:
                            if "annotated_image" in result:
                                annotated_url = API_BASE + result["annotated_image"]
                                annotated_response = requests.get(annotated_url)
                                if annotated_response.status_code == 200:
                                    img = Image.open(BytesIO(annotated_response.content))
                                    st.image(img, caption="📷 Annotated Image (After)", use_container_width=True)

                    else:
                        st.error("❌ Error: Could not get prediction from backend")
                except Exception:
                    st.error("❌ Failed to connect to backend.")



