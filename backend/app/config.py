import os

from dotenv import load_dotenv


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(dotenv_path=ENV_PATH)


# GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_API_KEY = "AIzaSyCuCDxsahx5UKS_EGubmV7s2bEF8VP59gI"

# print("API KEY:", GEMINI_API_KEY)


MODEL_NAME = "gemini-pro"

CHUNK_SIZE = 1000

CHUNK_OVERLAP = 200

CHROMA_DB_DIR = os.path.join(BASE_DIR, "chroma_db")