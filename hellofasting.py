import streamlit as st
import extra_streamlit_components as stx
from datetime import datetime, timedelta
import time
import json

st.set_page_config(
    page_title="Hello Fasting",
    page_icon="😈",
    layout="centered",
    initial_sidebar_state="collapsed"
)

apple_css = """
<style>
    :root {
        --ios-bg: #F2F2F7;
        --ios-card: #FFFFFF;
        --ios-text: #1C1C1E;
        --ios-subtext: #8E8E93;
        --ios-blue: #007AFF;
        --ios-red: #FF3B30;
    }

    .stApp {
        background-color: var(--ios-bg) !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", sans-serif !important;
        color: var(--ios-text) !important;
    }

    header, footer, .stDeployButton { display: none !important; }

    h1 {
        font-weight: 800 !important;
        color: var(--ios-text) !important;
        text-align: center;
        margin-top: 10px;
        letter-spacing: -0.5px;
    }

    .stButton > button {
        width: 100%;
        border-radius: 14px !important;
        background-color: var(--ios-blue) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 16px !important;
        font-size: 17px !important;
        box-shadow: 0 4px 12px rgba(0, 122, 255, 0.2);
        transition: transform 0.1s;
    }
    
    .stButton > button:active { transform: scale(0.96); }

    .big-timer {
        font-size: 80px;
        font-weight: 700;
        text-align: center;
        font-feature-settings: "tnum";
        font-variant-numeric: tabular-nums;
        color: var(--ios-text);
        margin-top: 20px;
        line-height: 1;
        letter-spacing: -2px;
    }

    .caption-note {
        font-size: 13px;
        color: var(--ios-subtext);
        text-align: center;
        margin-bottom: 25px;
        font-weight: 500;
        margin-top: 10px;
    }

    .status-card, .summary-card {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: saturate(180%) blur(20px);
        border-radius: 22px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        border: 1px solid rgba(255,255,255,0.5);
    }
    
    .history-card {
        background: white;
        border-radius: 16px;
        padding: 15px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }

    .status-emoji { font-size: 50px; margin-bottom: 15px; display: block; }
    
    .status-range {
        font-size: 11px; color: var(--ios-blue); font-weight: 700;
        text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; display: block;
    }
    
    .status-title { font-size: 22px; font-weight: 700; margin-bottom: 5px; }
    .status-desc { font-size: 15px; color: #3A3A3C; }

    .timeline-item {
        padding: 12px 16px;
        border-radius: 12px;
        margin-bottom: 8px;
        background: rgba(255,255,255,0.4);
    }
    .timeline-active { background: white; box-shadow: 0 2px 12px rgba(0,0,0,0.05); border: 1px solid rgba(0,0,0,0.05); }
    .timeline-passed { opacity: 0.5; }
    
    div[data-testid="stExpander"] {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    .confirm-box {
        background: #fff;
        border-radius: 18px;
        padding: 20px;
        text-align: center;
        margin-top: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        border: 1px solid rgba(0,0,0,0.05);
    }
</style>
"""
st.markdown(apple_css, unsafe_allow_html=True)
st.title("Hello Fasting")

cookie_manager = stx.CookieManager(key="fasting_manager")

if 'initialized' not in st.session_state:
    st.session_state.initialized = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'fasting_ended' not in st.session_state:
    st.session_state.fasting_ended = False
if 'final_duration' not in st.session_state:
    st.session_state.final_duration = ""
if 'final_hours' not in st.session_state:
    st.session_state.final_hours = 0
if 'confirm_stop' not in st.session_state:
    st.session_state.confirm_stop = False
if 'history' not in st.session_state:
    st.session_state.history = []

if not st.session_state.initialized:
    time.sleep(0.2)
    
    c_start = cookie_manager.get("fasting_start_time")
    if c_start:
        try:
            st.session_state.start_time = datetime.fromisoformat(c_start)
        except:
            st.session_state.start_time = None
            
    c_hist = cookie_manager.get("fasting_history")
    if c_hist:
        try:
            if isinstance(c_hist, str):
                st.session_state.history = json.loads(c_hist)
            elif isinstance(c_hist, list):
                st.session_state.history = c_hist
            else:
                st.session_state.history = []
        except:
            st.session_state.history = []
            
    st.session_state.initialized = True
    st.rerun()

