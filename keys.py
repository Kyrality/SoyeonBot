import os
from dotenv import load_dotenv

load_dotenv()

client_token = os.getenv("live_token")

lastfm_api_key = os.getenv("LF_API_KEY")
lastfm_root_url = os.getenv("LF_ROOT_URL")
lastfm_shared_secret = os.getenv("LF_SHARED_SECRET")

