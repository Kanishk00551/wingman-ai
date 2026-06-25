import os
from anthropic import Anthropic
from supabase import create_client, Client
from dotenv import load_dotenv

# 1. Force python to load from your exact absolute path
env_location = r"E:\wingman-ai\.env"
load_dotenv(dotenv_path=env_location)

# 2. Supabase Setup
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Failsafe check
if not SUPABASE_URL:
    raise ValueError(f"Variables are still empty! Please open {env_location} and make sure it has SUPABASE_URL=your_url")

supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 3. Anthropic Setup
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
claude_client = Anthropic(api_key=ANTHROPIC_API_KEY)