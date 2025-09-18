# bridge.ps1

function New-BridgeSignedHeaders {
  param(
    [Parameter(Mandatory)] [string]$Token,
    [Parameter(Mandatory)] [string]$Secret,
    [Parameter(Mandatory)] [ValidateSet('GET','POST','PUT','DELETE','PATCH')] [string]$Method,
    [Parameter(Mandatory)] [string]$Path,
    [string]$Body = ''
  )

  $ts    = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
  $nonce = [guid]::NewGuid().ToString('N')

  $sha256  = [System.Security.Cryptography.SHA256]::Create()
  $hash    = $sha256.ComputeHash([Text.Encoding]::UTF8.GetBytes($Body))
  $bodyHex = ($hash | ForEach-Object { $_.ToString('x2') }) -join ''

  $base = "$Method`n$Path`n$bodyHex`n$ts`n$nonce"

  $keyBytes = [Text.Encoding]::UTF8.GetBytes($Secret)
  $hmac     = New-Object System.Security.Cryptography.HMACSHA256 (,$keyBytes)  # führendes Komma!
  $sigBytes = $hmac.ComputeHash([Text.Encoding]::UTF8.GetBytes($base))
  $sig      = ($sigBytes | ForEach-Object { $_.ToString('x2') }) -join ''

  return @{
    Authorization     = "Bearer $Token"
    'X-Timestamp'     = "$ts"
    'X-Nonce'         = "$nonce"
    'X-Signature'     = "$sig"
    'Idempotency-Key' = [guid]::NewGuid().ToString('N')
  }
}

function Invoke-Bridge {
  param(
    [Parameter(Mandatory)] [ValidateSet('GET','POST','PUT','DELETE','PATCH')] [string]$Method,
    [Parameter(Mandatory)] [string]$Path,
    [hashtable]$BodyObj,
    [string]$BaseUrl = $env:BRIDGE_BASEURL
  )

  if (-not $BaseUrl) { $BaseUrl = 'http://127.0.0.1:8000' }
  $token  = if ($env:BRIDGE_TOKEN)  { $env:BRIDGE_TOKEN  } else { throw 'BRIDGE_TOKEN not set' }
  $secret = $env:BRIDGE_SECRET  # leer = ohne Signatur

  $body = if ($BodyObj) { $BodyObj | ConvertTo-Json -Compress } else { '' }

  $headers = if ($secret) {
    New-BridgeSignedHeaders -Token $token -Secret $secret -Method $Method -Path $Path -Body $body
  } else {
    $ts    = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
    $nonce = [guid]::NewGuid().ToString('N')
    @{
      Authorization     = "Bearer $token"
      'X-Timestamp'     = "$ts"
      'X-Nonce'         = "$nonce"
      'Idempotency-Key' = [guid]::NewGuid().ToString('N')
    }
  }

  $uri   = "$BaseUrl$Path"
  $splat = @{ Method = $Method; Uri = $uri; Headers = $headers }
  if ($body) { $splat.ContentType = 'application/json'; $splat.Body = $body }

  try { Invoke-RestMethod @splat }
  catch {
    $msg = $_.ErrorDetails.Message; if (-not $msg) { $msg = $_.Exception.Message }
    throw "Bridge call failed: $msg"
  }
}
