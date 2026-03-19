import urllib.parse
import streamlit as st
from quotes_service import get_random_quote, QuoteError

st.set_page_config(page_title="Dev Quote", page_icon="💡", layout="centered")

st.markdown("""
<style>
    .main { background-color: #0f1117; }
    .block-container { padding-top: 2rem; max-width: 680px; }
    .quote-box {
        background: #1e2333;
        border-left: 4px solid #6366f1;
        border-radius: 12px;
        padding: 28px 32px;
        margin: 20px 0;
    }
    .quote-text {
        font-size: 1.3rem;
        font-style: italic;
        color: #f0f0f8;
        line-height: 1.7;
        margin-bottom: 16px;
    }
    .quote-author {
        font-size: 0.95rem;
        color: #818cf8;
        font-weight: 600;
        letter-spacing: 0.03em;
    }
    .app-title {
        font-size: 2rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 4px;
    }
    .app-subtitle {
        color: #6b7280;
        font-size: 0.95rem;
        margin-bottom: 2rem;
    }
    div.stButton > button {
        background: #6366f1;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 10px 20px;
        width: 100%;
    }
    div.stButton > button:hover { opacity: 0.88; }
    div.stDownloadButton > button {
        background: #1e2333;
        color: #818cf8;
        border: 1px solid #6366f1;
        border-radius: 8px;
        font-weight: 600;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="app-title">💡 Dev Quote</div>', unsafe_allow_html=True)
st.markdown('<div class="app-subtitle">Instant inspiration for developers, founders, and builders.</div>', unsafe_allow_html=True)

if "current_quote" not in st.session_state:
    st.session_state.current_quote = None

with st.sidebar:
    st.markdown("### Options")
    topic = st.selectbox(
        "Topic",
        options=["Any", "Programming", "Technology", "Inspiration", "Entrepreneurship", "Mindset", "Finance"],
        index=0,
        help="Narrow the vibe; falls back gracefully if provider lacks tags.",
    )
    st.markdown("---")
    st.caption("Tip: Use the **↻ New quote** button any time.")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("↻ New quote", use_container_width=True):
        try:
            st.session_state.current_quote = get_random_quote(topic)
            st.toast("Fresh quote loaded ✅")
        except QuoteError as e:
            st.error(f"Could not fetch a quote: {e}")

with col2:
    if st.button("📋 Copy", use_container_width=True, disabled=st.session_state.current_quote is None):
        q = st.session_state.current_quote or {"text": "", "author": ""}
        st.code(f'{q["text"]}\n— {q["author"]}')
        st.toast("Select the block above and copy.")

if st.session_state.current_quote is None:
    try:
        st.session_state.current_quote = get_random_quote(topic)
    except QuoteError as e:
        st.error(f"Could not fetch a quote: {e}")

quote = st.session_state.current_quote

if quote:
    st.markdown(f"""
    <div class="quote-box">
        <div class="quote-text">"{quote['text']}"</div>
        <div class="quote-author">— {quote['author']}</div>
    </div>
    """, unsafe_allow_html=True)

    tweet_text = f'{quote["text"]} — {quote["author"]}'
    tweet_url = (
        "https://x.com/intent/tweet?"
        + urllib.parse.urlencode({"text": tweet_text, "hashtags": "DevQuote"})
    )

    c1, c2 = st.columns([1, 1])
    with c1:
        st.link_button("𝕏 Share on X", tweet_url, use_container_width=True)
    with c2:
        st.download_button(
            "⬇️ Save as text",
            data=f'{quote["text"]}\n— {quote["author"]}\n',
            file_name="quote.txt",
            mime="text/plain",
            use_container_width=True,
        )
