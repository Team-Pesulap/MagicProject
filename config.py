import os

from dotenv import load_dotenv

load_dotenv(".env")

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
REDIS_URI = os.environ.get("REDIS_URI")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")
REDISPORT = os.environ.get("REDISPORT")
MONGO_URL = os.environ.get("MONGO_URL")
SESSION = os.environ.get("SESSION")
SUDOERS = list(map(int, os.environ.get("SUDOERS", "").split()))
BLACKLIST_CHAT = os.environ.get("BLACKLIST_CHAT", None)
if not BLACKLIST_CHAT:
    BLACKLIST_CHAT = [-1001861414061]
BLACKLIST_GCAST = {int(x) for x in os.environ.get("BLACKLIST_GCAST", "").split()}
BRANCH = os.environ.get("BRANCH", "magic")
HEROKU_API = os.environ.get("HEROKU_API", None)
HEROKU_NAME = os.environ.get("HEROKU_NAME", None)
REPO_URL = os.environ.get("REPO_URL", "https://github.com/Team-Pesulap/MagicProject")
LOAD = os.environ.get("LOAD", "").split()
NOLOAD = os.environ.get("NOLOAD", "").split()
BOT_LOAD = os.environ.get("BOT_LOAD", "").split()
BOT_NOLOAD = os.environ.get("BOT_NOLOAD", "").split()
prefix = os.environ.get("prefix", ".")

