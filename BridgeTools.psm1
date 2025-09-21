# BridgeTools.psm1 – PowerShell-Modul für Bridge-API

# Globale Vars
$script:BridgeBase = 'http://127.0.0.1:8000'
$script:BridgeToken = 'my-super-token'
$script:BridgeSecret = 'my-super-secret'

function Set-BridgeEnv {
  param(
    [string]$Base = 'http://127.0.0.1:8000',
    [string]$Token = 'my-super-token',
    [string]$Secret = 'my-super-secret'
  )
  $script:BridgeBase = $Base
  $script:BridgeToken = $Token
  $script:BridgeSecret = $Secret
  Write-Host "Bridge Env set: Base=$Base"
}

function Invoke-Bridge {
  param(
    [string]$Method = 'GET',
    [string]$Path,
    [object]$Body = $null
  )
  $url = "$script:BridgeBase$Path"
  $headers = @{
    'Authorization' = "Bearer $script:BridgeToken"
  }
  if ($Body) {
    $bodyJson = $Body | ConvertTo-Json
    $headers['Content-Type'] = 'application/json'
    $bodyBytes = [System.Text.Encoding]::UTF8.GetBytes($bodyJson)
    $sha256 = New-Object System.Security.Cryptography.SHA256Managed
    $bodyHash = ($sha256.ComputeHash($bodyBytes) | ForEach-Object { '{0:x2}' -f $_ }) -join ''
  } else {
    $bodyHash = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
  }
  $timestamp = [int][DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
  $nonce = [guid]::NewGuid().ToString().Replace('-', '')
  $baseString = "$Method`n$Path`n$bodyHash`n$timestamp`n$nonce"
  $keyBytes = [System.Text.Encoding]::UTF8.GetBytes($script:BridgeSecret)
  $hmac = New-Object System.Security.Cryptography.HMACSHA256
  $hmac.Key = $keyBytes
  $signatureBytes = $hmac.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($baseString))
  $signature = ($signatureBytes | ForEach-Object { '{0:x2}' -f $_ }) -join ''
  $headers['X-Timestamp'] = $timestamp
  $headers['X-Nonce'] = $nonce
  $headers['X-Signature'] = $signature

  if ($Body) {
    Invoke-RestMethod -Uri $url -Method $Method -Headers $headers -Body $bodyJson
  } else {
    Invoke-RestMethod -Uri $url -Method $Method -Headers $headers
  }
}

function Get-BridgeHealth { Invoke-Bridge -Path '/health' }
function Get-BridgeMode { Invoke-Bridge -Path '/api/system/mode' }
function Set-BridgeMode { param([int]$Mode) Invoke-Bridge -Method 'POST' -Path '/api/system/mode' -Body @{mode = $Mode} }
function New-BridgeOrder { param([string]$ProductId, [string]$Timeslot) Invoke-Bridge -Method 'POST' -Path '/api/order/create' -Body @{product_id = $ProductId; timeslot = $Timeslot} }
function Get-BridgeOrderStatus { 
  param([string]$OrderId)
  # Fix: Signatur mit clean Path (/api/order/status), URL mit Query
  $signPath = '/api/order/status'
  $fullPath = "/api/order/status?order_id=$OrderId"
  $timestamp = [int][DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
  $nonce = [guid]::NewGuid().ToString().Replace('-', '')
  $bodyHash = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'  # Empty for GET
  $baseString = "GET`n$signPath`n$bodyHash`n$timestamp`n$nonce"
  $keyBytes = [System.Text.Encoding]::UTF8.GetBytes($script:BridgeSecret)
  $hmac = New-Object System.Security.Cryptography.HMACSHA256
  $hmac.Key = $keyBytes
  $signatureBytes = $hmac.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($baseString))
  $signature = ($signatureBytes | ForEach-Object { '{0:x2}' -f $_ }) -join ''
  $headers = @{
    'Authorization' = "Bearer $script:BridgeToken"
    'X-Timestamp' = $timestamp
    'X-Nonce' = $nonce
    'X-Signature' = $signature
  }
  $url = "$script:BridgeBase$fullPath"
  Invoke-RestMethod -Uri $url -Method 'GET' -Headers $headers
}
function Get-BridgeProductionTime { 
  param([string]$OrderId)
  # Ähnlicher Fix für Production
  $signPath = '/api/production/time'
  $fullPath = "/api/production/time?order_id=$OrderId"
  $timestamp = [int][DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
  $nonce = [guid]::NewGuid().ToString().Replace('-', '')
  $bodyHash = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
  $baseString = "GET`n$signPath`n$bodyHash`n$timestamp`n$nonce"
  $keyBytes = [System.Text.Encoding]::UTF8.GetBytes($script:BridgeSecret)
  $hmac = New-Object System.Security.Cryptography.HMACSHA256
  $hmac.Key = $keyBytes
  $signatureBytes = $hmac.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($baseString))
  $signature = ($signatureBytes | ForEach-Object { '{0:x2}' -f $_ }) -join ''
  $headers = @{
    'Authorization' = "Bearer $script:BridgeToken"
    'X-Timestamp' = $timestamp
    'X-Nonce' = $nonce
    'X-Signature' = $signature
  }
  $url = "$script:BridgeBase$fullPath"
  Invoke-RestMethod -Uri $url -Method 'GET' -Headers $headers
}
function Set-BridgePayment { param([string]$OrderId) Invoke-Bridge -Method 'POST' -Path '/api/payment/charge' -Body @{order_id = $OrderId; status = 'paid'} }
function Set-BridgeLockerLabel { param([string]$PickupCode, [string]$Label) Invoke-Bridge -Method 'POST' -Path '/api/locker/label' -Body @{pickup_code = $PickupCode; label_text = $Label} }
function Open-BridgeLocker { param([string]$PickupCode) Invoke-Bridge -Method 'POST' -Path '/api/locker/open' -Body @{pickup_code = $PickupCode} }
function Confirm-BridgePickup { param([string]$PickupCode) Invoke-Bridge -Method 'POST' -Path '/api/locker/pickup/confirm' -Body @{pickup_code = $PickupCode} }

# Export am Ende
Export-ModuleMember -Function Set-BridgeEnv, Invoke-Bridge, Get-BridgeHealth, Get-BridgeMode, Set-BridgeMode, New-BridgeOrder, Get-BridgeOrderStatus, Get-BridgeProductionTime, Set-BridgePayment, Set-BridgeLockerLabel, Open-BridgeLocker, Confirm-BridgePickup