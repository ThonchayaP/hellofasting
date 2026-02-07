import streamlit as st
import extra_streamlit_components as stx
from datetime import datetime, timedelta
import time

st.set_page_config(
    page_title="Hello Fasting",
    page_icon="😈",
    layout="centered",
    initial_sidebar_state="collapsed"
)

apple_css = """
<style>
    :root {
        color-scheme: light;
    }

    html, body, .stApp {
        background-color: white !important;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: black !important;
    }

    header, footer, .stDeployButton {
        display: none !important;
        visibility: hidden !important;
    }

    h1 {
        font-weight: 700 !important;
        color: black !important;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 30px;
    }

    .stButton > button {
        width: 100%;
        border-radius: 12px !important;
        background-color: rgb(0, 113, 227) !important;
        color: white !important;
        border: none !important;
        font-weight: 500 !important;
        padding: 14px !important;
        font-size: 16px !important;
    }
    
    .stButton > button:hover {
        background-color: rgb(0, 122, 255) !important;
    }

    .big-timer {
        font-size: 72px;
        font-weight: 600;
        text-align: center;
        font-feature-settings: "tnum";
        font-variant-numeric: tabular-nums;
        color: black;
        margin-top: 30px;
        margin-bottom: 20px;
        line-height: 1;
    }

    .status-card {
        background-color: rgb(245, 245, 247);
        border-radius: 24px;
        padding: 30px;
        text-align: center;
        margin-top: 10px;
    }

    .status-emoji {
        font-size: 48px;
        margin-bottom: 15px;
        display: block;
    }

    .status-title {
        font-size: 20px;
        font-weight: 600;
        color: black;
        margin-bottom: 8px;
    }

    .status-desc {
        font-size: 15px;
        color: rgb(100, 100, 100);
        line-height: 1.5;
    }
    
    div[data-baseweb="input"] {
        background-color: rgb(245, 245, 247) !important;
        border-radius: 12px !important;
        border: none !important;
        color: black !important;
    }
    
    input {
        color: black !important;
    }
    
    iframe {
        display: none;
    }
</style>
"""
st.markdown(apple_css, unsafe_allow_html=True)

st.title("Hello Fasting")

cookie_manager = stx.CookieManager()

if 'start_time' not in st.session_state:
    st.session_state.start_time = None

cookie_val = cookie_manager.get(cookie="fasting_start_time")
if st.session_state.start_time is None and cookie_val:
    try:
        st.session_state.start_time = datetime.fromisoformat(cookie_val)
    except:
        st.session_state.start_time = None

def get_fasting_stage(hours):
    if hours < 4:
        return "Full Stomach", "Enjoy that food baby? Your body is busy digesting the massive meal you just ate.", "😋"
    elif hours < 8:
        return "The Crash", "Sugar is dropping. You might feel hangry. Dont kill anyone.", "📉"
    elif hours < 12:
        return "Fat Burning... Maybe", "Your body is finally looking for fat to burn. Good luck with that.", "🔥"
    elif hours < 18:
        return "Ketosis Mode", "Your breath might smell weird, but hey, you are burning pure fat now.", "🥑"
    elif hours < 24:
        return "Cannibalism (Autophagy)", "Your body is literally eating its own junk cells. Science is wild.", "♻️"
    elif hours < 48:
        return "God Mode", "HGH is sky high. You are either glowing or hallucinating.", "🚀"
    else:
        return "You are my father", "Respect. Are you still human? Please eat something before you ascend.", "🙏"

if st.session_state.start_time is None:
    st.markdown(
        """
        <div style="text-align: center; padding: 60px 20px;">
            <div style="font-size: 60px; margin-bottom: 20px;">🍽️</div>
            <h3 style="color:rgb(134, 134, 139); font-weight: 500;">Ready to suffer?</h3>
        </div>
        """, 
        unsafe_allow_html=True
    )
    st.write("")
    
    if st.button("Start Fasting Now"):
        new_time = datetime.now()
        st.session_state.start_time = new_time
        cookie_manager.set("fasting_start_time", new_time.isoformat(), expires_at=datetime.now() + timedelta(days=30))
        st.rerun()
        
    with st.expander("Cheating? Set past time"):
        c1, c2 = st.columns(2)
        with c1:
            d_input = st.date_input("Date", value=datetime.now())
        with c2:
            t_input = st.time_input("Time", value=datetime.now())
            
        if st.button("Set Time"):
            custom_time = datetime.combine(d_input, t_input)
            st.session_state.start_time = custom_time
            cookie_manager.set("fasting_start_time", custom_time.isoformat(), expires_at=datetime.now() + timedelta(days=30))
            st.rerun()

else:
    placeholder = st.empty()
    
    now = datetime.now()
    diff = now - st.session_state.start_time
    total_seconds = int(diff.total_seconds())
    
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    stage_title, stage_desc, stage_emoji = get_fasting_stage(hours)

    st.markdown(f'<div class="big-timer">{hours:02}:{minutes:02}:{seconds:02}</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="status-card">
            <span class="status-emoji">{stage_emoji}</span>
            <div class="status-title">{stage_title}</div>
            <div class="status-desc">{stage_desc}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.write("")
    st.write("")
    if st.button("I Give Up (Stop)", type="secondary"):
        st.session_state.start_time = None
        cookie_manager.delete("fasting_start_time")
        st.rerun()

    time.sleep(1)
    st.rerun()
