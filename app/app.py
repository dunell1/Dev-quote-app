import urllib.parse
import streamlit as st
from quotes_service import get_random_quote, QuoteError

st.set_page_config(page_title="Dev Quote", page_icon="💡", layout="centered")

st.title("💡 Dev Quote")
st.caption("Instant inspiration for developers. Fresh quotes, one click.")

if "current_quote" not in st.session_state:
    st.session_state.current_quote = None

with st.sidebar:
    st.subheader("Options")
    topic = st.selectbox(
        "Topic",
        options=["Any", "Programming", "Technology", "Inspiration"],
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
            st.toast("Fetched a new quote ✅")
        except QuoteError as e:
            st.error(f"Could not fetch a quote: {e}")

with col2:
    if st.button("📋 Copy", use_container_width=True, disabled=st.session_state.current_quote is None):
        q = st.session_state.current_quote or {"text": "", "author": ""}
        st.code(f'{q["text"]}\n— {q["author"]}')
        st.toast("Copied block is shown above — Select & copy.")

if st.session_state.current_quote is None:
    try:
        st.session_state.current_quote = get_random_quote(topic)
    except QuoteError as e:
        st.error(f"Could not fetch a quote: {e}")

quote = st.session_state.current_quote

if quote:
    with st.container(border=True):
        st.markdown(f"### “{quote['text']}”")
        st.markdown(f"— **{quote['author']}**")

    tweet_text = f'{quote["text"]} — {quote["author"]}'
    tweet_url = (
        "https://twitter.com/intent/tweet?"
        + urllib.parse.urlencode({"text": tweet_text, "hashtags": "DevQuote"})
    )

    c1, c2 = st.columns([1, 1])
    with c1:
        st.link_button("🐦 Tweet this", tweet_url, use_container_width=True)
    with c2:
        st.download_button(
            "⬇️ Save as text",
            data=f'{quote["text"]}\n— {quote["author"]}\n',
            file_name="quote.txt",
            mime="text/plain",
            use_container_width=True,
        )

st.caption("Made with ❤️ using Streamlit. Source ready for deploy.")