FASTING_STAGES = [
    {"min": 0, "max": 4, "title": "Full", "desc": "Fueling up for the journey.", "emoji": "😋"},
    {"min": 4, "max": 8, "title": "Calm", "desc": "Blood sugar is stabilizing.", "emoji": "🧘"},
    {"min": 8, "max": 12, "title": "Ready", "desc": "Switching to fat burn.", "emoji": "🔥"},
    {"min": 12, "max": 16, "title": "Burn", "desc": "Fat loss in progress.", "emoji": "🥑"},
    {"min": 16, "max": 18, "title": "Zone", "desc": "Deep energy state.", "emoji": "⚡"},
    {"min": 18, "max": 24, "title": "Fresh", "desc": "Cellular cleanup time.", "emoji": "✨"},
    {"min": 24, "max": 36, "title": "Heal", "desc": "Body repair mode.", "emoji": "🌿"},
    {"min": 36, "max": 48, "title": "Clear", "desc": "Mind is sharp.", "emoji": "💡"},
    {"min": 48, "max": 9999, "title": "Hero", "desc": "Maximum benefits.", "emoji": "🚀"}
]

def get_current_stage(hours):
    for stage in FASTING_STAGES:
        if hours < stage["max"]: return stage
    return FASTING_STAGES[-1]

def get_quote(hours):
    if hours < 2: return "Off to a good start.", "🌱"
    elif hours < 8: return "You've got this.", "✌️"
    elif hours < 12: return "Staying strong.", "💪"
    elif hours < 16: return "Doing great work.", "🌟"
    elif hours < 20: return "Amazing dedication.", "💎"
    elif hours < 24: return "Super impressive.", "🏆"
    else: return "Fasting master.", "👑"

if st.session_state.fasting_ended:
    if st.session_state.final_hours >= 16:
        st.balloons()
    
    quote, emoji = get_quote(st.session_state.final_hours)
    
    st.markdown(
        f"""<div class="summary-card">
<span class="status-emoji">{emoji}</span>
<div style="font-size: 13px; color: #8E8E93; font-weight: 700; letter-spacing: 1px; text-transform: uppercase;">Total Fasted Time</div>
<div style="font-size: 56px; font-weight: 800; color: #1C1C1E; margin: 10px 0;">{st.session_state.final_duration}</div>
<div style="font-size: 16px; color: #8E8E93; font-style: italic;">"{quote}"</div>
</div>""",
        unsafe_allow_html=True
    )
    
    if st.button("Start New Fast"):
        st.session_state.fasting_ended = False
        st.session_state.start_time = None
        st.session_state.confirm_stop = False
        
        try:
            cookie_manager.delete("fasting_start_time")
        except:
            pass
        
        time.sleep(0.1)
        st.rerun()

elif st.session_state.start_time is None:
    st.markdown(
        """<div style="text-align: center; padding: 50px 20px;">
<div style="font-size: 72px; margin-bottom: 20px; filter: drop-shadow(0 10px 10px rgba(0,0,0,0.1));">🍽️</div>
<h3 style="color:#8E8E93; font-weight: 500;">Ready to suffer?</h3>
</div>""", 
        unsafe_allow_html=True
    )
    
    if st.button("Start Fasting Now"):
        new_time = datetime.now()
        st.session_state.start_time = new_time
        try:
            cookie_manager.set("fasting_start_time", new_time.isoformat(), expires_at=datetime.now() + timedelta(days=30))
        except:
            pass
        time.sleep(0.2)
        st.rerun()
        
    st.markdown("<div class='caption-note' style='margin-top:20px;'>Safe to close browser • Timer persists</div>", unsafe_allow_html=True)
    
    with st.expander("History (Last 7 Days)"):
        if not st.session_state.history:
            st.caption("No history yet.")
        else:
            for item in st.session_state.history:
                st.markdown(
                    f"""<div class="history-card">
<div style="display:flex; align-items:center;">
<span style="font-size:24px; margin-right:12px;">{item.get('emoji', '⏱️')}</span>
<div>
<div style="font-size:16px; font-weight:600; color:#1C1C1E;">{item.get('duration', '-')}</div>
<div style="font-size:12px; color:#8E8E93;">{item.get('date', '-')}</div>
</div>
</div>
</div>""",
                    unsafe_allow_html=True
                )

