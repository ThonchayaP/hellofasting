import streamlit as st
import extra_streamlit_components as stx
from datetime import datetime, timedelta
import time
import json

st.set_page_config(
    page_title="Hello Fasting 😈",
    page_icon="😈",
    layout="centered",
    initial_sidebar_state="collapsed"
)

apple_css = """
<style>
    :root {
        --glass-bg: rgba(255, 255, 255, 0.75);
        --glass-border: rgba(255, 255, 255, 0.5);
        --glass-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
        --ios-blue: #007AFF;
        --ios-text: #000000;
        --ios-subtext: #86868b;
        --ios-bg: #F5F5F7;
        --ios-red: #FF3B30;
    }

    .stApp {
        background-color: var(--ios-bg) !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", sans-serif !important;
        color: var(--ios-text) !important;
    }

    header, footer, .stDeployButton { display: none !important; }

    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-6px); }
        100% { transform: translateY(0px); }
    }

    @keyframes burn {
        0% { text-shadow: 0 0 5px rgba(0,0,0,0.1); transform: scale(1); }
        50% { text-shadow: 0 0 15px rgba(0,0,0,0.15); transform: scale(1.02); }
        100% { text-shadow: 0 0 5px rgba(0,0,0,0.1); transform: scale(1); }
    }

    .theme-idle { animation: float 4s ease-in-out infinite; color: var(--ios-text); }
    .theme-active { animation: burn 2s ease-in-out infinite; color: var(--ios-blue); }

    h1 {
        font-weight: 800 !important;
        text-align: center;
        margin-top: 10px;
        letter-spacing: -1px;
        font-size: 28px !important;
    }

    .stButton > button {
        width: 100%;
        border-radius: 18px !important;
        background: var(--ios-blue) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 16px !important;
        font-size: 17px !important;
        box-shadow: 0 4px 15px rgba(0, 122, 255, 0.3);
        transition: transform 0.2s;
        backdrop-filter: blur(10px);
    }
    
    .stButton > button:active { transform: scale(0.96); }

    .big-timer {
        font-size: 86px;
        font-weight: 700;
        text-align: center;
        font-feature-settings: "tnum";
        font-variant-numeric: tabular-nums;
        color: var(--ios-text);
        margin-top: 20px;
        line-height: 1;
        letter-spacing: -3px;
        text-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }

    .caption-note {
        font-size: 13px;
        color: var(--ios-subtext);
        text-align: center;
        margin-bottom: 30px;
        font-weight: 500;
        margin-top: 15px;
    }

    .status-card, .summary-card {
        background: var(--glass-bg);
        backdrop-filter: saturate(180%) blur(40px);
        -webkit-backdrop-filter: saturate(180%) blur(40px);
        border-radius: 32px;
        padding: 36px;
        text-align: center;
        box-shadow: var(--glass-shadow);
        border: 1px solid var(--glass-border);
        margin-bottom: 24px;
    }

    .status-emoji { 
        font-size: 56px; 
        margin-bottom: 15px; 
        display: block; 
        filter: drop-shadow(0 4px 12px rgba(0,0,0,0.1));
    }
    
    .status-range {
        font-size: 11px; 
        color: var(--ios-blue); 
        font-weight: 800;
        text-transform: uppercase; 
        letter-spacing: 2px; 
        margin-bottom: 10px; 
        display: block;
        opacity: 0.9;
    }
    
    .status-title { 
        font-size: 24px; 
        font-weight: 700; 
        margin-bottom: 8px; 
        letter-spacing: -0.5px;
    }
    
    .status-desc { 
        font-size: 16px; 
        color: #48484a; 
        line-height: 1.4;
    }

    .history-card {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 18px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border: 1px solid rgba(255,255,255,0.4);
    }

    .confirm-box {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 24px;
        padding: 24px;
        text-align: center;
        margin-top: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.5);
    }
    
    div[data-testid="stExpander"] {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
</style>
"""
st.markdown(apple_css, unsafe_allow_html=True)

cookie_manager = stx.CookieManager(key="fasting_v2")

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
if 'cookies_loaded' not in st.session_state:
    st.session_state.cookies_loaded = False

cookies = cookie_manager.get_all()

