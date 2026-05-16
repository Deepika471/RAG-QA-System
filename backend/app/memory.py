import json
import os
import uuid

HISTORY_FILE = "chat_history.json"


# ─────────────────────────────────────────────────────────────
# Load Data
# ─────────────────────────────────────────────────────────────

def load_data():

    if not os.path.exists(HISTORY_FILE):

        return {}

    with open(
        HISTORY_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


# ─────────────────────────────────────────────────────────────
# Save Data
# ─────────────────────────────────────────────────────────────

def save_data(data):

    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4
        )


# ─────────────────────────────────────────────────────────────
# Create PDF Session
# ─────────────────────────────────────────────────────────────

def create_pdf_session(pdf_name):

    data = load_data()

    if pdf_name not in data:

        first_chat_id = str(uuid.uuid4())

        data[pdf_name] = {

            "active_chat": first_chat_id,

            "chats": {

                first_chat_id: {

                    "title": "Chat 1",

                    "messages": []
                }
            }
        }

        save_data(data)


# ─────────────────────────────────────────────────────────────
# Create New Chat
# ─────────────────────────────────────────────────────────────

def create_new_chat(pdf_name):

    data = load_data()

    chat_id = str(uuid.uuid4())

    existing_count = len(
        data[pdf_name]["chats"]
    )

    data[pdf_name]["chats"][chat_id] = {

        "title": f"Chat {existing_count + 1}",

        "messages": []
    }

    data[pdf_name]["active_chat"] = chat_id

    save_data(data)

    return chat_id


# ─────────────────────────────────────────────────────────────
# Save Chat
# ─────────────────────────────────────────────────────────────

def save_chat(
    pdf_name,
    chat_id,
    question,
    answer
):

    data = load_data()

    data[pdf_name]["chats"][chat_id]["messages"].append({

        "role": "user",

        "content": question
    })

    data[pdf_name]["chats"][chat_id]["messages"].append({

        "role": "assistant",

        "content": answer
    })

    save_data(data)


# ─────────────────────────────────────────────────────────────
# Get All History
# ─────────────────────────────────────────────────────────────

def get_all_history():

    return load_data()


# ─────────────────────────────────────────────────────────────
# Get Chat Messages
# ─────────────────────────────────────────────────────────────

def get_chat_messages(
    pdf_name,
    chat_id
):

    data = load_data()

    return data[pdf_name]["chats"][chat_id]["messages"]


# ─────────────────────────────────────────────────────────────
# Clear Memory
# ─────────────────────────────────────────────────────────────

def clear_memory():

    save_data({})