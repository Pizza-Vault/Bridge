@'
# BridgeTools – Kurzguide

## Setup
```powershell
Import-Module BridgeTools
Set-BridgeEnv -Base "http://127.0.0.1:8000" -Token "my-super-token" -Secret "my-super-secret"


Health & Mode
ib -Method GET -Path "/health"
Get-BridgeMode
Set-BridgeMode -Mode 1

Order End-to-End
$ord = New-BridgeOrder -ProductId "pizza_margherita" -Timeslot "2025-09-17T12:00:00Z"
Set-BridgePayment -OrderId $ord.order_id -Status paid
Set-BridgeLockerLabel -PickupCode $ord.pickup_code -Label "Bestellung #$($ord.order_id)"
Open-BridgeLocker -PickupCode $ord.pickup_code
Confirm-BridgePickup -PickupCode $ord.pickup_code
Get-BridgeOrderStatus -OrderId $ord.order_id


Idempotency-Test
$idem = [guid]::NewGuid().ToString("N")
$body = @{ product_id="pizza_margherita"; timeslot="2025-09-17T12:00:00Z" }
$r1 = ib -Method POST -Path "/api/order/create" -BodyObj $body -IdempotencyKey $idem
$r2 = ib -Method POST -Path "/api/order/create" -BodyObj $body -IdempotencyKey $idem
$r1, $r2