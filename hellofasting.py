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
        margin-bottom: 5px;
        line-height: 1;
    }

    .caption-note {
        font-size: 13px;
        color: rgb(134, 134, 139);
        text-align: center;
        margin-bottom: 25px;
        font-weight: 400;
    }

    .status-card {
        background-color: rgb(245, 245, 247);
        border-radius: 24px;
        padding: 30px;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 20px;
    }
    
    .summary-card {
        background-color: rgb(245, 245, 247);
        border-radius: 24px;
        padding: 40px 20px;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 20px;
    }

    .status-emoji {
        font-size: 48px;
        margin-bottom: 15px;
        display: block;
    }
    
    .summary-emoji {
        font-size: 64px;
        margin-bottom: 20px;
        display: block;
    }

    .status-range {
        font-size: 11px;
        color: rgb(0, 113, 227);
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 5px;
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
    
    .timeline-item {
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 10px;
        border: 1px solid transparent;
        transition: all 0.2s;
    }
    
    .timeline-active {
        background-color: white;
        border: 2px solid rgb(0, 113, 227);
        box-shadow: 0 4px 12px rgba(0, 113, 227, 0.1);
    }
    
    .timeline-passed {
        opacity: 0.5;
        background-color: rgb(245, 245, 247);
    }
    
    .timeline-future {
        background-color: white;
        border: 1px solid rgb(240, 240, 240);
        opacity: 0.8;
    }
    
    .timeline-header {
        font-weight: 600;
        font-size: 14px;
        margin-bottom: 2px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .timeline-text {
        font-size: 12px;
        color: rgb(100, 100, 100);
    }
    
    .checkmark {
        color: rgb(0, 113, 227);
        font-weight: bold;
    }
    
    .final-time {
        font-size: 48px;
        font-weight: 700;
        color: black;
        margin-bottom: 10px;
        font-variant-numeric: tabular-nums;
    }
    
    .quote-text {
        font-size: 16px;
        color: rgb(134, 134, 139);
        font-style: italic;
        margin-bottom: 30px;
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
    
    div[data-testid="stExpander"] {
        background-color: white !important;
        border: none !important;
        box-shadow: none !important;
    }
    
    div[data-testid="stExpander"] > details > summary {
        color: rgb(0, 113, 227) !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        background-color: white !important;
        justify-content: center;
    }
    
    div[data-testid="stExpander"] > details > summary:hover {
        color: rgb(0, 122, 255) !important;
    }
</style>
"""
st.markdown(apple_css, unsafe_allow_html=True)

st.title("Hello Fasting")

cookie_manager = stx.CookieManager(key="fasting_cookies")

if 'start_time' not in st.session_state:
    st.session_state.start_time = None

if 'fasting_ended' not in st.session_state:
    st.session_state.fasting_ended = False
    
if 'final_duration' not in st.session_state:
    st.session_state.final_duration = ""
    
if 'final_hours' not in st.session_state:
    st.session_state.final_hours = 0

if st.session_state.start_time is None and not st.session_state.fasting_ended:
    time.sleep(0.1) 
    cookie_val = cookie_manager.get(cookie="fasting_start_time")
    if cookie_val:
        try:
            st.session_state.start_time = datetime.fromisoformat(cookie_val)
        except:
            st.session_state.start_time = None

FASTING_STAGES = [
    {"min": 0, "max": 4, "title": "Full Stomach", "desc": "Still digesting that massive meal, aren't you?", "emoji": "😋"},
    {"min": 4, "max": 8, "title": "The Crash", "desc": "Hangry mode activated. Don't talk to anyone.", "emoji": "📉"},
    {"min": 8, "max": 12, "title": "Fat Burning... Maybe", "desc": "Body is finally waking up. About time.", "emoji": "🔥"},
    {"min": 12, "max": 16, "title": "Ketosis Entry", "desc": "Burning fat now. Don't ruin it with a cookie.", "emoji": "🥑"},
    {"min": 16, "max": 18, "title": "Deep Ketosis", "desc": "You are literally melting. Keep going.", "emoji": "⚡"},
    {"min": 18, "max": 24, "title": "Autophagy", "desc": "Eating yourself (in a good way). Science!", "emoji": "♻️"},
    {"min": 24, "max": 36, "title": "HGH Spike", "desc": "You are basically Hulk right now.", "emoji": "🧬"},
    {"min": 36, "max": 48, "title": "God Mode", "desc": "Who needs food? Food is for the weak.", "emoji": "🚀"},
    {"min": 48, "max": 9999, "title": "Skeleton", "desc": "There is nothing left to burn. You are just bones.", "emoji": "💀"}
]

def get_current_stage_info(hours):
    for stage in FASTING_STAGES:
        if hours < stage["max"]:
            return stage
    return FASTING_STAGES[-1]

def get_motivational_quote(hours):
    if hours < 2:
        return "That was a nap, not a fast. Are you kidding me?", "🤡"
    elif hours < 8:
        return "Did you trip and fall into a buffet? Pathetic.", "🍼"
    elif hours < 12:
        return "My cat fasts longer than this. Try harder.", "🐈"
    elif hours < 16:
        return "Barely acceptable. You basically just skipped breakfast.", "🥱"
    elif hours < 20:
        return "Okay, not terrible. You survive another day.", "😏"
    elif hours < 24:
        return "Savage. You must really hate food (or yourself).", "💀"
    else:
        return "Absolute psychopath. Go eat a burger before you ascend.", "👽"

if st.session_state.fasting_ended:
    if st.session_state.final_hours >= 16:
        st.balloons()
    
    quote, emoji = get_motivational_quote(st.session_state.final_hours)
    
    st.markdown(
        f"""
        <div class="summary-card">
            <span class="summary-emoji">{emoji}</span>
            <div style="font-size: 14px; color: #86868b; margin-bottom: 5px; text-transform: uppercase; font-weight: 600;">Total Fasted Time</div>
            <div class="final-time">{st.session_state.final_duration}</div>
            <div class="quote-text">"{quote}"</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    if st.button("Start New Fast"):
        st.session_state.fasting_ended = False
        st.session_state.start_time = None
        st.session_state.final_duration = ""
        st.session_state.final_hours = 0
        st.rerun()

elif st.session_state.start_time is None:
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
        try:
            cookie_manager.set("fasting_start_time", new_time.isoformat(), expires_at=datetime.now() + timedelta(days=30))
        except:
            pass
        time.sleep(0.5)
        st.rerun()
        
    st.markdown("<p style='text-align:center; color:#86868b; font-size:12px; margin-top:10px;'>Safe to close browser • Timer persists</p>", unsafe_allow_html=True)
        
    with st.expander("Cheating? Set past time"):
        c1, c2 = st.columns(2)
        with c1:
            d_input = st.date_input("Date", value=datetime.now())
        with c2:
            t_input = st.time_input("Time", value=datetime.now())
            
        if st.button("Set Time"):
            custom_time = datetime.combine(d_input, t_input)
            st.session_state.start_time = custom_time
            try:
                cookie_manager.set("fasting_start_time", custom_time.isoformat(), expires_at=datetime.now() + timedelta(days=30))
            except:
                pass
            time.sleep(0.5)
            st.rerun()

else:
    placeholder = st.empty()
    
    now = datetime.now()
    diff = now - st.session_state.start_time
    total_seconds = int(diff.total_seconds())
    
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    current_stage = get_current_stage_info(hours)
    
    display_range = f"{current_stage['min']} - {current_stage['max']} HOURS" if current_stage['max'] < 9999 else "48+ HOURS"

    st.markdown(f'<div class="big-timer">{hours:02}:{minutes:02}:{seconds:02}</div>', unsafe_allow_html=True)
    st.markdown('<div class="caption-note">It is safe to close this tab. Progress is saved.</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="status-card">
            <span class="status-emoji">{current_stage['emoji']}</span>
            <span class="status-range">{display_range}</span>
            <div class="status-title">{current_stage['title']}</div>
            <div class="status-desc">{current_stage['desc']}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    with st.expander("See Fasting Journey", expanded=False):
        for stage in FASTING_STAGES:
            is_active = stage["min"] <= hours < stage["max"]
            is_passed = hours >= stage["max"]
            
            range_text = f"{stage['min']}-{stage['max']}h" if stage['max'] < 9999 else "48h+"
            
            card_class = "timeline-future"
            icon_html = ""
            
            if is_active:
                card_class = "timeline-active"
                icon_html = "<span class='checkmark'>● Doing</span>"
            elif is_passed:
                card_class = "timeline-passed"
                icon_html = "<span class='checkmark'>✓ Done</span>"
                
            st.markdown(
                f"""
                <div class="{card_class} timeline-item">
                    <div class="timeline-header">
                        <span>{stage['emoji']} {stage['title']}</span>
                        <span style="font-size:10px; color:#86868b;">{icon_html}</span>
                    </div>
                    <div class="timeline-text" style="display:flex; justify-content:space-between;">
                        <span>{stage['desc']}</span>
                        <span style="font-weight:600;">{range_text}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.write("")
    st.write("")
    
    if st.button("I Give Up (Stop)", type="secondary"):
        st.session_state.final_hours = hours
        st.session_state.final_duration = f"{hours}h {minutes}m"
        st.session_state.fasting_ended = True
        st.session_state.start_time = None
        
        try:
            cookie_manager.delete("fasting_start_time")
        except:
            pass
        time.sleep(0.5)
        st.rerun()

    time.sleep(1)
    st.rerun()
