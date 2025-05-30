import json
from datetime import datetime, timedelta
import config

USERS_FILE = "users.json"

def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def set_okx_account(user_id, api_key, api_secret, passphrase):
    users = load_users()
    if user_id not in users:
        users[user_id] = {}
    users[user_id]["okx"] = {
        "api_key": api_key,
        "api_secret": api_secret,
        "passphrase": passphrase
    }
    save_users(users)

def get_okx_account(user_id):
    users = load_users()
    return users.get(str(user_id), {}).get("okx")

def activate_subscription(user_id, code):
    from config import SUBSCRIPTION_CODES
    users = load_users()
    if code not in SUBSCRIPTION_CODES:
        return False
    users[user_id] = users.get(user_id, {})
    users[user_id]["active"] = True
    users[user_id]["expiry"] = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    save_users(users)
    return True

def is_active(user_id):
    # إذا المستخدم هو الأدمن يعتبر نشط دائماً
    if str(user_id) == str(config.ADMIN_USER_ID):
        return True
    users = load_users()
    user = users.get(str(user_id), {})
    if user.get("active") and user.get("expiry"):
        expiry = datetime.strptime(user["expiry"], "%Y-%m-%d")
        return expiry > datetime.now()
    return False
