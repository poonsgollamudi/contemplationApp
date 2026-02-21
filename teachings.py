"""
Curated teachings from Eastern and Western philosophical traditions.
Each teaching is paraphrased/distilled — the insight, not the exact words.

Now includes LLM-powered dynamic teaching generation to supplement the curated list.
"""

import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

THEMES = {
    "all": {"label": "All Teachings", "icon": "◎", "color": "#c9b8a0"},
    "mind": {"label": "Mind & Thought", "icon": "◉", "color": "#e8c9a0"},
    "love": {"label": "Love & Connection", "icon": "❋", "color": "#c9a0e8"},
    "body": {"label": "Body & Presence", "icon": "⊛", "color": "#a0e8c9"},
    "ego": {"label": "Ego & Self", "icon": "◈", "color": "#e8a0a0"},
    "freedom": {"label": "Freedom & Truth", "icon": "✦", "color": "#a0c9e8"},
    "stillness": {"label": "Stillness & Being", "icon": "○", "color": "#c9c9a0"},
}

TEACHINGS = [
    # ── KRISHNAMURTI ──
    {"philosopher": "J. Krishnamurti", "theme": "mind", "tradition": "Indian",
     "teaching": "The observer is the observed. When you watch your jealousy, the watcher is not separate from the jealousy — they are one movement."},
    {"philosopher": "J. Krishnamurti", "theme": "freedom", "tradition": "Indian",
     "teaching": "Truth is a pathless land. No organization, no belief, no dogma can lead you to it. You must walk alone."},
    {"philosopher": "J. Krishnamurti", "theme": "mind", "tradition": "Indian",
     "teaching": "The ability to observe without evaluating is the highest form of intelligence."},
    {"philosopher": "J. Krishnamurti", "theme": "love", "tradition": "Indian",
     "teaching": "When you love, there is no duty. Duty arises only when love has gone. Where there is love, the word duty has no meaning."},
    {"philosopher": "J. Krishnamurti", "theme": "ego", "tradition": "Indian",
     "teaching": "The constant assertion of belief is an indication of fear. When there is no fear, the mind is free to inquire."},
    {"philosopher": "J. Krishnamurti", "theme": "stillness", "tradition": "Indian",
     "teaching": "In the space between two thoughts, there is a silence — and in that silence, the whole of life is contained."},
    {"philosopher": "J. Krishnamurti", "theme": "mind", "tradition": "Indian",
     "teaching": "It is no measure of health to be well adjusted to a profoundly sick society."},
    {"philosopher": "J. Krishnamurti", "theme": "body", "tradition": "Indian",
     "teaching": "The body has its own intelligence, which has been developed over millennia. We override it constantly with thought."},
    {"philosopher": "J. Krishnamurti", "theme": "freedom", "tradition": "Indian",
     "teaching": "Freedom is not a reaction; freedom is not choice. Where there is choice, there is no freedom, because choice is always motivated by conditioning."},
    {"philosopher": "J. Krishnamurti", "theme": "mind", "tradition": "Indian",
     "teaching": "To understand the immeasurable, the mind must be extraordinarily quiet, still."},

    # ── OSHO ──
    {"philosopher": "Osho", "theme": "stillness", "tradition": "Indian",
     "teaching": "Be — don't try to become. Becoming is the disease of the mind. Being is the nature of existence."},
    {"philosopher": "Osho", "theme": "love", "tradition": "Indian",
     "teaching": "If you love a flower, don't pick it up. Because if you pick it up it dies. Love is not about possession. Love is about appreciation."},
    {"philosopher": "Osho", "theme": "ego", "tradition": "Indian",
     "teaching": "The ego is just a shadow on the wall. You have mistaken the shadow for reality, and now you defend something that was never there."},
    {"philosopher": "Osho", "theme": "mind", "tradition": "Indian",
     "teaching": "Mind is a beautiful servant but a dangerous master. When you allow it to take over, you lose touch with what is alive in you."},
    {"philosopher": "Osho", "theme": "freedom", "tradition": "Indian",
     "teaching": "Courage is not the absence of fear. Courage is the total presence of fear, with the willingness to move forward regardless."},
    {"philosopher": "Osho", "theme": "body", "tradition": "Indian",
     "teaching": "The body is your first home. Before you try to reach the sky, learn to be rooted in the earth. The tree that reaches highest is the one with the deepest roots."},
    {"philosopher": "Osho", "theme": "stillness", "tradition": "Indian",
     "teaching": "Meditation is not concentration. Concentration is narrowing. Meditation is expanding — becoming vast, becoming the sky."},
    {"philosopher": "Osho", "theme": "love", "tradition": "Indian",
     "teaching": "Love is the only real thing. Everything else is mind-made. But you cannot practice love — you can only remove the barriers you have built against it."},

    # ── RUMI ──
    {"philosopher": "Rumi", "theme": "love", "tradition": "Sufi",
     "teaching": "Your task is not to seek for love, but merely to find all the barriers within yourself that you have built against it."},
    {"philosopher": "Rumi", "theme": "stillness", "tradition": "Sufi",
     "teaching": "Silence is the language of God. Everything else is a poor translation."},
    {"philosopher": "Rumi", "theme": "ego", "tradition": "Sufi",
     "teaching": "You are not a drop in the ocean. You are the entire ocean in a drop."},
    {"philosopher": "Rumi", "theme": "freedom", "tradition": "Sufi",
     "teaching": "Why do you stay in prison when the door is so wide open? The chains you feel are the ones you have forged yourself."},
    {"philosopher": "Rumi", "theme": "body", "tradition": "Sufi",
     "teaching": "There is a voice that doesn't use words. Listen to it. The body knows things the mind has not yet understood."},
    {"philosopher": "Rumi", "theme": "love", "tradition": "Sufi",
     "teaching": "Let yourself be silently drawn by the strange pull of what you truly love. It will not lead you astray."},
    {"philosopher": "Rumi", "theme": "mind", "tradition": "Sufi",
     "teaching": "Sell your cleverness and buy bewilderment. Cleverness is mere opinion; bewilderment is the beginning of seeing."},
    {"philosopher": "Rumi", "theme": "stillness", "tradition": "Sufi",
     "teaching": "In the middle of the night, I cry out — who in this house is awake? The real answer is not a name. It is the wakefulness itself."},

    # ── LAO TZU ──
    {"philosopher": "Lao Tzu", "theme": "stillness", "tradition": "Taoist",
     "teaching": "Nature does not hurry, yet everything is accomplished. The river reaches the sea not by force but by finding the way."},
    {"philosopher": "Lao Tzu", "theme": "ego", "tradition": "Taoist",
     "teaching": "When I let go of what I am, I become what I might be. The soft overcomes the hard. The gentle overcomes the rigid."},
    {"philosopher": "Lao Tzu", "theme": "mind", "tradition": "Taoist",
     "teaching": "The more you know, the less you understand. True wisdom is knowing what you do not know."},
    {"philosopher": "Lao Tzu", "theme": "freedom", "tradition": "Taoist",
     "teaching": "Care about what other people think and you will always be their prisoner."},
    {"philosopher": "Lao Tzu", "theme": "body", "tradition": "Taoist",
     "teaching": "The body follows the breath. The breath follows the mind. But the wise let the mind follow the body's natural rhythm."},

    # ── BUDDHA ──
    {"philosopher": "Buddha", "theme": "mind", "tradition": "Buddhist",
     "teaching": "We are what we think. All that we are arises with our thoughts. With our thoughts, we make the world."},
    {"philosopher": "Buddha", "theme": "body", "tradition": "Buddhist",
     "teaching": "To keep the body in good health is a duty — otherwise we shall not be able to keep the mind strong and clear."},
    {"philosopher": "Buddha", "theme": "ego", "tradition": "Buddhist",
     "teaching": "The root of suffering is attachment. Not to things, but to the idea that things should be other than they are."},
    {"philosopher": "Buddha", "theme": "stillness", "tradition": "Buddhist",
     "teaching": "Do not dwell in the past, do not dream of the future. Concentrate the mind on the present moment."},
    {"philosopher": "Buddha", "theme": "love", "tradition": "Buddhist",
     "teaching": "Hatred does not cease by hatred, but only by love. This is the ancient and eternal law."},

    # ── NIETZSCHE ──
    {"philosopher": "Nietzsche", "theme": "body", "tradition": "Western",
     "teaching": "Behind your thoughts and feelings stands a mighty ruler, an unknown sage — whose name is self. In your body it dwells, your body it is."},
    {"philosopher": "Nietzsche", "theme": "freedom", "tradition": "Western",
     "teaching": "The individual has always had to struggle to keep from being overwhelmed by the tribe. But no price is too high for the privilege of owning yourself."},
    {"philosopher": "Nietzsche", "theme": "ego", "tradition": "Western",
     "teaching": "He who has a why to live can bear almost any how. But first he must discover his own why — not borrow someone else's."},
    {"philosopher": "Nietzsche", "theme": "mind", "tradition": "Western",
     "teaching": "There are no facts, only interpretations. The mind does not discover truth — it constructs it from what it has already decided to believe."},

    # ── SPINOZA ──
    {"philosopher": "Spinoza", "theme": "body", "tradition": "Western",
     "teaching": "The mind and body are not two things but two expressions of the same reality. You cannot nourish one while neglecting the other."},
    {"philosopher": "Spinoza", "theme": "love", "tradition": "Western",
     "teaching": "The highest activity a human being can attain is learning for understanding, because to understand is to be free."},
    {"philosopher": "Spinoza", "theme": "freedom", "tradition": "Western",
     "teaching": "Peace is not the absence of war — it is a virtue, a state of mind, a disposition for benevolence, confidence, and justice."},

    # ── MARCUS AURELIUS ──
    {"philosopher": "Marcus Aurelius", "theme": "mind", "tradition": "Stoic",
     "teaching": "You have power over your mind — not outside events. Realize this, and you will find strength."},
    {"philosopher": "Marcus Aurelius", "theme": "stillness", "tradition": "Stoic",
     "teaching": "Look well into thyself; there is a source of strength which will always spring up if thou wilt always look."},
    {"philosopher": "Marcus Aurelius", "theme": "ego", "tradition": "Stoic",
     "teaching": "How much time he gains who does not look to see what his neighbor says or does or thinks, but only at what he himself is doing."},

    # ── EPICTETUS ──
    {"philosopher": "Epictetus", "theme": "freedom", "tradition": "Stoic",
     "teaching": "It is not things that disturb us, but our judgments about things. The interpretation is where the suffering lives."},
    {"philosopher": "Epictetus", "theme": "mind", "tradition": "Stoic",
     "teaching": "First say to yourself what you would be; and then do what you have to do. But begin with the saying — because the saying reveals what you truly believe."},

    # ── THICH NHAT HANH ──
    {"philosopher": "Thich Nhat Hanh", "theme": "body", "tradition": "Buddhist",
     "teaching": "Feelings come and go like clouds in a windy sky. Conscious breathing is my anchor."},
    {"philosopher": "Thich Nhat Hanh", "theme": "stillness", "tradition": "Buddhist",
     "teaching": "The present moment is filled with joy and happiness. If you are attentive, you will see it."},
    {"philosopher": "Thich Nhat Hanh", "theme": "love", "tradition": "Buddhist",
     "teaching": "Understanding someone's suffering is the best gift you can give another person. Understanding is love's other name."},

    # ── MERLEAU-PONTY ──
    {"philosopher": "Merleau-Ponty", "theme": "body", "tradition": "Western",
     "teaching": "We do not have bodies — we are bodies. The body is not an object we observe from outside. It is the very medium through which we experience the world."},
    {"philosopher": "Merleau-Ponty", "theme": "mind", "tradition": "Western",
     "teaching": "The body understands what the mind has not yet learned to say. There is knowledge in your hands, your posture, your breath."},

    # ── ALAN WATTS ──
    {"philosopher": "Alan Watts", "theme": "ego", "tradition": "Western-Eastern",
     "teaching": "Trying to define yourself is like trying to bite your own teeth. The self you are looking for is the self that is looking."},
    {"philosopher": "Alan Watts", "theme": "stillness", "tradition": "Western-Eastern",
     "teaching": "Muddy water is best cleared by leaving it alone. The mind, too, clears itself when you stop stirring it."},
    {"philosopher": "Alan Watts", "theme": "body", "tradition": "Western-Eastern",
     "teaching": "You didn't come into this world. You came out of it, like a wave from the ocean. You are not a stranger here."},
    {"philosopher": "Alan Watts", "theme": "freedom", "tradition": "Western-Eastern",
     "teaching": "The only way to make sense out of change is to plunge into it, move with it, and join the dance."},

    # ── HAFIZ ──
    {"philosopher": "Hafiz", "theme": "love", "tradition": "Sufi",
     "teaching": "Even after all this time, the sun never says to the earth, 'You owe me.' Look what happens with a love like that — it lights the whole world."},
    {"philosopher": "Hafiz", "theme": "freedom", "tradition": "Sufi",
     "teaching": "Fear is the cheapest room in the house. I would like to see you living in better conditions."},

    # ── SENECA ──
    {"philosopher": "Seneca", "theme": "mind", "tradition": "Stoic",
     "teaching": "We suffer more often in imagination than in reality. The mind rehearses disasters that never arrive."},
    {"philosopher": "Seneca", "theme": "stillness", "tradition": "Stoic",
     "teaching": "It is not that we have a short time to live, but that we waste a great deal of it."},

    # ── HERACLITUS ──
    {"philosopher": "Heraclitus", "theme": "body", "tradition": "Western",
     "teaching": "No one steps in the same river twice, for it is not the same river and they are not the same person. Everything flows."},
    {"philosopher": "Heraclitus", "theme": "mind", "tradition": "Western",
     "teaching": "The eyes and ears are poor witnesses to those who have barbarian souls. Perception without understanding is noise."},

    # ── KABIR ──
    {"philosopher": "Kabir", "theme": "love", "tradition": "Indian",
     "teaching": "I laugh when I hear that the fish in the water is thirsty. You wander restlessly from forest to forest while the reality is within your own dwelling."},
    {"philosopher": "Kabir", "theme": "ego", "tradition": "Indian",
     "teaching": "Wherever you are is the entry point. Do not search for the door — you are standing in it."},

    # ── CHUANG TZU ──
    {"philosopher": "Chuang Tzu", "theme": "freedom", "tradition": "Taoist",
     "teaching": "Happiness is the absence of the striving for happiness. The fish does not know it swims in water."},
    {"philosopher": "Chuang Tzu", "theme": "stillness", "tradition": "Taoist",
     "teaching": "Flow with whatever may happen and let your mind be free. Stay centered by accepting whatever you are doing."},
]


