import json
import os
from datetime import datetime
from django.conf import settings

BLOCKCHAIN_FILE = os.path.join(settings.BASE_DIR, 'blockchain_log.json')

def save_to_blockchain(sha256_hash, user, title):
    record = {
        'timestamp': datetime.utcnow().isoformat(),
        'hash': sha256_hash,
        'user': str(user),
        'title': title
    }

    if not os.path.exists(BLOCKCHAIN_FILE):
        with open(BLOCKCHAIN_FILE, 'w') as f:
            json.dump([record], f, indent=4)
    else:
        with open(BLOCKCHAIN_FILE, 'r+') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
            data.append(record)
            f.seek(0)
            json.dump(data, f, indent=4)

def is_hash_recorded(sha256_hash):
    if not os.path.exists(BLOCKCHAIN_FILE):
        return False
    with open(BLOCKCHAIN_FILE, 'r') as f:
        try:
            data = json.load(f)
            return any(entry['hash'] == sha256_hash for entry in data)
        except json.JSONDecodeError:
            return False
