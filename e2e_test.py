# e2e_test.py
import json
import uuid
from datetime import datetime, timezone, timedelta

import requests

BASE_URL = "http://127.0.0.1:8000"
TOKEN = "Bearer demo-token"  # muss zu auth.verify_headers in auth.py passen

def rfc3339_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def headers():
    return {
        "Authorization": TOKEN,
        "X-Timestamp": rfc3339_now(),
        "X-Nonce": uuid.uuid4().hex,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

def pretty(title, resp):
    print(f"\n=== {title} [{resp.status_code}] ===")
    try:
        print(json.dumps(resp.json(), indent=2))
    except Exception:
        print(resp.text)

def main():
    # 1) Mode -> OPEN_ALL (1)
    resp = requests.post(
        f"{BASE_URL}/api/machine/set_mode",
        headers=headers(),
        json={"mode": 1},
        timeout=10,
    )
    pretty("SET MODE -> 1 (OPEN_ALL)", resp)
    resp.raise_for_status()

    # 2) Order anlegen (Timeslot in ~2 Minuten)
    ts = datetime.now(timezone.utc) + timedelta(minutes=2)
    ts_str = ts.replace(second=0, microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")
    idem = uuid.uuid4().hex

    h = headers()
    h["Idempotency-Key"] = idem
    payload = {
        "product_id": "pizza_margherita",
        "timeslot": ts_str,
        "pickup_code": "PICK123",
    }

    resp = requests.post(
        f"{BASE_URL}/api/order/create",
        headers=h,
        json=payload,
        timeout=10,
    )
    pretty("CREATE ORDER", resp)
    resp.raise_for_status()
    order_id = resp.json()["order_id"]

    # 3) Status prüfen
    resp = requests.get(
        f"{BASE_URL}/api/order/status",
        headers=headers(),
        params={"order_id": order_id},
        timeout=10,
    )
    pretty("ORDER STATUS (pending erwartet)", resp)
    resp.raise_for_status()

    # 4) Order abschließen
    resp = requests.post(
        f"{BASE_URL}/api/order/complete",
        headers=headers(),
        params={"order_id": order_id},
        timeout=10,
    )
    pretty("ORDER COMPLETE", resp)
    resp.raise_for_status()

    # 5) Status erneut prüfen
    resp = requests.get(
        f"{BASE_URL}/api/order/status",
        headers=headers(),
        params={"order_id": order_id},
        timeout=10,
    )
    pretty("ORDER STATUS (completed erwartet)", resp)
    resp.raise_for_status()

    print("\n>>> End-to-End Test erfolgreich.")

if __name__ == "__main__":
    main()