def get_philosophers():
    """Return unique list of philosophers."""
    return sorted(set(t["philosopher"] for t in TEACHINGS))


def get_traditions():
    """Return unique list of traditions."""
    return sorted(set(t["tradition"] for t in TEACHINGS))


def filter_teachings(theme=None, philosopher=None, tradition=None):
    """Filter teachings by theme, philosopher, or tradition."""
    results = TEACHINGS
    if theme and theme != "all":
        results = [t for t in results if t["theme"] == theme]
    if philosopher:
        results = [t for t in results if t["philosopher"] == philosopher]
    if tradition:
        results = [t for t in results if t["tradition"] == tradition]
    return results


def generate_teaching_from_llm(
    philosopher=None,
    theme=None,
    tradition=None,
    api_key=None,
    count=1
):
    """
    Generate new teachings using Claude AI based on specified criteria.

    Args:
        philosopher: Specific philosopher to generate teachings from (e.g., "Rumi", "Krishnamurti")
        theme: Theme category (e.g., "mind", "love", "stillness")
        tradition: Philosophical tradition (e.g., "Buddhist", "Stoic", "Sufi")
        api_key: Anthropic API key (if not provided, will use environment variable)
        count: Number of teachings to generate (default: 1)

    Returns:
        List of teaching dictionaries with keys: philosopher, theme, tradition, teaching
    """
    if not api_key:
        api_key = os.environ.get("ANTHROPIC_API_KEY")

    if not api_key:
        raise ValueError("API key required. Set ANTHROPIC_API_KEY or pass api_key parameter.")

    # Build context for the LLM
    context_parts = []

    if philosopher:
        context_parts.append(f"philosopher: {philosopher}")
    else:
        # Suggest a random philosopher from the existing list
        philosopher = "a philosopher from Eastern or Western traditions"
        context_parts.append(f"philosopher: {philosopher} (choose one)")

    if theme:
        theme_label = THEMES.get(theme, {}).get("label", theme)
        context_parts.append(f"theme: {theme_label}")
    else:
        theme = "any theme"
        context_parts.append("theme: choose from Mind & Thought, Love & Connection, Body & Presence, Ego & Self, Freedom & Truth, or Stillness & Being")

    if tradition:
        context_parts.append(f"tradition: {tradition}")
    else:
        tradition = "any tradition"
        context_parts.append("tradition: choose from Indian, Buddhist, Taoist, Sufi, Stoic, or Western philosophical traditions")

    context = "\n".join(context_parts)

    # Create the prompt
    prompt = f"""Generate {count} philosophical teaching(s) in JSON format based on these criteria:

{context}

Requirements:
1. Each teaching should be a paraphrased distillation of the philosopher's core insight — the essence, not exact quotes
2. Keep teachings concise (1-3 sentences), profound, and accessible
3. The teaching should capture the authentic spirit and style of the philosopher/tradition
4. Focus on lived wisdom that can be applied to daily life

Return ONLY a JSON array (even if generating 1 teaching) with this exact structure:
[
  {{
    "philosopher": "Name of Philosopher",
    "theme": "mind|love|body|ego|freedom|stillness",
    "tradition": "Indian|Buddhist|Taoist|Sufi|Stoic|Western|Western-Eastern",
    "teaching": "The actual teaching text here..."
  }}
]

Examples from the existing collection:
- J. Krishnamurti (Indian, mind): "The observer is the observed. When you watch your jealousy, the watcher is not separate from the jealousy — they are one movement."
- Rumi (Sufi, love): "Your task is not to seek for love, but merely to find all the barriers within yourself that you have built against it."
- Lao Tzu (Taoist, stillness): "Nature does not hurry, yet everything is accomplished. The river reaches the sea not by force but by finding the way."

Generate {count} new teaching(s) now:"""

    try:
        client = anthropic.Anthropic(api_key=api_key)

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        import json
        response_text = message.content[0].text

        # Extract JSON from response (in case there's extra text)
        start_idx = response_text.find('[')
        end_idx = response_text.rfind(']') + 1

        if start_idx == -1 or end_idx == 0:
            raise ValueError("No JSON array found in response")

        json_str = response_text[start_idx:end_idx]
        teachings = json.loads(json_str)

        # Validate the structure
        for teaching in teachings:
            if not all(k in teaching for k in ["philosopher", "theme", "tradition", "teaching"]):
                raise ValueError("Invalid teaching structure returned from LLM")

        return teachings

    except anthropic.AuthenticationError:
        raise ValueError("Invalid API key")
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse LLM response as JSON: {e}")
    except Exception as e:
        raise RuntimeError(f"Error generating teaching: {str(e)}")
