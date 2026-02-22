import os

import streamlit as st
import anthropic
import json
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Get API key from environment
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

# Page config is set in main.py when running as part of the suite
if __name__ == "__main__":
    st.set_page_config(
        page_title="The Observer is the Observed",
        page_icon="👁",
        layout="centered"
    )

# Bright, vibrant CSS theme
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;500&display=swap');

/* Main background */
.stApp {
    background: linear-gradient(#000, #000 0%, #000 50%, #000 100%);
    min-height: 100vh;
}

/* Hide Streamlit default elements */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 800px; }

/* Typography */
h1, h2, h3 { font-family: 'Playfair Display', serif !important; }

/* Title styling */
.main-title {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 700;
    text-align: center;
    background: linear-gradient(90deg, #ff6b6b, #feca57, #48dbfb, #ff9ff3);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.2;
    margin-bottom: 0.5rem;
}

.subtitle {
    font-family: 'Playfair Display', serif;
    font-style: italic;
    text-align: center;
    color: #a29bfe;
    font-size: 1.1rem;
    margin-bottom: 0.3rem;
}

.tagline {
    text-align: center;
    color: #74b9ff;
    font-size: 0.9rem;
    margin-bottom: 2rem;
    font-family: 'Inter', sans-serif;
    font-weight: 300;
}

/* Divider */
.rainbow-divider {
    height: 2px;
    background: linear-gradient(90deg, #ff6b6b, #feca57, #48dbfb, #ff9ff3, #a29bfe);
    border-radius: 2px;
    margin: 1.5rem 0;
}

/* Card styles */
.observer-card {
    background: linear-gradient(135deg, rgba(255,107,107,0.15), rgba(254,202,87,0.1));
    border: 1px solid rgba(255,107,107,0.4);
    border-left: 4px solid #ff6b6b;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
}

.observed-card {
    background: linear-gradient(135deg, rgba(72,219,251,0.15), rgba(162,155,254,0.1));
    border: 1px solid rgba(72,219,251,0.4);
    border-left: 4px solid #48dbfb;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
}

.unity-card {
    background: linear-gradient(135deg, rgba(255,159,243,0.15), rgba(162,155,254,0.15));
    border: 1px solid rgba(255,159,243,0.4);
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    text-align: center;
}

.reflection-card {
    background: linear-gradient(135deg, rgba(254,202,87,0.12), rgba(255,107,107,0.08));
    border: 1px solid rgba(254,202,87,0.3);
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
}

.mirror-card {
    background: linear-gradient(135deg, rgba(162,155,254,0.2), rgba(72,219,251,0.1));
    border: 2px solid rgba(162,155,254,0.5);
    border-radius: 16px;
    padding: 2rem;
    margin: 1.5rem 0;
    text-align: center;
}

.card-label {
    font-family: 'Inter', sans-serif;
    font-size: 0.7rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    font-weight: 500;
    margin-bottom: 0.5rem;
}

.card-content {
    font-family: 'Playfair Display', serif;
    font-size: 1rem;
    line-height: 1.7;
    color: #dfe6e9;
}

.mirror-text {
    font-family: 'Playfair Display', serif;
    font-style: italic;
    font-size: 1.3rem;
    line-height: 1.6;
    background: linear-gradient(90deg, #a29bfe, #74b9ff, #55efc4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.quote-box {
    text-align: center;
    padding: 1.5rem;
    color: #fff;
    font-family: 'Playfair Display', serif;
    font-style: italic;
    font-size: 0.85rem;
    line-height: 1.8;
    border-top: 1px solid rgba(255,255,255,0.05);
    margin-top: 2rem;
}

.input-echo {
    font-family: 'Playfair Display', serif;
    font-style: italic;
    color: #b2bec3;
    font-size: 1rem;
    padding: 1rem 1.5rem;
    border-left: 3px solid rgba(162,155,254,0.5);
    margin-bottom: 1.5rem;
    background: rgba(255,255,255,0.03);
    border-radius: 0 8px 8px 0;
}

/* Streamlit widget styling */
.stTextArea textarea {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(162,155,254,0.3) !important;
    border-radius: 12px !important;
    color: #000 !important;
    font-family: 'Playfair Display', serif !important;
    font-style: italic !important;
    font-size: 1rem !important;
    padding: 1rem !important;
}

.stTextArea textarea:focus {
    border-color: rgba(162,155,254,0.7) !important;
    box-shadow: 0 0 0 2px rgba(162,155,254,0.1) !important;
}

.stButton button {
    background: linear-gradient(135deg, #6c5ce7, #a29bfe) !important;
    color: white !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 0.6rem 2.5rem !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    font-size: 0.85rem !important;
    transition: all 0.3s !important;
    width: 100% !important;
}

.stButton button:hover {
    background: linear-gradient(135deg, #a29bfe, #74b9ff) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 20px rgba(108,92,231,0.4) !important;
}

/* Example pills */
.example-pill {
    display: inline-block;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 50px;
    padding: 4px 14px;
    font-size: 0.8rem;
    color: #b2bec3;
    margin: 3px;
    cursor: pointer;
    font-family: 'Inter', sans-serif;
    font-style: italic;
}

/* Spinner color */
.stSpinner > div { border-top-color: #FFFFFF; color: #FFFFFF !important; }

/* Label colors */
.observer-label { color: #ff6b6b; }
.observed-label { color: #48dbfb; }
.unity-label { color: #ff9ff3; }
.reflection-label { color: #feca57; }
.mirror-label { color: #a29bfe; }

</style>
""", unsafe_allow_html=True)

SYSTEM_PROMPT = """You are a contemplative guide deeply versed in Jiddu Krishnamurti's teaching that "the observer is the observed."

When a user shares a thought, emotion, or experience, your role is to:

1. IDENTIFY THE OBSERVER: Find the "I" voice in their statement — the part judging, naming, analyzing, wanting to change, resisting, or commenting on the experience. Quote or describe it briefly.

2. IDENTIFY THE OBSERVED: What is being observed — the emotion, thought, sensation, or situation.

3. SHOW THE UNITY: Reveal how the observer and the observed are the same movement of thought. Be precise and gentle. Show that the one who says "I am angry" and the anger itself are not two separate things. The labeling, commentary, resistance — all of it IS the emotion, not a separate entity watching it.

4. REFLECTION: A gentle 2-3 sentence overall reflection in Krishnamurti's spirit.

5. MIRROR QUESTION: End with one simple, open question that invites direct seeing — not analysis, not fixing, not accepting. Something that points to the bare fact of the experience before the observer labels it.

Important guidelines:
- Speak with warmth and precision, not spiritual jargon
- Never instruct them to meditate, accept, or practice anything
- Never diagnose or therapize
- Keep each section concise
- The goal is not to help them feel better — it's to see clearly
- Krishnamurti's key insight: thought creates the observer and the observed, then suffers from the division between them

Respond ONLY with valid JSON in exactly this format:
{
  "observer": "brief description of the observer voice",
  "observed": "what is being observed",
  "unity": "2-3 sentences showing they are the same movement",
  "reflection": "2-3 sentence gentle reflection",
  "mirror": "one open question for direct seeing"
}"""

def analyze_with_claude(user_input):
    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_input}]
    )
    text = response.content[0].text
    clean = text.replace("```json", "").replace("```", "").strip()
    return json.loads(clean)


# ─── UI ───────────────────────────────────────────────

st.markdown('<div class="main-title">The Observer<br>is the Observed</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle"><span style="color:#fff;">J. Krishnamurti</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">Share a thought or emotion. See how the watcher and what is watched are one.</div>', unsafe_allow_html=True)
st.markdown('<div class="rainbow-divider"></div>', unsafe_allow_html=True)

# Examples
examples = [
    "I keep procrastinating and I hate myself for it",
    "I feel anxious about the future but I know I shouldn't",
    "I'm angry at someone but trying not to be",
    "I feel empty and I don't know why",
    "I'm jealous and it feels shameful",
    "I can't stop overthinking",
]

st.markdown(" <span style=\"color:#fff; font-weight:bold;\">Try an example:</span>", unsafe_allow_html=True)
cols = st.columns(3)
for i, ex in enumerate(examples):
    if cols[i % 3].button(ex, key=f"ex_{i}", use_container_width=True):
        st.session_state["main_input"] = ex
        st.rerun()

# Text input
user_input = st.text_area(
    "What thought or emotion are you carrying right now?",
    placeholder="I feel...  /  I keep thinking...  /  There is...",
    height=120,
    label_visibility="collapsed",
    key="main_input"
)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analyze_btn = st.button("✦ See Clearly", use_container_width=True)

# ─── Analysis ───────────────────────────────────────────────

if analyze_btn and user_input.strip():
    with st.spinner("Looking without the looker..."):
        try:
            result = analyze_with_claude(user_input.strip())
            
            st.markdown('<div class="rainbow-divider"></div>', unsafe_allow_html=True)
            
            # Input echo
            st.markdown(f'<div class="input-echo">"{user_input.strip()}"</div>', unsafe_allow_html=True)

            # Observer
            st.markdown(f"""
            <div class="observer-card">
                <div class="card-label observer-label">👁 The Observer — the voice that separates</div>
                <div class="card-content">{result['observer']}</div>
            </div>
            """, unsafe_allow_html=True)

            # Visual connector
            st.markdown('<div style="text-align:center; font-size:1.5rem; color:#636e72; margin:0.2rem 0;">⟷</div>', unsafe_allow_html=True)

            # Observed
            st.markdown(f"""
            <div class="observed-card">
                <div class="card-label observed-label">◉ The Observed — what is being watched</div>
                <div class="card-content">{result['observed']}</div>
            </div>
            """, unsafe_allow_html=True)

            # Unity
            st.markdown(f"""
            <div class="unity-card">
                <div class="card-label unity-label">∞ They Are The Same Movement</div>
                <div class="card-content" style="text-align:left;">{result['unity']}</div>
            </div>
            """, unsafe_allow_html=True)

            # Reflection
            st.markdown(f"""
            <div class="reflection-card">
                <div class="card-label reflection-label">✦ Reflection</div>
                <div class="card-content">{result['reflection']}</div>
            </div>
            """, unsafe_allow_html=True)

            # Mirror question
            st.markdown(f"""
            <div class="mirror-card">
                <div class="card-label mirror-label" style="margin-bottom:1rem;">◈ sit with this</div>
                <div class="mirror-text">{result['mirror']}</div>
            </div>
            """, unsafe_allow_html=True)

            # K quote
            st.markdown("""
            <div class="quote-box">
                "Observe, and in that observation there is neither the observer nor the observed<br>
                — there is only observation taking place."<br><br>
                <span style="letter-spacing:0.2em; font-size:0.75rem; font-style:normal; color:#fff;">J. KRISHNAMURTI</span>
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Something dissolved in transmission: {str(e)}")

elif analyze_btn and not user_input.strip():
    st.warning("Share a thought or emotion to begin.")

# Instructions at bottom
if not analyze_btn:
    st.markdown("""
    <div style="text-align:center; margin-top:3rem; color:#fff; font-family:'Inter',sans-serif; font-size:0.8rem; line-height:2;">
        Type any thought, emotion, or inner struggle<br>
        The app reveals how the one watching and what is watched are not two things<br>
        <span style="color:#fff;">⌘ Enter</span> or click the button to see clearly
    </div>
    """, unsafe_allow_html=True)
