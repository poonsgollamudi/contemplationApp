"""
Contemplation Suite - Home Page
Two contemplative apps for deeper self-understanding

Run: streamlit run Home.py
"""

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Contemplation Suite",
    page_icon="◎",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Custom CSS
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
    .block-container { padding-top: 3rem; padding-bottom: 3rem; max-width: 900px; }

    /* Typography */
    h1, h2, h3 {
        font-family: 'Newsreader', Georgia, serif !important;
        color: #ece8e0 !important;
        font-weight: 300 !important;
    }

    p, li, span, div {
        font-family: 'DM Sans', sans-serif;
    }

    /* App cards */
    .app-card {
        background: linear-gradient(135deg, rgba(138,104,64,0.08), rgba(106,80,48,0.05));
        border: 1px solid #2a2520;
        border-left: 4px solid #8a6840;
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        transition: all 0.3s;
    }

    .app-card:hover {
        border-left-width: 6px;
        background: linear-gradient(135deg, rgba(138,104,64,0.12), rgba(106,80,48,0.08));
        transform: translateX(4px);
    }

    .app-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }

    .app-title {
        font-family: 'Newsreader', Georgia, serif;
        font-size: 1.8rem;
        color: #c9b8a0;
        margin-bottom: 0.5rem;
        font-weight: 400;
    }

    .app-subtitle {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.9rem;
        color: #7a7570;
        font-style: italic;
        margin-bottom: 1rem;
    }

    .app-description {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.95rem;
        line-height: 1.7;
        color: #a8a098;
    }

    .feature-list {
        margin-top: 1rem;
        padding-left: 0;
        list-style: none;
    }

    .feature-list li {
        padding: 0.3rem 0;
        color: #8a7a6a;
        font-size: 0.85rem;
    }

    .feature-list li:before {
        content: "◦ ";
        color: #8a6840;
        font-weight: bold;
        margin-right: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div style="text-align: center; margin-bottom: 3rem;">
    <div style="font-size: 0.7rem; letter-spacing: 0.25em; text-transform: uppercase; color: #5a5550; font-family: 'DM Sans', sans-serif; margin-bottom: 14px;">
        Welcome to
    </div>
    <h1 style='text-align:center; font-size:3.2rem; margin-bottom:12px; letter-spacing:-0.02em;'>
        Contemplation Suite
    </h1>
    <p style="text-align:center; font-size:1rem; color:#6a6560; font-weight:300; max-width:600px; margin:0 auto; line-height:1.7;">
        Two contemplative practices for deeper self-understanding and philosophical exploration
    </p>
</div>
""", unsafe_allow_html=True)

# Divider
st.markdown('<hr style="border: none; border-top: 1px solid #1a1816; margin: 2rem 0;">', unsafe_allow_html=True)

# App 1: Sit With This
st.markdown("""
<div class="app-card">
    <div class="app-icon">◎</div>
    <div class="app-title">Sit With This</div>
    <div class="app-subtitle">Daily Philosophical Contemplation</div>
    <div class="app-description">
        Discover teachings from the world's great philosophers and mystics. Each day brings
        a new wisdom to carry with you — not to memorize, but to live with and discover.
    </div>
    <ul class="feature-list">
        <li>65+ curated teachings from 17+ philosophers</li>
        <li>Daily teaching that changes at midnight</li>
        <li>Explore mode to browse by theme and tradition</li>
        <li>AI-generated contemplations and new teachings</li>
        <li>Themes: Mind, Love, Body, Ego, Freedom, Stillness</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown('<div style="margin: 1rem 0; text-align: center;">', unsafe_allow_html=True)
if st.button("◎ Open Sit With This", type="primary", use_container_width=True):
    st.switch_page("pages/1_◎_Sit_With_This.py")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# App 2: The Observer
st.markdown("""
<div class="app-card" style="border-left-color: #a29bfe;">
    <div class="app-icon">👁</div>
    <div class="app-title">The Observer is the Observed</div>
    <div class="app-subtitle">Based on J. Krishnamurti's Teaching</div>
    <div class="app-description">
        Share a thought or emotion and see how the watcher and what is watched are not
        two separate things, but one unified movement. A tool for direct seeing.
    </div>
    <ul class="feature-list">
        <li>Interactive analysis of thoughts and emotions</li>
        <li>Reveals the unity of observer and observed</li>
        <li>Example prompts to get started</li>
        <li>Contemplative reflections and mirror questions</li>
        <li>Grounded in Krishnamurti's core teaching</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown('<div style="margin: 1rem 0; text-align: center;">', unsafe_allow_html=True)
if st.button("👁 Open The Observer", type="primary", use_container_width=True):
    st.switch_page("pages/2_👁_The_Observer.py")
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('<hr style="border: none; border-top: 1px solid #1a1816; margin: 3rem 0 1.5rem 0;">', unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; font-size: 0.8rem; color: #fff; line-height: 1.8;">
    <strong style="color: #fff;">Quick Tip:</strong> Use the sidebar to navigate between apps<br>
    Powered by Claude AI • Built with Streamlit
</div>
""", unsafe_allow_html=True)
