# Streamlit Multipage App Guide

## What Changed?

The app has been restructured to use Streamlit's native **multipage app** feature instead of tabs. This is cleaner and gives each app its own URL and navigation.

## New Structure

```
contemplationApp/
├── Home.py                         # 🏠 Main entry point (run this!)
└── pages/
    ├── 1_◎_Sit_With_This.py       # Page 1
    └── 2_👁_The_Observer.py        # Page 2
```

## How It Works

### 1. **Run the Home Page**
```bash
streamlit run Home.py
```

### 2. **Streamlit Auto-Discovers Pages**
- Any `.py` files in the `pages/` folder become separate pages
- The filename prefix (`1_`, `2_`) determines the order
- The emoji and text after become the page name in the sidebar

### 3. **Navigation**
- **Sidebar**: Automatically populated with page links
- **Home buttons**: Direct navigation via `st.switch_page()`
- **URL-based**: Each page has its own URL (e.g., `/Sit_With_This`)

## Benefits Over Tabs

### ✅ Cleaner Code
- No `exec()` calls or code injection
- Each app runs independently
- No CSS conflicts

### ✅ Better UX
- Each app has its own URL (shareable links!)
- Browser back/forward buttons work
- Sidebar navigation is automatic

### ✅ Individual Styling
- Each page keeps its own CSS completely
- No need to remove conflicting styles
- Original colors and layouts preserved

### ✅ State Management
- Each page has isolated state
- Switching pages doesn't lose app-specific state
- More predictable behavior

## File Naming Convention

Streamlit uses the filename to determine:
1. **Sort order**: `1_`, `2_`, `3_`
2. **Icon**: `◎`, `👁`, etc.
3. **Display name**: `Sit_With_This` → "Sit With This"

Examples:
- `1_◎_Sit_With_This.py` → "◎ Sit With This" (first in sidebar)
- `2_👁_The_Observer.py` → "👁 The Observer" (second in sidebar)

## URLs

Each page gets its own URL:
- Home: `http://localhost:8501/`
- Sit With This: `http://localhost:8501/Sit_With_This`
- The Observer: `http://localhost:8501/The_Observer`

## Adding More Pages

To add a new page:

1. Create a new file in `pages/` folder
2. Name it: `3_🔮_Your_Page_Name.py`
3. Add page config at the top:
   ```python
   st.set_page_config(
       page_title="Your Page",
       page_icon="🔮",
       layout="centered",
       initial_sidebar_state="expanded"
   )
   ```
4. Build your app below
5. Streamlit automatically adds it to the sidebar!

## Legacy Files

These files are kept for backward compatibility but are no longer the main entry point:
- `main.py` - Old tab-based combined app
- `SitwithIt.py` - Old standalone version
- `observer_app.py` - Old standalone version

You can still run them individually if needed, but the multipage app is the recommended approach.

## Key Differences

### Old (Tab-based with main.py)
```python
tab1, tab2 = st.tabs(["App 1", "App 2"])
with tab1:
    exec(...)  # Load app 1
with tab2:
    exec(...)  # Load app 2
```

### New (Multipage)
```
Home.py (landing page)
pages/
  ├── 1_App_One.py
  └── 2_App_Two.py
```

Each page is a standalone script that Streamlit automatically discovers and adds to navigation!

## Running the App

**New way (recommended):**
```bash
streamlit run Home.py
```

**Old ways (still work):**
```bash
streamlit run main.py        # Tab-based version
streamlit run SitwithIt.py   # Standalone Sit With This
streamlit run observer_app.py # Standalone Observer
```
