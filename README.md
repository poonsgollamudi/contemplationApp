# Contemplation Suite

A combined interface featuring two contemplative applications powered by Claude AI.

## Apps

### 1. **Sit With This** (◎)
A daily philosophical contemplation app with teachings from Krishnamurti, Osho, Rumi, Lao Tzu, Buddha, Nietzsche, Spinoza, Marcus Aurelius, Epictetus, Thich Nhat Hanh, Merleau-Ponty, Alan Watts, Hafiz, Seneca, Heraclitus, Kabir, and Chuang Tzu.

Uses Claude to generate personalized contemplations — not explanations, but invitations to sit with the insight.

### 2. **The Observer is the Observed** (👁)
An interactive tool based on J. Krishnamurti's teaching that "the observer is the observed."

Share a thought or emotion and the app helps you see:
- The observer (the part that's watching/judging)
- The observed (what's being watched)
- How they are the same movement of thought

## Quick Start

```bash
# 1. Install dependencies
pip install streamlit anthropic python-dotenv

# 2. Set your Anthropic API key
export ANTHROPIC_API_KEY=sk-ant-your-key-here

# 3. Run the app
streamlit run Home.py
```

The app opens at `http://localhost:8501`.

You can also enter your API key directly in the sidebar (for Sit With This).

### Navigate Between Apps
- Use the sidebar to switch between "Sit With This" and "The Observer"
- Or click the buttons on the home page
- Each app maintains its own unique styling and features

## Features

### Sit With This
- **Today's Teaching** — one consistent teaching per day, changes at midnight
- **Explore** — browse random teachings, discover new philosophers
- **Generate New** — AI-generated teachings based on your preferences
- **6 themes** — Mind & Thought, Love & Connection, Body & Presence, Ego & Self, Freedom & Truth, Stillness & Being
- **Claude-powered contemplations** — unpacks the insight, offers a micro-practice, leaves you with a question to carry
- **65+ curated teachings** across Indian, Sufi, Taoist, Buddhist, Stoic, and Western traditions

### The Observer is the Observed
- **Interactive analysis** — share any thought or emotion
- **Clear seeing** — reveals how the watcher and the watched are one movement
- **Example prompts** — quick-start with common experiences
- **Contemplative guidance** — grounded in Krishnamurti's teachings

## Adding Your Own Teachings

Edit `teachings.py` and add entries to the `TEACHINGS` list:

```python
{"philosopher": "Your Philosopher", "theme": "mind", "tradition": "Your Tradition",
 "teaching": "The teaching text goes here."},
```

Valid themes: `mind`, `love`, `body`, `ego`, `freedom`, `stillness`

## Deploy to Streamlit Cloud (Free)

1. Push this folder to a GitHub repo
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo, set `app.py` as the main file
4. Add `ANTHROPIC_API_KEY` in the Secrets section:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-your-key-here"
   ```
5. Deploy

## Project Structure

```
contemplationApp/
├── Home.py                         # Main landing page
├── pages/
│   ├── 1_◎_Sit_With_This.py       # Sit With This app page
│   └── 2_👁_The_Observer.py        # The Observer app page
├── teachings.py                    # Curated teachings database
├── requirements.txt                # Dependencies
├── main.py                         # (Legacy tab-based version)
├── SitwithIt.py                    # (Legacy standalone version)
├── observer_app.py                 # (Legacy standalone version)
└── README.md                       # This file
```

### File Organization
- **Home.py** - The main entry point with navigation
- **pages/** - Contains the individual app pages (Streamlit auto-detects these)
- **teachings.py** - Shared database of philosophical teachings
- Legacy files (main.py, SitwithIt.py, observer_app.py) are kept for backward compatibility

## Get Your API Key

Get your Anthropic API key at: https://console.anthropic.com
