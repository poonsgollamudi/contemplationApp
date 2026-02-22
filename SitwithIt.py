"""
Sit With This — A Daily Philosophical Contemplation App
Powered by teachings from Krishnamurti, Osho, Rumi, and more.
Uses Claude for generating personalized contemplations.

Run: streamlit run app.py
Set your API key: export ANTHROPIC_API_KEY=your-key-here
"""

import streamlit as st
import anthropic
import random
import math
import os
from datetime import datetime, date
from teachings import TEACHINGS, THEMES, filter_teachings, get_philosophers, get_traditions, generate_teaching_from_llm
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Get API key from environment
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────

# Page config is set in main.py when running as part of the suite
if __name__ == "__main__":
    st.set_page_config(
        page_title="Sit With This",
        page_icon="○",
        layout="centered",
        initial_sidebar_state="collapsed",
    )

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Newsreader:ital,wght@0,300;0,400;0,500;1,300;1,400&family=DM+Sans:wght@300;400;500;600&display=swap');

    /* Global */
    .stApp {
        background-color: #08080c;
        color: #d8d4ce;
    }

    /* Hide streamlit chrome */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 2rem; max-width: 960px; }

    /* Typography */
    h1, h2, h3 {
        font-family: 'Newsreader', Georgia, serif !important;
        color: #ece8e0 !important;
        font-weight: 300 !important;
    }
    p, li, span, div {
        font-family: 'DM Sans', sans-serif;
    }

    /* Teaching card */
    .teaching-card {
        background: #0e0e12;
        border: 1px solid #1a1816;
        border-radius: 20px;
        padding: 44px 40px;
        margin: 20px 0;
        position: relative;
        overflow: hidden;
    }
    .teaching-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 40px;
        right: 40px;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(200,170,130,0.2), transparent);
    }

    /* Teaching text */
    .teaching-text {
        font-family: 'Newsreader', Georgia, serif;
        font-size: 1.5rem;
        line-height: 1.65;
        color: #e8e4de;
        font-weight: 300;
        font-style: italic;
        margin: 24px 0 28px;
    }

    /* Philosopher info */
    .philosopher-name {
        font-family: 'Newsreader', Georgia, serif;
        font-size: 1.05rem;
        color: #c9c0b8;
        font-weight: 400;
    }
    .philosopher-meta {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.75rem;
        color: #fff;
        letter-spacing: 0.02em;
    }

    /* Tradition tag */
    .tradition-tag {
        display: inline-block;
        padding: 4px 14px;
        border-radius: 100px;
        font-size: 0.7rem;
        font-family: 'DM Sans', sans-serif;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }

    /* Contemplation box */
    .contemplation-box {
        background: #0c0c10;
        border: 1px solid #1a1816;
        border-radius: 20px;
        padding: 36px 40px;
        margin-top: 24px;
    }
    .contemplation-label {
        font-size: 0.7rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: #fff;
        font-family: 'DM Sans', sans-serif;
        margin-bottom: 16px;
    }
    .contemplation-text {
        font-family: 'Newsreader', Georgia, serif;
        font-size: 1.02rem;
        line-height: 1.85;
        color: #a8a098;
        font-weight: 300;
    }
    .contemplation-text p {
        font-family: 'Newsreader', Georgia, serif !important;
        margin-bottom: 14px;
    }

    /* Streamlit button overrides */
    .stButton > button {
        border-radius: 100px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 500 !important;
        letter-spacing: 0.02em !important;
        transition: all 0.3s !important;
        white-space: nowrap !important;
    }

    /* Primary button */
    .stButton > button[kind="primary"],
    div[data-testid="stButton"] > button[kind="primary"] {
        background: linear-gradient(135deg, #8a6840, #6a5030) !important;
        color: #f0ece6 !important;
        border: none !important;
        padding: 12px 24px !important;
        min-width: 180px !important;
        box-shadow: 0 4px 20px rgba(138,104,64,0.2) !important;
    }

    /* Secondary button */
    .stButton > button[kind="secondary"],
    div[data-testid="stButton"] > button[kind="secondary"] {
        background: transparent !important;
        border: 1px solid #2a2520 !important;
        color: #7a7570 !important;
        padding: 12px 24px !important;
        min-width: 180px !important;
    }

    /* Button container spacing */
    div[data-testid="stButton"] {
        margin: 8px 0 !important;
    }

    /* Column gap fix */
    div[data-testid="column"] {
        padding: 0 8px !important;
    }
    div[data-testid="column"]:first-child {
        padding-left: 0 !important;
    }
    div[data-testid="column"]:last-child {
        padding-right: 0 !important;
    }

    /* Radio/selectbox overrides */
    .stRadio > div { flex-direction: row !important; gap: 8px; flex-wrap: wrap; }
    .stRadio > div > label {
        background: transparent !important;
        border: 1px solid #1e1c18 !important;
        border-radius: 100px !important;
        padding: 6px 16px !important;
        color: #4a4540 !important;
        font-size: 0.78rem !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    .stRadio > div > label[data-checked="true"],
    .stRadio > div > label:has(input:checked) {
        border-color: #6a6050 !important;
        background: rgba(106,96,80,0.1) !important;
        color: #c9b8a0 !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        justify-content: center;
        border-bottom: none;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 100px;
        border: 1px solid #2a2520;
        background: transparent;
        color: #fff;
        padding: 8px 22px;
        font-family: 'DM Sans', sans-serif;
        font-size: 0.82rem;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(138,117,96,0.12) !important;
        border-color: #8a7560 !important;
        color: #c9b8a0 !important;
    }
    .stTabs [data-baseweb="tab-highlight"] { display: none; }
    .stTabs [data-baseweb="tab-border"] { display: none; }

    /* Divider */
    hr { border-color: #141210 !important; }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #0a0a0f;
        border-right: 1px solid #1a1816;
    }

    /* Spinner */
    .stSpinner > div { border-top-color: #8a6840 !important; }

    /* Footer */
    .app-footer {
        text-align: center;
        margin-top: 48px;
        padding-top: 24px;
        border-top: 1px solid #141210;
        font-size: 0.72rem;
        color: #3a3530;
        font-family: 'DM Sans', sans-serif;
        letter-spacing: 0.05em;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# STATE
# ─────────────────────────────────────────────

if "current_teaching" not in st.session_state:
    st.session_state.current_teaching = None
if "contemplation" not in st.session_state:
    st.session_state.contemplation = None
if "contemplation_loading" not in st.session_state:
    st.session_state.contemplation_loading = False


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def get_daily_teaching(teachings_list):
    """Deterministic daily pick based on date."""
    today = date.today()
    day_of_year = today.timetuple().tm_yday
    index = day_of_year % len(teachings_list)
    return teachings_list[index]


def get_random_teaching(teachings_list):
    """Random pick from filtered list."""
    return random.choice(teachings_list)


TRADITION_COLORS = {
    "Indian": "#e8c9a0",
    "Sufi": "#c9a0e8",
    "Taoist": "#a0c9e8",
    "Buddhist": "#a0e8c9",
    "Western": "#e8a0a0",
    "Stoic": "#c9c9a0",
    "Western-Eastern": "#a0c9b0",
}


def generate_contemplation(teaching):
    """Call Claude API to generate a contemplation for the teaching."""
    api_key = st.session_state.get("api_key", ANTHROPIC_API_KEY)
    if not api_key:
        return "⚠️ Please enter your Anthropic API key in the sidebar to generate contemplations."

    try:
        client = anthropic.Anthropic(api_key=api_key)
        theme_label = THEMES.get(teaching["theme"], {}).get("label", teaching["theme"])

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": f"""You are a contemplative guide helping someone sit with a philosophical teaching for the day. The teaching is from {teaching['philosopher']} ({teaching['tradition']} tradition), on the theme of "{theme_label}":

"{teaching['teaching']}"

Write a brief contemplation (3-5 short paragraphs) that:
1. Unpacks the core insight in simple, accessible language — what is the philosopher actually pointing at?
2. Offers a practical way to notice this in daily life today — a specific observation or micro-practice
3. Ends with a single question to sit with, not to answer but to carry through the day

Keep the tone warm, personal, and grounded — like a wise friend speaking over morning tea. No bullet points. No academic language. Write as if speaking to someone who thinks deeply but wants to feel, not just understand."""
                }
            ]
        )
        return message.content[0].text
    except anthropic.AuthenticationError:
        return "⚠️ Invalid API key. Please check your key in the sidebar."
    except Exception as e:
        return f"⚠️ Could not generate contemplation: {str(e)}"


def render_teaching_card(teaching):
    """Render the teaching in a styled card."""
    trad_color = TRADITION_COLORS.get(teaching["tradition"], "#e8c9a0")
    theme_info = THEMES.get(teaching["theme"], {"icon": "◎", "label": teaching["theme"]})

    st.markdown(f"""
    <div class="teaching-card">
        <span class="tradition-tag" style="border: 1px solid {trad_color}25; color: {trad_color}; background: {trad_color}08;">
            {teaching['tradition']} tradition
        </span>
        <div class="teaching-text">
            "{teaching['teaching']}"
        </div>
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="
                width: 50px; height: 36px; border-radius: 50%;
                background: {trad_color}15; border: 1px solid {trad_color}25;
                display: flex; align-items: center; justify-content: center;
                font-size: 0.9rem; color: {trad_color}; line-height: 36px; text-align: center;
            ">{teaching['philosopher'][0]}</div>
            <div>
                <div class="philosopher-name">{teaching['philosopher']}</div>
                <div class="philosopher-meta">{theme_info['icon']} {theme_info['label']}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_contemplation(text):
    """Render the contemplation in a styled box."""
    paragraphs = "".join(f"<p>{p.strip()}</p>" for p in text.split("\n") if p.strip())
    st.markdown(f"""
    <div class="contemplation-box">
        <div class="contemplation-label">○ Contemplation</div>
        <div class="contemplation-text">
            {paragraphs}
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown("### ○ Settings")
    st.markdown("")

    api_key = st.text_input(
        "Anthropic API Key",
        type="password",
        placeholder="sk-ant-...",
        help="Required for generating contemplations. Get one at console.anthropic.com",
    )
    if api_key:
        st.session_state.api_key = api_key

    st.markdown("---")
    st.markdown(f"""
    <div style="font-size: 0.78rem; color: #fff; line-height: 1.7;">
        <strong style="color: #8a7a6a;">{len(TEACHINGS)}</strong> teachings<br>
        <strong style="color: #8a7a6a;">{len(get_philosophers())}</strong> philosophers<br>
        <strong style="color: #8a7a6a;">{len(get_traditions())}</strong> traditions<br>
        <strong style="color: #8a7a6a;">{len(THEMES) - 1}</strong> themes
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="font-size: 0.72rem; color: #3a3530; line-height: 1.6;">
        Teachings from Krishnamurti, Osho, Rumi, Lao Tzu, Buddha, Nietzsche, 
        Spinoza, Marcus Aurelius, Epictetus, Thich Nhat Hanh, Merleau-Ponty, 
        Alan Watts, Hafiz, Seneca, Heraclitus, Kabir, and Chuang Tzu.
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────

st.markdown("""
<div style="text-align: center; margin-bottom: 8px;">
    <div style="font-size: 0.7rem; letter-spacing: 0.25em; text-transform: uppercase; color: #fff; font-family: 'DM Sans', sans-serif; margin-bottom: 14px;">
        Daily Contemplation
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; font-size:2.6rem; margin-bottom:4px; letter-spacing:-0.02em;'>Sit With This</h1>", unsafe_allow_html=True)

st.markdown("""
<p style="text-align:center; font-size:0.88rem; color:#fff; font-weight:300; max-width:400px; margin:0 auto 36px; line-height:1.6; font-family:'DM Sans',sans-serif;">
    A teaching to carry through your day.<br>Not to memorize — to discover.
</p>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MODE TABS
# ─────────────────────────────────────────────

tab_daily, tab_explore, tab_generate = st.tabs(["Today's Teaching", "Explore", "✨ Generate New"])


# ─────────────────────────────────────────────
# THEME SELECTOR (shared)
# ─────────────────────────────────────────────

def theme_selector(key_suffix):
    """Render theme pill selector."""
    theme_options = list(THEMES.keys())
    theme_labels = [f"{v['icon']} {v['label']}" for v in THEMES.values()]
    selected = st.session_state.get(f"theme_{key_suffix}", "all")

    # Split into 2 rows: 4 buttons in first row, 3 in second row
    # Row 1: First 4 themes
    cols1 = st.columns(4)
    for i in range(min(4, len(theme_options))):
        key = theme_options[i]
        label = theme_labels[i]
        with cols1[i]:
            if st.button(
                label,
                key=f"theme_btn_{key}_{key_suffix}",
                use_container_width=True,
                type="primary" if selected == key else "secondary",
            ):
                st.session_state[f"theme_{key_suffix}"] = key
                # Clear all contemplations and teachings when theme changes
                st.session_state.contemplation = None
                st.session_state.explore_contemplation = None
                st.session_state.generated_contemplation = None
                if "explore_teaching" in st.session_state:
                    del st.session_state.explore_teaching
                st.rerun()

    # Row 2: Remaining themes
    if len(theme_options) > 4:
        st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
        remaining = len(theme_options) - 4
        cols2 = st.columns(remaining)
        for i in range(remaining):
            idx = i + 4
            key = theme_options[idx]
            label = theme_labels[idx]
            with cols2[i]:
                if st.button(
                    label,
                    key=f"theme_btn_{key}_{key_suffix}",
                    use_container_width=True,
                    type="primary" if selected == key else "secondary",
                ):
                    st.session_state[f"theme_{key_suffix}"] = key
                    # Clear all contemplations and teachings when theme changes
                    st.session_state.contemplation = None
                    st.session_state.explore_contemplation = None
                    st.session_state.generated_contemplation = None
                    if "explore_teaching" in st.session_state:
                        del st.session_state.explore_teaching
                    st.rerun()

    return selected


# ─────────────────────────────────────────────
# TODAY'S TEACHING
# ─────────────────────────────────────────────

with tab_daily:
    st.markdown("")
    theme = theme_selector("daily")
    filtered = filter_teachings(theme=theme)

    if not filtered:
        st.warning("No teachings found for this theme.")
    else:
        teaching = get_daily_teaching(filtered)
        st.session_state.current_teaching = teaching
        render_teaching_card(teaching)

        # Contemplation button
        st.markdown("<div style='margin-top: 32px;'></div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("✧ Help Me Sit With This", key="contemplate_daily", type="primary", use_container_width=True):
                with st.spinner("Contemplating..."):
                    result = generate_contemplation(teaching)
                    st.session_state.contemplation = result

        if st.session_state.contemplation:
            render_contemplation(st.session_state.contemplation)


# ─────────────────────────────────────────────
# EXPLORE
# ─────────────────────────────────────────────

with tab_explore:
    st.markdown("")
    theme = theme_selector("explore")
    filtered = filter_teachings(theme=theme)

    if not filtered:
        st.warning("No teachings found for this theme.")
    else:
        # Initialize or get teaching for explore mode
        if "explore_teaching" not in st.session_state:
            st.session_state.explore_teaching = get_random_teaching(filtered)
            st.session_state.explore_contemplation = None

        render_teaching_card(st.session_state.explore_teaching)

        # Buttons
        st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)
        col1, col_gap, col2 = st.columns([1, 1, 1])
        with col1:
            if st.button("✧ Help Me Sit With This", key="contemplate_explore", type="primary", use_container_width=True):
                with st.spinner("Contemplating..."):
                    result = generate_contemplation(st.session_state.explore_teaching)
                    st.session_state.explore_contemplation = result

        with col2:
            if st.button("↻ Another Teaching", key="next_explore", type="secondary", use_container_width=True):
                st.session_state.explore_teaching = get_random_teaching(filtered)
                st.session_state.explore_contemplation = None
                st.rerun()

        if st.session_state.get("explore_contemplation"):
            render_contemplation(st.session_state.explore_contemplation)


# ─────────────────────────────────────────────
# GENERATE NEW (AI-POWERED)
# ─────────────────────────────────────────────

with tab_generate:
    st.markdown("")
    st.markdown("""
    <div style="text-align: center; margin-bottom: 24px;">
        <div style="font-size: 0.82rem; color: #8a7a6a; line-height: 1.7; max-width: 500px; margin: 0 auto;">
            Generate new teachings using AI based on your preferences.
            These supplement the curated collection with fresh insights.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Generation options
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("<div style='font-size: 0.75rem; color: #6a6560; margin-bottom: 8px;'>PHILOSOPHER</div>", unsafe_allow_html=True)
        philosopher_options = ["Any"] + get_philosophers()
        selected_philosopher = st.selectbox(
            "Philosopher",
            philosopher_options,
            key="gen_philosopher",
            label_visibility="collapsed"
        )

    with col2:
        st.markdown("<div style='font-size: 0.75rem; color: #6a6560; margin-bottom: 8px;'>THEME</div>", unsafe_allow_html=True)
        theme_options = [("all", "Any Theme")] + [(k, v["label"]) for k, v in THEMES.items() if k != "all"]
        selected_theme = st.selectbox(
            "Theme",
            [t[0] for t in theme_options],
            format_func=lambda x: next(t[1] for t in theme_options if t[0] == x),
            key="gen_theme",
            label_visibility="collapsed"
        )

    with col3:
        st.markdown("<div style='font-size: 0.75rem; color: #6a6560; margin-bottom: 8px;'>TRADITION</div>", unsafe_allow_html=True)
        tradition_options = ["Any"] + get_traditions()
        selected_tradition = st.selectbox(
            "Tradition",
            tradition_options,
            key="gen_tradition",
            label_visibility="collapsed"
        )

    st.markdown("")

    # Generate button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("✨ Generate Teaching", key="generate_btn", type="primary", use_container_width=True):
            api_key = st.session_state.get("api_key", ANTHROPIC_API_KEY)
            if not api_key:
                st.error("⚠️ Please enter your Anthropic API key in the sidebar to generate new teachings.")
            else:
                with st.spinner("Generating new teaching..."):
                    try:
                        # Prepare parameters
                        gen_params = {
                            "api_key": api_key,
                            "count": 1
                        }

                        if selected_philosopher != "Any":
                            gen_params["philosopher"] = selected_philosopher

                        if selected_theme != "all":
                            gen_params["theme"] = selected_theme

                        if selected_tradition != "Any":
                            gen_params["tradition"] = selected_tradition

                        # Generate teaching
                        generated = generate_teaching_from_llm(**gen_params)

                        if generated and len(generated) > 0:
                            st.session_state.generated_teaching = generated[0]
                            st.session_state.generated_contemplation = None
                            st.rerun()
                        else:
                            st.error("Failed to generate teaching. Please try again.")

                    except ValueError as e:
                        st.error(f"⚠️ {str(e)}")
                    except RuntimeError as e:
                        st.error(f"⚠️ {str(e)}")
                    except Exception as e:
                        st.error(f"⚠️ Unexpected error: {str(e)}")

    # Display generated teaching
    if "generated_teaching" in st.session_state and st.session_state.generated_teaching:
        teaching = st.session_state.generated_teaching
        render_teaching_card(teaching)

        # Contemplation and regenerate buttons
        st.markdown("<div style='margin-top: 32px;'></div>", unsafe_allow_html=True)
        col1, col_gap, col2 = st.columns([1, 1, 1])
        with col1:
            if st.button("✧ Help Me Sit With This", key="contemplate_generated", type="primary", use_container_width=True):
                with st.spinner("Contemplating..."):
                    result = generate_contemplation(teaching)
                    st.session_state.generated_contemplation = result

        with col2:
            if st.button("✨ Generate Another", key="regenerate", type="secondary", use_container_width=True):
                api_key = st.session_state.get("api_key", ANTHROPIC_API_KEY)
                if not api_key:
                    st.error("⚠️ Please enter your Anthropic API key in the sidebar.")
                else:
                    with st.spinner("Generating new teaching..."):
                        try:
                            gen_params = {"api_key": api_key, "count": 1}

                            if selected_philosopher != "Any":
                                gen_params["philosopher"] = selected_philosopher
                            if selected_theme != "all":
                                gen_params["theme"] = selected_theme
                            if selected_tradition != "Any":
                                gen_params["tradition"] = selected_tradition

                            generated = generate_teaching_from_llm(**gen_params)
                            if generated and len(generated) > 0:
                                st.session_state.generated_teaching = generated[0]
                                st.session_state.generated_contemplation = None
                                st.rerun()
                        except Exception as e:
                            st.error(f"⚠️ {str(e)}")

        if st.session_state.get("generated_contemplation"):
            render_contemplation(st.session_state.generated_contemplation)


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────

st.markdown(f"""
<div class="app-footer">
    {len(TEACHINGS)} teachings · {len(get_philosophers())} philosophers · {len(get_traditions())} traditions · {len(THEMES) - 1} themes
</div>
""", unsafe_allow_html=True)