else:
    now = datetime.now()
    diff = now - st.session_state.start_time
    total_seconds = int(diff.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    stage = get_current_stage(hours)
    display_range = f"{stage['min']} - {stage['max']} HOURS" if stage['max'] < 9999 else "48+ HOURS"

    st.markdown(f'<div class="big-timer">{hours:02}:{minutes:02}:{seconds:02}</div>', unsafe_allow_html=True)
    st.markdown('<div class="caption-note">It is safe to close this tab. Progress is saved.</div>', unsafe_allow_html=True)

    st.markdown(
        f"""<div class="status-card">
<span class="status-emoji">{stage['emoji']}</span>
<span class="status-range">{display_range}</span>
<div class="status-title">{stage['title']}</div>
<div class="status-desc">{stage['desc']}</div>
</div>""",
        unsafe_allow_html=True
    )
    
    with st.expander("See Fasting Journey", expanded=False):
        for s in FASTING_STAGES:
            is_active = s["min"] <= hours < s["max"]
            is_passed = hours >= s["max"]
            range_text = f"{s['min']}-{s['max']}h" if s['max'] < 9999 else "48h+"
            
            card_class = "timeline-future"
            icon_html = ""
            if is_active:
                card_class = "timeline-active"
                icon_html = "<span style='color:#007AFF; font-weight:bold; font-size:12px;'>● Doing</span>"
            elif is_passed:
                card_class = "timeline-passed"
                icon_html = "<span style='color:#8E8E93; font-size:12px;'>✓ Done</span>"
                
            st.markdown(
                f"""<div class="{card_class} timeline-item">
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
<span style="font-weight:600; font-size:14px;">{s['emoji']} {s['title']}</span>
{icon_html}
</div>
<div style="font-size:12px; color:#666;">{s['desc']}</div>
</div>""",
                unsafe_allow_html=True
            )

    st.write("")
    
    if not st.session_state.confirm_stop:
        if st.button("I Give Up (Stop)"):
            st.session_state.confirm_stop = True
            st.rerun()
    else:
        st.markdown(
            """<div class="confirm-box">
<h4 style="margin:0 0 5px 0; color:#FF3B30;">End Fasting?</h4>
<p style="font-size:13px; color:#8E8E93;">This session will be saved to history.</p>
</div>""", 
            unsafe_allow_html=True
        )
        col1, col2 = st.columns(2)
        with col1:
            if st.button("End It"):
                st.session_state.final_hours = hours
                st.session_state.final_duration = f"{hours}h {minutes}m"
                st.session_state.fasting_ended = True
                
                hist_emoji = get_quote(hours)[1]
                new_entry = {
                    "date": datetime.now().strftime("%d/%m"),
                    "duration": f"{hours}h {minutes}m",
                    "emoji": hist_emoji
                }
                
                st.session_state.history.insert(0, new_entry)
                st.session_state.history = st.session_state.history[:7]
                
                try:
                    cookie_manager.delete("fasting_start_time")
                    cookie_manager.set("fasting_history", json.dumps(st.session_state.history), expires_at=datetime.now() + timedelta(days=365))
                except:
                    pass
                
                st.session_state.start_time = None
                st.session_state.confirm_stop = False
                time.sleep(0.1)
                st.rerun()
                
        with col2:
            if st.button("Resume"):
                st.session_state.confirm_stop = False
                st.rerun()

    time.sleep(1)
    st.rerun()
