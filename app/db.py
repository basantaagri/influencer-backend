from dotenv import load_dotenv
load_dotenv()

import os
from supabase import create_client, Client

# -------------------------------------------------
# SUPABASE ENV VARIABLES (LOCAL .env or RENDER ENV)
# -------------------------------------------------
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    raise RuntimeError(
        "Supabase environment variables missing. "
        "Ensure SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are set."
    )

# -------------------------------------------------
# SUPABASE CLIENT (HTTP ONLY — NO DB SOCKETS)
# -------------------------------------------------
supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_SERVICE_ROLE_KEY
)

# -------------------------------------------------
# EXPORT CLIENT
# -------------------------------------------------
def get_supabase() -> Client:
    """
    Returns a singleton Supabase client.
    Uses HTTP API (safe for Render Free & local).
    """
    return supabase
