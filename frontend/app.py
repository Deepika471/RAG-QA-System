import streamlit as st

from utils.api_client import (
    ask_question,
    upload_pdf,
    reset_all,
    health_check,
    get_history,
    create_new_chat
)

# ─────────────────────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="PDF Q&A",
    page_icon="📄",
    layout="wide"
)

# ─────────────────────────────────────────────────────────────
# Backend Health Check
# ─────────────────────────────────────────────────────────────

if not health_check():

    st.error(
        "Backend is not running.\n\n"
        "Start backend using:\n"
        "`py -m uvicorn main:app --reload --port 8000`"
    )

    st.stop()

# ─────────────────────────────────────────────────────────────
# Session State
# ─────────────────────────────────────────────────────────────

if "selected_pdf" not in st.session_state:
    st.session_state.selected_pdf = None

if "selected_chat" not in st.session_state:
    st.session_state.selected_chat = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# ─────────────────────────────────────────────────────────────
# Load Persistent History
# ─────────────────────────────────────────────────────────────

history_response = get_history()

history_data = history_response.get(
    "history",
    {}
)

# ─────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────

with st.sidebar:

    st.title("📄 PDF Q&A")

    st.caption(
        "Powered by Gemini + RAG"
    )

    st.divider()

     # ─────────────────────────────────────────────────────────
    # NEW PDF CHAT BUTTON
    # ─────────────────────────────────────────────────────────

    if st.button(
        "➕ New PDF Chat",
        use_container_width=True
    ):

        st.session_state.selected_pdf = None

        st.session_state.selected_chat = None

        st.session_state.messages = []

        if "last_uploaded_file" in st.session_state:
            del st.session_state.last_uploaded_file

        st.rerun()

    st.divider()

    # ─────────────────────────────────────────────────────────
    # Chat History
    # ─────────────────────────────────────────────────────────

    st.subheader("🕓 Chat History")

    if history_data:

        for pdf_name, pdf_data in history_data.items():

            with st.expander(
                f"📄 {pdf_name}",
                expanded=False
            ):

                chats = pdf_data.get(
                    "chats",
                    {}
                )

                for chat_id, chat_data in chats.items():

                    if st.button(
                        f"💬 {chat_data['title']}",
                        key=f"{pdf_name}_{chat_id}",
                        use_container_width=True
                    ):

                        st.session_state.selected_pdf = pdf_name

                        st.session_state.selected_chat = chat_id

                        st.session_state.messages = (
                            chat_data.get(
                                "messages",
                                []
                            )
                        )

                        st.rerun()

                st.divider()

                # ─────────────────────────────────────────────
                # NEW CHAT FOR SAME PDF
                # ─────────────────────────────────────────────

                if st.button(
                    "➕ New Chat",
                    key=f"new_chat_{pdf_name}",
                    use_container_width=True
                ):

                    response = create_new_chat(
                        pdf_name
                    )

                    new_chat_id = response[
                        "chat_id"
                    ]

                    st.session_state.selected_pdf = pdf_name

                    st.session_state.selected_chat = new_chat_id

                    st.session_state.messages = []

                    st.rerun()

    else:

        st.caption(
            "No PDFs uploaded yet."
        )

    st.divider()

    # ─────────────────────────────────────────────────────────
    # Clear Everything
    # ─────────────────────────────────────────────────────────

    if st.button(
        "🗑️ Clear Everything",
        use_container_width=True
    ):

        try:

            reset_all()

            st.session_state.messages = []

            st.session_state.selected_pdf = None

            st.session_state.selected_chat = None

            if "last_uploaded_file" in st.session_state:
                del st.session_state.last_uploaded_file

            st.success(
                "Everything cleared."
            )

            st.rerun()

        except Exception as e:

            st.error(
                f"Reset failed: {e}"
            )
    
    # ─────────────────────────────────────────────────────────
    # Model Info
    # ─────────────────────────────────────────────────────────

    st.subheader("🤖 Model Info")

    st.info(
        "**LLM:** Gemini 2.5 Flash\n\n"
        "**Embeddings:** HuggingFace MiniLM\n\n"
        "**Vector DB:** ChromaDB"
    )

    st.divider()

# ─────────────────────────────────────────────────────────────
# Main Area
# ─────────────────────────────────────────────────────────────

st.title("Ask anything about your PDF")

st.caption(
    "Upload PDFs, create multiple chats, and continue conversations."
)

st.divider()

# ─────────────────────────────────────────────────────────────
# Upload PDF
# ─────────────────────────────────────────────────────────────

uploaded = st.file_uploader(
    "📎 Upload a PDF",
    type=["pdf"]
)

if uploaded is not None:

    if (
        "last_uploaded_file" not in st.session_state
        or st.session_state.last_uploaded_file != uploaded.name
    ):

        with st.spinner(
            "Reading and indexing PDF..."
        ):

            try:

                result = upload_pdf(
                    uploaded.read(),
                    uploaded.name
                )

                st.session_state.last_uploaded_file = uploaded.name

                st.session_state.selected_pdf = uploaded.name

                # reload history
                history_response = get_history()

                history_data = history_response.get(
                    "history",
                    {}
                )

                pdf_data = history_data.get(
                    uploaded.name,
                    {}
                )

                active_chat = pdf_data.get(
                    "active_chat"
                )

                st.session_state.selected_chat = active_chat

                st.session_state.messages = []

                st.success(
                    f"✅ {uploaded.name} indexed successfully!"
                )

                st.info(
                    f"{result['chunks']} chunks indexed"
                )

                st.rerun()

            except Exception as e:

                st.error(
                    f"Upload failed: {e}"
                )

# ─────────────────────────────────────────────────────────────
# Current Chat Header
# ─────────────────────────────────────────────────────────────

if st.session_state.selected_pdf:

    st.markdown(
        f"### 📄 {st.session_state.selected_pdf}"
    )

if st.session_state.selected_chat:

    st.caption(
        f"Current Chat ID: "
        f"{st.session_state.selected_chat[:8]}"
    )

st.divider()

# ─────────────────────────────────────────────────────────────
# Render Messages
# ─────────────────────────────────────────────────────────────

for msg in st.session_state.messages:

    with st.chat_message(
        msg["role"]
    ):

        st.write(
            msg["content"]
        )

        if msg.get("sources"):

            st.caption(
                f"Sources: {', '.join(msg['sources'])}"
            )

# ─────────────────────────────────────────────────────────────
# Chat Input
# ─────────────────────────────────────────────────────────────

question = st.chat_input(
    "Ask a question about your PDF..."
)

if question:

    if not st.session_state.selected_pdf:

        st.warning(
            "Please upload a PDF first."
        )

        st.stop()

    # user message
    st.session_state.messages.append({

        "role": "user",

        "content": question
    })

    with st.chat_message("user"):

        st.write(question)

    # assistant response
    with st.chat_message("assistant"):

        with st.spinner(
            "Searching document..."
        ):

            try:

                data = ask_question(

                    question,

                    st.session_state.selected_pdf,

                    st.session_state.selected_chat
                )

                answer = data.get(
                    "answer",
                    "No answer returned."
                )

                sources = data.get(
                    "sources",
                    []
                )

            except Exception as e:

                answer = (
                    f"Error contacting backend: {e}"
                )

                sources = []

        st.write(answer)

        if sources:

            st.caption(
                f"Sources: {', '.join(sources)}"
            )

    # assistant message
    st.session_state.messages.append({

        "role": "assistant",

        "content": answer,

        "sources": sources
    })