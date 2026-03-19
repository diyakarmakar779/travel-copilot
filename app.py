import streamlit as st
import asyncio
import datetime
from server.agent import run_agent

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Travel Copilot",
    page_icon="✈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --cream:      #FAF7F2;
    --sand:       #EDE8DF;
    --warm:       #D4C5A9;
    --terracotta: #C1694F;
    --terra-lt:   #EDD5CC;
    --ink:        #1A1714;
    --ink-muted:  #6B6460;
    --gold:       #B8860B;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--cream) !important;
    font-family: 'DM Sans', sans-serif;
    color: var(--ink);
}

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"]  { display: none; }
.block-container { padding: 2rem 3rem 4rem !important; max-width: 980px !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: var(--ink) !important;
    border-right: none !important;
}
[data-testid="stSidebar"] * { color: #F5F0EA !important; }

/* sidebar toggle — always visible */
[data-testid="collapsedControl"],
button[kind="header"] {
    display:        flex !important;
    visibility:     visible !important;
    opacity:        1 !important;
    pointer-events: auto !important;
}

/* sidebar nav buttons */
[data-testid="stSidebar"] [data-testid="stButton"] > button {
    background:     transparent !important;
    color:          #C8C0B6 !important;
    border:         none !important;
    border-radius:  4px !important;
    text-align:     left !important;
    font-size:      0.87rem !important;
    font-weight:    400 !important;
    letter-spacing: 0.02em !important;
    text-transform: none !important;
    padding:        0.42rem 0.7rem !important;
    box-shadow:     none !important;
    width:          100% !important;
    transition:     all 0.12s !important;
}
[data-testid="stSidebar"] [data-testid="stButton"] > button:hover {
    background: rgba(250,247,242,0.08) !important;
    color:      #FAF7F2 !important;
}

/* ── Masthead ── */
.masthead {
    border-bottom: 2px solid var(--ink);
    padding-bottom: 0.5rem;
    margin-bottom: 0.2rem;
    display: flex;
    align-items: baseline;
    gap: 1rem;
}
.masthead-title {
    font-family: 'Playfair Display', serif;
    font-size:   3rem;
    font-weight: 700;
    letter-spacing: -1px;
    line-height: 1;
    color: var(--ink);
}
.masthead-sub {
    font-size:   0.72rem;
    font-weight: 300;
    text-transform: uppercase;
    letter-spacing: 0.18em;
    color: var(--ink-muted);
}
.dateline {
    font-size:   0.68rem;
    color:       var(--ink-muted);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 1.4rem;
    border-bottom: 0.5px solid var(--warm);
    padding-bottom: 0.45rem;
}

/* ── Pills — pure HTML, no Streamlit button conflicts ── */
.pill-row { display: flex; gap: 0.5rem; margin-bottom: 0.4rem; flex-wrap: wrap; }
.pill {
    padding:        0.38rem 1.1rem;
    border:         1.5px solid var(--ink);
    border-radius:  100px;
    font-size:      0.8rem;
    font-weight:    500;
    font-family:    'DM Sans', sans-serif;
    background:     transparent;
    color:          var(--ink);
    cursor:         pointer;
    transition:     all 0.15s;
    white-space:    nowrap;
}
.pill:hover                  { background: var(--sand); }
.pill.p-ink                  { background: var(--ink);        color: #FAF7F2; border-color: var(--ink); }
.pill.p-terra                { background: var(--terracotta); color: white;   border-color: var(--terracotta); }
.pill.p-gold                 { background: var(--gold);       color: white;   border-color: var(--gold); }

/* ── Pull quote ── */
.pull-quote {
    border-left:   3px solid var(--terracotta);
    padding:       0.5rem 1rem;
    margin:        0.8rem 0 1.4rem;
    font-family:   'Playfair Display', serif;
    font-style:    italic;
    font-size:     0.98rem;
    color:         var(--ink-muted);
    background:    var(--terra-lt);
    border-radius: 0 4px 4px 0;
}

/* ── Prompt label ── */
.prompt-label {
    font-family:   'Playfair Display', serif;
    font-size:     1.2rem;
    font-style:    italic;
    color:         var(--ink-muted);
    margin-bottom: 0.4rem;
}

/* ── Textarea ── */
[data-testid="stTextArea"] textarea {
    background:    white !important;
    border:        1.5px solid var(--ink) !important;
    border-radius: 4px !important;
    font-family:   'DM Sans', sans-serif !important;
    font-size:     1rem !important;
    color:         var(--ink) !important;
    padding:       0.8rem 1rem !important;
    box-shadow:    3px 3px 0 var(--sand) !important;
    transition:    box-shadow 0.15s !important;
}
[data-testid="stTextArea"] textarea:focus {
    box-shadow: 5px 5px 0 var(--warm) !important;
    outline:    none !important;
}

/* ── ☰ toggle: ghost style, must come before general rule ── */
div[data-testid="stColumn"]:first-child [data-testid="stButton"] > button {
    background:     transparent !important;
    color:          var(--ink-muted) !important;
    border:         1px solid var(--warm) !important;
    border-radius:  4px !important;
    font-size:      1rem !important;
    letter-spacing: 0 !important;
    text-transform: none !important;
    padding:        0.28rem 0.6rem !important;
}
div[data-testid="stColumn"]:first-child [data-testid="stButton"] > button:hover {
    background: var(--sand) !important;
    color:      var(--ink) !important;
}

/* ── All other Streamlit buttons ── */
[data-testid="stButton"] > button {
    background:     var(--ink) !important;
    color:          #FAF7F2 !important;
    border:         none !important;
    border-radius:  4px !important;
    font-family:    'DM Sans', sans-serif !important;
    font-size:      0.82rem !important;
    font-weight:    500 !important;
    letter-spacing: 0.07em !important;
    text-transform: uppercase !important;
    padding:        0.55rem 1.2rem !important;
    transition:     all 0.15s !important;
}
[data-testid="stButton"] > button:hover,
[data-testid="stButton"] > button:active,
[data-testid="stButton"] > button:focus {
    background: var(--terracotta) !important;
    color:      #FAF7F2 !important;
}

/* ── Download button ── */
[data-testid="stDownloadButton"] > button {
    background:     var(--ink) !important;
    color:          #FAF7F2 !important;
    border:         none !important;
    border-radius:  4px !important;
    font-family:    'DM Sans', sans-serif !important;
    font-size:      0.82rem !important;
    font-weight:    500 !important;
    letter-spacing: 0.07em !important;
    text-transform: uppercase !important;
    padding:        0.55rem 1.2rem !important;
    width:          100% !important;
    transition:     all 0.15s !important;
}
[data-testid="stDownloadButton"] > button:hover,
[data-testid="stDownloadButton"] > button:active,
[data-testid="stDownloadButton"] > button:focus {
    background: var(--terracotta) !important;
    color:      #FAF7F2 !important;
}

/* ── Output header ── */
.output-header {
    display:        flex;
    align-items:    center;
    gap:            0.7rem;
    margin:         1.8rem 0 1rem;
    padding-bottom: 0.6rem;
    border-bottom:  1.5px solid var(--ink);
}
.output-badge {
    font-size:      0.65rem;
    font-weight:    500;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    padding:        0.22rem 0.7rem;
    border-radius:  2px;
}
.b-ink   { background: var(--ink);        color: var(--cream); }
.b-terra { background: var(--terracotta); color: white; }
.b-gold  { background: var(--gold);       color: white; }
.b-all   { background: var(--sand); color: var(--ink); border: 1px solid var(--warm); }

.output-title {
    font-family: 'Playfair Display', serif;
    font-size:   1.1rem;
    font-style:  italic;
    color:       var(--ink-muted);
}

/* ── Divider ── */
.editorial-divider {
    display:     flex;
    align-items: center;
    gap:         0.8rem;
    margin:      1.8rem 0 1rem;
    color:       var(--ink-muted);
    font-size:   0.68rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}
.editorial-divider::before,
.editorial-divider::after {
    content:    '';
    flex:       1;
    height:     0.5px;
    background: var(--warm);
}

/* ── Sidebar custom text elements ── */
.sb-logo    { font-family: 'Playfair Display', serif; font-size: 1.3rem; font-weight: 700; }
.sb-tagline { font-size: 0.6rem; letter-spacing: 0.18em; text-transform: uppercase; color: #9E9892 !important; margin-bottom: 1.4rem; }
.sb-section {
    font-size: 0.6rem; font-weight: 500; letter-spacing: 0.18em;
    text-transform: uppercase; color: #6B6560 !important;
    margin: 1.1rem 0 0.45rem; padding-bottom: 0.3rem;
    border-bottom: 0.5px solid #2E2A26;
}
.dest-chip {
    display: inline-block; padding: 0.22rem 0.6rem;
    background: rgba(250,247,242,0.07); border: 0.5px solid rgba(250,247,242,0.14);
    border-radius: 100px; font-size: 0.7rem; color: #C8C0B6 !important; margin: 0.12rem;
}
.hist-item {
    padding: 0.4rem 0.15rem; border-bottom: 0.5px solid #2A2620;
    font-size: 0.75rem; color: #9E9892 !important; line-height: 1.4;
}

/* selectbox inside sidebar */
[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
    border:        0.5px solid #3A3530 !important;
    background:    rgba(250,247,242,0.05) !important;
    border-radius: 4px !important;
    font-size:     0.82rem !important;
}
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
for k, v in {"mode": "All Features", "history": [], "result": None, "prompt": ""}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Constants ─────────────────────────────────────────────────────────────────
MODES = {
    "All Features": ("✦", "Let Claude decide which tools to invoke"),
    "Itinerary":    ("🗺", "Generate a detailed day-wise travel plan"),
    "Captions":     ("📸", "Instagram captions for your destination"),
    "Reel Ideas":   ("🎬", "Creative short-video concepts for social"),
}
PILL_CLASS  = {"All Features": "p-ink", "Itinerary": "p-ink", "Captions": "p-terra", "Reel Ideas": "p-gold"}
BADGE_CLASS = {"All Features": "b-all",  "Itinerary": "b-ink",  "Captions": "b-terra", "Reel Ideas": "b-gold"}
VERB        = {"All Features": "Plan my trip to", "Itinerary": "Plan my trip to",
               "Captions": "Write Instagram captions for", "Reel Ideas": "Give me reel ideas for"}
DESTINATIONS = ["Jaisalmer", "Kyoto", "Bali", "New York", "Leh",
                "Santorini", "Istanbul", "Kerala", "Paris", "Lisbon"]
MODE_HINTS   = {
    "Itinerary":    "Focus only on generating a detailed day-wise travel itinerary. ",
    "Captions":     "Focus only on generating creative Instagram captions. ",
    "Reel Ideas":   "Focus only on generating creative short-video / Reel ideas. ",
    "All Features": "",
}

# ── Agent wrapper ─────────────────────────────────────────────────────────────
def call_agent(user_prompt: str, mode: str) -> str:
    hint = MODE_HINTS.get(mode, "")
    return asyncio.run(run_agent(f"{hint}{user_prompt}"))

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="sb-logo">Travel Copilot</p>', unsafe_allow_html=True)
    st.markdown('<p class="sb-tagline">AI-powered travel companion</p>', unsafe_allow_html=True)

    st.markdown('<p class="sb-section">Navigation</p>', unsafe_allow_html=True)
    for label, (icon, _) in MODES.items():
        # Show ▶ prefix for active mode so user can tell which is selected
        prefix = "▶  " if st.session_state.mode == label else "     "
        if st.button(f"{prefix}{icon}  {label}", key=f"nav_{label}", use_container_width=True):
            st.session_state.mode = label
            st.rerun()

    st.markdown('<p class="sb-section">Quick Picks</p>', unsafe_allow_html=True)
    chips = "".join(f'<span class="dest-chip">{d}</span>' for d in DESTINATIONS)
    st.markdown(f'<div style="margin-bottom:0.5rem">{chips}</div>', unsafe_allow_html=True)
    chosen = st.selectbox("dest", ["— choose —"] + DESTINATIONS,
                          label_visibility="collapsed", key="dest_select")
    if chosen != "— choose —":
        st.session_state.prompt = f"{VERB[st.session_state.mode]} {chosen}"
        st.rerun()

    if st.session_state.history:
        st.markdown('<p class="sb-section">Recent</p>', unsafe_allow_html=True)
        for h in reversed(st.session_state.history[-5:]):
            st.markdown(
                f'<div class="hist-item">✦ {h[:46]}{"…" if len(h)>46 else ""}</div>',
                unsafe_allow_html=True,
            )

# ── Masthead ──────────────────────────────────────────────────────────────────
today = datetime.date.today().strftime("%B %d, %Y").upper()
st.markdown(f"""
<div class="masthead">
    <span class="masthead-title">Travel Copilot</span>
    <span class="masthead-sub">AI Travel Companion</span>
</div>
<div class="dateline">✈ Your AI-powered travel companion &nbsp;·&nbsp; {today}</div>
""", unsafe_allow_html=True)

# ── Mode pills — st.radio styled as pills (actually clickable) ───────────────
st.markdown("""
<style>
/* Hide the radio circle, style each label as a pill */
div[data-testid="stRadio"] { margin-bottom: 0.4rem; }
div[data-testid="stRadio"] > div { display: flex; gap: 0.5rem; flex-wrap: wrap; }
div[data-testid="stRadio"] > div > label {
    padding: 0.38rem 1.1rem;
    border: 1.5px solid var(--ink);
    border-radius: 100px;
    font-size: 0.8rem;
    font-weight: 500;
    font-family: 'DM Sans', sans-serif;
    cursor: pointer;
    transition: all 0.15s;
    background: transparent !important;
    color: var(--ink) !important;
    white-space: nowrap;
}
div[data-testid="stRadio"] > div > label:hover {
    background: var(--sand) !important;
    color: var(--ink) !important;
}
/* Hide the actual radio dot */
div[data-testid="stRadio"] > div > label > div:first-child { display: none !important; }
/* Active pill — selected label */
div[data-testid="stRadio"] > div > label:has(input:checked) {
    background: var(--ink) !important;
    color: #FAF7F2 !important;
    border-color: var(--ink) !important;
}
/* Active pill text span inside */
div[data-testid="stRadio"] > div > label:has(input:checked) p,
div[data-testid="stRadio"] > div > label:has(input:checked) span {
    color: #FAF7F2 !important;
}
/* Inactive pill text span inside */
div[data-testid="stRadio"] > div > label:not(:has(input:checked)) p,
div[data-testid="stRadio"] > div > label:not(:has(input:checked)) span {
    color: var(--ink) !important;
}
</style>
""", unsafe_allow_html=True)

radio_labels = [f"{icon} {label}" for label, (icon, _) in MODES.items()]
radio_idx    = list(MODES.keys()).index(st.session_state.mode)
selected     = st.radio("mode", radio_labels, index=radio_idx,
                        horizontal=True, label_visibility="collapsed")
# Map selected label back to mode key
selected_mode = list(MODES.keys())[radio_labels.index(selected)]
if selected_mode != st.session_state.mode:
    st.session_state.mode = selected_mode
    st.rerun()

_, desc = MODES[st.session_state.mode]
st.markdown(f'<div class="pull-quote">{desc}</div>', unsafe_allow_html=True)

# ── Prompt input ──────────────────────────────────────────────────────────────
st.markdown('<p class="prompt-label">Where are we headed?</p>', unsafe_allow_html=True)
prompt = st.text_area(
    "prompt",
    value=st.session_state.prompt,
    placeholder='e.g. "Plan my 5-day trip to Jaisalmer" or "Captions for Bali sunset"',
    height=110,
    label_visibility="collapsed",
    key="prompt_box",
)

c1, c2, _ = st.columns([2, 1, 4])
with c1:
    generate = st.button("✦ Generate", use_container_width=True)
with c2:
    if st.button("Clear", use_container_width=True):
        st.session_state.prompt = ""
        st.session_state.result = None
        st.rerun()

# ── Generate ──────────────────────────────────────────────────────────────────
if generate and prompt.strip():
    st.session_state.prompt = prompt
    if prompt not in st.session_state.history:
        st.session_state.history.append(prompt)
    with st.spinner("Crafting your travel story…"):
        st.session_state.result = call_agent(prompt, st.session_state.mode)

# ── Output ────────────────────────────────────────────────────────────────────
if st.session_state.result:
    icon, _ = MODES[st.session_state.mode]
    st.markdown(f"""
<div class="output-header">
    <span class="output-badge {BADGE_CLASS[st.session_state.mode]}">{icon} {st.session_state.mode}</span>
    <span class="output-title">Your travel story</span>
</div>
""", unsafe_allow_html=True)

    st.markdown(st.session_state.result)

    st.markdown('<div class="editorial-divider">Actions</div>', unsafe_allow_html=True)
    a1, a2, a3 = st.columns(3)
    with a1:
        st.download_button(
            "⬇ Download",
            data=st.session_state.result,
            file_name="travel_plan.md",
            mime="text/markdown",
            use_container_width=True,
        )
    with a2:
        if st.button("🔄 Regenerate", use_container_width=True):
            with st.spinner("Reimagining your trip…"):
                st.session_state.result = call_agent(st.session_state.prompt, st.session_state.mode)
            st.rerun()
    with a3:
        if st.button("✦ Follow-up", use_container_width=True):
            st.session_state.prompt = f"Follow up on: {st.session_state.prompt}"
            st.rerun()

elif not generate:
    st.markdown("""
<div style="
    text-align: center; padding: 4rem 2rem; margin-top: 1.5rem;
    border: 1.5px dashed #D4C5A9; border-radius: 4px;
    background: rgba(255,255,255,0.5);
">
    <div style="font-family:'Playfair Display',serif;font-size:1.5rem;font-style:italic;color:#6B6460;margin-bottom:0.4rem;">
        The world is waiting.
    </div>
    <div style="font-size:0.75rem;letter-spacing:0.12em;text-transform:uppercase;color:#B4ABA6;">
        Type a destination above to begin
    </div>
</div>
""", unsafe_allow_html=True)