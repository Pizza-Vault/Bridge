# \### Kompletter Markdown-Text für README.md

# 

# Hier ist der vollständige Markdown-Text nochmal – kopiere ihn 1:1 in Notepad (`notepad README.md` im Bridge-Root), speichere (Ctrl+S) und push (`git add README.md \&\& git commit -m "Add README" \&\& git push origin main`). Das macht das Repo sofort nutzbar.

# 

# ```markdown

# \# Pizza-Vault Bridge

# 

# "The Swiss Vault" – Sichere API-Schicht für Pizza-Automaten. Verbindet Hardware (Locker, Produktion) mit Zahlungen und Buchhaltung (Bexio/HubRise/Odoo).

# 

# \## Quick Start

# 

# \### Requirements

# \- Python 3.10+

# \- PowerShell 5.1+ (für Tools)

# \- SQLite (DB, inklusive)

# 

# \### Setup

# 1\. Clone the repo:

# &nbsp;  ```

# &nbsp;  git clone https://github.com/Pizza-Vault/Bridge.git

# &nbsp;  cd Bridge

# &nbsp;  ```

# 

# 2\. Virtual Env \& Dependencies:

# &nbsp;  ```

# &nbsp;  python -m venv .venv

# &nbsp;  .\\.venv\\Scripts\\activate  # Windows

# &nbsp;  pip install -r requirements.txt

# &nbsp;  ```

# 

# 3\. Env-Vars setzen (z. B. in .env oder PowerShell):

# &nbsp;  ```

# &nbsp;  $env:BRIDGE\_TOKEN = "your-bearer-token"

# &nbsp;  $env:BRIDGE\_SECRET = "your-hmac-secret"

# &nbsp;  ```

# 

# 4\. Start the API:

# &nbsp;  ```

# &nbsp;  python -m uvicorn app.main:app --reload --port 8000

# &nbsp;  ```

# &nbsp;  - API: http://127.0.0.1:8000

# &nbsp;  - Docs (Swagger): http://127.0.0.1:8000/docs

# 

# \### PowerShell-Tools (BridgeTools)

# 1\. Install the module (einmalig):

# &nbsp;  ```

# &nbsp;  # Läuft im Bridge-Root

# &nbsp;  Import-Module .\\BridgeTools.psm1

# &nbsp;  ```

# 2\. Env setzen:

# &nbsp;  ```

# &nbsp;  Set-BridgeEnv -Base 'http://127.0.0.1:8000' -Token 'your-token' -Secret 'your-secret'

# &nbsp;  ```

# 3\. E2E-Beispiel:

# &nbsp;  ```

# &nbsp;  $ord = New-BridgeOrder -ProductId 'pizza\_margherita' -Timeslot '2025-09-20T12:00:00Z'

# &nbsp;  Set-BridgePayment -OrderId $ord.order\_id

# &nbsp;  Set-BridgeLockerLabel -PickupCode $ord.pickup\_code -Label "Bestellung #$($ord.order\_id)"

# &nbsp;  Open-BridgeLocker -PickupCode $ord.pickup\_code

# &nbsp;  Confirm-BridgePickup -PickupCode $ord.pickup\_code

# &nbsp;  Get-BridgeOrderStatus -OrderId $ord.order\_id

# &nbsp;  ```

# 

# \## Auth \& Security

# 

# \### Bearer + HMAC

# \- \*\*Authorization\*\*: `Bearer <BRIDGE\_TOKEN>`

# \- \*\*X-Timestamp\*\*: Unix-Sekunden (UTC)

# \- \*\*X-Nonce\*\*: 32-stellige GUID (ohne Bindestriche)

# \- \*\*X-Signature\*\*: HMAC-SHA256 (hex, lowercase) über Base-String

# 

# \*\*Base-String\*\* (mit Newlines):

# ```

# <HTTP\_METHOD>

# <PATH>

# <SHA256\_HEX(BODY)>

# <TIMESTAMP>

# <NONCE>

# ```

# 

# \*\*Beispiel (curl)\*\*:

# ```

# curl -X POST http://127.0.0.1:8000/api/order/create \\

# &nbsp; -H "Authorization: Bearer my-super-token" \\

