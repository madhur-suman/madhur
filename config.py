import os
from dotenv import load_dotenv

# Load environment variables from .env file
try:
    load_dotenv()
except Exception as e:
    print(f"Warning: Could not load .env file: {e}")

class Config:
    # --- Twilio Configuration (for WhatsApp bot) ---
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '')
    TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER', '')

    # --- Hugging Face / Gemini / OpenAI ---
    HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY', '')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

    # --- Database (default to SQLite for hackathon) ---
    # If DATABASE_URL not set, fallback to SQLite file in project root
    DATABASE_URL = os.getenv('DATABASE_URL', f"sqlite:///{os.path.abspath('sales.db')}")
    DB_PATH = os.path.abspath('sales.db')  # Useful if plain SQLite path needed

    # --- Expiry Alert Configuration ---
    EXPIRY_ALERT_DAYS = int(os.getenv('EXPIRY_ALERT_DAYS', '3'))

    # --- Flask Configuration ---
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
