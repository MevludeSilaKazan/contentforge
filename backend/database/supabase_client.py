"""
Supabase Database Client
"""

from supabase import create_client, Client
from config.settings import SUPABASE_URL, SUPABASE_KEY

_client: Client = None


def get_supabase() -> Client:
    """Supabase client singleton"""
    global _client
    
    if _client is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError("SUPABASE_URL ve SUPABASE_KEY gerekli")
        _client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    return _client
