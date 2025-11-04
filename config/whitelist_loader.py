# config/whitelist_loader.py
from whitelist import Whitelist

WL_PATH = "whitelist.json"
whitelist = Whitelist.load(WL_PATH)

# Примеры:
# whitelist.is_allowed(message.from_user.id)
# whitelist.add_user(6165946917); whitelist.save()
