# ○ Sit With This

A daily philosophical contemplation app. Teachings from Krishnamurti, Osho, Rumi, Lao Tzu, Buddha, Nietzsche, Spinoza, Marcus Aurelius, Epictetus, Thich Nhat Hanh, Merleau-Ponty, Alan Watts, Hafiz, Seneca, Heraclitus, Kabir, and Chuang Tzu.

Uses Claude to generate personalized contemplations — not explanations, but invitations to sit with the insight.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your Anthropic API key
export ANTHROPIC_API_KEY=sk-ant-your-key-here

# 3. Run the app
streamlit run app.py
```

The app opens at `http://localhost:8501`.

You can also enter your API key directly in the sidebar.

## Features

- **Today's Teaching** — one consistent teaching per day, changes at midnight
- **Explore** — browse random teachings, discover new philosophers  
- **6 themes** — Mind & Thought, Love & Connection, Body & Presence, Ego & Self, Freedom & Truth, Stillness & Being
- **Claude-powered contemplations** — unpacks the insight, offers a micro-practice, leaves you with a question to carry
- **65+ teachings** across Indian, Sufi, Taoist, Buddhist, Stoic, and Western traditions

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
sit-with-this/
├── app.py           # Main Streamlit app
├── teachings.py     # Curated teachings database
├── requirements.txt # Dependencies
└── README.md        # This file
```