# &nbsp; -H "X-Timestamp: 1726811234" \\

# &nbsp; -H "X-Nonce: f0d123456789abcdef0123456789abcdef" \\

# &nbsp; -H "X-Signature: 5f4dcc3b5aa765d61d8327deb882cf99" \\

# &nbsp; -H "Content-Type: application/json" \\

# &nbsp; -d '{"product\_id": "pizza\_margherita", "timeslot": "2025-09-20T12:00:00Z"}'

# ```

# 

# \*\*Idempotency\*\*: Füge `Idempotency-Key: <uuid>` zu POSTs hinzu (verhindert Duplikate).

# 

# \### Zeitfenster \& Replay-Schutz

# \- Timestamp: ±300s, sonst 401.

# \- Nonce: Persistenter Store (zukünftig Redis/DB).

# 

# \## Endpunkte

# 

# \### System

# \- \*\*GET /health\*\*: `{ "ok": true }`

# \- \*\*GET /api/system/mode\*\*: `{ "mode": 1, "mode\_version": 1, "at": "2025-09-20T12:00:00Z" }`

# \- \*\*POST /api/system/mode\*\*: Body `{ "mode": 1 }` → `{ "mode": 1, "message": "Set" }`

# 

# \### Orders

# \- \*\*POST /api/order/create\*\*: Body `{ "product\_id": "pizza\_margherita", "timeslot": "2025-09-20T12:00:00Z" }` → `{ "order\_id": "ord\_123", "pickup\_code": "pc\_456", "status": "pending" }`

# \- \*\*GET /api/order/status?order\_id=ord\_123\*\*: `{ "order\_id": "ord\_123", "status": "pending", "payment": "not\_paid" }`

# 

# \### Payment

# \- \*\*POST /api/payment/charge\*\*: Body `{ "order\_id": "ord\_123", "status": "paid" }` → `{ "order\_id": "ord\_123", "payment": "paid" }`

# 

# \### Locker

# \- \*\*POST /api/locker/label\*\*: Body `{ "pickup\_code": "pc\_456", "label\_text": "Bestellung #ord\_123" }` → `{ "pickup\_code": "pc\_456", "label": "Bestellung #ord\_123" }`

# \- \*\*POST /api/locker/open\*\*: Body `{ "pickup\_code": "pc\_456" }` → `{ "status": "opened" }`

# \- \*\*POST /api/locker/pickup/confirm\*\*: Body `{ "pickup\_code": "pc\_456" }` → `{ "status": "completed" }`

# 

# \### Production

# \- \*\*GET /api/production/time?order\_id=ord\_123\*\*: `{ "order\_id": "ord\_123", "estimate\_sec": 180 }`

# 

# \### Fehlerbilder

# \- 401/403: `{ "error": "Unauthorized", "detail": "Invalid signature" }`

# \- 400: `{ "error": "Bad Request", "detail": "Missing field" }`

# 

# \## Datenmodell

# \- \*\*Order\*\*: order\_id (PK), product\_id, timeslot, pickup\_code, status (pending/completed), payment (not\_paid/paid), created\_at (UTC).

# 

# \## To-Dos

# \- Security: Zeitfenster/Nonce-Store, Dependabot-Fix.

# \- Persistenz: Idempotency in DB/Redis.

# \- Deployment: Docker/Compose, Monitoring.

# \- Integration: Odoo/Bexio-Anbindung, Hardware-Adapter (IoT-Sensoren).

# 

# \## Changelog

# \- v0.1.0: E2E-Flow, Auth, DB-Init.

# 

# For questions, open an Issue.

# ```

# 

# \### So pushst du es

# 1\. Speichere in Notepad (`notepad README.md`).

# 2\. In PowerShell (im Bridge-Root):  

# &nbsp;  ```

# &nbsp;  git add README.md

# &nbsp;  git commit -m "Add README with API docs and setup"

# &nbsp;  git push origin main

# &nbsp;  ```

# 3\. Überprüfe: https://github.com/Pizza-Vault/Bridge – README sollte da sein.

# 

# Falls du den nächsten To-Do (Security-Alert) brauchst, sag Bescheid!

