import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    CHROMA_PATH: str = os.getenv("CHROMA_PATH", "./chroma_db")
    CHUNK_SIZE: int = 200
    OVERLAP: int = 50
    TOP_K: int = 3

settings = Settings()