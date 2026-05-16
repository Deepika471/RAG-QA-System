import google.generativeai as genai

from app.vector_store import load_vector_store

from app.memory import (
    get_chat_messages,
    save_chat
)

from app.config import GEMINI_API_KEY


# ─────────────────────────────────────────────────────────────
# Gemini Configuration
# ─────────────────────────────────────────────────────────────

genai.configure(
    api_key=GEMINI_API_KEY
)

model = genai.GenerativeModel(
    "models/gemini-2.5-flash"
)

# ─────────────────────────────────────────────────────────────
# Ask Question
# ─────────────────────────────────────────────────────────────

def ask_question(
    query,
    pdf_name,
    chat_id
):

    try:

        # load vector db
        vectorstore = load_vector_store()

        retriever = vectorstore.as_retriever(
            search_kwargs={"k": 5}
        )

        # retrieve docs
        relevant_docs = retriever.invoke(query)

        print(
            "RETRIEVED DOCS:",
            len(relevant_docs)
        )

        # build context
        context = "\n\n".join([
            doc.page_content
            for doc in relevant_docs
        ])

        # previous chat history
        previous_messages = get_chat_messages(
            pdf_name,
            chat_id
        )

        history_text = ""

        for msg in previous_messages:

            history_text += (
                f"{msg['role']}: "
                f"{msg['content']}\n"
            )

        # final prompt
        prompt = f"""
        You are an intelligent PDF assistant.

        Use the uploaded PDF context
        and previous conversation to answer.

        Previous Conversation:
        {history_text}

        PDF Context:
        {context}

        User Question:
        {query}

        Give a clear, concise,
        intelligent answer.
        """

        # Gemini response
        response = model.generate_content(
            prompt
        )

        answer = response.text

        # save into history
        save_chat(
            pdf_name,
            chat_id,
            query,
            answer
        )

        return answer

    except Exception as e:

        return f"Error: {str(e)}"