if not st.session_state.cookies_loaded:
    if cookies is None:
        time.sleep(0.5)
        st.rerun()
    else:
        c_start = cookies.get("fasting_start_time")
        if c_start:
            try:
                st.session_state.start_time = datetime.fromisoformat(c_start)
            except:
                pass
        
        c_hist = cookies.get("fasting_history")
        if c_hist:
            try:
                if isinstance(c_hist, str):
                    st.session_state.history = json.loads(c_hist)
            except:
                pass
        
        st.session_state.cookies_loaded = True
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

title_class = "theme-idle"
if st.session_state.start_time is not None:
    title_class = "theme-active"

st.markdown(f'<h1 class="{title_class}">Hello Fasting 😈</h1>', unsafe_allow_html=True)

if st.session_state.fasting_ended:
    if st.session_state.final_hours >= 16:
        st.balloons()
    
    quote, emoji = get_quote(st.session_state.final_hours)
    
    st.markdown(
        f"""<div class="summary-card">
<span class="status-emoji">{emoji}</span>
<div style="font-size: 13px; color: #8E8E93; font-weight: 700; letter-spacing: 1px; text-transform: uppercase;">Total Fasted Time</div>
<div style="font-size: 64px; font-weight: 800; color: #1C1C1E; margin: 15px 0; letter-spacing: -2px;">{st.session_state.final_duration}</div>
<div style="font-size: 17px; color: #8E8E93; font-style: italic;">"{quote}"</div>
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
        
        time.sleep(0.5)
        st.rerun()

elif st.session_state.start_time is None:
    st.markdown(
        """<div style="text-align: center; padding: 60px 20px;">
<div style="font-size: 80px; margin-bottom: 25px; filter: drop-shadow(0 15px 25px rgba(0,0,0,0.15));">🍽️</div>
<h3 style="color:#8E8E93; font-weight: 600; font-size: 24px;">Ready to suffer?</h3>
</div>""", 
        unsafe_allow_html=True
    )
    
    if st.button("Start Fasting Now"):
        new_time = datetime.now()
        st.session_state.start_time = new_time
        try:
            cookie_manager.set("fasting_start_time", new_time.isoformat(), expires_at=datetime.now() + timedelta(days=365))
        except:
            pass
        time.sleep(0.5)
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
<span style="font-size:28px; margin-right:16px;">{item.get('emoji', '⏱️')}</span>
<div>
<div style="font-size:17px; font-weight: 700; color:#1C1C1E; letter-spacing: -0.5px;">{item.get('duration', '-')}</div>
<div style="font-size:13px; color:#8E8E93; font-weight: 500;">{item.get('date', '-')}</div>
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
    st.markdown('<div class="caption-note">Progress is saved automatically.</div>', unsafe_allow_html=True)

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
            
            card_style = "background: rgba(255,255,255,0.4); opacity: 0.5;"
            icon_html = ""
            
            if is_active:
                card_style = "background: rgba(255,255,255,0.9); box-shadow: 0 4px 12px rgba(0,0,0,0.05); transform: scale(1.02); border: 1px solid rgba(255,255,255,0.8);"
                icon_html = "<span style='color:#007AFF; font-weight:800; font-size:12px;'>● Doing</span>"
            elif is_passed:
                card_style = "background: rgba(255,255,255,0.6);"
                icon_html = "<span style='color:#8E8E93; font-size:12px; font-weight:600;'>✓ Done</span>"
                
            st.markdown(
                f"""<div style="padding: 16px 20px; border-radius: 20px; margin-bottom: 10px; {card_style} transition: all 0.3s ease;">
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
<span style="font-weight:700; font-size:15px; color:#1C1C1E;">
    {s['emoji']} {s['title']} 
    <span style="color:#8E8E93; font-size:13px; margin-left:8px; font-weight:400;">{range_text}</span>
</span>
{icon_html}
</div>
<div style="font-size:13px; color:#555; line-height:1.4;">{s['desc']}</div>
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
<h4 style="margin:0 0 8px 0; color:#FF3B30; font-weight: 700; font-size: 18px;">End Fasting?</h4>
<p style="font-size:14px; color:#8E8E93; font-weight: 500;">This session will be saved to history.</p>
</div>""", 
            unsafe_allow_html=True
        )
        col1, col2 = st.columns(2)
        with col1:
            if st.button("End It"):
                st.session_state.final_hours = hours
                st.session_state.final_duration = f"{hours}h {minutes}m {seconds}s"
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
                time.sleep(0.5)
                st.rerun()
                
        with col2:
            if st.button("Resume"):
                st.session_state.confirm_stop = False
                st.rerun()

    time.sleep(1)
    st.rerun()
