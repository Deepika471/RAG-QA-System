import requests

BASE_URL = "http://localhost:8000"


# ─────────────────────────────────────────────────────────────
# Upload PDF
# ─────────────────────────────────────────────────────────────

def upload_pdf(
    file_bytes,
    filename
):

    response = requests.post(

        f"{BASE_URL}/upload",

        files={
            "file": (
                filename,
                file_bytes,
                "application/pdf"
            )
        }
    )

    response.raise_for_status()

    return response.json()


# ─────────────────────────────────────────────────────────────
# Ask Question
# ─────────────────────────────────────────────────────────────

def ask_question(question, pdf_name, chat_id):

    response = requests.post(
        f"{BASE_URL}/ask",
        json={
            "question": question,
            "pdf_name": pdf_name,
            "chat_id": chat_id
        }
    )

    response.raise_for_status()

    return response.json()

# ─────────────────────────────────────────────────────────────
# Create New Chat
# ─────────────────────────────────────────────────────────────

def create_new_chat(
    pdf_name
):

    response = requests.post(
        f"{BASE_URL}/new-chat/{pdf_name}"
    )

    response.raise_for_status()

    return response.json()


# ─────────────────────────────────────────────────────────────
# Get History
# ─────────────────────────────────────────────────────────────

def get_history():

    response = requests.get(
        f"{BASE_URL}/history"
    )

    response.raise_for_status()

    return response.json()


# ─────────────────────────────────────────────────────────────
# Reset
# ─────────────────────────────────────────────────────────────

def reset_all():

    response = requests.post(
        f"{BASE_URL}/reset"
    )

    response.raise_for_status()

    return response.json()


# ─────────────────────────────────────────────────────────────
# Health Check
# ─────────────────────────────────────────────────────────────

def health_check():

    try:

        response = requests.get(
            f"{BASE_URL}/health",
            timeout=2
        )

        return response.status_code == 200

    except Exception:

        return False