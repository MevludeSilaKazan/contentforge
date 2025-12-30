import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")  # anon/public key

# Model ayarları
DEFAULT_MODEL = "llama-3.3-70b-versatile"

# Web Search ayarları
SEARCH_RESULTS_COUNT = 5

# Kullanım limitleri
FREE_MONTHLY_LIMIT = 3
PRO_MONTHLY_LIMIT = 30

# Çıktı ayarları
OUTPUT_DIR = "outputs"
DEFAULT_LANGUAGE = "tr"
